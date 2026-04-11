from enum import Enum

class ValidationStatus(str, Enum):
    VALID = "VALID"
    UNSUPPORTED = "UNSUPPORTED"
    INVALID_FIELD = "INVALID_FIELD"

class TaskType(str, Enum):
    PREDICTION = "PREDICTION"
    OPTIMIZATION = "OPTIMIZATION"
    UNSUPPORTED = "UNSUPPORTED"

class ProcessType(str, Enum):
    ETCH = "ETCH"
    UNKNOWN = "UNKNOWN"

class FieldStatus(str, Enum):
    VALID = "VALID"
    AMBIGUOUS = "AMBIGUOUS"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    MISSING = "MISSING"