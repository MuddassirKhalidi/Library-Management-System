"""
Integration tests for book and member deletion with active loans.

These tests verify the business rules around deletion when loans exist.
"""

import pytest
from datetime import date
from library_system.models.bookcopy import BookCopy
from library_system.utils.enums import CopyStatus, LoanStatus


@pytest.mark.integration
class TestBookMemberDeletion:
    """Integration tests for deletion prevention with active loans."""
    
    def test_cannot_delete_book_with_active_loan(
        self,
        book_service,
        member_service,
        loan_service,
        cleanup_test_data,
        sample_test_book,
        sample_test_member,
        db_connection
    ):
        """
        Integration test: Verify that books with active loans cannot be deleted.
        """
        client = db_connection.get_client()
        
        # Setup: Create book, copy, member, and active loan
        author_result = client.table('author').insert({
            'full_name': 'Test Author Delete'
        }).execute()
        
        created_book = book_service.create_book(
            book=sample_test_book,
            author_ids=[author_result.data[0]['author_id']],
            category_ids=[]
        )
        
        copy = book_service.add_book_copy(BookCopy(
            book_id=created_book.book_id,
            barcode='TEST_DELETE001',
            status=CopyStatus.AVAILABLE,
            acquired_on=date.today()
        ))
        
        created_member = member_service.register_member(sample_test_member)
        
        librarian_result = client.table('user').insert({
            'name': 'Test Librarian Delete',
            'email': 'test_librarian_delete@integration.test',
            'password_hash': 'test_hash',
            'role': 'librarian'
        }).execute()
        
        # Issue loan
        loan = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_result.data[0]['user_id']
        )
        
        assert loan is not None
        
        # Attempt to delete book with active loan
        delete_result = book_service.delete_book(created_book.book_id)
        
        # Should fail because book has active loan
        assert delete_result is False
        
        # Return the book
        loan_service.return_book(loan.loan_id)
        
        # Now deletion should succeed
        delete_result_after_return = book_service.delete_book(created_book.book_id)
        assert delete_result_after_return is True
    
    def test_cannot_delete_member_with_active_loan(
        self,
        book_service,
        member_service,
        loan_service,
        cleanup_test_data,
        sample_test_book,
        sample_test_member,
        db_connection
    ):
        """
        Integration test: Verify that members with active loans cannot be deleted.
        """
        client = db_connection.get_client()
        
        # Setup: Create book, copy, member, and active loan
        author_result = client.table('author').insert({
            'full_name': 'Test Author Delete Member'
        }).execute()
        
        created_book = book_service.create_book(
            book=sample_test_book,
            author_ids=[author_result.data[0]['author_id']],
            category_ids=[]
        )
        
        copy = book_service.add_book_copy(BookCopy(
            book_id=created_book.book_id,
            barcode='TEST_DELETE_MEMBER001',
            status=CopyStatus.AVAILABLE,
            acquired_on=date.today()
        ))
        
        created_member = member_service.register_member(sample_test_member)
        
        librarian_result = client.table('user').insert({
            'name': 'Test Librarian Delete Member',
            'email': 'test_librarian_delete_member@integration.test',
            'password_hash': 'test_hash',
            'role': 'librarian'
        }).execute()
        
        # Issue loan
        loan = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_result.data[0]['user_id']
        )
        
        assert loan is not None
        
        # Attempt to delete member with active loan
        delete_result = member_service.delete_member(created_member.member_id)
        
        # Should fail because member has active loan
        assert delete_result is False
        
        # Return the book
        loan_service.return_book(loan.loan_id)
        
        # Now deletion should succeed
        delete_result_after_return = member_service.delete_member(created_member.member_id)
        assert delete_result_after_return is True

