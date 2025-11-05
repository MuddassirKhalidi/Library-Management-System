# Pytesting Library Management System

A comprehensive library management system with Python backend and web frontend for managing books, members, loans, and reservations.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Quick Start](#quick-start)
5. [Backend Documentation](#backend-documentation)
   - [Setup & Installation](#setup--installation)
   - [Usage](#usage)
   - [API Server](#api-server)
   - [Authentication & Login](#authentication--login)
6. [Frontend Documentation](#frontend-documentation)
7. [Testing](#testing)
   - [Unit Tests](#unit-tests)
   - [Integration Tests](#integration-tests)
8. [Database Schema](#database-schema)
9. [Functional Requirements](#functional-requirements)

---

## Overview

This is a Python-based library management system that provides:
- **Backend**: RESTful API built with FastAPI and Supabase
- **Frontend**: Modern web interface for interacting with the system
- **Command-Line Interface**: Direct access to library operations
- **Comprehensive Testing**: Unit and integration test suites

---

## Features

### Core Functionality
- **Book Management**: CRUD operations for books with support for authors and categories
- **Member Management**: Register, update, suspend, and deactivate members
- **Loan Management**: Issue books, return books, track overdue loans
- **Reservation System**: Allow members to reserve books
- **Search & Filter**: Search books by ISBN, title, author, or category
- **Authentication & Authorization**: Role-based access control (Member, Librarian, Administrator)
- **Data Integrity**: Prevents deletion of books/members with active loans

### Frontend Features
- **Books Management**: View all books and search by ISBN, title, author, or category
- **Members Management**: View all library members with their details
- **Loans Management**: View all loans, active loans, and overdue loans
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, user-friendly interface with smooth animations

---

## Project Structure

```
src/
├── backend/
│   ├── library_system/          # Main backend package
│   │   ├── __init__.py
│   │   ├── main.py              # Command-line interface
│   │   ├── models/              # Data models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── member.py
│   │   │   ├── librarian.py
│   │   │   ├── book.py
│   │   │   ├── bookcopy.py
│   │   │   ├── author.py
│   │   │   ├── category.py
│   │   │   ├── reservation.py
│   │   │   └── loan.py
│   │   ├── database/            # Database related files
│   │   │   ├── __init__.py
│   │   │   ├── connection.py    # Supabase connection
│   │   │   ├── schema.sql       # Database schema
│   │   │   └── seed_data.sql    # Sample data
│   │   ├── services/            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── book_service.py
│   │   │   ├── member_service.py
│   │   │   ├── loan_service.py
│   │   │   ├── reservation_service.py
│   │   │   └── auth_service.py
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       └── enums.py         # Enum definitions
│   ├── tests/                   # Test suite
│   │   ├── integration/         # Integration tests
│   │   ├── test_fr1_book_management.py
│   │   ├── test_fr2_member_management.py
│   │   ├── test_fr3_issue_book.py
│   │   ├── test_fr4_return_book.py
│   │   ├── test_fr5_overdue_loans.py
│   │   ├── test_fr6_search_filter.py
│   │   ├── test_fr7_prevent_deletion.py
│   │   ├── test_fr8_authentication.py
│   │   └── conftest.py          # Test fixtures
│   ├── api_server.py            # FastAPI server
│   ├── requirements.txt
│   ├── README.md                # Backend documentation
│   └── README_API.md            # API login instructions
├── frontend/
│   ├── index.html               # Main HTML file
│   ├── styles.css               # CSS styling
│   ├── script.js                # JavaScript for API interactions
│   └── README.md                # Frontend documentation
└── README.md                    # This file
```

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Web browser (for frontend)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd src
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   export SUPABASE_URL="your-supabase-project-url"
   export SUPABASE_KEY="your-supabase-anon-key"
   ```
   
   Or create a `.env` file in the `backend/` directory:
   ```
   SUPABASE_URL=your-supabase-project-url
   SUPABASE_KEY=your-supabase-anon-key
   ```

4. **Set up the database:**
   - In your Supabase project, go to the SQL Editor
   - Run the schema file: Copy and execute the contents of `backend/library_system/database/schema.sql`
   - (Optional) Seed the database: Copy and execute the contents of `backend/library_system/database/seed_data.sql`

5. **Start the API server:**
   ```bash
   cd backend
   python api_server.py
   ```
   The server will start on `http://localhost:8000`

6. **Open the frontend:**
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Then open `http://localhost:8080` in your browser

---

## Backend Documentation

### Setup & Installation

See [Quick Start](#quick-start) for initial setup instructions.

### Usage

The system provides a command-line interface through `main.py`. All commands follow this pattern:

```bash
python -m library_system.main <command> [options]
```

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

### API Server

The FastAPI server provides RESTful endpoints for frontend and external integrations.

**Start the API server:**
```bash
cd backend
python api_server.py
```

The server will start on `http://localhost:8000`

**Available API Endpoints:**
- `GET /api/health` - Health check
- `GET /api/books` - Get all books
- `GET /api/books/search` - Search books
- `GET /api/members` - Get all members
- `GET /api/loans` - Get all loans
- `GET /api/loans/active` - Get active loans
- `GET /api/loans/overdue` - Get overdue loans
- `POST /api/auth/login` - User login

### Authentication & Login

#### Current Password Configuration

All user passwords have been set to: **`password123`**

#### Login Credentials

**Librarian Accounts** (can manage books/members):
- Email: `julia.roberts@example.com`
- Password: `password123`

- Email: `ivan.petrov@example.com`
- Password: `password123`

**Administrator Account:**
- Email: `kevin.spacey@example.com`
- Password: `password123`

**Member Accounts** (regular users):
- Any email from the `user` table
- Password: `password123`

#### Changing Passwords

To change a specific user's password, use the `change_password.py` script:

```bash
cd backend
source venv/bin/activate  # if using virtual environment
python change_password.py <email> <new_password>
```

**Example:**
```bash
python change_password.py julia.roberts@example.com mySecurePassword123
```

#### Password Hashing

**Important:** Passwords are stored as SHA-256 hashes in the database. This means:
- ✅ You can verify if a password is correct
- ❌ You cannot "get back" the original password from the hash
- ✅ You can change a password by providing a new one

The hash is one-way: `password123` → `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`

When you login:
1. You enter the plain text password: `password123`
2. The system hashes it: `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`
3. It compares this hash with the hash stored in the database
4. If they match, login succeeds

#### Troubleshooting Login

If login is not working:

1. **Check API server is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return: `{"status":"healthy",...}`

2. **Check the endpoint exists:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"julia.roberts@example.com","password":"password123"}'
   ```

3. **Restart the API server** if you made changes:
   ```bash
   cd backend
   python api_server.py
   ```

4. **Verify password hash in database:**
   - Check Supabase dashboard
   - The `password_hash` for all users should be: `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`
   - If it's still `hashed_password_12` or similar, run the password fix script again

---

## Frontend Documentation

### Features

- **Books Management**: View all books and search by ISBN, title, author, or category
- **Members Management**: View all library members with their details
- **Loans Management**: View all loans, active loans, and overdue loans
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, user-friendly interface with smooth animations

### Setup

1. **Make sure the backend API server is running** (see [API Server](#api-server))

2. **Open the frontend:**
   - Simply double-click the `frontend/index.html` file, or
   - Use a local web server (recommended):
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     Then open `http://localhost:8080` in your browser

3. **Configure API Base URL:**
   - If the API server is running on a different URL or port, update the "API Base URL" field at the top of the page (default: `http://localhost:8000`)

### Usage

#### Books Tab

- **Get All Books**: Retrieves and displays all books in the library
- **Search Books**: Allows you to search books by:
  - ISBN
  - Title
  - Author name
  - Category name

#### Members Tab

- **Get All Members**: Displays all registered library members with their details including status (Active, Suspended, Inactive)

#### Loans Tab

- **Get All Loans**: Shows all loans in the system
- **Get Active Loans**: Shows only currently active loans
- **Get Overdue Loans**: Shows only overdue loans

### Troubleshooting

#### Cannot connect to API

- Make sure the API server is running
- Check that the API Base URL in the frontend matches the server URL
- Verify that CORS is enabled in the API server (it should be by default)

#### No data showing

- Check the browser console for errors
- Verify the API server is returning data by testing endpoints directly
- Make sure your database is properly set up with data

---

## Testing

### Unit Tests

The unit test suite uses mocks and doesn't require a database connection. Tests are organized by functional requirements (FR1-FR8).

#### Test Structure

Tests are located in `backend/tests/`:
- **test_fr1_book_management.py**: Tests for adding, editing, and deleting book records
- **test_fr2_member_management.py**: Tests for member registration and management
- **test_fr3_issue_book.py**: Tests for issuing books to members
- **test_fr4_return_book.py**: Tests for returning books and updating loan status
- **test_fr5_overdue_loans.py**: Tests for detecting overdue loans
- **test_fr6_search_filter.py**: Tests for searching and filtering books
- **test_fr7_prevent_deletion.py**: Tests for preventing deletion of loaned books or members with active loans
- **test_fr8_authentication.py**: Tests for authentication and role-based access control

#### Running Unit Tests

**Run all tests:**
```bash
cd backend
python -m pytest
```

**Run tests for a specific functional requirement:**
```bash
python -m pytest tests/test_fr1_book_management.py
```

**Run a specific test case:**
```bash
python -m pytest tests/test_fr1_book_management.py::TestFR1BookManagement::test_tc1_1_add_new_book
```

**Run tests with verbose output:**
```bash
python -m pytest -v
```

**Run tests with coverage:**
```bash
python -m pytest --cov=library_system --cov-report=html
```

#### Test Coverage

The test suite covers all functional requirements:

- **FR1**: Add, Edit, and Delete Book Records (TC1.1, TC1.2, TC1.3)
- **FR2**: Member Registration and Management (TC2.1, TC2.2, TC2.3)
- **FR3**: Issue Book to Member (TC3.1, TC3.2)
- **FR4**: Return Book and Update Loan Status (TC4.1)
- **FR5**: Detect Overdue Loans (TC5.1)
- **FR6**: Search and Filter Books (TC6.1, TC6.2)
- **FR7**: Prevent Deletion of Loaned Books or Members with Active Loans (TC7.1, TC7.2)
- **FR8**: Authentication and Role-Based Access (TC8.1, TC8.2)

### Integration Tests

Integration tests use a real database connection and test multiple components working together. They are located in `backend/tests/integration/`.

#### Setup for Integration Tests

1. **Set environment variables for test database:**
   
   Create or update your `.env` file in `backend/` directory:
   ```bash
   # For integration tests (recommended)
   SUPABASE_TEST_URL=your_test_supabase_url
   SUPABASE_TEST_KEY=your_test_supabase_key
   
   # Or use your development database (not recommended)
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

   **Important**: Integration tests will create and delete test data. Use a separate test database to avoid affecting your development data.

2. **The integration tests will automatically load environment variables from:**
   - `backend/.env` (preferred)
   - `src/.env` (fallback)

#### Running Integration Tests

**Run all integration tests:**
```bash
python -m pytest tests/integration/ -m integration
```

**Run a specific integration test file:**
```bash
python -m pytest tests/integration/test_book_loan_workflow.py -m integration
```

**Run integration tests with coverage:**
```bash
python -m pytest tests/integration/ -m integration --cov=library_system --cov-report=html
```

**Skip integration tests** (run only unit tests):
```bash
python -m pytest tests/ -m "not integration"
```

#### Integration Test Files

- **test_book_loan_workflow.py**: Tests complete workflows involving multiple services
  - Complete book loan cycle (create → issue → return)
  - Cannot issue unavailable books
  - Member loan history tracking

- **test_book_member_deletion.py**: Tests deletion rules with active loans
  - Cannot delete books with active loans
  - Cannot delete members with active loans

- **test_search_and_filter.py**: Tests search and filter with real database
  - Search by title
  - Filter by category

#### Test Data Management

Integration tests use a cleanup fixture that automatically removes test data after each test. Test data is identified by:
- Books: ISBN starting with "TEST", "SEARCH", or "CATEGORY"
- Members: Email starting with "test"
- Book copies: Barcode starting with "TEST"
- Users: Email starting with "test"

#### Best Practices

1. **Always use a test database** - Never run integration tests against production data
2. **Isolate test data** - Use unique prefixes or test schemas
3. **Clean up after tests** - The cleanup fixture handles this, but verify it works
4. **Test real workflows** - Integration tests should mirror real-world usage
5. **Keep tests independent** - Each test should be able to run in isolation

#### Troubleshooting Integration Tests

**Tests are skipped:**
- Check that `SUPABASE_TEST_URL` and `SUPABASE_TEST_KEY` are set
- Verify the database connection is working

**Test data not cleaned up:**
- Check the cleanup fixture in `conftest.py`
- Manually clean up test data if needed

**Database errors:**
- Verify your Supabase connection credentials
- Check that your test database has the correct schema
- Ensure you have proper permissions

---

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

See `backend/library_system/database/schema.sql` for the complete schema definition.

---

## Functional Requirements

The system implements all functional requirements:

1. ✅ **Book Record Management**: CRUD operations for books (title, author, ISBN, category)
2. ✅ **Member Management**: Register, update, suspend/deactivate members
3. ✅ **Book Issuance Condition**: Only issues if at least one available copy exists
4. ✅ **Loan Return Process**: Updates loan status and increments available copy count
5. ✅ **Overdue Loan Detection**: Automatically identifies and updates overdue loans
6. ✅ **Book Search and Filtering**: Search by ISBN, title, author, or category
7. ✅ **Deletion Restrictions**: Prevents deletion of books/members with active loans
8. ✅ **Authentication and RBAC**: Role-based access control for administrative functions

---

## Notes

- Password hashing uses SHA-256 (simple implementation). For production, consider using bcrypt.
- The system uses Supabase's PostgREST API for database operations.
- Some operations may require raw SQL execution (e.g., running schema.sql), which should be done through Supabase's SQL Editor.
- All tests use mocking to avoid requiring actual database connections (unit tests), or use a dedicated test database (integration tests).

---

## License

This project is for educational purposes.

