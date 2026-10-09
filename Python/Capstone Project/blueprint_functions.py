"""Function-based implementation of the Blueprint Generator using functional paradigms."""

import json
import logging
import time
from functools import wraps, reduce
from pathlib import Path
from typing import Dict, List, Any, Callable, Generator, Tuple, Optional, Set

from exceptions import (
    ConfigurationError,
    ValidationError,
    MissingKeyError,
    InvalidDataTypeError,
    UnsupportedDomainError,
    FileAccessError,
)

# Setup Logger
logger = logging.getLogger("BlueprintFunctions")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SUPPORTED_DOMAINS: Set[str] = {"retail", "logistics", "healthcare", "finance", "general"}
REQUIRED_TOP_KEYS: Set[str] = {
    "domain", "role", "company", "problem",
    "input_fields", "output_fields", "constraints", "core_task"
}

# --- Decorators & Closures ---

def log_execution(func: Callable) -> Callable:
    """Decorator to log function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug("Executing %s...", func.__name__)
        return func(*args, **kwargs)
    return wrapper


def time_execution(func: Callable) -> Callable:
    """Decorator to measure execution time of generation functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug("Function %s took %.5f seconds", func.__name__, elapsed)
        return result
    return wrapper


def make_section_formatter(header_level: int = 2) -> Callable[[str, str], str]:
    """Closure returning a function to format Markdown section headers and body."""
    prefix = "#" * header_level
    def format_section(title: str, content: str) -> str:
        return f"{prefix} {title}\n\n{content.strip()}\n\n"
    return format_section


# Standard Formatter instance created via closure
format_h2 = make_section_formatter(2)


# --- Recursive Configuration Validation ---

def validate_config_recursive(config: Dict[str, Any], path_prefix: str = "") -> None:
    """Recursively validates JSON configuration structures and field definitions."""
    if not isinstance(config, dict):
        raise InvalidDataTypeError(path_prefix or "root", dict, type(config))

    # Top-level validation
    if not path_prefix:
        missing_keys = REQUIRED_TOP_KEYS - set(config.keys())
        if missing_keys:
            raise MissingKeyError(sorted(list(missing_keys))[0])

        domain = str(config.get("domain", "")).lower()
        if domain not in SUPPORTED_DOMAINS:
            raise UnsupportedDomainError(domain, SUPPORTED_DOMAINS)

    # Validate string fields
    for str_key in ["domain", "role", "company", "problem", "core_task"]:
        if str_key in config:
            val = config[str_key]
            current_path = f"{path_prefix}.{str_key}" if path_prefix else str_key
            if not isinstance(val, str):
                raise InvalidDataTypeError(current_path, str, type(val))
            if not val.strip():
                raise ValidationError(f"Field '{current_path}' cannot be empty.")

    # Validate recursive field arrays
    for list_key in ["input_fields", "output_fields"]:
        if list_key in config:
            current_path = f"{path_prefix}.{list_key}" if path_prefix else list_key
            fields = config[list_key]
            if not isinstance(fields, list):
                raise InvalidDataTypeError(current_path, list, type(fields))
            if not fields:
                raise ValidationError(f"Field list '{current_path}' must contain at least one field definition.")
            
            for idx, field in enumerate(fields):
                field_path = f"{current_path}[{idx}]"
                if not isinstance(field, dict):
                    raise InvalidDataTypeError(field_path, dict, type(field))
                if "name" not in field or "type" not in field:
                    raise MissingKeyError(f"{field_path}.name or type")
                if not field["name"].isidentifier():
                    raise ValidationError(f"Invalid field identifier name '{field['name']}' at {field_path}.")
                
                # Recursive call if nested fields exist
                if "nested_fields" in field:
                    validate_config_recursive({"domain": config.get("domain", "general"),
                                               "role": "r", "company": "c", "problem": "p", "core_task": "t",
                                               "constraints": [], "input_fields": field["nested_fields"],
                                               "output_fields": [{"name": "o", "type": "str"}]},
                                              path_prefix=f"{field_path}.nested_fields")


# --- Functional Section Generators ---

@log_execution
def generate_business_scenario(config: Dict[str, Any]) -> str:
    content = (
        f"**Role:** {config['role']}\n\n"
        f"**Company:** {config['company']} ({config['domain'].capitalize()} Domain)\n\n"
        f"**Problem Statement:**\n{config['problem']}"
    )
    return format_h2("Business Scenario", content)


@log_execution
def generate_input_specification(config: Dict[str, Any]) -> str:
    fields: List[Dict[str, Any]] = config["input_fields"]
    
    # Use map/lambda for line formatting
    format_field = lambda f: f"- **`{f['name']}`** (`{f['type']}`): {f.get('description', 'Input field required for processing.')}"
    lines = list(map(format_field, fields))
    content = "The implementation must parse and validate the following input data fields:\n\n" + "\n".join(lines)
    return format_h2("Input Specification", content)


@log_execution
def generate_output_specification(config: Dict[str, Any]) -> str:
    fields: List[Dict[str, Any]] = config["output_fields"]
    
    # Comprehension formatting
    lines = [
        f"- **`{f['name']}`** (`{f['type']}`): {f.get('derivation_rule', 'Derived per business requirements.')}"
        for f in fields
    ]
    content = "The system must derive and output the following calculated attributes:\n\n" + "\n".join(lines)
    return format_h2("Output Specification", content)


