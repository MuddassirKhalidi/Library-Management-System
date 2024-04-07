"""
Library Management System

This module provides functionality for managing a library system including adding/removing books and students,
borrowing/returning books, and checking penalties for late returns. It utilizes a PostgreSQL database and external
libraries for email communication.

Dependencies:
    - psycopg2: PostgreSQL database adapter
    - Levenshtein: Calculates Levenshtein distance between strings
    - tabulate: Pretty prints tabular data
    - email_with_python: Module for sending emails

This module contains the following functions:
    - add_book(): Adds a new book to the database.
    - remove_book(): Removes a book from the database.
    - make_book_available(): Makes a book available for borrowing.
    - borrow_book(): Borrows a book from the library.
    - show_borrowed(): Displays a list of borrowed books.
    - return_book(): Returns a borrowed book to the library.
    - add_student(): Adds a new student to the database.
    - remove_student(): Removes a student from the database.
    - get_id(): Retrieves the ID of a record from a specified table.
    - get_similar(): Retrieves similar strings based on Levenshtein distance.
    - show_data(): Displays tabulated data obtained from SQL queries.
    - check_library(): Checks for late returns and updates penalties.
    - send_emails(): Sends reminder emails to students with overdue books.
    - main_page(): Displays the main menu.
    - database_page(): Displays the database management menu.
    - library_page(): Displays the library management menu.

Note: Before running the module, ensure that the PostgreSQL database is properly configured and accessible.
"""

from datetime import datetime, timedelta
from Levenshtein import distance
from tabulate import tabulate
import psycopg2 as pg2
from email_with_python import EmailSender

# Function to add a new book to the database
def add_book():
    """Add a new book to the database."""
    date = datetime.now()
    fdate = date.strftime("%Y%m")

    title = input('Enter title: ').strip()
    author = input('Enter author: ').strip()

    author_first_letters = ''.join([name[0] for name in author.split()])
    title_first_letters = ''.join(title[0] for title in title.split())
    bookid = author_first_letters + title_first_letters + fdate

    available = 'yes'
    genre = input('Enter genre: ').strip()

    insert_query = '''
    INSERT INTO book(bookid, name, bookauthor, available, genre) 
    VALUES (%s, %s, %s, %s, %s)
    '''
    data = (bookid, title, author, available, genre)

    cursor.execute(insert_query, data)
    connection.commit()

    print("Book has been added!")

# Main function to remove a book from the database
def remove_book(bookid):
    """Remove a book from the database."""
    update_query = "UPDATE book SET available = False WHERE bookid = %s"
    return_query = "SELECT available FROM book WHERE bookid = %s"
    attempt = 1
    while attempt:
        cursor.execute(return_query, (bookid,))
        removed = cursor.fetchall()
        if removed[0][0]:
            cursor.execute(update_query, (bookid,))
            connection.commit()
            cursor.execute(return_query, (bookid,))
            removed = cursor.fetchall()
            if not removed[0][0]:
                attempt = 0
            else:
                print('')
        else:
            print('Book unavailable')
            attempt = 0

# Function to make a book available for borrowing
def make_book_available(bookid):
    """Make a book available for borrowing."""
    update_query = "UPDATE book SET available = 'Yes' WHERE bookid = %s"
    return_query = "SELECT available FROM book WHERE bookid = %s"
    attempt = 1
    while attempt:
        cursor.execute(return_query, (bookid,))
        added = cursor.fetchall()
        if not added[0][0]:
            cursor.execute(update_query, (bookid,))
            connection.commit()
            cursor.execute(return_query, (bookid,))
            added = cursor.fetchall()
            if added[0][0]:
                print('Book is now available')
                attempt = 0
            else:
                print('Update failed')
        else:
            print('Book already available')
            attempt = 0

# Function to borrow a book from the library
def borrow_book():
    """Borrow a book from the library."""
    borrowing_query = 'SELECT name FROM student'
    sid = get_id('student', borrowing_query)
    if sid == 0:
        main_page()
        return
    available_query = 'SELECT name FROM book WHERE available = True'
    bid = get_id('book', available_query)
    if bid == 0:
        main_page()
        return
    borrow_date = datetime.now().date()
    return_date = borrow_date + timedelta(days=15)
    insert_query = '''INSERT INTO borrows (studentid, bookid, borrow_date, return_date)
    VALUES(%s, %s, %s, %s)'''
    update_query = '''UPDATE student SET currently_borrowing = True WHERE studentid = %s'''
    data = (sid, bid, borrow_date, return_date)
    cursor.execute(insert_query, data)
    cursor.execute(update_query, (sid,))
    connection.commit()
    remove_book(bid)
    print('Book lent')

