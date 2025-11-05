"""Reservation model."""

from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Reservation:
    """Represents a book reservation."""
    reservation_id: Optional[int] = None
    member_id: Optional[int] = None
    book_id: Optional[int] = None
    created_at: Optional[date] = None
    expires_at: Optional[date] = None
    active: Optional[bool] = None

    def to_dict(self) -> dict:
        """Convert reservation to dictionary."""
        return {
            'reservation_id': self.reservation_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'active': self.active
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Reservation':
        """Create reservation from dictionary."""
        created_at = None
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = date.fromisoformat(data['created_at'])
            else:
                created_at = data['created_at']
        
        expires_at = None
        if data.get('expires_at'):
            if isinstance(data['expires_at'], str):
                expires_at = date.fromisoformat(data['expires_at'])
            else:
                expires_at = data['expires_at']
        
        return cls(
            reservation_id=data.get('reservation_id'),
            member_id=data.get('member_id'),
            book_id=data.get('book_id'),
            created_at=created_at,
            expires_at=expires_at,
            active=data.get('active')
        )

