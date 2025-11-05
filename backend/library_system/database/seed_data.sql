-- Seed data for Library Management System
-- Inserting at least 10 entries per table

-- Insert Users (at least 10)
INSERT INTO "user" (name, email, password_hash, role) VALUES
('John Doe', 'john.doe@example.com', 'hashed_password_1', 'member'),
('Jane Smith', 'jane.smith@example.com', 'hashed_password_2', 'member'),
('Alice Johnson', 'alice.johnson@example.com', 'hashed_password_3', 'member'),
('Bob Williams', 'bob.williams@example.com', 'hashed_password_4', 'member'),
('Charlie Brown', 'charlie.brown@example.com', 'hashed_password_5', 'member'),
('Diana Prince', 'diana.prince@example.com', 'hashed_password_6', 'member'),
('Edward Norton', 'edward.norton@example.com', 'hashed_password_7', 'member'),
('Fiona Apple', 'fiona.apple@example.com', 'hashed_password_8', 'member'),
('George Lucas', 'george.lucas@example.com', 'hashed_password_9', 'member'),
('Helen Troy', 'helen.troy@example.com', 'hashed_password_10', 'member'),
('Ivan Petrov', 'ivan.petrov@example.com', 'hashed_password_11', 'librarian'),
('Julia Roberts', 'julia.roberts@example.com', 'hashed_password_12', 'librarian'),
('Kevin Spacey', 'kevin.spacey@example.com', 'hashed_password_13', 'administrator');

-- Insert Members (at least 10)
INSERT INTO member (name, email, phone, status, join_date) VALUES
('John Doe', 'john.doe@example.com', '555-0101', 'active', '2023-01-15'),
('Jane Smith', 'jane.smith@example.com', '555-0102', 'active', '2023-02-20'),
('Alice Johnson', 'alice.johnson@example.com', '555-0103', 'active', '2023-03-10'),
('Bob Williams', 'bob.williams@example.com', '555-0104', 'active', '2023-04-05'),
('Charlie Brown', 'charlie.brown@example.com', '555-0105', 'active', '2023-05-12'),
('Diana Prince', 'diana.prince@example.com', '555-0106', 'suspended', '2023-06-18'),
('Edward Norton', 'edward.norton@example.com', '555-0107', 'active', '2023-07-22'),
('Fiona Apple', 'fiona.apple@example.com', '555-0108', 'active', '2023-08-30'),
('George Lucas', 'george.lucas@example.com', '555-0109', 'active', '2023-09-14'),
('Helen Troy', 'helen.troy@example.com', '555-0110', 'inactive', '2023-10-25'),
('Isaac Newton', 'isaac.newton@example.com', '555-0111', 'active', '2023-11-01'),
('Julia Child', 'julia.child@example.com', '555-0112', 'active', '2023-12-05');

-- Insert Librarians (linking to users)
INSERT INTO librarian (user_id) VALUES
((SELECT user_id FROM "user" WHERE email = 'ivan.petrov@example.com')),
((SELECT user_id FROM "user" WHERE email = 'julia.roberts@example.com'));

-- Insert Authors (at least 10)
INSERT INTO author (full_name) VALUES
('J.K. Rowling'),
('George R.R. Martin'),
('Stephen King'),
('Agatha Christie'),
('Ernest Hemingway'),
('Jane Austen'),
('Mark Twain'),
('Charles Dickens'),
('Virginia Woolf'),
('F. Scott Fitzgerald'),
('Toni Morrison'),
('Harper Lee'),
('Isaac Asimov'),
('Ray Bradbury'),
('Margaret Atwood');

-- Insert Categories (at least 10)
INSERT INTO category (name) VALUES
('Fiction'),
('Non-Fiction'),
('Mystery'),
('Science Fiction'),
('Fantasy'),
('Romance'),
('Biography'),
('History'),
('Science'),
('Technology'),
('Philosophy'),
('Poetry'),
('Drama'),
('Horror'),
('Young Adult');

