"""Parallel execution engine and SQLite persistence backend for Blueprint Specs."""

import sqlite3
import json
import logging
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from blueprint_classes import GeneratorFactory
from exceptions import BlueprintGeneratorError

logger = logging.getLogger("ParallelGenerator")


class DatabaseManager:
    """Context manager for SQLite database interactions storing generated blueprints."""

    def __init__(self, db_path: str = "blueprints.db"):
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "DatabaseManager":
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()

    def create_table(self) -> None:
        """Create blueprints table if it doesn't exist."""
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blueprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    config_json TEXT NOT NULL,
                    markdown_spec TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_blueprint(self, company: str, domain: str, config: Dict[str, Any], markdown_spec: str) -> int:
        if not self.conn:
            raise RuntimeError("Database connection is not open.")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO blueprints (company, domain, config_json, markdown_spec) VALUES (?, ?, ?, ?)",
            (company, domain, json.dumps(config), markdown_spec)
        )
        return cursor.lastrowid

    def get_all_blueprints(self) -> List[Tuple[int, str, str, str]]:
        if not self.conn:
            raise RuntimeError("Database connection is not open.")
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, company, domain, created_at FROM blueprints")
        return cursor.fetchall()


def process_single_config(config_path: str) -> Tuple[str, str, str]:
    """Worker function for concurrent execution."""
    path = Path(config_path)
    generator = GeneratorFactory.from_json(path)
    doc = generator.generate_document()
    return generator.company, generator.domain, doc


def batch_generate_parallel(config_file_paths: List[str], db_path: str = "blueprints.db") -> List[Tuple[str, bool]]:
    """Generates specifications in parallel using ProcessPoolExecutor and saves to SQLite."""
    results = []
    
    with ProcessPoolExecutor() as executor:
        future_to_path = {executor.submit(process_single_config, p): p for p in config_file_paths}
        
        with DatabaseManager(db_path) as db:
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    company, domain, doc = future.result()
                    with open(path, 'r', encoding='utf-8') as f:
                        cfg = json.load(f)
                    db.save_blueprint(company, domain, cfg, doc)
                    results.append((path, True))
                    logger.info("Successfully generated blueprint for %s (%s)", company, path)
                except Exception as err:
                    logger.error("Failed parallel task for %s: %s", path, err)
                    results.append((path, False))

    return results