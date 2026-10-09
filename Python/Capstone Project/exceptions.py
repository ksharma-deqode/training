"""Custom exception classes for Capstone Project Blueprint Generator."""

class BlueprintGeneratorError(Exception):
    """Base exception class for all Blueprint Generator Error."""
    pass

class ConfigurationError(BlueprintGeneratorError):
    """Raised when configuration loading or processing fails."""
    pass

class ValidationError(ConfigurationError):
    """Raised when configuration fails schema validation."""
    pass

class MissingKeyError(ValidationError):
    """Raised wgen required configuration keys are missing."""
    def __init__(self, key_path:str):
        self.key_path = key_path
        super().__init__(f"Missing required configuration key: '{key_path}'")

class InvalidDataTypeError(ValidationError):
    """Raised when configuration values have unexpected data types."""
    def __init__(self, key:str,expected_type:type, actual_type:type):
        self.key = key
        self.expected_type = expected_type
        self.actual_type=actual_type
        super().__init__(
            f"Key '{key} expected type '{expected_type.__name__}"
            f"got '{actual_type.__name__}"
        )

class UnsupportedDomainError(ValidationError):
    """Raised whena an unsupported business domain is provided."""
    def __init__(self, domain:str, supported_domain: set):
        self.domain=domain
        self.supported_domain = supported_domain
        super().__init__(
            f"Domain '{domain} is unsupported. Supported domains: {sorted(list(supported_domain))}"
        )

class FileAccessError(BlueprintGeneratorError):
    """Raised when reading configuration or writing output fails."""
    pass