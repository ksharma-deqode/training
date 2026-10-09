"""Class-based OOP implementation of the Blueprint Generator with domain inheritance."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))

from exceptions import (
    ConfigurationError,
    ValidationError,
    MissingKeyError,
    InvalidDataTypeError,
    UnsupportedDomainError,
    FileAccessError,
)

SUPPORTED_DOMAINS = {"retail", "logistics", "healthcare", "finance", "general"}


class BlueprintIterator(Iterator[str]):
    """Custom iterator to iterate through generated section strings in exact blueprint order."""

    def __init__(self, sections: List[str]):
        self._sections = sections
        self._index = 0

    def __iter__(self) -> "BlueprintIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._sections):
            raise StopIteration
        section = self._sections[self._index]
        self._index += 1
        return section


class BlueprintGenerator:
    """Base class for generating 10-section Capstone Project Specifications."""

    def __init__(self, config: Dict[str, Any]):
        self.validate_config(config)
        self.config = config
        self.domain: str = config["domain"].lower()
        self.role: str = config["role"]
        self.company: str = config["company"]
        self.problem: str = config["problem"]
        self.input_fields: List[Dict[str, Any]] = config["input_fields"]
        self.output_fields: List[Dict[str, Any]] = config["output_fields"]
        self.constraints: List[str] = config.get("constraints", [])
        self.core_task: str = config["core_task"]

    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> "BlueprintGenerator":
        """Factory class method delegating JSON loading to GeneratorFactory."""
        return GeneratorFactory.from_json(json_path)

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Static method validating config structure recursively."""
        if not isinstance(config, dict):
            raise InvalidDataTypeError("root", dict, type(config))

        required = {"domain", "role", "company", "problem", "input_fields", "output_fields", "constraints", "core_task"}
        missing = required - set(config.keys())
        if missing:
            raise MissingKeyError(sorted(list(missing))[0])

        domain = str(config.get("domain", "")).lower()
        if domain not in SUPPORTED_DOMAINS:
            raise UnsupportedDomainError(domain, SUPPORTED_DOMAINS)

        if not isinstance(config["input_fields"], list) or len(config["input_fields"]) == 0:
            raise ValidationError("input_fields must be a non-empty list.")
        if not isinstance(config["output_fields"], list) or len(config["output_fields"]) == 0:
            raise ValidationError("output_fields must be a non-empty list.")

        return True

    def _format_header(self, title: str) -> str:
        return f"## {title}\n\n"

    def generate_business_scenario(self) -> str:
        return (
            f"{self._format_header('Business Scenario')}"
            f"**Role:** {self.role}\n\n"
            f"**Company:** {self.company} ({self.domain.capitalize()} Industry)\n\n"
            f"**Problem Statement:**\n{self.problem}\n\n"
        )

    def generate_input_specification(self) -> str:
        lines = [f"- **`{f['name']}`** (`{f['type']}`): {f.get('description', 'Input field.')}" for f in self.input_fields]
        return f"{self._format_header('Input Specification')}" + "\n".join(lines) + "\n\n"

    def generate_output_specification(self) -> str:
        lines = [f"- **`{f['name']}`** (`{f['type']}`): {f.get('derivation_rule', 'Calculated rule.')}" for f in self.output_fields]
        return f"{self._format_header('Output Specification')}" + "\n".join(lines) + "\n\n"

    def generate_constraints_assumptions(self) -> str:
        lines = [f"{idx + 1}. {c}" for idx, c in enumerate(self.constraints)]
        return f"{self._format_header('Constraints & Assumptions')}" + "\n".join(lines) + "\n\n"

    def generate_core_task(self) -> str:
        return f"{self._format_header('Core Task')}{self.core_task}\n\n"

    def generate_required_implementations(self) -> str:
        return (
            f"{self._format_header('Required Implementations')}"
            "1. Object-Oriented Domain Abstraction Class Hierarchy.\n"
            "2. Input Validation, Error Interception, and Exception Propagation.\n"
            "3. Document Export pipeline supporting both Markdown and JSON streams.\n\n"
        )

    def generate_error_handling_requirements(self) -> str:
        return (
            f"{self._format_header('Error Handling Requirements')}"
            "- Catch missing file operations using `FileAccessError`.\n"
            "- Intercept corrupted payload configurations using `ValidationError`.\n\n"
        )

    def generate_testing_requirements(self) -> str:
        return (
            f"{self._format_header('Testing Requirements')}"
            "Validate base class, specialized domain subclasses, and static methods using `unittest`.\n\n"
        )

    def generate_stretch_goals(self) -> str:
        return (
            f"{self._format_header('Stretch Goals')}"
            "- Multi-threaded specification generation using `concurrent.futures`.\n"
            "- SQLite backend persistence for produced specifications.\n\n"
        )

    def generate_deliverable_checklist(self) -> str:
        items = [
            "Source Code Modules",
            "Exception Package",
            "Unit Test Suite",
            "Documentation README"
        ]
        lines = [f"- [ ] {item}" for item in items]
        return f"{self._format_header('Deliverable Checklist')}" + "\n".join(lines) + "\n\n"

    def get_sections(self) -> List[str]:
        """Returns all 10 generated section contents as a list."""
        return [
            self.generate_business_scenario(),
            self.generate_input_specification(),
            self.generate_output_specification(),
            self.generate_constraints_assumptions(),
            self.generate_core_task(),
            self.generate_required_implementations(),
            self.generate_error_handling_requirements(),
            self.generate_testing_requirements(),
            self.generate_stretch_goals(),
            self.generate_deliverable_checklist(),
        ]

    def generate_document(self) -> str:
        title = f"# Capstone Project Specification: {self.company}\n\n---\n\n"
        return title + "".join(self.get_sections())

    def save_to_file(self, output_path: Union[str, Path]) -> None:
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(self.generate_document())

    def __iter__(self) -> BlueprintIterator:
        return BlueprintIterator(self.get_sections())

    def __len__(self) -> int:
        return 10

    def __str__(self) -> str:
        return f"BlueprintGenerator(Company='{self.company}', Domain='{self.domain}')"

    def __repr__(self) -> str:
        return f"BlueprintGenerator(config={self.config!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlueprintGenerator):
            return False
        return self.config == other.config


