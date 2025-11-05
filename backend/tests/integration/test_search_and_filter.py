"""
Integration tests for search and filter functionality.

These tests verify that BookService search and filter work with real database data.
"""

import pytest
from library_system.utils.enums import CopyStatus


@pytest.mark.integration
class TestSearchAndFilter:
    """Integration tests for search and filter operations."""
    
    def test_search_by_title_integration(
        self,
        book_service,
        cleanup_test_data,
        sample_test_book,
        db_connection
    ):
        """
        Integration test: Search for books by title with real database.
        """
        client = db_connection.get_client()
        
        # Create test books with different titles
        author_result = client.table('author').insert({
            'full_name': 'Search Test Author'
        }).execute()
        author_id = author_result.data[0]['author_id']
        
        # Create book with "Alchemist" in title
        book1 = Book(
            isbn='SEARCH001',
            title='The Alchemist',
            publisher='Test Publisher',
            published_year=2024
        )
        created_book1 = book_service.create_book(
            book=book1,
            author_ids=[author_id],
            category_ids=[]
        )
        
        # Create another book with different title
        book2 = Book(
            isbn='SEARCH002',
            title='Different Book Title',
            publisher='Test Publisher',
            published_year=2024
        )
        created_book2 = book_service.create_book(
            book=book2,
            author_ids=[author_id],
            category_ids=[]
        )
        
        # Search for "Alchemist"
        results = book_service.search_books(title='Alchemist')
        
        # Should find at least one book
        assert len(results) >= 1
        assert any('Alchemist' in book.get('title', '') for book in results)
        
        # Search for "Different"
        results2 = book_service.search_books(title='Different')
        
        # Should find the other book
        assert len(results2) >= 1
        assert any('Different' in book.get('title', '') for book in results2)
    
    def test_filter_by_category_integration(
        self,
        book_service,
        cleanup_test_data,
        sample_test_book,
        db_connection
    ):
        """
        Integration test: Filter books by category with real database.
        """
        client = db_connection.get_client()
        
        # Create categories
        fiction_category = client.table('category').insert({
            'name': 'Fiction'
        }).execute()
        fiction_id = fiction_category.data[0]['category_id']
        
        nonfiction_category = client.table('category').insert({
            'name': 'Non-Fiction'
        }).execute()
        nonfiction_id = nonfiction_category.data[0]['category_id']
        
        # Create author
        author_result = client.table('author').insert({
            'full_name': 'Category Test Author'
        }).execute()
        author_id = author_result.data[0]['author_id']
        
        # Create fiction book
        fiction_book = Book(
            isbn='CATEGORY001',
            title='Fiction Book',
            publisher='Test Publisher',
            published_year=2024
        )
        created_fiction_book = book_service.create_book(
            book=fiction_book,
            author_ids=[author_id],
            category_ids=[fiction_id]
        )
        
        # Create non-fiction book
        nonfiction_book = Book(
            isbn='CATEGORY002',
            title='Non-Fiction Book',
            publisher='Test Publisher',
            published_year=2024
        )
        created_nonfiction_book = book_service.create_book(
            book=nonfiction_book,
            author_ids=[author_id],
            category_ids=[nonfiction_id]
        )
        
        # Filter by Fiction category
        fiction_results = book_service.search_books(category='Fiction')
        
        # Should find fiction books
        assert len(fiction_results) >= 1
        
        # Filter by Non-Fiction category
        nonfiction_results = book_service.search_books(category='Non-Fiction')
        
        # Should find non-fiction books
        assert len(nonfiction_results) >= 1

