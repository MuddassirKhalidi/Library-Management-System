# Library Management System

A Python-based backend system for managing library operations including book management, member management, loans, and reservations.

## Features

- **Book Management**: CRUD operations for books with support for authors and categories
- **Member Management**: Register, update, suspend, and deactivate members
- **Loan Management**: Issue books, return books, track overdue loans
- **Reservation System**: Allow members to reserve books
- **Search & Filter**: Search books by ISBN, title, author, or category
- **Authentication & Authorization**: Role-based access control (Member, Librarian, Administrator)
- **Data Integrity**: Prevents deletion of books/members with active loans

## Project Structure

```
src/
├── library_system/
│   ├── __init__.py
│   ├── main.py                 # Command-line interface
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── member.py
│   │   ├── librarian.py
│   │   ├── book.py
│   │   ├── bookcopy.py
│   │   ├── author.py
│   │   ├── category.py
│   │   ├── reservation.py
│   │   └── loan.py
│   ├── database/               # Database related files
│   │   ├── __init__.py
│   │   ├── connection.py       # Supabase connection
│   │   ├── schema.sql          # Database schema
│   │   └── seed_data.sql       # Sample data
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   ├── member_service.py
│   │   ├── loan_service.py
│   │   ├── reservation_service.py
│   │   └── auth_service.py
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── enums.py            # Enum definitions
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.8 or higher
- Supabase account and project

### Installation

1. Clone or navigate to the project directory:
```bash
cd src
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export SUPABASE_URL="your-supabase-project-url"
export SUPABASE_KEY="your-supabase-anon-key"
```

Or create a `.env` file:
```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key
```

### Database Setup

1. In your Supabase project, go to the SQL Editor.

2. Run the schema file to create tables:
   - Copy and execute the contents of `library_system/database/schema.sql`

3. (Optional) Seed the database with sample data:
   - Copy and execute the contents of `library_system/database/seed_data.sql`

## Usage

The system provides a command-line interface through `main.py`. All commands follow this pattern:

```bash
python -m library_system.main <command> [options]
```

### Available Commands

#### Book Management

**Create a book** (Librarian/Administrator only):
```bash
python -m library_system.main create-book \
  --email librarian@example.com \
  --password password123 \
  --isbn "978-0-123456-78-9" \
  --title "Example Book" \
  --publisher "Example Publisher" \
  --year 2024 \
  --description "A great book" \
  --authors "1,2" \
  --categories "1,3"
```

**Search books**:
```bash
python -m library_system.main search-books --title "Harry Potter"
python -m library_system.main search-books --author "J.K. Rowling"
python -m library_system.main search-books --category "Fantasy"
python -m library_system.main search-books --isbn "978-0-7475-3269-9"
```

**Delete a book** (Librarian/Administrator only):
```bash
python -m library_system.main delete-book \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --book-id 1
```

#### Member Management

**Register a member** (Librarian/Administrator only):
```bash
python -m library_system.main register-member \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --name "John Doe" \
  --email "john.doe@example.com" \
  --phone "555-1234"
```

**Update member** (Librarian/Administrator only):
```bash
python -m library_system.main update-member \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --member-id 1 \
  --name "Jane Doe" \
  --email "jane.doe@example.com"
```

**Suspend a member** (Librarian/Administrator only):
```bash
python -m library_system.main suspend-member \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --member-id 1
```

**Delete a member** (Librarian/Administrator only):
```bash
python -m library_system.main delete-member \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --member-id 1
```

#### Loan Management

**Issue a book** (Librarian/Administrator only):
```bash
python -m library_system.main issue-book \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --member-id 1 \
  --book-id 1 \
  --days 14
```

**Return a book** (Librarian/Administrator only):
```bash
python -m library_system.main return-book \
  --email-auth librarian@example.com \
  --password-auth password123 \
  --loan-id 1
```

**Update overdue loans** (Librarian/Administrator only):
```bash
python -m library_system.main update-overdue \
  --email-auth librarian@example.com \
  --password-auth password123
```

**List overdue loans**:
```bash
python -m library_system.main list-overdue
```

## Functional Requirements Implementation

The system implements all functional requirements:

1. ✅ **Book Record Management**: CRUD operations for books (title, author, ISBN, category)
2. ✅ **Member Management**: Register, update, suspend/deactivate members
3. ✅ **Book Issuance Condition**: Only issues if at least one available copy exists
4. ✅ **Loan Return Process**: Updates loan status and increments available copy count
5. ✅ **Overdue Loan Detection**: Automatically identifies and updates overdue loans
6. ✅ **Book Search and Filtering**: Search by ISBN, title, author, or category
7. ✅ **Deletion Restrictions**: Prevents deletion of books/members with active loans
8. ✅ **Authentication and RBAC**: Role-based access control for administrative functions

## Database Schema

The database includes the following tables:

- `user`: System users (members, librarians, administrators)
- `member`: Library members
- `librarian`: Librarian employees (linked to users)
- `book`: Book records
- `book_copy`: Physical copies of books
- `author`: Authors
- `category`: Book categories
- `book_author`: Junction table for book-author relationships
- `book_category`: Junction table for book-category relationships
- `reservation`: Book reservations
- `loan`: Book loans

## Notes

- Password hashing uses SHA-256 (simple implementation). For production, consider using bcrypt.
- The system uses Supabase's PostgREST API for database operations.
- Some operations may require raw SQL execution (e.g., running schema.sql), which should be done through Supabase's SQL Editor.

## License

This project is for educational purposes.