# Function to display a list of borrowed books
def show_borrowed():
    """Display a list of borrowed books."""
    cursor.execute('SELECT * FROM borrows')
    data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(tabulate(data, headers=headers, tablefmt="grid"))

# Function to return a borrowed book
def return_book():
    """Return a borrowed book."""
    borrowing_query = 'SELECT name FROM student WHERE currently_borrowing = True'
    sid = get_id('student', borrowing_query)
    data_query = 'SELECT * FROM borrows WHERE studentid = %s'
    show_data(sid, data_query)
    bid = input('Enter the book ID: ')
    make_book_available(bid)
    update_borrows = 'UPDATE borrows SET returned = True WHERE studentid = %s and bookid = %s'
    cursor.execute(update_borrows, (sid, bid))

    update_student = 'UPDATE student SET currently_borrowing = False WHERE studentid = %s'
    check_borrows = 'SELECT * FROM borrows WHERE (studentid = %s AND returned = False)'
    cursor.execute(check_borrows, (sid,))
    if not cursor.fetchall():
        cursor.execute(update_student, (sid,))

    connection.commit()

# Function to add a new student to the database
def add_student():
    """Add a new student to the database."""
    date = datetime.now()
    studentid = date.strftime("%Y%m%d%H%M%S")
    name = input('Enter name: ').strip()
    level = ''
    while level not in ('Freshman', 'Sophomore', 'Junior', 'Senior'):
        level = input('Enter level (Freshman, Sophomore, Junior, Senior): ')
        if level not in ('Freshman', 'Sophomore', 'Junior', 'Senior'):
            print('Invalid level')
    major = input('Enter major: ').strip()
    college = input('Enter college: ').strip()

    data = (studentid, name, level, major, college)
    insert_query = '''
    INSERT INTO student (studentid, name, level, major, college) 
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, data)
    connection.commit()

    print("Student data added!")

# Function to remove a student from the database
def remove_student():
    """Remove a student from the database."""
    query = 'SELECT name FROM student'
    sid = get_id('student', query)
    check_query = 'SELECT currently_borrowing FROM student WHERE studentid = %s'
    cursor.execute(check_query, (sid,))
    result = cursor.fetchall()
    if result[0][0]:
        print('Student has not returned a book')
    else:
        attempt = 1
        while attempt:
            query = "DELETE FROM student WHERE studentid = %s"
            cursor.execute(query, (sid,))
            query = "SELECT * FROM student WHERE studentid = %s"
            cursor.execute(query, (sid,))
            connection.commit()

            if cursor.fetchall():
                print('Deletion failed')
            else:
                print('Deletion successful')
                attempt = 0

# Function to get the ID of a record from the specified table
def get_id(table: str, query):
    """Get the ID of a record from the specified table."""
    name = input(f'Enter {table} name: ').strip()
    data = get_similar(name, query)
    if data:
        data_query = f'SELECT * FROM {table} WHERE name in %s'
        show_data(data, data_query)
        check = input(f'Do you see your {table} here? (y/n): ').strip().lower()
        if check == 'y':
            attempt = True
            while attempt:
                id_value = input(f'Enter {table} ID: ').strip()
                cursor.execute(f'SELECT * FROM {table} WHERE {table}id = %s', (id_value,))
                data = cursor.fetchall()
                if data:
                    return id_value
                out = table.capitalize()
                print(f'{out} ID not found')
        else:
            print('Try something else')
            return ''
    else:
        print('No entries found')

# Function to get strings which have a similarity of 1-% and above
def get_similar(input_name, query):
    """Gets strings which have a similarity of 1-% and above."""
    cursor.execute(query)
    names = [name[0] for name in cursor.fetchall()]

    similar_names = []
    for name in names:
        dist = distance(name.lower(), input_name.lower())
        similarity_score = ((1 - dist / max(len(name), len(input_name))) * 100)
        if similarity_score >= 10:
            similar_names.append(name)
    if similar_names:
        print(similar_names)
        return tuple(similar_names)
    print('None found')
    return []

# Function to tabulate the data obtained from SQL
def show_data(data, query):
    """Tabulates the data we get from SQL"""
    cursor.execute(query, (data,))
    all_data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(tabulate(all_data, headers=headers, tablefmt="grid"))

# Function to check for late returns and update penalties
def check_library():
    """Check for late returns and update penalties."""
    query = 'SELECT studentid FROM borrows WHERE (return_date < CURRENT_DATE AND returned = False)'
    cursor.execute(query)
    studentids = [id[0] for id in cursor.fetchall()]
    if studentids:
        penalty_query = 'UPDATE student SET penalty = penalty + 100 WHERE studentid = %s'
        for id_value in studentids:
            cursor.execute(penalty_query, (id_value,))
        connection.commit()
    else:
        return

# Function to send emails to students who have not returned borrowed books
def send_emails():
    """
    Utilizes the email_with_python module to log in to the user's email
    The passowrd is NOT the regular password. You must use the App Password
    The function sends an email to all the students who have not returned a book they borrowed"""
    admin = EmailSender()
    admin_email = admin.login()
    query = '''
        SELECT DISTINCT s.name, s.email, s.penalty, b.name as book_name
        FROM borrows
        JOIN student AS s ON borrows.studentid = s.studentid
        JOIN book AS b ON b.bookid = borrows.bookid
        WHERE (borrows.return_date < CURRENT_DATE AND borrows.returned = False)
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    for name, email, penalty, book_name in data:
        subject = f'You have not returned {book_name}'
        content = f'''
    Dear {name},
    We hope this email finds you well. 
    This email is to inform you that the return date for {book_name}, which you borrowed has passed.
    Because you failed to return the book before the due date, you have incurred a penalty of {penalty} SAR/-.
    Please return the book as soon as possible to avoid any future penalties. 
        
    Best Regards,
    Library
    '''
        message = f'Subject: {subject} \n{content}'
        admin.smtp_object.sendmail(admin_email, email, message)
    admin.close_connection()

