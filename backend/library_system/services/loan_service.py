"""Loan service for managing loan operations."""

from typing import List, Optional
from datetime import date, timedelta
from library_system.models.loan import Loan
from library_system.models.bookcopy import BookCopy
from library_system.database.connection import DatabaseConnection
from library_system.utils.enums import LoanStatus, CopyStatus
from library_system.services.book_service import BookService


class LoanService:
    """Service for loan-related operations."""
    
    def __init__(self, db: DatabaseConnection):
        """Initialize loan service with database connection."""
        self.db = db
        self.client = db.get_client()
        self.book_service = BookService(db)
    
    def issue_book(self, member_id: int, book_id: int, librarian_id: int, loan_days: int = 14) -> Optional[Loan]:
        """
        Issue a book to a member if available copy exists.
        
        Args:
            member_id: ID of the member
            book_id: ID of the book
            librarian_id: ID of the librarian processing the loan
            loan_days: Number of days for the loan (default 14)
            
        Returns:
            Created loan or None if no available copy
        """
        # Check for available copies
        available_copies = self.book_service.get_available_copies(book_id)
        if not available_copies:
            return None  # No available copies
        
        # Get first available copy
        copy = available_copies[0]
        
        # Create loan
        issue_date = date.today()
        due_date = issue_date + timedelta(days=loan_days)
        
        loan = Loan(
            member_id=member_id,
            copy_id=copy.copy_id,
            librarian_id=librarian_id,
            issue_date=issue_date,
            due_date=due_date,
            status=LoanStatus.ACTIVE
        )
        
        # Insert loan - exclude loan_id as it's auto-generated
        loan_dict = loan.to_dict()
        loan_dict.pop('loan_id', None)  # Remove loan_id if present
        result = self.client.table('loan').insert(loan_dict).execute()
        if not result.data:
            raise Exception("Failed to create loan")
        
        # Update copy status
        self.client.table('book_copy').update({'status': CopyStatus.LOANED.value}).eq('copy_id', copy.copy_id).execute()
        
        return Loan.from_dict(result.data[0])
    
    def return_book(self, loan_id: int) -> bool:
        """
        Return a book and update loan status and copy availability.
        
        Returns:
            True if successful
        """
        # Get loan
        loan_result = self.client.table('loan').select('*').eq('loan_id', loan_id).execute()
        if not loan_result.data:
            return False
        
        loan_data = loan_result.data[0]
        copy_id = loan_data['copy_id']
        
        # Update loan
        return_date = date.today()
        self.client.table('loan').update({
            'return_date': return_date.isoformat(),
            'status': LoanStatus.RETURNED.value
        }).eq('loan_id', loan_id).execute()
        
        # Update copy status to available
        self.client.table('book_copy').update({'status': CopyStatus.AVAILABLE.value}).eq('copy_id', copy_id).execute()
        
        return True
    
    def get_loan(self, loan_id: int) -> Optional[Loan]:
        """Get loan by ID."""
        result = self.client.table('loan').select('*').eq('loan_id', loan_id).execute()
        if result.data:
            return Loan.from_dict(result.data[0])
        return None
    
    def get_member_loans(self, member_id: int) -> List[Loan]:
        """Get all loans for a member."""
        result = self.client.table('loan').select('*').eq('member_id', member_id).execute()
        return [Loan.from_dict(row) for row in result.data]
    
    def get_active_loans(self) -> List[Loan]:
        """Get all active loans."""
        result = self.client.table('loan').select('*').eq('status', LoanStatus.ACTIVE.value).execute()
        return [Loan.from_dict(row) for row in result.data]
    
    def update_overdue_loans(self) -> int:
        """
        Automatically identify and update status of overdue loans.
        
        Returns:
            Number of loans updated
        """
        today = date.today()
        result = self.client.table('loan').update({
            'status': LoanStatus.OVERDUE.value
        }).eq('status', LoanStatus.ACTIVE.value).lt('due_date', today.isoformat()).is_('return_date', 'null').execute()
        
        return len(result.data) if result.data else 0
    
    def get_overdue_loans(self) -> List[Loan]:
        """Get all overdue loans."""
        result = self.client.table('loan').select('*').eq('status', LoanStatus.OVERDUE.value).execute()
        return [Loan.from_dict(row) for row in result.data]