-- Insert Books (at least 10)
INSERT INTO book (isbn, title, publisher, published_year, description) VALUES
('978-0-7475-3269-9', 'Harry Potter and the Philosopher''s Stone', 'Bloomsbury', 1997, 'The first book in the Harry Potter series'),
('978-0-553-57340-3', 'A Game of Thrones', 'Bantam Books', 1996, 'First book in A Song of Ice and Fire series'),
('978-0-385-12167-5', 'The Shining', 'Doubleday', 1977, 'A horror novel about a haunted hotel'),
('978-0-00-711931-7', 'Murder on the Orient Express', 'HarperCollins', 1934, 'A Hercule Poirot mystery'),
('978-0-684-80122-3', 'The Old Man and the Sea', 'Scribner', 1952, 'A story about an aging fisherman'),
('978-0-14-143951-8', 'Pride and Prejudice', 'Penguin Classics', 1813, 'A romantic novel by Jane Austen'),
('978-0-486-27557-5', 'The Adventures of Tom Sawyer', 'Dover Publications', 1876, 'Classic American novel'),
('978-0-14-143956-3', 'Great Expectations', 'Penguin Classics', 1861, 'A bildungsroman by Charles Dickens'),
('978-0-15-602819-6', 'Mrs. Dalloway', 'Harcourt Brace', 1925, 'A modernist novel by Virginia Woolf'),
('978-0-7432-7356-5', 'The Great Gatsby', 'Scribner', 1925, 'A novel about the Jazz Age'),
('978-0-679-43919-7', 'Beloved', 'Alfred A. Knopf', 1987, 'A novel by Toni Morrison'),
('978-0-06-112008-4', 'To Kill a Mockingbird', 'J.B. Lippincott & Co.', 1960, 'A novel about racial injustice'),
('978-0-553-29338-5', 'Foundation', 'Gnome Press', 1951, 'First book in the Foundation series'),
('978-0-345-34296-8', 'Fahrenheit 451', 'Ballantine Books', 1953, 'A dystopian novel about censorship'),
('978-0-385-26454-0', 'The Handmaid''s Tale', 'McClelland & Stewart', 1985, 'A dystopian novel');

-- Link Books to Authors (many-to-many)
INSERT INTO book_author (book_id, author_id) VALUES
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), (SELECT author_id FROM author WHERE full_name = 'J.K. Rowling')),
((SELECT book_id FROM book WHERE isbn = '978-0-553-57340-3'), (SELECT author_id FROM author WHERE full_name = 'George R.R. Martin')),
((SELECT book_id FROM book WHERE isbn = '978-0-385-12167-5'), (SELECT author_id FROM author WHERE full_name = 'Stephen King')),
((SELECT book_id FROM book WHERE isbn = '978-0-00-711931-7'), (SELECT author_id FROM author WHERE full_name = 'Agatha Christie')),
((SELECT book_id FROM book WHERE isbn = '978-0-684-80122-3'), (SELECT author_id FROM author WHERE full_name = 'Ernest Hemingway')),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), (SELECT author_id FROM author WHERE full_name = 'Jane Austen')),
((SELECT book_id FROM book WHERE isbn = '978-0-486-27557-5'), (SELECT author_id FROM author WHERE full_name = 'Mark Twain')),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143956-3'), (SELECT author_id FROM author WHERE full_name = 'Charles Dickens')),
((SELECT book_id FROM book WHERE isbn = '978-0-15-602819-6'), (SELECT author_id FROM author WHERE full_name = 'Virginia Woolf')),
((SELECT book_id FROM book WHERE isbn = '978-0-7432-7356-5'), (SELECT author_id FROM author WHERE full_name = 'F. Scott Fitzgerald')),
((SELECT book_id FROM book WHERE isbn = '978-0-679-43919-7'), (SELECT author_id FROM author WHERE full_name = 'Toni Morrison')),
((SELECT book_id FROM book WHERE isbn = '978-0-06-112008-4'), (SELECT author_id FROM author WHERE full_name = 'Harper Lee')),
((SELECT book_id FROM book WHERE isbn = '978-0-553-29338-5'), (SELECT author_id FROM author WHERE full_name = 'Isaac Asimov')),
((SELECT book_id FROM book WHERE isbn = '978-0-345-34296-8'), (SELECT author_id FROM author WHERE full_name = 'Ray Bradbury')),
((SELECT book_id FROM book WHERE isbn = '978-0-385-26454-0'), (SELECT author_id FROM author WHERE full_name = 'Margaret Atwood'));

