"""Category model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Category:
    """Represents a book category."""
    category_id: Optional[int] = None
    name: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert category to dictionary."""
        return {
            'category_id': self.category_id,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        """Create category from dictionary."""
        return cls(
            category_id=data.get('category_id'),
            name=data.get('name')
        )

