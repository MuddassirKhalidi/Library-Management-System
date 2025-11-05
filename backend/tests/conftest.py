"""Pytest configuration and fixtures for test suite."""

import pytest
import os
from unittest.mock import Mock, MagicMock
from datetime import date, timedelta
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
from library_system.models.loan import Loan
from library_system.models.user import User
from library_system.utils.enums import MemberStatus, CopyStatus, LoanStatus, RoleName


@pytest.fixture
def mock_db_client():
    """Create a mock Supabase client."""
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def mock_db_connection(mock_db_client):
    """Create a mock database connection."""
    mock_db = MagicMock(spec=DatabaseConnection)
    mock_db.get_client.return_value = mock_db_client
    mock_db.client = mock_db_client
    return mock_db


@pytest.fixture
def book_service(mock_db_connection):
    """Create a BookService instance with mock database."""
    return BookService(mock_db_connection)


@pytest.fixture
def member_service(mock_db_connection):
    """Create a MemberService instance with mock database."""
    return MemberService(mock_db_connection)


@pytest.fixture
def loan_service(mock_db_connection):
    """Create a LoanService instance with mock database."""
    return LoanService(mock_db_connection)


@pytest.fixture
def auth_service(mock_db_connection):
    """Create an AuthService instance with mock database."""
    return AuthService(mock_db_connection)


@pytest.fixture
def sample_book():
    """Create a sample book for testing."""
    return Book(
        book_id=101,
        isbn='1234567890',
        title='The Alchemist',
        publisher='HarperOne',
        published_year=1988,
        description='A novel about following your dreams'
    )


@pytest.fixture
def sample_author():
    """Create a sample author for testing."""
    return Author(
        author_id=1,
        full_name='Paulo Coelho'
    )


@pytest.fixture
def sample_category():
    """Create a sample category for testing."""
    return Category(
        category_id=1,
        name='Fiction'
    )


@pytest.fixture
def sample_member():
    """Create a sample member for testing."""
    return Member(
        member_id=202,
        name='Ali',
        email='ali@test.com',
        phone='1234567890',
        status=MemberStatus.ACTIVE,
        join_date=date.today()
    )


@pytest.fixture
def sample_book_copy(sample_book):
    """Create a sample book copy for testing."""
    return BookCopy(
        copy_id=1,
        book_id=sample_book.book_id,
        barcode='BC001',
        status=CopyStatus.AVAILABLE,
        acquired_on=date.today()
    )


@pytest.fixture
def sample_loan(sample_member, sample_book_copy):
    """Create a sample loan for testing."""
    return Loan(
        loan_id=301,
        member_id=sample_member.member_id,
        copy_id=sample_book_copy.copy_id,
        librarian_id=1,
        issue_date=date.today() - timedelta(days=5),
        due_date=date.today() + timedelta(days=9),
        return_date=None,
        status=LoanStatus.ACTIVE
    )


@pytest.fixture
def sample_librarian_user():
    """Create a sample librarian user for testing."""
    return User(
        user_id=1,
        name='Librarian',
        email='librarian@library.com',
        password_hash='hash12345',  # Will be hashed properly in tests
        role=RoleName.LIBRARIAN
    )


@pytest.fixture
def sample_member_user():
    """Create a sample member user for testing."""
    return User(
        user_id=2,
        name='Member User',
        email='member@library.com',
        password_hash='hash12345',
        role=RoleName.MEMBER
    )

