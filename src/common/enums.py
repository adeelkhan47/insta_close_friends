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


class RoleNames(Enum):
    SUPER_ADMIN = "Super Admin"
    CLIENT = "Client"
class WebsiteStatus(Enum):
    Pending = "Pending"
    Approved = "Approved"
    Error = "Error"
    Rejected = "Rejected"

