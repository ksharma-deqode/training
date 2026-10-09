"""Unit test suite covering functional, OOP, domain subclasses, and edge cases."""

import json
import tempfile
import unittest
from pathlib import Path

from exceptions import (
    MissingKeyError,
    InvalidDataTypeError,
    UnsupportedDomainError,
    FileAccessError,
)
from blueprint_functions import (
    generate_blueprint_functional,
    validate_config_recursive,
)
from blueprint_classes import (
    BlueprintGenerator,
    RetailGenerator,
    LogisticsGenerator,
    GeneratorFactory,
)


class TestBlueprintGenerator(unittest.TestCase):

    def setUp(self):
        self.valid_config = {
            "domain": "retail",
            "role": "Lead Architect",
            "company": "Test Co",
            "problem": "Sample business problem text.",
            "input_fields": [{"name": "item_id", "type": "str"}],
            "output_fields": [{"name": "total_cost", "type": "float", "derivation_rule": "item * price"}],
            "constraints": ["Must complete in under 1 second."],
            "core_task": "Build robust inventory tracking pipeline."
        }

    def test_happy_path_class_generator(self):
        generator = GeneratorFactory.create_generator(self.valid_config)
        self.assertIsInstance(generator, RetailGenerator)
        
        sections = generator.get_sections()
        self.assertEqual(len(sections), 10)
        
        doc = generator.generate_document()
        self.assertIn("## Business Scenario", doc)
        self.assertIn("## Deliverable Checklist", doc)
        self.assertIn("Retail Domain Requirement", doc)

    def test_happy_path_functional_generator(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as tf:
            json.dump(self.valid_config, tf)
            tf_path = tf.name

        doc = generate_blueprint_functional(tf_path)
        self.assertIn("# Capstone Project Specification: Test Co", doc)
        self.assertIn("## Core Task", doc)
        Path(tf_path).unlink()

    def test_domain_subclass_factory(self):
        logistics_cfg = dict(self.valid_config, domain="logistics")
        gen = GeneratorFactory.create_generator(logistics_cfg)
        self.assertIsInstance(gen, LogisticsGenerator)
        self.assertIn("Logistics Domain Requirement", gen.generate_required_implementations())

    def test_missing_required_key_raises_exception(self):
        invalid_cfg = dict(self.valid_config)
        del invalid_cfg["company"]
        with self.assertRaises(MissingKeyError):
            BlueprintGenerator(invalid_cfg)

    def test_unsupported_domain_raises_exception(self):
        invalid_cfg = dict(self.valid_config, domain="quantum_computing")
        with self.assertRaises(UnsupportedDomainError):
            BlueprintGenerator(invalid_cfg)

    def test_invalid_data_type_raises_exception(self):
        invalid_cfg = dict(self.valid_config, role=12345)
        with self.assertRaises(InvalidDataTypeError):
            validate_config_recursive(invalid_cfg)

    def test_missing_file_raises_file_access_error(self):
        with self.assertRaises(FileAccessError):
            generate_blueprint_functional("non_existent_file.json")

    def test_generator_iteration(self):
        generator = BlueprintGenerator(self.valid_config)
        count = 0
        for section in generator:
            self.assertTrue(section.startswith("## "))
            count += 1
        self.assertEqual(count, 10)


if __name__ == "__main__":
    unittest.main()