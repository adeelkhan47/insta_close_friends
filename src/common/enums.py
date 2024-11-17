from enum import Enum as PyEnum


class Enum(str, PyEnum):
    @classmethod
    def exists(cls, item):
        return item in [x.value for x in cls]

    @classmethod
    def list(cls):
        return [x.value for x in cls]

    @classmethod
    def select(cls, key):
        for member in cls:
            if member.name == key:
                return member.value


class RecordStatus(Enum):
    Success = "Success"
    Failed = "Failed"
    Partial = "Partial"
    Pending = "Pending"
class EntryStatus(Enum):
    Passed = "Passed"
    Failed = "Failed"