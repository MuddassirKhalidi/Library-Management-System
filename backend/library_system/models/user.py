"""User model."""

from dataclasses import dataclass
from typing import Optional
from library_system.utils.enums import RoleName


@dataclass
class User:
    """Represents a user in the system."""
    user_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[RoleName] = None

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role.value if self.role else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary."""
        return cls(
            user_id=data.get('user_id'),
            name=data.get('name'),
            email=data.get('email'),
            password_hash=data.get('password_hash'),
            role=RoleName(data['role']) if data.get('role') else None
        )

