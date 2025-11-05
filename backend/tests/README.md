# Test Suite for Library Management System

This directory contains comprehensive test cases for the library management system, organized by functional requirements (FR1-FR8).

## Test Structure

The test suite is organized into **unit tests** and **integration tests**:

### Unit Tests (in `tests/` directory)
These tests use mocks and don't require a database connection.

- **test_fr1_book_management.py**: Tests for adding, editing, and deleting book records
- **test_fr2_member_management.py**: Tests for member registration and management
- **test_fr3_issue_book.py**: Tests for issuing books to members
- **test_fr4_return_book.py**: Tests for returning books and updating loan status
- **test_fr5_overdue_loans.py**: Tests for detecting overdue loans
- **test_fr6_search_filter.py**: Tests for searching and filtering books
- **test_fr7_prevent_deletion.py**: Tests for preventing deletion of loaned books or members with active loans
- **test_fr8_authentication.py**: Tests for authentication and role-based access control

## Test Coverage

The test suite covers all functional requirements specified in the test case documentation:

### FR1: Add, Edit, and Delete Book Records
- TC1.1: Add New Book
- TC1.2: Edit Existing Book
- TC1.3: Delete Book Record

### FR2: Member Registration and Management
- TC2.1: Register New Member
- TC2.2: Update Member Information
- TC2.3: Deactivate Membership

### FR3: Issue Book to Member
- TC3.1: Issue Available Book
- TC3.2: Issue Unavailable Book

### FR4: Return Book and Update Loan Status
- TC4.1: Return Borrowed Book

### FR5: Detect Overdue Loans
- TC5.1: Detect Overdue Book

### FR6: Search and Filter Books
- TC6.1: Search by Title
- TC6.2: Filter by Category

### FR7: Prevent Deletion of Loaned Books or Members with Active Loans
- TC7.1: Attempt to Delete Loaned Book
- TC7.2: Attempt to Delete Member with Active Loan

### FR8: Authentication and Role-Based Access
- TC8.1: Librarian Login Success
- TC8.2: Member Access Restricted

## Setup

### Prerequisites

1. Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

Run all tests:
```bash
python -m pytest
```

Run tests for a specific functional requirement:
```bash
python -m pytest tests/test_fr1_book_management.py
```

Run a specific test case:
```bash
python -m pytest tests/test_fr1_book_management.py::TestFR1BookManagement::test_tc1_1_add_new_book
```

Run tests with verbose output:
```bash
python -m pytest -v
```

Run tests with coverage:
```bash
python -m pytest --cov=library_system --cov-report=html
```

### Integration Tests (in `tests/integration/` directory)
Integration tests use a real database connection and test multiple components working together.

**Setup for integration tests:**
1. Set environment variables for test database:
   ```bash
   export SUPABASE_TEST_URL=your_test_supabase_url
   export SUPABASE_TEST_KEY=your_test_supabase_key
   ```

2. Run integration tests:
   ```bash
   python -m pytest tests/integration/ -m integration
   ```

3. Skip integration tests (run only unit tests):
   ```bash
   python -m pytest tests/ -m "not integration"
   ```

See `tests/integration/README.md` for detailed integration test documentation.

## Test Fixtures

The test suite uses pytest fixtures defined in `conftest.py`:

- `mock_db_client`: Mock Supabase client
- `mock_db_connection`: Mock database connection
- `book_service`: BookService instance with mocked database
- `member_service`: MemberService instance with mocked database
- `loan_service`: LoanService instance with mocked database
- `auth_service`: AuthService instance with mocked database
- `sample_book`: Sample book for testing
- `sample_member`: Sample member for testing
- `sample_loan`: Sample loan for testing
- And more...

## Notes

- Tests use mocking to avoid requiring actual database connections
- All tests are designed to be independent and can run in any order
- Test data follows the specifications from the test case documentation
- Mock objects simulate the Supabase client behavior

## Test Execution Results

Each test case verifies:
- Correct method calls to service layer
- Expected return values
- Database interaction patterns
- Business logic validation

