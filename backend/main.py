#!/usr/bin/env python3
"""
Library Management System - Main Entry Point
Command-line interface for library operations.
"""

import argparse
import sys
import os
from datetime import date, timedelta
from dotenv import load_dotenv
from library_system.database.connection import DatabaseConnection
from library_system.services.book_service import BookService
from library_system.services.member_service import MemberService
from library_system.services.loan_service import LoanService
from library_system.services.reservation_service import ReservationService
from library_system.services.auth_service import AuthService
from library_system.models.book import Book
from library_system.models.member import Member
from library_system.models.user import User
from library_system.models.bookcopy import BookCopy
from library_system.utils.enums import RoleName, MemberStatus, CopyStatus

# Load environment variables from .env file
load_dotenv()


def setup_database():
    """Initialize database connection."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
        print("Please create a .env file in the src directory with:")
        print("  SUPABASE_URL=your-supabase-url")
        print("  SUPABASE_KEY=your-supabase-key")
        sys.exit(1)
    
    return DatabaseConnection(url, key)


def cmd_create_book(args, db):
    """Create a new book."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email, args.password)
    
    if not user or not auth_service.can_manage_books(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    book_service = BookService(db)
    
    book = Book(
        isbn=args.isbn,
        title=args.title,
        publisher=args.publisher,
        published_year=args.year,
        description=args.description
    )
    
    author_ids = [int(aid) for aid in args.authors.split(',')] if args.authors else []
    category_ids = [int(cid) for cid in args.categories.split(',')] if args.categories else []
    
    try:
        created_book = book_service.create_book(book, author_ids, category_ids)
        print(f"Book created successfully: ID={created_book.book_id}, Title={created_book.title}")
    except Exception as e:
        print(f"Error creating book: {e}")


def cmd_search_books(args, db):
    """Search books."""
    book_service = BookService(db)
    
    results = book_service.search_books(
        isbn=args.isbn,
        title=args.title,
        author=args.author,
        category=args.category
    )
    
    if not results:
        print("No books found.")
        return
    
    print(f"\nFound {len(results)} book(s):\n")
    for book in results:
        print(f"ID: {book['book_id']}")
        print(f"ISBN: {book['isbn']}")
        print(f"Title: {book['title']}")
        print(f"Authors: {', '.join(book['authors']) if book['authors'] else 'N/A'}")
        print(f"Categories: {', '.join(book['categories']) if book['categories'] else 'N/A'}")
        print(f"Publisher: {book.get('publisher', 'N/A')}")
        print(f"Year: {book.get('published_year', 'N/A')}")
        print("-" * 50)


def cmd_register_member(args, db):
    """Register a new member."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_members(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    member_service = MemberService(db)
    
    member = Member(
        name=args.name,
        email=args.email,
        phone=args.phone,
        status=MemberStatus.ACTIVE,
        join_date=date.today()
    )
    
    try:
        created_member = member_service.register_member(member)
        print(f"Member registered successfully: ID={created_member.member_id}, Name={created_member.name}")
    except Exception as e:
        print(f"Error registering member: {e}")


def cmd_update_member(args, db):
    """Update member information."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_members(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    member_service = MemberService(db)
    
    member = Member(
        name=args.name,
        email=args.email,
        phone=args.phone
    )
    
    try:
        updated = member_service.update_member(args.member_id, member)
        if updated:
            print(f"Member updated successfully: ID={updated.member_id}")
        else:
            print(f"Error: Member with ID {args.member_id} not found.")
    except Exception as e:
        print(f"Error updating member: {e}")


def cmd_suspend_member(args, db):
    """Suspend a member."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_members(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    member_service = MemberService(db)
    
    if member_service.suspend_member(args.member_id):
        print(f"Member {args.member_id} suspended successfully.")
    else:
        print(f"Error: Failed to suspend member {args.member_id}.")


def cmd_issue_book(args, db):
    """Issue a book to a member."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_books(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    loan_service = LoanService(db)
    
    # Get librarian ID from user
    librarian_result = db.get_client().table('librarian').select('employee_id').eq('user_id', user.user_id).execute()
    if not librarian_result.data:
        print("Error: User is not a librarian.")
        return
    
    librarian_id = librarian_result.data[0]['employee_id']
    
    try:
        loan = loan_service.issue_book(args.member_id, args.book_id, librarian_id, args.days or 14)
        if loan:
            print(f"Book issued successfully: Loan ID={loan.loan_id}, Due Date={loan.due_date}")
        else:
            print("Error: No available copies of this book.")
    except Exception as e:
        print(f"Error issuing book: {e}")


def cmd_return_book(args, db):
    """Return a book."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_books(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    loan_service = LoanService(db)
    
    if loan_service.return_book(args.loan_id):
        print(f"Book returned successfully: Loan ID={args.loan_id}")
    else:
        print(f"Error: Failed to return book. Loan ID {args.loan_id} not found.")


def cmd_update_overdue(args, db):
    """Update overdue loans."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_books(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    loan_service = LoanService(db)
    count = loan_service.update_overdue_loans()
    print(f"Updated {count} overdue loan(s).")


def cmd_list_overdue(args, db):
    """List overdue loans."""
    loan_service = LoanService(db)
    overdue = loan_service.get_overdue_loans()
    
    if not overdue:
        print("No overdue loans.")
        return
    
    print(f"\nFound {len(overdue)} overdue loan(s):\n")
    for loan in overdue:
        print(f"Loan ID: {loan.loan_id}")
        print(f"Member ID: {loan.member_id}")
        print(f"Due Date: {loan.due_date}")
        print("-" * 50)


def cmd_delete_book(args, db):
    """Delete a book."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_books(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    book_service = BookService(db)
    
    if book_service.delete_book(args.book_id):
        print(f"Book {args.book_id} deleted successfully.")
    else:
        print(f"Error: Cannot delete book {args.book_id}. Book has active loans.")


def cmd_delete_member(args, db):
    """Delete a member."""
    auth_service = AuthService(db)
    user = auth_service.authenticate(args.email_auth, args.password_auth)
    
    if not user or not auth_service.can_manage_members(user):
        print("Error: Unauthorized. Librarian or administrator access required.")
        return
    
    member_service = MemberService(db)
    
    if member_service.delete_member(args.member_id):
        print(f"Member {args.member_id} deleted successfully.")
    else:
        print(f"Error: Cannot delete member {args.member_id}. Member has active loans.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Library Management System')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create book command
    create_book_parser = subparsers.add_parser('create-book', help='Create a new book')
    create_book_parser.add_argument('--email', required=True, help='Librarian email')
    create_book_parser.add_argument('--password', required=True, help='Librarian password')
    create_book_parser.add_argument('--isbn', required=True, help='Book ISBN')
    create_book_parser.add_argument('--title', required=True, help='Book title')
    create_book_parser.add_argument('--publisher', help='Publisher name')
    create_book_parser.add_argument('--year', type=int, help='Published year')
    create_book_parser.add_argument('--description', help='Book description')
    create_book_parser.add_argument('--authors', help='Comma-separated author IDs')
    create_book_parser.add_argument('--categories', help='Comma-separated category IDs')
    
    # Search books command
    search_parser = subparsers.add_parser('search-books', help='Search books')
    search_parser.add_argument('--isbn', help='ISBN filter')
    search_parser.add_argument('--title', help='Title filter')
    search_parser.add_argument('--author', help='Author name filter')
    search_parser.add_argument('--category', help='Category name filter')
    
    # Register member command
    register_member_parser = subparsers.add_parser('register-member', help='Register a new member')
    register_member_parser.add_argument('--email-auth', required=True, help='Librarian email')
    register_member_parser.add_argument('--password-auth', required=True, help='Librarian password')
    register_member_parser.add_argument('--name', required=True, help='Member name')
    register_member_parser.add_argument('--email', required=True, help='Member email')
    register_member_parser.add_argument('--phone', help='Member phone')
    
    # Update member command
    update_member_parser = subparsers.add_parser('update-member', help='Update member information')
    update_member_parser.add_argument('--email-auth', required=True, help='Librarian email')
    update_member_parser.add_argument('--password-auth', required=True, help='Librarian password')
    update_member_parser.add_argument('--member-id', type=int, required=True, help='Member ID')
    update_member_parser.add_argument('--name', help='Member name')
    update_member_parser.add_argument('--email', help='Member email')
    update_member_parser.add_argument('--phone', help='Member phone')
    
    # Suspend member command
    suspend_member_parser = subparsers.add_parser('suspend-member', help='Suspend a member')
    suspend_member_parser.add_argument('--email-auth', required=True, help='Librarian email')
    suspend_member_parser.add_argument('--password-auth', required=True, help='Librarian password')
    suspend_member_parser.add_argument('--member-id', type=int, required=True, help='Member ID')
    
    # Issue book command
    issue_book_parser = subparsers.add_parser('issue-book', help='Issue a book to a member')
    issue_book_parser.add_argument('--email-auth', required=True, help='Librarian email')
    issue_book_parser.add_argument('--password-auth', required=True, help='Librarian password')
    issue_book_parser.add_argument('--member-id', type=int, required=True, help='Member ID')
    issue_book_parser.add_argument('--book-id', type=int, required=True, help='Book ID')
    issue_book_parser.add_argument('--days', type=int, help='Loan duration in days (default: 14)')
    
    # Return book command
    return_book_parser = subparsers.add_parser('return-book', help='Return a book')
    return_book_parser.add_argument('--email-auth', required=True, help='Librarian email')
    return_book_parser.add_argument('--password-auth', required=True, help='Librarian password')
    return_book_parser.add_argument('--loan-id', type=int, required=True, help='Loan ID')
    
    # Update overdue command
    update_overdue_parser = subparsers.add_parser('update-overdue', help='Update overdue loans')
    update_overdue_parser.add_argument('--email-auth', required=True, help='Librarian email')
    update_overdue_parser.add_argument('--password-auth', required=True, help='Librarian password')
    
    # List overdue command
    list_overdue_parser = subparsers.add_parser('list-overdue', help='List overdue loans')
    
    # Delete book command
    delete_book_parser = subparsers.add_parser('delete-book', help='Delete a book')
    delete_book_parser.add_argument('--email-auth', required=True, help='Librarian email')
    delete_book_parser.add_argument('--password-auth', required=True, help='Librarian password')
    delete_book_parser.add_argument('--book-id', type=int, required=True, help='Book ID')
    
    # Delete member command
    delete_member_parser = subparsers.add_parser('delete-member', help='Delete a member')
    delete_member_parser.add_argument('--email-auth', required=True, help='Librarian email')
    delete_member_parser.add_argument('--password-auth', required=True, help='Librarian password')
    delete_member_parser.add_argument('--member-id', type=int, required=True, help='Member ID')
    
    # Handle common mistakes where users use -- before command
    if len(sys.argv) > 1 and sys.argv[1].startswith('--'):
        cmd = sys.argv[1].lstrip('--')
        if cmd in ['list-overdue', 'create-book', 'search-books', 'register-member', 
                   'update-member', 'suspend-member', 'issue-book', 'return-book',
                   'update-overdue', 'delete-book', 'delete-member']:
            print(f"Error: '{sys.argv[1]}' is a command, not a flag.")
            print(f"Correct usage: python main.py {cmd}")
            print(f"\nFor help: python main.py {cmd} --help")
            sys.exit(1)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\nNote: Commands are subcommands (e.g., 'list-overdue'), not flags (e.g., '--list-overdue')")
        sys.exit(1)
    
    # Initialize database
    try:
        db = setup_database()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Route to appropriate command handler
    command_handlers = {
        'create-book': cmd_create_book,
        'search-books': cmd_search_books,
        'register-member': cmd_register_member,
        'update-member': cmd_update_member,
        'suspend-member': cmd_suspend_member,
        'issue-book': cmd_issue_book,
        'return-book': cmd_return_book,
        'update-overdue': cmd_update_overdue,
        'list-overdue': cmd_list_overdue,
        'delete-book': cmd_delete_book,
        'delete-member': cmd_delete_member,
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        handler(args, db)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == '__main__':
    main()

