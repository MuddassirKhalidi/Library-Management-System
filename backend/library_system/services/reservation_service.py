"""Reservation service for managing reservation operations."""

from typing import List, Optional
from datetime import date, timedelta
from library_system.models.reservation import Reservation
from library_system.database.connection import DatabaseConnection


class ReservationService:
    """Service for reservation-related operations."""
    
    def __init__(self, db: DatabaseConnection):
        """Initialize reservation service with database connection."""
        self.db = db
        self.client = db.get_client()
    
    def create_reservation(self, member_id: int, book_id: int, days_valid: int = 14) -> Reservation:
        """Create a new reservation."""
        created_at = date.today()
        expires_at = created_at + timedelta(days=days_valid)
        
        reservation = Reservation(
            member_id=member_id,
            book_id=book_id,
            created_at=created_at,
            expires_at=expires_at,
            active=True
        )
        
        # Exclude reservation_id as it's auto-generated
        reservation_dict = reservation.to_dict()
        reservation_dict.pop('reservation_id', None)  # Remove reservation_id if present
        result = self.client.table('reservation').insert(reservation_dict).execute()
        if result.data:
            return Reservation.from_dict(result.data[0])
        raise Exception("Failed to create reservation")
    
    def get_reservation(self, reservation_id: int) -> Optional[Reservation]:
        """Get reservation by ID."""
        result = self.client.table('reservation').select('*').eq('reservation_id', reservation_id).execute()
        if result.data:
            return Reservation.from_dict(result.data[0])
        return None
    
    def get_member_reservations(self, member_id: int) -> List[Reservation]:
        """Get all reservations for a member."""
        result = self.client.table('reservation').select('*').eq('member_id', member_id).execute()
        return [Reservation.from_dict(row) for row in result.data]
    
    def cancel_reservation(self, reservation_id: int) -> bool:
        """Cancel a reservation."""
        result = self.client.table('reservation').update({'active': False}).eq('reservation_id', reservation_id).execute()
        return bool(result.data)

