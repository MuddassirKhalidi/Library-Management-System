"""Author model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Author:
    """Represents an author."""
    author_id: Optional[int] = None
    full_name: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert author to dictionary."""
        return {
            'author_id': self.author_id,
            'full_name': self.full_name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Author':
        """Create author from dictionary."""
        return cls(
            author_id=data.get('author_id'),
            full_name=data.get('full_name')
        )

