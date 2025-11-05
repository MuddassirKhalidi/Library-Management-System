#!/usr/bin/env python3
"""
REST API Server for Library Management System
FastAPI server that exposes endpoints for books, members, and loans.
"""

import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List
from datetime import date
from library_system.database.connection import DatabaseConnection
from library_system.services.book_service import BookService
from library_system.services.member_service import MemberService
from library_system.services.loan_service import LoanService
from library_system.services.auth_service import AuthService
from library_system.services.reservation_service import ReservationService
from library_system.models.loan import Loan
from library_system.models.book import Book
from library_system.models.member import Member
from library_system.models.reservation import Reservation
from library_system.utils.enums import MemberStatus

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Library Management System API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
def get_db():
    """Initialize and return database connection."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        raise Exception("SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
    
    return DatabaseConnection(url, key)


# Pydantic models for request bodies
class LoginRequest(BaseModel):
    email: str
    password: str


class BookCreateRequest(BaseModel):
    isbn: str
    title: str
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None
    author_ids: Optional[List[int]] = []
    category_ids: Optional[List[int]] = []


class BookUpdateRequest(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    description: Optional[str] = None


class MemberRegisterRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class MemberUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class IssueBookRequest(BaseModel):
    member_id: int
    book_id: int
    days: Optional[int] = 14


class ReturnBookRequest(BaseModel):
    loan_id: int


class ReservationCreateRequest(BaseModel):
    member_id: int
    book_id: int
    days_valid: Optional[int] = 14


# Helper function to get authenticated user
async def get_authenticated_user(email: str, password: str):
    """Authenticate user and return user object."""
    db = get_db()
    auth_service = AuthService(db)
    user = auth_service.authenticate(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


# Helper function to check if user can manage books
async def check_book_management_permission(email: str, password: str):
    """Check if user can manage books."""
    user = await get_authenticated_user(email, password)
    auth_service = AuthService(get_db())
    if not auth_service.can_manage_books(user):
        raise HTTPException(status_code=403, detail="Librarian or administrator access required")
    return user


# Helper function to check if user can manage members
async def check_member_management_permission(email: str, password: str):
    """Check if user can manage members."""
    user = await get_authenticated_user(email, password)
    auth_service = AuthService(get_db())
    if not auth_service.can_manage_members(user):
        raise HTTPException(status_code=403, detail="Librarian or administrator access required")
    return user


# Helper function to get librarian_id from user
def get_librarian_id(db: DatabaseConnection, user_id: int) -> Optional[int]:
    """Get librarian employee_id from user_id."""
    client = db.get_client()
    result = client.table('librarian').select('employee_id').eq('user_id', user_id).execute()
    if result.data:
        return result.data[0]['employee_id']
    return None


# Books endpoints
@app.get("/api/books")
async def get_all_books():
    """Get all books."""
    try:
        db = get_db()
        book_service = BookService(db)
        books = book_service.get_all_books()
        
        # Enrich with author and category info
        enriched_books = []
        for book in books:
            book_dict = book.to_dict()
            # Get authors and categories using search_books
            search_results = book_service.search_books(title=book.title)
            if search_results:
                enriched = search_results[0]
                book_dict['authors'] = enriched.get('authors', [])
                book_dict['categories'] = enriched.get('categories', [])
            else:
                book_dict['authors'] = []
                book_dict['categories'] = []
            enriched_books.append(book_dict)
        
        return {"books": enriched_books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/search")
async def search_books(
    isbn: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    category: Optional[str] = None
):
    """Search books by various criteria."""
    try:
        db = get_db()
        book_service = BookService(db)
        results = book_service.search_books(isbn=isbn, title=title, author=author, category=category)
        return {"books": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/{book_id}")
async def get_book(book_id: int):
    """Get a specific book by ID."""
    try:
        db = get_db()
        book_service = BookService(db)
        book = book_service.get_book(book_id)
        
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book_dict = book.to_dict()
        # Enrich with author and category info
        search_results = book_service.search_books(title=book.title)
        if search_results:
            enriched = search_results[0]
            book_dict['authors'] = enriched.get('authors', [])
            book_dict['categories'] = enriched.get('categories', [])
        else:
            book_dict['authors'] = []
            book_dict['categories'] = []
        
        return {"book": book_dict}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Members endpoints
@app.get("/api/members")
async def get_all_members():
    """Get all members."""
    try:
        db = get_db()
        member_service = MemberService(db)
        members = member_service.get_all_members()
        return {"members": [member.to_dict() for member in members]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/members/{member_id}")
async def get_member(member_id: int):
    """Get a specific member by ID."""
    try:
        db = get_db()
        member_service = MemberService(db)
        member = member_service.get_member(member_id)
        
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        return {"member": member.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Loans endpoints
@app.get("/api/loans")
async def get_all_loans():
    """Get all loans."""
    try:
        db = get_db()
        loan_service = LoanService(db)
        # Get all loans by querying the database directly
        client = db.get_client()
        result = client.table('loan').select('*').execute()
        loans = [Loan.from_dict(row) for row in result.data]
        return {"loans": [loan.to_dict() for loan in loans]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/loans/overdue")
async def get_overdue_loans():
    """Get all overdue loans."""
    try:
        db = get_db()
        loan_service = LoanService(db)
        overdue = loan_service.get_overdue_loans()
        return {"loans": [loan.to_dict() for loan in overdue]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/loans/active")
async def get_active_loans():
    """Get all active loans."""
    try:
        db = get_db()
        loan_service = LoanService(db)
        active = loan_service.get_active_loans()
        return {"loans": [loan.to_dict() for loan in active]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/loans/member/{member_id}")
async def get_member_loans(member_id: int):
    """Get all loans for a specific member."""
    try:
        db = get_db()
        loan_service = LoanService(db)
        loans = loan_service.get_member_loans(member_id)
        return {"loans": [loan.to_dict() for loan in loans]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Authentication endpoints
@app.post("/api/auth/login")
async def login(request: LoginRequest):
    """Authenticate a user."""
    try:
        db = get_db()
        auth_service = AuthService(db)
        user = auth_service.authenticate(request.email, request.password)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Get librarian_id if user is a librarian
        librarian_id = None
        if user.role.value in ['librarian', 'administrator']:
            librarian_id = get_librarian_id(db, user.user_id)
        
        return {
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            },
            "librarian_id": librarian_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Books CRUD endpoints
@app.post("/api/books")
async def create_book(request: BookCreateRequest, email: str, password: str):
    """Create a new book (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        book_service = BookService(db)
        
        book = Book(
            isbn=request.isbn,
            title=request.title,
            publisher=request.publisher,
            published_year=request.published_year,
            description=request.description
        )
        
        created_book = book_service.create_book(book, request.author_ids or [], request.category_ids or [])
        book_dict = created_book.to_dict()
        
        # Enrich with author and category info
        search_results = book_service.search_books(title=created_book.title)
        if search_results:
            enriched = search_results[0]
            book_dict['authors'] = enriched.get('authors', [])
            book_dict['categories'] = enriched.get('categories', [])
        else:
            book_dict['authors'] = []
            book_dict['categories'] = []
        
        return {"book": book_dict}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/books/{book_id}")
async def update_book(book_id: int, request: BookUpdateRequest, email: str, password: str):
    """Update a book (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        book_service = BookService(db)
        
        # Get existing book
        existing_book = book_service.get_book(book_id)
        if not existing_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Update fields
        update_dict = {}
        if request.isbn is not None:
            update_dict['isbn'] = request.isbn
        if request.title is not None:
            update_dict['title'] = request.title
        if request.publisher is not None:
            update_dict['publisher'] = request.publisher
        if request.published_year is not None:
            update_dict['published_year'] = request.published_year
        if request.description is not None:
            update_dict['description'] = request.description
        
        if update_dict:
            book = Book(**{**existing_book.to_dict(), **update_dict})
            updated_book = book_service.update_book(book_id, book)
            if updated_book:
                book_dict = updated_book.to_dict()
                # Enrich with author and category info
                search_results = book_service.search_books(title=updated_book.title)
                if search_results:
                    enriched = search_results[0]
                    book_dict['authors'] = enriched.get('authors', [])
                    book_dict['categories'] = enriched.get('categories', [])
                else:
                    book_dict['authors'] = []
                    book_dict['categories'] = []
                return {"book": book_dict}
        
        return {"book": existing_book.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/books/{book_id}")
async def delete_book(book_id: int, email: str, password: str):
    """Delete a book (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        book_service = BookService(db)
        
        if book_service.delete_book(book_id):
            return {"message": f"Book {book_id} deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Cannot delete book. Book has active loans.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Members CRUD endpoints
@app.post("/api/members")
async def register_member(request: MemberRegisterRequest, email: str, password: str):
    """Register a new member (Librarian/Administrator only)."""
    try:
        user = await check_member_management_permission(email, password)
        db = get_db()
        member_service = MemberService(db)
        
        member = Member(
            name=request.name,
            email=request.email,
            phone=request.phone,
            status=MemberStatus.ACTIVE,
            join_date=date.today()
        )
        
        created_member = member_service.register_member(member)
        return {"member": created_member.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/members/{member_id}")
async def update_member(member_id: int, request: MemberUpdateRequest, email: str, password: str):
    """Update member information (Librarian/Administrator only)."""
    try:
        user = await check_member_management_permission(email, password)
        db = get_db()
        member_service = MemberService(db)
        
        # Get existing member
        existing_member = member_service.get_member(member_id)
        if not existing_member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Update fields
        update_dict = {}
        if request.name is not None:
            update_dict['name'] = request.name
        if request.email is not None:
            update_dict['email'] = request.email
        if request.phone is not None:
            update_dict['phone'] = request.phone
        
        if update_dict:
            member = Member(**{**existing_member.to_dict(), **update_dict})
            updated_member = member_service.update_member(member_id, member)
            if updated_member:
                return {"member": updated_member.to_dict()}
        
        return {"member": existing_member.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/members/{member_id}/suspend")
async def suspend_member(member_id: int, email: str, password: str):
    """Suspend a member (Librarian/Administrator only)."""
    try:
        user = await check_member_management_permission(email, password)
        db = get_db()
        member_service = MemberService(db)
        
        if member_service.suspend_member(member_id):
            return {"message": f"Member {member_id} suspended successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to suspend member")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/members/{member_id}")
async def delete_member(member_id: int, email: str, password: str):
    """Delete a member (Librarian/Administrator only)."""
    try:
        user = await check_member_management_permission(email, password)
        db = get_db()
        member_service = MemberService(db)
        
        if member_service.delete_member(member_id):
            return {"message": f"Member {member_id} deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Cannot delete member. Member has active loans.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Loan operations
@app.post("/api/loans/issue")
async def issue_book(request: IssueBookRequest, email: str, password: str):
    """Issue a book to a member (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        loan_service = LoanService(db)
        
        # Get librarian_id from user
        librarian_id = get_librarian_id(db, user.user_id)
        if not librarian_id:
            raise HTTPException(status_code=400, detail="User is not a librarian")
        
        loan = loan_service.issue_book(
            request.member_id,
            request.book_id,
            librarian_id,
            request.days or 14
        )
        
        if loan:
            return {"loan": loan.to_dict(), "message": "Book issued successfully"}
        else:
            raise HTTPException(status_code=400, detail="No available copies of this book")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/loans/return")
async def return_book(request: ReturnBookRequest, email: str, password: str):
    """Return a book (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        loan_service = LoanService(db)
        
        if loan_service.return_book(request.loan_id):
            return {"message": f"Book returned successfully: Loan ID={request.loan_id}"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to return book. Loan ID {request.loan_id} not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/loans/update-overdue")
async def update_overdue_loans(email: str, password: str):
    """Update overdue loans (Librarian/Administrator only)."""
    try:
        user = await check_book_management_permission(email, password)
        db = get_db()
        loan_service = LoanService(db)
        
        count = loan_service.update_overdue_loans()
        return {"message": f"Updated {count} overdue loan(s)"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Reservation endpoints
@app.get("/api/reservations")
async def get_all_reservations():
    """Get all reservations."""
    try:
        db = get_db()
        reservation_service = ReservationService(db)
        client = db.get_client()
        result = client.table('reservation').select('*').execute()
        reservations = [Reservation.from_dict(row) for row in result.data]
        return {"reservations": [r.to_dict() for r in reservations]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reservations/member/{member_id}")
async def get_member_reservations(member_id: int):
    """Get all reservations for a member."""
    try:
        db = get_db()
        reservation_service = ReservationService(db)
        reservations = reservation_service.get_member_reservations(member_id)
        return {"reservations": [r.to_dict() for r in reservations]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reservations")
async def create_reservation(request: ReservationCreateRequest):
    """Create a new reservation."""
    try:
        db = get_db()
        reservation_service = ReservationService(db)
        reservation = reservation_service.create_reservation(
            request.member_id,
            request.book_id,
            request.days_valid or 14
        )
        return {"reservation": reservation.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reservations/{reservation_id}/cancel")
async def cancel_reservation(reservation_id: int):
    """Cancel a reservation."""
    try:
        db = get_db()
        reservation_service = ReservationService(db)
        if reservation_service.cancel_reservation(reservation_id):
            return {"message": f"Reservation {reservation_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to cancel reservation")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Library Management System API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