# Main menu function
def main_page():
    """Display the main menu."""
    print('-' * 50)
    print('Main Page')
    print('''
1. Manage database (Add or remove students and books)
2. Manage library (Borrow or return books)
3. Log out''')

# Database management menu function
def database_page():
    """Display the database management menu."""
    print('-' * 50)
    print('Manage Database')
    print('''
1. Add book
2. Remove book
3. Add student
4. Remove student
5. Back''')

# Library management menu function
def library_page():
    """Display the library management menu."""
    print('-' * 50)
    print('Manage Library')
    print('''
1. Borrow book
2. Return book
3. Back''')

try:
    connection = pg2.connect(dbname='library',
                             user='muddassirkhalidi',
                             password='Mjkt260421pgadmin',
                             host='localhost',
                             port=5432
                             )
    cursor = connection.cursor()
    check_library()
    send_emails()

    print('Welcome to your personal Library Management System'.center(10))
    LOGGED_IN = True
    while LOGGED_IN:
        MAIN_SELECTION = 1
        while MAIN_SELECTION in (1, 2, 3):
            main_page()
            MAIN_SELECTION = int(input('Enter an option from above (1, 2, 3): '))
            if MAIN_SELECTION == 1:
                ON_DB = True
                while ON_DB:
                    DB_SELECTION = 1
                    while DB_SELECTION in (1, 2, 3, 4, 5):
                        database_page()
                        DB_SELECTION = int(input('Enter an option from above (1, 2, 3, 4, 5): '))
                        if DB_SELECTION == 1:
                            add_book()
                        elif DB_SELECTION == 2:
                            pass
                            # remove_book() #Review
                        elif DB_SELECTION == 3:
                            add_student()
                        elif DB_SELECTION == 4:
                            remove_student()
                        elif DB_SELECTION == 5:
                            ON_DB = False
                            break  # Exit the inner loop and go back to the main menu
                    else:
                        break  # Exit the outer loop and go back to the main menu
            elif MAIN_SELECTION == 2:
                ON_LIB = True
                while ON_LIB:
                    LIB_SELECTION = 1
                    while LIB_SELECTION in (1, 2, 3):
                        library_page()
                        LIB_SELECTION = int(input('Enter an option from above (1, 2, 3): '))
                        if LIB_SELECTION == 1:
                            borrow_book()
                        elif LIB_SELECTION == 2:
                            return_book()
                        elif LIB_SELECTION == 3:
                            ON_LIB = False
                            break  # Exit the inner loop and go back to the main menu
                    else:
                        break  # Exit the outer loop and go back to the main menu
            elif MAIN_SELECTION == 3:
                print('Logging out')
                LOGGED_IN = False
                break


except pg2.Error as e:
    print('Connection failed: ', e)