class RetailGenerator(BlueprintGenerator):
    """Subclass tailored for Retail domain business scenarios."""

    def generate_required_implementations(self) -> str:
        base = super().generate_required_implementations()
        return base + "**Retail Domain Requirement:** Incorporate real-time inventory tracking and dynamic basket price calculation logic.\n\n"


class LogisticsGenerator(BlueprintGenerator):
    """Subclass tailored for Logistics domain business scenarios."""

    def generate_required_implementations(self) -> str:
        base = super().generate_required_implementations()
        return base + "**Logistics Domain Requirement:** Incorporate route optimization and delivery SLA delay penalty tracking logic.\n\n"


class FinanceGenerator(BlueprintGenerator):
    """Subclass tailored for Financial domain business scenarios."""

    def generate_required_implementations(self) -> str:
        base = super().generate_required_implementations()
        return base + "**Finance Domain Requirement:** Ensure strict double-entry ledger accuracy and risk score evaluations.\n\n"


class GeneratorFactory:
    """Factory class to create domain-specific generator instances."""

    @staticmethod
    def create_generator(config: Dict[str, Any]) -> BlueprintGenerator:
        domain = config.get("domain", "").lower()
        if domain == "retail":
            return RetailGenerator(config)
        elif domain == "logistics":
            return LogisticsGenerator(config)
        elif domain == "finance":
            return FinanceGenerator(config)
        else:
            return BlueprintGenerator(config)

    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> BlueprintGenerator:
        """Factory method to instantiate a generator directly from a JSON file path."""
        path = Path(json_path)
        if not path.is_file():
            raise FileAccessError(f"Configuration file not found: {json_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as err:
            raise ConfigurationError(f"Invalid JSON contents: {err}") from err
        except Exception as err:
            raise FileAccessError(f"Unable to read file '{json_path}': {err}") from err

        return cls.create_generator(data)