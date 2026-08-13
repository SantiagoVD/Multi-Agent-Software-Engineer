from enum import Enum


class TaskStatus(str, Enum):
    RECEIVED = "received"
    CLONING_REPOSITORY = "cloning_repository"
    ANALYZING_REPOSITORY = "analyzing_repository"
    DEVELOPING = "developing"
    TESTING = "testing"
    REVIEWING = "reviewing"
    COMPLETED = "completed"
    FAILED = "failed"