-- Link Books to Categories (many-to-many)
INSERT INTO book_category (book_id, category_id) VALUES
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), (SELECT category_id FROM category WHERE name = 'Fantasy')),
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), (SELECT category_id FROM category WHERE name = 'Young Adult')),
((SELECT book_id FROM book WHERE isbn = '978-0-553-57340-3'), (SELECT category_id FROM category WHERE name = 'Fantasy')),
((SELECT book_id FROM book WHERE isbn = '978-0-385-12167-5'), (SELECT category_id FROM category WHERE name = 'Horror')),
((SELECT book_id FROM book WHERE isbn = '978-0-00-711931-7'), (SELECT category_id FROM category WHERE name = 'Mystery')),
((SELECT book_id FROM book WHERE isbn = '978-0-684-80122-3'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), (SELECT category_id FROM category WHERE name = 'Romance')),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-486-27557-5'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143956-3'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-15-602819-6'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-7432-7356-5'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-679-43919-7'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-06-112008-4'), (SELECT category_id FROM category WHERE name = 'Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-553-29338-5'), (SELECT category_id FROM category WHERE name = 'Science Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-345-34296-8'), (SELECT category_id FROM category WHERE name = 'Science Fiction')),
((SELECT book_id FROM book WHERE isbn = '978-0-385-26454-0'), (SELECT category_id FROM category WHERE name = 'Science Fiction'));

-- Insert Book Copies (at least 10, multiple copies per book)
INSERT INTO book_copy (book_id, barcode, status, acquired_on) VALUES
-- Copies for Harry Potter
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), 'BC-001', 'available', '2023-01-10'),
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), 'BC-002', 'available', '2023-01-10'),
((SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), 'BC-003', 'loaned', '2023-01-10'),
-- Copies for A Game of Thrones
((SELECT book_id FROM book WHERE isbn = '978-0-553-57340-3'), 'BC-004', 'available', '2023-02-15'),
((SELECT book_id FROM book WHERE isbn = '978-0-553-57340-3'), 'BC-005', 'loaned', '2023-02-15'),
-- Copies for The Shining
((SELECT book_id FROM book WHERE isbn = '978-0-385-12167-5'), 'BC-006', 'available', '2023-03-20'),
((SELECT book_id FROM book WHERE isbn = '978-0-385-12167-5'), 'BC-007', 'reserved', '2023-03-20'),
-- Copies for Murder on the Orient Express
((SELECT book_id FROM book WHERE isbn = '978-0-00-711931-7'), 'BC-008', 'available', '2023-04-05'),
((SELECT book_id FROM book WHERE isbn = '978-0-00-711931-7'), 'BC-009', 'available', '2023-04-05'),
-- Copies for The Old Man and the Sea
((SELECT book_id FROM book WHERE isbn = '978-0-684-80122-3'), 'BC-010', 'loaned', '2023-05-12'),
-- Copies for Pride and Prejudice
((SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), 'BC-011', 'available', '2023-06-18'),
((SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), 'BC-012', 'available', '2023-06-18'),
-- Copies for Tom Sawyer
((SELECT book_id FROM book WHERE isbn = '978-0-486-27557-5'), 'BC-013', 'available', '2023-07-22'),
-- Copies for Great Expectations
((SELECT book_id FROM book WHERE isbn = '978-0-14-143956-3'), 'BC-014', 'loaned', '2023-08-30'),
-- Copies for Mrs. Dalloway
((SELECT book_id FROM book WHERE isbn = '978-0-15-602819-6'), 'BC-015', 'available', '2023-09-14'),
-- Copies for The Great Gatsby
((SELECT book_id FROM book WHERE isbn = '978-0-7432-7356-5'), 'BC-016', 'available', '2023-10-25'),
((SELECT book_id FROM book WHERE isbn = '978-0-7432-7356-5'), 'BC-017', 'available', '2023-10-25'),
-- Copies for Beloved
((SELECT book_id FROM book WHERE isbn = '978-0-679-43919-7'), 'BC-018', 'available', '2023-11-01'),
-- Copies for To Kill a Mockingbird
((SELECT book_id FROM book WHERE isbn = '978-0-06-112008-4'), 'BC-019', 'loaned', '2023-11-15'),
-- Copies for Foundation
((SELECT book_id FROM book WHERE isbn = '978-0-553-29338-5'), 'BC-020', 'available', '2023-12-05'),
((SELECT book_id FROM book WHERE isbn = '978-0-553-29338-5'), 'BC-021', 'available', '2023-12-05'),
-- Copies for Fahrenheit 451
((SELECT book_id FROM book WHERE isbn = '978-0-345-34296-8'), 'BC-022', 'available', '2024-01-10'),
-- Copies for The Handmaid's Tale
((SELECT book_id FROM book WHERE isbn = '978-0-385-26454-0'), 'BC-023', 'reserved', '2024-01-20');

