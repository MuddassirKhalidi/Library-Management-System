-- Library Management System Database Schema
-- This schema is designed for PostgreSQL (Supabase)

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS book_author CASCADE;
DROP TABLE IF EXISTS book_category CASCADE;
DROP TABLE IF EXISTS loan CASCADE;
DROP TABLE IF EXISTS reservation CASCADE;
DROP TABLE IF EXISTS book_copy CASCADE;
DROP TABLE IF EXISTS librarian CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS book CASCADE;
DROP TABLE IF EXISTS author CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- Create ENUM types
CREATE TYPE role_name AS ENUM ('member', 'librarian', 'administrator');
CREATE TYPE member_status AS ENUM ('active', 'suspended', 'inactive');
CREATE TYPE copy_status AS ENUM ('available', 'loaned', 'reserved', 'maintenance');
CREATE TYPE loan_status AS ENUM ('active', 'returned', 'overdue');

-- User table
CREATE TABLE "user" (
    user_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role role_name NOT NULL DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Member table
CREATE TABLE member (
    member_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    status member_status NOT NULL DEFAULT 'active',
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Librarian table
CREATE TABLE librarian (
    employee_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- Author table
CREATE TABLE author (
    author_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL
);

-- Category table
CREATE TABLE category (
    category_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Book table
CREATE TABLE book (
    book_id BIGSERIAL PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    publisher VARCHAR(255),
    published_year INTEGER,
    description TEXT
);

-- BookCopy table
CREATE TABLE book_copy (
    copy_id BIGSERIAL PRIMARY KEY,
    book_id BIGINT NOT NULL REFERENCES book(book_id) ON DELETE CASCADE,
    barcode VARCHAR(50) UNIQUE NOT NULL,
    status copy_status NOT NULL DEFAULT 'available',
    acquired_on DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Junction table for Book-Author (many-to-many)
CREATE TABLE book_author (
    book_id BIGINT NOT NULL REFERENCES book(book_id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES author(author_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

-- Junction table for Book-Category (many-to-many)
CREATE TABLE book_category (
    book_id BIGINT NOT NULL REFERENCES book(book_id) ON DELETE CASCADE,
    category_id BIGINT NOT NULL REFERENCES category(category_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, category_id)
);

-- Reservation table
CREATE TABLE reservation (
    reservation_id BIGSERIAL PRIMARY KEY,
    member_id BIGINT NOT NULL REFERENCES member(member_id) ON DELETE CASCADE,
    book_id BIGINT NOT NULL REFERENCES book(book_id) ON DELETE CASCADE,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE,
    expires_at DATE NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Loan table
CREATE TABLE loan (
    loan_id BIGSERIAL PRIMARY KEY,
    member_id BIGINT NOT NULL REFERENCES member(member_id) ON DELETE RESTRICT,
    copy_id BIGINT NOT NULL REFERENCES book_copy(copy_id) ON DELETE RESTRICT,
    librarian_id BIGINT NOT NULL REFERENCES librarian(employee_id) ON DELETE RESTRICT,
    issue_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    status loan_status NOT NULL DEFAULT 'active'
);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_member_email ON member(email);
CREATE INDEX idx_member_status ON member(status);
CREATE INDEX idx_book_isbn ON book(isbn);
CREATE INDEX idx_book_title ON book(title);
CREATE INDEX idx_book_copy_book_id ON book_copy(book_id);
CREATE INDEX idx_book_copy_status ON book_copy(status);
CREATE INDEX idx_book_copy_barcode ON book_copy(barcode);
CREATE INDEX idx_loan_member_id ON loan(member_id);
CREATE INDEX idx_loan_copy_id ON loan(copy_id);
CREATE INDEX idx_loan_status ON loan(status);
CREATE INDEX idx_loan_due_date ON loan(due_date);
CREATE INDEX idx_reservation_member_id ON reservation(member_id);
CREATE INDEX idx_reservation_book_id ON reservation(book_id);
CREATE INDEX idx_reservation_active ON reservation(active);

-- Create function to automatically update overdue loans
CREATE OR REPLACE FUNCTION update_overdue_loans()
RETURNS void AS $$
BEGIN
    UPDATE loan
    SET status = 'overdue'
    WHERE status = 'active'
    AND due_date < CURRENT_DATE
    AND return_date IS NULL;
END;
$$ LANGUAGE plpgsql;

