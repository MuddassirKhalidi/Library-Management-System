"""Pytest fixtures for integration tests."""

import pytest
import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file in backend directory (backend/.env)
# From integration/conftest.py, go up 2 levels: integration -> tests -> backend
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    # Also try loading from src/.env if backend/.env doesn't exist
    src_dir = backend_dir.parent
    env_path = src_dir / '.env'
    if env_path.exists():
        load_dotenv(env_path)

from library_system.database.connection import DatabaseConnection
from library_system.services.book_service import BookService
from library_system.services.member_service import MemberService
from library_system.services.loan_service import LoanService
from library_system.services.auth_service import AuthService
from library_system.models.book import Book
from library_system.models.member import Member
from library_system.models.bookcopy import BookCopy
from library_system.models.author import Author
from library_system.models.category import Category
from library_system.models.user import User
from library_system.utils.enums import MemberStatus, CopyStatus, RoleName


@pytest.fixture(scope="session")
def db_connection():
    """
    Create a real database connection for integration tests.
    
    Requires SUPABASE_URL and SUPABASE_KEY environment variables.
    For integration tests, you should use a test database.
    """
    url = os.getenv('SUPABASE_URL') 
    key = os.getenv('SUPABASE_KEY') 
    
    if not url or not key:
        pytest.skip("Integration tests require SUPABASE_URL and SUPABASE_KEY environment variables")
    
    return DatabaseConnection(url=url, key=key)


@pytest.fixture(scope="function")
def book_service(db_connection):
    """Create BookService with real database connection."""
    return BookService(db_connection)


@pytest.fixture(scope="function")
def member_service(db_connection):
    """Create MemberService with real database connection."""
    return MemberService(db_connection)


@pytest.fixture(scope="function")
def loan_service(db_connection):
    """Create LoanService with real database connection."""
    return LoanService(db_connection)


@pytest.fixture(scope="function")
def auth_service(db_connection):
    """Create AuthService with real database connection."""
    return AuthService(db_connection)


@pytest.fixture(scope="function")
def cleanup_test_data(db_connection):
    """
    Cleanup fixture that removes test data after each test.
    
    This fixture runs after each test to clean up any data created during testing.
    """
    yield
    
    # Cleanup code runs after test
    client = db_connection.get_client()
    
    # Delete test loans (clean up in reverse dependency order)
    try:
        # Get test loans (you may want to tag test data with a prefix or use a test schema)
        client.table('loan').delete().like('member_id', '202%').execute()
        client.table('loan').delete().like('copy_id', '999%').execute()
    except:
        pass
    
    # Delete test book copies
    try:
        client.table('book_copy').delete().like('barcode', 'TEST%').execute()
    except:
        pass
    
    # Delete test books
    try:
        client.table('book').delete().like('isbn', 'TEST%').execute()
    except:
        pass
    
    # Delete test members
    try:
        client.table('member').delete().like('email', 'test%').execute()
        client.table('member').delete().eq('member_id', 202).execute()
    except:
        pass
    
    # Delete test users
    try:
        client.table('user').delete().like('email', 'test%').execute()
    except:
        pass


@pytest.fixture
def sample_test_book():
    """Create a sample book for integration testing."""
    return Book(
        isbn='TEST1234567890',
        title='Test Book for Integration',
        publisher='Test Publisher',
        published_year=2024,
        description='A test book for integration testing'
    )


@pytest.fixture
def sample_test_member():
    """Create a sample member for integration testing."""
    return Member(
        name='Test Member',
        email='test_member@integration.test',
        phone='1234567890',
        status=MemberStatus.ACTIVE,
        join_date=date.today()
    )


@pytest.fixture
def sample_test_author():
    """Create a sample author for integration testing."""
    return Author(
        full_name='Test Author'
    )


@pytest.fixture
def sample_test_category():
    """Create a sample category for integration testing."""
    return Category(
        name='Test Category'
    )

