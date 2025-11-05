"""Member model."""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from library_system.utils.enums import MemberStatus


@dataclass
class Member:
    """Represents a library member."""
    member_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[MemberStatus] = None
    join_date: Optional[date] = None

    def to_dict(self) -> dict:
        """Convert member to dictionary."""
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status.value if self.status else None,
            'join_date': self.join_date.isoformat() if self.join_date else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        """Create member from dictionary."""
        join_date = None
        if data.get('join_date'):
            if isinstance(data['join_date'], str):
                join_date = date.fromisoformat(data['join_date'])
            else:
                join_date = data['join_date']
        
        return cls(
            member_id=data.get('member_id'),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            status=MemberStatus(data['status']) if data.get('status') else None,
            join_date=join_date
        )

