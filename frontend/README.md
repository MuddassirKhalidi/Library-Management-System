# Library Management System - Frontend

A simple, modern web interface for interacting with the Library Management System API.

## Features

- **Books Management**: View all books and search by ISBN, title, author, or category
- **Members Management**: View all library members with their details
- **Loans Management**: View all loans, active loans, and overdue loans
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, user-friendly interface with smooth animations

## Setup

### Prerequisites

1. Make sure the backend API server is running (see backend/README.md)
2. Install FastAPI and uvicorn if not already installed:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the API Server

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the API server:
   ```bash
   python api_server.py
   ```

   The server will start on `http://localhost:8000`

### Running the Frontend

1. Open the `index.html` file in a web browser:
   - Simply double-click the file, or
   - Use a local web server (recommended):
     ```bash
     cd frontend
     python -m http.server 8080
     ```
     Then open `http://localhost:8080` in your browser

2. If the API server is running on a different URL or port, update the "API Base URL" field at the top of the page.

## Usage

### Books Tab

- **Get All Books**: Retrieves and displays all books in the library
- **Search Books**: Allows you to search books by:
  - ISBN
  - Title
  - Author name
  - Category name

### Members Tab

- **Get All Members**: Displays all registered library members with their details including status (Active, Suspended, Inactive)

### Loans Tab

- **Get All Loans**: Shows all loans in the system
- **Get Active Loans**: Shows only currently active loans
- **Get Overdue Loans**: Shows only overdue loans

## API Endpoints

The frontend interacts with the following API endpoints:

- `GET /api/books` - Get all books
- `GET /api/books/search` - Search books
- `GET /api/members` - Get all members
- `GET /api/loans` - Get all loans
- `GET /api/loans/active` - Get active loans
- `GET /api/loans/overdue` - Get overdue loans
- `GET /api/health` - Health check

## Troubleshooting

### Cannot connect to API

- Make sure the API server is running
- Check that the API Base URL in the frontend matches the server URL
- Verify that CORS is enabled in the API server (it should be by default)

### No data showing

- Check the browser console for errors
- Verify the API server is returning data by testing endpoints directly
- Make sure your database is properly set up with data

## File Structure

```
frontend/
├── index.html      # Main HTML file
├── styles.css      # CSS styling
├── script.js       # JavaScript for API interactions
└── README.md       # This file
```

