"""Enum definitions for the library system."""

from enum import Enum


class RoleName(str, Enum):
    """User role types."""
    MEMBER = "member"
    LIBRARIAN = "librarian"
    ADMINISTRATOR = "administrator"


class MemberStatus(str, Enum):
    """Member account status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class CopyStatus(str, Enum):
    """Book copy status."""
    AVAILABLE = "available"
    LOANED = "loaned"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


class LoanStatus(str, Enum):
    """Loan status."""
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

