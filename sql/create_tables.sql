-- Create book table
CREATE TABLE IF NOT EXISTS book (
    bookid SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bookauthor VARCHAR(255) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    genre VARCHAR(100)
);

-- Create student table
CREATE TABLE IF NOT EXISTS student (
    studentid SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    level VARCHAR(20) NOT NULL,
    major VARCHAR(100),
    college VARCHAR(100),
    currently_borrowing BOOLEAN DEFAULT FALSE,
    penalty INT DEFAULT 0
);

-- Create borrows table
CREATE TABLE IF NOT EXISTS borrows (
    borrow_id SERIAL PRIMARY KEY,
    studentid INT REFERENCES student(studentid),
    bookid INT REFERENCES book(bookid),
    borrow_date DATE NOT NULL,
    return_date DATE,
    returned BOOLEAN DEFAULT FALSE
);
