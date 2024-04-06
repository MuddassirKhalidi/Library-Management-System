# Library Management System

This repository contains a Python module for managing a library system. The module provides functionality for adding/removing books and students, borrowing/returning books, and checking penalties for late returns. It utilizes a PostgreSQL database for data storage and external libraries for additional features.

## Features

- Add new books to the library database.
- Remove books from the library database.
- Borrow books from the library.
- Return borrowed books to the library.
- Add new students to the library system.
- Remove students from the library system.
- Check penalties for late returns and update student records.
- Send reminder emails to students with overdue books.

## Dependencies

- [psycopg2](https://pypi.org/project/psycopg2/): PostgreSQL database adapter for Python.
- [Levenshtein](https://pypi.org/project/python-Levenshtein/): Calculates Levenshtein distance between strings.
- [tabulate](https://pypi.org/project/tabulate/): Pretty prints tabular data.
- [email_with_python](git@github.com:MuddassirKhalidi/Email-Sender-Python.git): Module for sending emails.

## Usage

To use the library management system, follow these steps:

1. Ensure PostgreSQL is installed and properly configured.
2. Install the required dependencies using pip

