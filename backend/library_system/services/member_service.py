"""Member service for managing member operations."""

from typing import List, Optional
from library_system.models.member import Member
from library_system.database.connection import DatabaseConnection
from library_system.utils.enums import MemberStatus


class MemberService:
    """Service for member-related operations."""
    
    def __init__(self, db: DatabaseConnection):
        """Initialize member service with database connection."""
        self.db = db
        self.client = db.get_client()
    
    def register_member(self, member: Member) -> Member:
        """Register a new member."""
        # Exclude member_id as it's auto-generated
        member_dict = member.to_dict()
        member_dict.pop('member_id', None)  # Remove member_id if present
        result = self.client.table('member').insert(member_dict).execute()
        if result.data:
            return Member.from_dict(result.data[0])
        raise Exception("Failed to register member")
    
    def get_member(self, member_id: int) -> Optional[Member]:
        """Get member by ID."""
        result = self.client.table('member').select('*').eq('member_id', member_id).execute()
        if result.data:
            return Member.from_dict(result.data[0])
        return None
    
    def get_all_members(self) -> List[Member]:
        """Get all members."""
        result = self.client.table('member').select('*').execute()
        return [Member.from_dict(row) for row in result.data]
    
    def update_member(self, member_id: int, member: Member) -> Optional[Member]:
        """Update member information."""
        result = self.client.table('member').update(member.to_dict()).eq('member_id', member_id).execute()
        if result.data:
            return Member.from_dict(result.data[0])
        return None
    
    def suspend_member(self, member_id: int) -> bool:
        """Suspend a member account."""
        result = self.client.table('member').update({'status': MemberStatus.SUSPENDED.value}).eq('member_id', member_id).execute()
        return bool(result.data)
    
    def deactivate_member(self, member_id: int) -> bool:
        """Deactivate a member account."""
        result = self.client.table('member').update({'status': MemberStatus.INACTIVE.value}).eq('member_id', member_id).execute()
        return bool(result.data)
    
    def delete_member(self, member_id: int) -> bool:
        """
        Delete member if no active loans exist.
        
        Returns:
            True if deleted, False if member has active loans
        """
        # Check for active loans
        loan_result = self.client.table('loan').select('loan_id').eq('member_id', member_id).in_('status', ['active', 'overdue']).execute()
        if loan_result.data:
            return False  # Member has active loans, cannot delete
        
        # Delete member (cascade will handle related records)
        self.client.table('member').delete().eq('member_id', member_id).execute()
        return True