@log_execution
def generate_constraints_assumptions(config: Dict[str, Any]) -> str:
    raw_constraints: List[str] = config.get("constraints", [])
    # Filter non-empty constraints
    valid_constraints = list(filter(lambda c: isinstance(c, str) and len(c.strip()) > 0, raw_constraints))
    
    lines = [f"{idx + 1}. {c.strip()}" for idx, c in enumerate(valid_constraints)]
    content = "The core solution must adhere to the following operational and technical constraints:\n\n" + "\n".join(lines)
    return format_h2("Constraints & Assumptions", content)


@log_execution
def generate_core_task(config: Dict[str, Any]) -> str:
    content = f"### Main Objective\n{config['core_task']}\n\n" \
              f"Implement an end-to-end Python pipeline capable of processing input configurations, " \
              f"validating constraints, and outputting deterministic specification results."
    return format_h2("Core Task", content)


@log_execution
def generate_required_implementations(config: Dict[str, Any]) -> str:
    domain = config['domain'].lower()
    specific_rule = f"Domain-specific processing rules for **{domain.upper()}** transactions."
    
    content = (
        "The project must provide both modular and extensible architectural components:\n\n"
        "1. **Functional Module:** Pure functions, list/dict comprehensions, high-order functions (`map`, `filter`, `reduce`).\n"
        "2. **Object-Oriented Module:** Class abstractions, domain inheritance, static/class methods, and dunder interfaces.\n"
        f"3. **Domain Customization:** {specific_rule}\n"
        "4. **I/O Pipeline:** Context-managed JSON parsing, Markdown generation, and CLI integration."
    )
    return format_h2("Required Implementations", content)


@log_execution
def generate_error_handling_requirements(config: Dict[str, Any]) -> str:
    content = (
        "The codebase must gracefully intercept and handle execution anomalies:\n\n"
        "- **Custom Exception Hierarchy:** Deriving from `BlueprintGeneratorError`.\n"
        "- **Validation Rules:** Catch missing keys, malformed types, and unidentifiable variable names.\n"
        "- **I/O Operations:** Ensure safe handling of missing files and invalid JSON formatting using `try/except/else/finally` blocks."
    )
    return format_h2("Error Handling Requirements", content)


@log_execution
def generate_testing_requirements(config: Dict[str, Any]) -> str:
    content = (
        "Comprehensive unit test suites must be implemented:\n\n"
        "1. **Happy Path Testing:** Validate production of all 10 standard specification sections.\n"
        "2. **Edge Case Analysis:** Empty field sets, deeply nested object configurations, and high-volume parameters.\n"
        "3. **Failure Cases:** Intercept invalid schema keys, unknown business domains, and corrupt JSON files using `pytest` or `unittest`."
    )
    return format_h2("Testing Requirements", content)


@log_execution
def generate_stretch_goals(config: Dict[str, Any]) -> str:
    content = (
        "- **Parallel Processing:** Utilize `concurrent.futures.ProcessPoolExecutor` for bulk specification batch generation.\n"
        "- **Persistence Layer:** Store generated specifications and configurations inside a SQLite database.\n"
        "- **Extensibility:** Support API or external JSON template loading engines."
    )
    return format_h2("Stretch Goals", content)


@log_execution
def generate_deliverable_checklist(config: Dict[str, Any]) -> str:
    checklist = [
        "Functional Implementation Module (`blueprint_functions.py`)",
        "Class Implementation Module (`blueprint_classes.py`)",
        "Custom Exception Definitions (`exceptions.py`)",
        "Unit Test Execution Suite (`test_blueprint.py`)",
        "CLI Entry Point & Executable Scripts (`cli.py`)",
        "Sample JSON Configuration (`sample_config.json`)",
        "Comprehensive Documentation (`README.md`)"
    ]
    lines = [f"- [ ] {item}" for item in checklist]
    return format_h2("Deliverable Checklist", "\n".join(lines))


# Generator to yield sections sequentially
def yield_blueprint_sections(config: Dict[str, Any]) -> Generator[Tuple[str, str], None, None]:
    """Yields tuple of (section_name, section_markdown) sequentially."""
    generators = [
        ("Business Scenario", generate_business_scenario),
        ("Input Specification", generate_input_specification),
        ("Output Specification", generate_output_specification),
        ("Constraints & Assumptions", generate_constraints_assumptions),
        ("Core Task", generate_core_task),
        ("Required Implementations", generate_required_implementations),
        ("Error Handling Requirements", generate_error_handling_requirements),
        ("Testing Requirements", generate_testing_requirements),
        ("Stretch Goals", generate_stretch_goals),
        ("Deliverable Checklist", generate_deliverable_checklist),
    ]
    for title, gen_func in generators:
        yield title, gen_func(config)


@time_execution
def generate_blueprint_functional(config_path: str | Path, output_path: Optional[str | Path] = None) -> str:
    """Loads configuration, validates, and generates full 10-section blueprint string."""
    path = Path(config_path)
    if not path.is_file():
        raise FileAccessError(f"Configuration file not found at '{config_path}'")

    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as err:
        raise ConfigurationError(f"Malformed JSON in configuration file: {err}") from err
    except Exception as err:
        raise FileAccessError(f"Failed to read file: {err}") from err

    # Perform recursive validation
    validate_config_recursive(config)

    # Use reduce to assemble sections generated by the yield iterator
    sections = [section_md for _, section_md in yield_blueprint_sections(config)]
    title_header = f"# Capstone Project Specification: {config['company']}\n\n---\n\n"
    full_document = reduce(lambda acc, section: acc + section, sections, title_header)

    if output_path:
        out_p = Path(output_path)
        try:
            out_p.parent.mkdir(parents=True, exist_ok=True)
            with open(out_p, "w", encoding="utf-8") as f:
                f.write(full_document)
        except Exception as err:
            raise FileAccessError(f"Failed to write output to file: {err}") from err

    return full_document