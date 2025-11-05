"""Authentication and authorization service."""

from typing import Optional, List
from library_system.models.user import User
from library_system.database.connection import DatabaseConnection
from library_system.utils.enums import RoleName
import hashlib


class AuthService:
    """Service for authentication and role-based access control."""
    
    def __init__(self, db: DatabaseConnection):
        """Initialize auth service with database connection."""
        self.db = db
        self.client = db.get_client()
    
    def hash_password(self, password: str) -> str:
        """Hash a password (simple implementation)."""
        # In production, use bcrypt or similar
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user.
        
        Returns:
            User object if authentication successful, None otherwise
        """
        result = self.client.table('user').select('*').eq('email', email).execute()
        if not result.data:
            return None
        
        user_data = result.data[0]
        password_hash = self.hash_password(password)
        
        if user_data['password_hash'] == password_hash:
            return User.from_dict(user_data)
        return None
    
    def has_role(self, user: User, required_roles: List[RoleName]) -> bool:
        """Check if user has one of the required roles."""
        return user.role in required_roles
    
    def can_manage_books(self, user: User) -> bool:
        """Check if user can manage books (librarian or administrator)."""
        return user.role in [RoleName.LIBRARIAN, RoleName.ADMINISTRATOR]
    
    def can_manage_members(self, user: User) -> bool:
        """Check if user can manage members (librarian or administrator)."""
        return user.role in [RoleName.LIBRARIAN, RoleName.ADMINISTRATOR]
    
    def create_user(self, user: User, password: str) -> User:
        """Create a new user."""
        user.password_hash = self.hash_password(password)
        result = self.client.table('user').insert(user.to_dict()).execute()
        if result.data:
            return User.from_dict(result.data[0])
        raise Exception("Failed to create user")

