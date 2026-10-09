"""Command-Line Interface (CLI) for Capstone Project Blueprint Generator."""

import argparse
import sys
from pathlib import Path

# Resolve project root path dynamically to prevent ModuleNotFoundError
sys.path.insert(0, str(Path(__file__).resolve().parent))

from blueprint_functions import generate_blueprint_functional
from blueprint_classes import GeneratorFactory
from generator_parallel import batch_generate_parallel, DatabaseManager
from exceptions import BlueprintGeneratorError


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capstone Project Blueprint Generator CLI Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Single generation command
    gen_parser = subparsers.add_parser("generate", help="Generate specification from a JSON config file")
    gen_parser.add_argument("-c", "--config", required=True, help="Path to input JSON config file")
    gen_parser.add_argument("-o", "--output", help="Path to output Markdown file (default: stdout)")
    gen_parser.add_argument("--mode", choices=["functional", "oop"], default="oop", help="Generator mode implementation")

    # Parallel batch generation command
    batch_parser = subparsers.add_parser("batch", help="Batch generate specifications concurrently")
    batch_parser.add_argument("-d", "--directory", required=True, help="Directory containing config JSON files")
    batch_parser.add_argument("--db", default="blueprints.db", help="Target SQLite database file")

    # List DB command
    list_parser = subparsers.add_parser("list-db", help="List stored specifications in SQLite DB")
    list_parser.add_argument("--db", default="blueprints.db", help="SQLite database file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "generate":
            if args.mode == "functional":
                doc = generate_blueprint_functional(args.config, args.output)
            else:
                gen = GeneratorFactory.from_json(args.config)
                doc = gen.generate_document()
                if args.output:
                    gen.save_to_file(args.output)
            
            if not args.output:
                print(doc)
            else:
                print(f"Successfully generated specification -> {args.output}")

        elif args.command == "batch":
            dir_path = Path(args.directory)
            if not dir_path.is_dir():
                print(f"Error: Directory '{args.directory}' does not exist.", file=sys.stderr)
                sys.exit(1)
            
            json_files = [str(p) for p in dir_path.glob("*.json")]
            print(f"Found {len(json_files)} configuration file(s). Processing...")
            results = batch_generate_parallel(json_files, db_path=args.db)
            successful = sum(1 for _, ok in results if ok)
            print(f"Batch execution completed: {successful}/{len(json_files)} succeeded.")

        elif args.command == "list-db":
            with DatabaseManager(args.db) as db:
                records = db.get_all_blueprints()
                print(f"\nStored Blueprints in Database ({len(records)} entries):\n" + "-"*50)
                for rec in records:
                    print(f"ID: {rec[0]} | Company: {rec[1]} | Domain: {rec[2]} | Created: {rec[3]}")

    except BlueprintGeneratorError as err:
        print(f"Execution Error: {err}", file=sys.stderr)
        sys.exit(2)
    except Exception as err:
        print(f"Unexpected System Error: {err}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()