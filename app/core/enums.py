from enum import Enum


class TaskType(str, Enum):
    PREDICTION = "PREDICTION"
    OPTIMIZATION = "OPTIMIZATION"
    UNSUPPORTED = "UNSUPPORTED"


class ProcessType(str, Enum):
    ETCH = "ETCH"
    UNKNOWN = "UNKNOWN"


class ValidationStatus(str, Enum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    FAILED = "FAILED"


class GoalType(str, Enum):
    EXACT = "exact"
    """ 
    RANGE = "range"
    MIN = "min"
    MAX = "max"
    OPTIMIZE_HIGH = "optimize_high"
    OPTIMIZE_LOW = "optimize_low" 
    """