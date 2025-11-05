"""BookCopy model."""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from library_system.utils.enums import CopyStatus


@dataclass
class BookCopy:
    """Represents a physical copy of a book."""
    copy_id: Optional[int] = None
    book_id: Optional[int] = None
    barcode: Optional[str] = None
    status: Optional[CopyStatus] = None
    acquired_on: Optional[date] = None

    def to_dict(self) -> dict:
        """Convert book copy to dictionary."""
        return {
            'copy_id': self.copy_id,
            'book_id': self.book_id,
            'barcode': self.barcode,
            'status': self.status.value if self.status else None,
            'acquired_on': self.acquired_on.isoformat() if self.acquired_on else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BookCopy':
        """Create book copy from dictionary."""
        acquired_on = None
        if data.get('acquired_on'):
            if isinstance(data['acquired_on'], str):
                acquired_on = date.fromisoformat(data['acquired_on'])
            else:
                acquired_on = data['acquired_on']
        
        return cls(
            copy_id=data.get('copy_id'),
            book_id=data.get('book_id'),
            barcode=data.get('barcode'),
            status=CopyStatus(data['status']) if data.get('status') else None,
            acquired_on=acquired_on
        )

