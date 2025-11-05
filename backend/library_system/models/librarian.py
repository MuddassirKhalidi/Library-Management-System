"""Librarian model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Librarian:
    """Represents a librarian."""
    employee_id: Optional[int] = None
    user_id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert librarian to dictionary."""
        return {
            'employee_id': self.employee_id,
            'user_id': self.user_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Librarian':
        """Create librarian from dictionary."""
        return cls(
            employee_id=data.get('employee_id'),
            user_id=data.get('user_id')
        )

