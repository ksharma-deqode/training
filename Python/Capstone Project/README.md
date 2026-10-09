# Capstone Project Blueprint Generator

An enterprise-grade Python tool that generates structured 10-section project specifications from standard JSON configuration files.

---

## Technical Features

1. **Dual Paradigms:** Complete functional (closures, decorators, high-order functions) and Object-Oriented implementations (inheritance, factory pattern, dunder protocols).
2. **Strict Schema Validation:** Intercepts missing keys, invalid types, empty lists, and unsupported business domains using custom exceptions.
3. **10 Fixed Sections:** Business Scenario, Input Spec, Output Spec, Constraints, Core Task, Required Implementations, Error Handling, Testing, Stretch Goals, and Deliverables.
4. **Parallel Processing:** Bulk concurrent generation utilizing Python's `concurrent.futures`.
5. **Database Storage:** SQLite backend persistence context manager.

---

## Quickstart Guide

### 1. Run via CLI

Generate single specification:
```bash
python cli.py generate -c sample_config.json -o sample_output.md --mode oop