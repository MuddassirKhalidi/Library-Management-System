"""
FR7: Prevent Deletion of Loaned Books or Members with Active Loans

Test Cases:
- TC7.1: Attempt to Delete Loaned Book
- TC7.2: Attempt to Delete Member with Active Loan
"""

import pytest
from unittest.mock import MagicMock
from library_system.utils.enums import LoanStatus, CopyStatus


class TestFR7PreventDeletion:
    """Test cases for FR7: Prevent Deletion of Loaned Books or Members with Active Loans."""
    
    def test_tc7_1_attempt_to_delete_loaned_book(self, book_service, mock_db_client):
        """
        TC7.1: Attempt to Delete Loaned Book
        
        Test Item: BookService.deleteBook()
        Input Specification:
            Book ID=101 (currently loaned)
        Expected Output:
            Error message 'Cannot delete loaned book'
        Environmental / Special Requirements: Database connected
        """
        # Setup: Mock active loan exists for book copies
        mock_active_loan_result = MagicMock()
        mock_active_loan_result.data = [{'loan_id': 301}]  # Active loan exists
        
        mock_copies_result = MagicMock()
        mock_copies_result.data = [{'copy_id': 1}]  # Book has copies
        
        # Setup table mocks
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'loan':
                # First call for initial check, second for copy-based check
                if not hasattr(mock_table, '_call_count'):
                    mock_table._call_count = 0
                mock_table._call_count += 1
                mock_query = MagicMock()
                mock_query.in_.return_value.execute.return_value = mock_active_loan_result
                mock_table.select.return_value.eq.return_value = mock_query
            elif table_name == 'book_copy':
                mock_table.select.return_value.eq.return_value.execute.return_value = mock_copies_result
            return mock_table
        
        mock_db_client.table.side_effect = table_side_effect
        
        # Execute: Attempt to delete loaned book
        result = book_service.delete_book(book_id=101)
        
        # Verify: Book deletion prevented (returns False)
        assert result is False
        
        # Verify: Delete was not called on book table
        # (The method should return False before attempting deletion)
        
    def test_tc7_2_attempt_to_delete_member_with_active_loan(self, member_service, mock_db_client):
        """
        TC7.2: Attempt to Delete Member with Active Loan
        
        Test Item: MemberService.deleteMember()
        Input Specification:
            Member ID=202 (active loan)
        Expected Output:
            Error message 'Cannot delete member with active loan'
        Environmental / Special Requirements: None
        """
        # Setup: Mock active loan exists for member
        mock_active_loan_result = MagicMock()
        mock_active_loan_result.data = [{'loan_id': 301}]  # Active loan exists
        
        # Setup table mocks
        def table_side_effect(table_name):
            mock_table = MagicMock()
            if table_name == 'loan':
                mock_query = MagicMock()
                mock_query.in_.return_value.execute.return_value = mock_active_loan_result
                mock_table.select.return_value.eq.return_value = mock_query
            elif table_name == 'member':
                mock_delete = MagicMock()
                mock_delete.eq.return_value.execute.return_value = MagicMock()
                mock_table.delete.return_value = mock_delete
            return mock_table
        
        mock_db_client.table.side_effect = table_side_effect
        
        # Execute: Attempt to delete member with active loan
        result = member_service.delete_member(member_id=202)
        
        # Verify: Member deletion prevented (returns False)
        assert result is False
        
        # Verify: Delete was not called on member table
        # (The method should return False before attempting deletion)

