"""Loan model."""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from library_system.utils.enums import LoanStatus


@dataclass
class Loan:
    """Represents a book loan."""
    loan_id: Optional[int] = None
    member_id: Optional[int] = None
    copy_id: Optional[int] = None
    librarian_id: Optional[int] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    return_date: Optional[date] = None
    status: Optional[LoanStatus] = None

    def to_dict(self) -> dict:
        """Convert loan to dictionary."""
        return {
            'loan_id': self.loan_id,
            'member_id': self.member_id,
            'copy_id': self.copy_id,
            'librarian_id': self.librarian_id,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status.value if self.status else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Loan':
        """Create loan from dictionary."""
        issue_date = None
        if data.get('issue_date'):
            if isinstance(data['issue_date'], str):
                issue_date = date.fromisoformat(data['issue_date'])
            else:
                issue_date = data['issue_date']
        
        due_date = None
        if data.get('due_date'):
            if isinstance(data['due_date'], str):
                due_date = date.fromisoformat(data['due_date'])
            else:
                due_date = data['due_date']
        
        return_date = None
        if data.get('return_date'):
            if isinstance(data['return_date'], str):
                return_date = date.fromisoformat(data['return_date'])
            else:
                return_date = data['return_date']
        
        return cls(
            loan_id=data.get('loan_id'),
            member_id=data.get('member_id'),
            copy_id=data.get('copy_id'),
            librarian_id=data.get('librarian_id'),
            issue_date=issue_date,
            due_date=due_date,
            return_date=return_date,
            status=LoanStatus(data['status']) if data.get('status') else None
        )