-- Insert Reservations (at least 10)
INSERT INTO reservation (member_id, book_id, created_at, expires_at, active) VALUES
((SELECT member_id FROM member WHERE email = 'john.doe@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-345-34296-8'), '2024-01-15', '2024-01-29', TRUE),
((SELECT member_id FROM member WHERE email = 'jane.smith@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-385-26454-0'), '2024-01-16', '2024-01-30', TRUE),
((SELECT member_id FROM member WHERE email = 'alice.johnson@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-553-57340-3'), '2024-01-17', '2024-01-31', TRUE),
((SELECT member_id FROM member WHERE email = 'bob.williams@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-679-43919-7'), '2024-01-18', '2024-02-01', TRUE),
((SELECT member_id FROM member WHERE email = 'charlie.brown@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-06-112008-4'), '2024-01-19', '2024-02-02', TRUE),
((SELECT member_id FROM member WHERE email = 'edward.norton@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-7432-7356-5'), '2024-01-20', '2024-02-03', TRUE),
((SELECT member_id FROM member WHERE email = 'fiona.apple@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-15-602819-6'), '2024-01-21', '2024-02-04', TRUE),
((SELECT member_id FROM member WHERE email = 'george.lucas@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-14-143956-3'), '2024-01-22', '2024-02-05', TRUE),
((SELECT member_id FROM member WHERE email = 'isaac.newton@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-486-27557-5'), '2024-01-23', '2024-02-06', TRUE),
((SELECT member_id FROM member WHERE email = 'julia.child@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-14-143951-8'), '2024-01-24', '2024-02-07', TRUE),
((SELECT member_id FROM member WHERE email = 'john.doe@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-553-29338-5'), '2024-01-25', '2024-02-08', TRUE),
((SELECT member_id FROM member WHERE email = 'jane.smith@example.com'), (SELECT book_id FROM book WHERE isbn = '978-0-7475-3269-9'), '2024-01-26', '2024-02-09', FALSE);

-- Insert Loans (at least 10)
INSERT INTO loan (member_id, copy_id, librarian_id, issue_date, due_date, return_date, status) VALUES
-- Active loans
((SELECT member_id FROM member WHERE email = 'john.doe@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-003'), (SELECT employee_id FROM librarian LIMIT 1), '2024-01-10', '2024-01-24', NULL, 'active'),
((SELECT member_id FROM member WHERE email = 'jane.smith@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-005'), (SELECT employee_id FROM librarian LIMIT 1), '2024-01-12', '2024-01-26', NULL, 'active'),
((SELECT member_id FROM member WHERE email = 'alice.johnson@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-010'), (SELECT employee_id FROM librarian LIMIT 1), '2024-01-08', '2024-01-22', NULL, 'active'),
((SELECT member_id FROM member WHERE email = 'bob.williams@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-014'), (SELECT employee_id FROM librarian LIMIT 1), '2024-01-05', '2024-01-19', NULL, 'overdue'),
((SELECT member_id FROM member WHERE email = 'edward.norton@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-019'), (SELECT employee_id FROM librarian LIMIT 1), '2024-01-03', '2024-01-17', NULL, 'overdue'),
-- Returned loans
((SELECT member_id FROM member WHERE email = 'charlie.brown@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-001'), (SELECT employee_id FROM librarian LIMIT 1), '2023-12-15', '2023-12-29', '2023-12-28', 'returned'),
((SELECT member_id FROM member WHERE email = 'diana.prince@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-004'), (SELECT employee_id FROM librarian LIMIT 1), '2023-12-10', '2023-12-24', '2023-12-23', 'returned'),
((SELECT member_id FROM member WHERE email = 'fiona.apple@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-006'), (SELECT employee_id FROM librarian LIMIT 1), '2023-12-05', '2023-12-19', '2023-12-18', 'returned'),
((SELECT member_id FROM member WHERE email = 'george.lucas@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-008'), (SELECT employee_id FROM librarian LIMIT 1), '2023-11-28', '2023-12-12', '2023-12-11', 'returned'),
((SELECT member_id FROM member WHERE email = 'helen.troy@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-011'), (SELECT employee_id FROM librarian LIMIT 1), '2023-11-20', '2023-12-04', '2023-12-03', 'returned'),
((SELECT member_id FROM member WHERE email = 'isaac.newton@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-013'), (SELECT employee_id FROM librarian LIMIT 1), '2023-11-15', '2023-11-29', '2023-11-28', 'returned'),
((SELECT member_id FROM member WHERE email = 'julia.child@example.com'), (SELECT copy_id FROM book_copy WHERE barcode = 'BC-015'), (SELECT employee_id FROM librarian LIMIT 1), '2023-11-10', '2023-11-24', '2023-11-23', 'returned');

