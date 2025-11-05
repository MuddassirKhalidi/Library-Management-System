"""Book service for managing book operations."""

from typing import List, Optional, Dict
from library_system.models.book import Book
from library_system.models.bookcopy import BookCopy
from library_system.models.author import Author
from library_system.models.category import Category
from library_system.database.connection import DatabaseConnection
from library_system.utils.enums import CopyStatus


class BookService:
    """Service for book-related operations."""
    
    def __init__(self, db: DatabaseConnection):
        """Initialize book service with database connection."""
        self.db = db
        self.client = db.get_client()
    
    def create_book(self, book: Book, author_ids: List[int], category_ids: List[int]) -> Book:
        """
        Create a new book record.
        
        Args:
            book: Book object to create
            author_ids: List of author IDs
            category_ids: List of category IDs
            
        Returns:
            Created book with ID
        """
        # Insert book - exclude book_id as it's auto-generated
        book_dict = book.to_dict()
        book_dict.pop('book_id', None)  # Remove book_id if present (should be None anyway)
        result = self.client.table('book').insert(book_dict).execute()
        if not result.data:
            raise Exception("Failed to create book")
        
        book_id = result.data[0]['book_id']
        
        # Link authors
        if author_ids:
            book_author_data = [{'book_id': book_id, 'author_id': aid} for aid in author_ids]
            self.client.table('book_author').insert(book_author_data).execute()
        
        # Link categories
        if category_ids:
            book_category_data = [{'book_id': book_id, 'category_id': cid} for cid in category_ids]
            self.client.table('book_category').insert(book_category_data).execute()
        
        return Book.from_dict(result.data[0])
    
    def get_book(self, book_id: int) -> Optional[Book]:
        """Get book by ID."""
        result = self.client.table('book').select('*').eq('book_id', book_id).execute()
        if result.data:
            return Book.from_dict(result.data[0])
        return None
    
    def get_all_books(self) -> List[Book]:
        """Get all books."""
        result = self.client.table('book').select('*').execute()
        return [Book.from_dict(row) for row in result.data]
    
    def update_book(self, book_id: int, book: Book) -> Optional[Book]:
        """Update book record."""
        result = self.client.table('book').update(book.to_dict()).eq('book_id', book_id).execute()
        if result.data:
            return Book.from_dict(result.data[0])
        return None
    
    def delete_book(self, book_id: int) -> bool:
        """
        Delete book if no active loans exist.
        
        Returns:
            True if deleted, False if book has active loans
        """
        # Check for active loans
        loan_result = self.client.table('loan').select('loan_id').eq('copy_id', book_id).in_('status', ['active', 'overdue']).execute()
        
        # Get all copies for this book
        copies_result = self.client.table('book_copy').select('copy_id').eq('book_id', book_id).execute()
        copy_ids = [c['copy_id'] for c in copies_result.data]
        
        if copy_ids:
            loan_result = self.client.table('loan').select('loan_id').in_('copy_id', copy_ids).in_('status', ['active', 'overdue']).execute()
            if loan_result.data:
                return False  # Book has active loans, cannot delete
        
        # Delete book (cascade will handle related records)
        self.client.table('book').delete().eq('book_id', book_id).execute()
        return True
    
    def search_books(self, isbn: Optional[str] = None, title: Optional[str] = None,
                     author: Optional[str] = None, category: Optional[str] = None) -> List[Dict]:
        """
        Search and filter books.
        
        Returns:
            List of books with author and category information
        """
        query = self.client.table('book').select('*')
        
        if isbn:
            query = query.ilike('isbn', f'%{isbn}%')
        if title:
            query = query.ilike('title', f'%{title}%')
        
        books_result = query.execute()
        books = books_result.data
        
        # Filter by author if specified
        if author:
            author_result = self.client.table('author').select('author_id').ilike('full_name', f'%{author}%').execute()
            author_ids = [a['author_id'] for a in author_result.data]
            if author_ids:
                book_author_result = self.client.table('book_author').select('book_id').in_('author_id', author_ids).execute()
                book_ids = {ba['book_id'] for ba in book_author_result.data}
                books = [b for b in books if b['book_id'] in book_ids]
            else:
                books = []
        
        # Filter by category if specified
        if category:
            category_result = self.client.table('category').select('category_id').ilike('name', f'%{category}%').execute()
            category_ids = [c['category_id'] for c in category_result.data]
            if category_ids:
                book_category_result = self.client.table('book_category').select('book_id').in_('category_id', category_ids).execute()
                book_ids = {bc['book_id'] for bc in book_category_result.data}
                books = [b for b in books if b['book_id'] in book_ids]
            else:
                books = []
        
        # Enrich with author and category info
        enriched_books = []
        for book in books:
            book_id = book['book_id']
            
            # Get authors
            author_ids_result = self.client.table('book_author').select('author_id').eq('book_id', book_id).execute()
            author_ids = [a['author_id'] for a in author_ids_result.data]
            authors_result = self.client.table('author').select('*').in_('author_id', author_ids).execute() if author_ids else []
            authors = [Author.from_dict(a).full_name for a in authors_result.data] if author_ids else []
            
            # Get categories
            category_ids_result = self.client.table('book_category').select('category_id').eq('book_id', book_id).execute()
            category_ids = [c['category_id'] for c in category_ids_result.data]
            categories_result = self.client.table('category').select('*').in_('category_id', category_ids).execute() if category_ids else []
            categories = [Category.from_dict(c).name for c in categories_result.data] if category_ids else []
            
            enriched_books.append({
                **book,
                'authors': authors,
                'categories': categories
            })
        
        return enriched_books
    
    def get_available_copies(self, book_id: int) -> List[BookCopy]:
        """Get available copies of a book."""
        result = self.client.table('book_copy').select('*').eq('book_id', book_id).eq('status', CopyStatus.AVAILABLE.value).execute()
        return [BookCopy.from_dict(row) for row in result.data]
    
    def add_book_copy(self, book_copy: BookCopy) -> BookCopy:
        """Add a new copy of a book."""
        result = self.client.table('book_copy').insert(book_copy.to_dict()).execute()
        if result.data:
            return BookCopy.from_dict(result.data[0])
        raise Exception("Failed to create book copy")

