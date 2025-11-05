"""Book model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """Represents a book."""
    book_id: Optional[int] = None
    isbn: Optional[str] = None
    title: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert book to dictionary."""
        return {
            'book_id': self.book_id,
            'isbn': self.isbn,
            'title': self.title,
            'publisher': self.publisher,
            'published_year': self.published_year,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create book from dictionary."""
        return cls(
            book_id=data.get('book_id'),
            isbn=data.get('isbn'),
            title=data.get('title'),
            publisher=data.get('publisher'),
            published_year=data.get('published_year'),
            description=data.get('description')
        )

