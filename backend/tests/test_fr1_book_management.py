"""
FR1: Add, Edit, and Delete Book Records

Test Cases:
- TC1.1: Add New Book
- TC1.2: Edit Existing Book
- TC1.3: Delete Book Record
"""

import pytest
from unittest.mock import MagicMock
from library_system.models.book import Book
from library_system.models.author import Author
from library_system.models.category import Category
from library_system.utils.enums import CopyStatus


class TestFR1BookManagement:
    """Test cases for FR1: Add, Edit, and Delete Book Records."""
    
    def test_tc1_1_add_new_book(self, book_service, mock_db_client, sample_book, sample_author, sample_category):
        """
        TC1.1: Add New Book
        
        Test Item: BookService.create_book()
        Input Specification:
            Title: 'The Alchemist'
            Author: 'Paulo Coelho'
            ISBN: '1234567890'
            Category: 'Fiction'
        Expected Output:
            Book successfully added
            Confirmation message displayed
        Environmental / Special Requirements: Database connected
        """
        # Setup: Mock database responses
        mock_insert_result = MagicMock()
        mock_insert_result.data = [{
            'book_id': 101,
            'isbn': '1234567890',
            'title': 'The Alchemist',
            'publisher': 'HarperOne',
            'published_year': 1988,
            'description': None
        }]
        
        mock_db_client.table.return_value.insert.return_value.execute.return_value = mock_insert_result
        
        # Mock author and category lookups (if needed)
        mock_author_result = MagicMock()
        mock_author_result.data = [{'author_id': 1, 'full_name': 'Paulo Coelho'}]
        mock_category_result = MagicMock()
        mock_category_result.data = [{'category_id': 1, 'name': 'Fiction'}]
        
        # Execute: Create book
        created_book = book_service.create_book(
            book=sample_book,
            author_ids=[1],
            category_ids=[1]
        )
        
        # Verify: Book successfully created
        assert created_book is not None
        assert created_book.book_id == 101
        assert created_book.title == 'The Alchemist'
        assert created_book.isbn == '1234567890'
        
        # Verify: Database insert was called
        assert mock_db_client.table.called
        
    def test_tc1_2_edit_existing_book(self, book_service, mock_db_client, sample_book):
        """
        TC1.2: Edit Existing Book
        
        Test Item: BookService.update_book()
        Input Specification:
            Existing book with ID=101
            Update title to 'The Alchemist (Updated)'
        Expected Output:
            Updated book record saved successfully
        Environmental / Special Requirements: Database connected
        """
        # Setup: Create existing book and mock update response
        existing_book = Book(
            book_id=101,
            isbn='1234567890',
            title='The Alchemist',
            publisher='HarperOne',
            published_year=1988
        )
        
        updated_book_data = {
            'book_id': 101,
            'isbn': '1234567890',
            'title': 'The Alchemist (Updated)',
            'publisher': 'HarperOne',
            'published_year': 1988,
            'description': None
        }
        
        mock_update_result = MagicMock()
        mock_update_result.data = [updated_book_data]
        
        mock_table = MagicMock()
        mock_table.update.return_value.eq.return_value.execute.return_value = mock_update_result
        mock_db_client.table.return_value = mock_table
        
        # Execute: Update book
        updated_book = Book(
            book_id=101,
            isbn='1234567890',
            title='The Alchemist (Updated)',
            publisher='HarperOne',
            published_year=1988
        )
        
        result = book_service.update_book(101, updated_book)
        
        # Verify: Book successfully updated
        assert result is not None
        assert result.title == 'The Alchemist (Updated)'
        assert result.book_id == 101
        
        # Verify: Update was called with correct parameters
        mock_table.update.assert_called_once()
        mock_table.update.return_value.eq.assert_called_once_with('book_id', 101)
        
    def test_tc1_3_delete_book_record(self, book_service, mock_db_client, sample_book):
        """
        TC1.3: Delete Book Record
        
        Test Item: BookService.deleteBook()
        Input Specification: Book ID=101 (no active loans)
        Expected Output: Book successfully removed
        Environmental / Special Requirements: None
        """
        # Setup: Mock no active loans and successful deletion
        mock_loan_result = MagicMock()
        mock_loan_result.data = []  # No active loans
        
        mock_copies_result = MagicMock()
        mock_copies_result.data = []  # No copies or no active loans on copies
        
        mock_delete_result = MagicMock()
        mock_delete_result.data = []
        
        # Setup chain of calls for loan check
        mock_loan_table = MagicMock()
        mock_loan_table.select.return_value.eq.return_value.in_.return_value.execute.return_value = mock_loan_result
        
        # Setup chain for copies check
        mock_copies_table = MagicMock()
        mock_copies_table.select.return_value.eq.return_value.execute.return_value = mock_copies_result
        
        # Setup chain for delete
        mock_delete_table = MagicMock()
        mock_delete_table.delete.return_value.eq.return_value.execute.return_value = mock_delete_result
        
        # Configure table() to return different mocks based on table name
        def table_side_effect(table_name):
            if table_name == 'loan':
                return mock_loan_table
            elif table_name == 'book_copy':
                return mock_copies_table
            elif table_name == 'book':
                return mock_delete_table
            return MagicMock()
        
        mock_db_client.table.side_effect = table_side_effect
        
        # Execute: Delete book
        result = book_service.delete_book(101)
        
        # Verify: Book successfully deleted
        assert result is True
        
        # Verify: Delete was called
        mock_delete_table.delete.assert_called_once()

