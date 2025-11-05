"""
Integration tests for book loan workflow.

These tests verify that multiple services work together correctly:
- BookService and LoanService integration
- MemberService and LoanService integration
- Complete workflows from book creation to loan to return
"""

import pytest
from datetime import date, timedelta
from library_system.models.bookcopy import BookCopy
from library_system.utils.enums import CopyStatus, LoanStatus, MemberStatus


@pytest.mark.integration
class TestBookLoanWorkflow:
    """Integration tests for complete book loan workflows."""
    
    def test_complete_book_loan_cycle(
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
        Test complete workflow: Create book -> Add copy -> Register member -> Issue loan -> Return book.
        
        This integration test verifies that:
        1. Book can be created with author and category
        2. Book copy can be added
        3. Member can be registered
        4. Book can be issued to member
        5. Book can be returned
        6. Copy availability is updated correctly
        """
        client = db_connection.get_client()
        
        # Step 1: Create author and category
        author_result = client.table('author').insert({
            'full_name': 'Integration Test Author'
        }).execute()
        author_id = author_result.data[0]['author_id']
        
        category_result = client.table('category').insert({
            'name': 'Integration Test Category'
        }).execute()
        category_id = category_result.data[0]['category_id']
        
        # Step 2: Create book with author and category
        created_book = book_service.create_book(
            book=sample_test_book,
            author_ids=[author_id],
            category_ids=[category_id]
        )
        
        assert created_book.book_id is not None
        assert created_book.title == sample_test_book.title
        
        # Step 3: Add book copy
        test_copy = BookCopy(
            book_id=created_book.book_id,
            barcode='TEST001',
            status=CopyStatus.AVAILABLE,
            acquired_on=date.today()
        )
        created_copy = book_service.add_book_copy(test_copy)
        
        assert created_copy.copy_id is not None
        assert created_copy.status == CopyStatus.AVAILABLE
        
        # Step 4: Register member
        created_member = member_service.register_member(sample_test_member)
        
        assert created_member.member_id is not None
        assert created_member.email == sample_test_member.email
        
        # Step 5: Issue book to member
        # First, create a librarian user for the loan
        librarian_result = client.table('user').insert({
            'name': 'Test Librarian',
            'email': 'test_librarian@integration.test',
            'password_hash': 'test_hash',
            'role': 'librarian'
        }).execute()
        librarian_id = librarian_result.data[0]['user_id']
        
        # Issue the book
        loan = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_id
        )
        
        assert loan is not None
        assert loan.member_id == created_member.member_id
        assert loan.copy_id == created_copy.copy_id
        assert loan.status == LoanStatus.ACTIVE
        
        # Verify copy is no longer available
        available_copies = book_service.get_available_copies(created_book.book_id)
        assert len(available_copies) == 0
        
        # Step 6: Return the book
        return_result = loan_service.return_book(loan.loan_id)
        
        assert return_result is True
        
        # Verify copy is available again
        available_copies_after = book_service.get_available_copies(created_book.book_id)
        assert len(available_copies_after) == 1
        
        # Verify loan status
        returned_loan = loan_service.get_loan(loan.loan_id)
        assert returned_loan.status == LoanStatus.RETURNED
        assert returned_loan.return_date is not None
    
    def test_cannot_issue_unavailable_book(
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
        Integration test: Verify that books with no available copies cannot be issued.
        """
        client = db_connection.get_client()
        
        # Create book without any copies
        author_result = client.table('author').insert({
            'full_name': 'Test Author 2'
        }).execute()
        
        created_book = book_service.create_book(
            book=sample_test_book,
            author_ids=[author_result.data[0]['author_id']],
            category_ids=[]
        )
        
        # Register member
        created_member = member_service.register_member(sample_test_member)
        
        # Create librarian
        librarian_result = client.table('user').insert({
            'name': 'Test Librarian 2',
            'email': 'test_librarian2@integration.test',
            'password_hash': 'test_hash',
            'role': 'librarian'
        }).execute()
        
        # Attempt to issue book with no copies
        loan = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_result.data[0]['user_id']
        )
        
        # Should return None because no copies available
        assert loan is None
    
    def test_member_loan_history(
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
        Integration test: Verify member loan history tracking.
        """
        client = db_connection.get_client()
        
        # Setup: Create book, copy, member, librarian
        author_result = client.table('author').insert({
            'full_name': 'Test Author 3'
        }).execute()
        
        created_book = book_service.create_book(
            book=sample_test_book,
            author_ids=[author_result.data[0]['author_id']],
            category_ids=[]
        )
        
        # Add two copies
        copy1 = book_service.add_book_copy(BookCopy(
            book_id=created_book.book_id,
            barcode='TEST002',
            status=CopyStatus.AVAILABLE,
            acquired_on=date.today()
        ))
        
        copy2 = book_service.add_book_copy(BookCopy(
            book_id=created_book.book_id,
            barcode='TEST003',
            status=CopyStatus.AVAILABLE,
            acquired_on=date.today()
        ))
        
        created_member = member_service.register_member(sample_test_member)
        
        librarian_result = client.table('user').insert({
            'name': 'Test Librarian 3',
            'email': 'test_librarian3@integration.test',
            'password_hash': 'test_hash',
            'role': 'librarian'
        }).execute()
        librarian_id = librarian_result.data[0]['user_id']
        
        # Issue first loan
        loan1 = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_id
        )
        
        assert loan1 is not None
        
        # Issue second loan
        loan2 = loan_service.issue_book(
            member_id=created_member.member_id,
            book_id=created_book.book_id,
            librarian_id=librarian_id
        )
        
        assert loan2 is not None
        
        # Get member's loan history
        member_loans = loan_service.get_member_loans(created_member.member_id)
        
        # Should have at least 2 loans
        assert len(member_loans) >= 2
        
        # Return one loan
        loan_service.return_book(loan1.loan_id)
        
        # Get updated loan history
        updated_loans = loan_service.get_member_loans(created_member.member_id)
        
        # Should still have both loans, but one should be returned
        returned_loans = [loan for loan in updated_loans if loan.status == LoanStatus.RETURNED]
        active_loans = [loan for loan in updated_loans if loan.status == LoanStatus.ACTIVE]
        
        assert len(returned_loans) >= 1
        assert len(active_loans) >= 1

