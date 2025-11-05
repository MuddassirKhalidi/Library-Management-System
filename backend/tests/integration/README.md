# Integration Tests

This directory contains integration tests for the library management system. Unlike unit tests, these tests use a real database connection and test multiple components working together.

## Setup

### Prerequisites

1. A test Supabase database (recommended) or use your development database
2. Environment variables set for database connection

### Environment Variables

The integration tests will automatically load environment variables from a `.env` file. The tests will look for:
1. `backend/.env` (preferred)
2. `src/.env` (fallback)

Create or update your `.env` file with your Supabase credentials:

```bash
# For integration tests (recommended)
SUPABASE_TEST_URL=your_test_supabase_url
SUPABASE_TEST_KEY=your_test_supabase_key

# Or use your development database (not recommended)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

**Important**: Integration tests will create and delete test data. Use a separate test database to avoid affecting your development data.

## Running Integration Tests

### Run all integration tests:
```bash
python -m pytest tests/integration/ -m integration
```

### Run a specific integration test file:
```bash
python -m pytest tests/integration/test_book_loan_workflow.py -m integration
```

### Run integration tests with coverage:
```bash
python -m pytest tests/integration/ -m integration --cov=library_system --cov-report=html
```

### Skip integration tests (run only unit tests):
```bash
python -m pytest tests/ -m "not integration"
```

## Test Files

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

## Test Data Management

Integration tests use a cleanup fixture that automatically removes test data after each test. Test data is identified by:
- Books: ISBN starting with "TEST", "SEARCH", or "CATEGORY"
- Members: Email starting with "test"
- Book copies: Barcode starting with "TEST"
- Users: Email starting with "test"

## Best Practices

1. **Always use a test database** - Never run integration tests against production data
2. **Isolate test data** - Use unique prefixes or test schemas
3. **Clean up after tests** - The cleanup fixture handles this, but verify it works
4. **Test real workflows** - Integration tests should mirror real-world usage
5. **Keep tests independent** - Each test should be able to run in isolation

## Differences from Unit Tests

| Unit Tests | Integration Tests |
|------------|-------------------|
| Use mocks | Use real database |
| Fast execution | Slower execution |
| Test individual components | Test multiple components together |
| No external dependencies | Require database connection |
| Located in `tests/` | Located in `tests/integration/` |

## Troubleshooting

### Tests are skipped
- Check that `SUPABASE_TEST_URL` and `SUPABASE_TEST_KEY` are set
- Verify the database connection is working

### Test data not cleaned up
- Check the cleanup fixture in `conftest.py`
- Manually clean up test data if needed

### Database errors
- Verify your Supabase connection credentials
- Check that your test database has the correct schema
- Ensure you have proper permissions

