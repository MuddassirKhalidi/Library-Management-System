import psycopg2 as pg2
import datetime
from tabulate import tabulate

conn=pg2.connect(host='localhost', user='postgres', password='sqlpassword',database='library')
mycursor=conn.cursor()
#mycursor.execute("CREATE TABLE LIBRARY_BOOKS(BOOKID INT PRIMARY KEY, NAME VARCHAR(30), AUTHOR VARCHAR(30),AVAILABILITY VARCHAR(15))")
#mycursor.execute("create table issued_books(bookid int references library_books(bookid) primary key, bookname varchar(30), author varchar(30), date_issued date, time_issued time, issuedto varchar(15))

def login(): #function determines the flow of the entire program by authorising staff or students to perform functions restricted to either entity
    staff1,staff2,student1,student2='staff1','staff2','student1','student2'
    passwordstaff,passwordstudent='staffpw','studentpw'
    loop1=True
    loop2=True
    while loop1:
        print('1. Staff')
        print('2. Student')
        print('3. Admin')
        print('4. Exit')
        entity_verification=input('Enter your identity from above (1,2,3,4): ')
        if entity_verification=='1':
            while loop2:
                username=input('Enter username: ')
                password=input('Enter password: ')
                if username=='staff1' and password=='staffpw':
                    staffPage()
                    loop1,loop2=False,False
                    pass
                    
                else:
                    print('Incorrect username or password')
                    loop=True
        elif entity_verification=='2':
            while loop2:
                username=input('Enter username: ')
                password=input('Enter password: ')
                if (username=='student1' or username=='student2') and password=='studentpw':
                    studentPage()
                    loop1,loop2=False,False
                    pass
                else:
                    print('Incorrect username or password')
                    loop2=True
        elif entity_verification=='3':
            while loop2:
                username=input('Enter username: ')
                password=input('Enter password: ')
                if username=='admin' and password=='adminpw':
                    adminPage()
                    pass
                else:
                    print('Incorrect username or password')
                    loop2=True
        elif entity_verification=='4':
            loop1,loop2=False,False
        else:
            print('Please enter a valid key')
            loop1=True
    

def validateoldID(): #validating ID to update previous records
    mycursor.execute("SELECT BOOKID FROM LIBRARY_BOOKS")
    existing_id=[str(x[0]) for x in mycursor.fetchall()] 
    loop=True
    while loop:
        ID=input('Enter the ID of the book from the table above: ')
        if ID in existing_id:
            loop=False
            return int(ID)
        else:
            print('ID does not exist')
            loop=True
            

def availID(): #validating available IDs during time of borrowing
    mycursor.execute("SELECT BOOKID FROM LIBRARY_BOOKS WHERE AVAILABILITY='available'")
    avail_id=[str(x[0]) for x in mycursor.fetchall()] #fetching the IDs as individual strings from the "mycursor.fetchall()" function which returns tuples of IDs
    loop=True
    while loop:
        ID=input('Enter the ID of the book from the table above: ')
        if ID in avail_id:
            loop=False
            return int(ID)
        else:
            print("Book inavailable")
            loop=True

def inavailID(): #validating the ID during time of returning
    mycursor.execute("SELECT BOOKID FROM ISSUED_BOOKS")
    inavail_id=[str(x[0]) for x in mycursor.fetchall()]
    loop=True
    while loop:
        ID=input('Enter the ID of the book you borrowed from the table above: ')
        if ID in inavail_id:
            loop=False
            return int(ID)
        else:
            print('Enter a valid ID')
            loop=True

def fetchBooks(): #stores the ID,name and author of the pre-existing books
    mycursor.execute("SELECT * FROM LIBRARY_BOOKS")
    existing_books=mycursor.fetchall()
    return existing_books


def tableBooks(): #tabulates the pre-existing lists of details
    books=fetchBooks()
    books.insert(0,['ID','Book Name', 'Author','Availability']) #inserting the headers for the table
    print('The following books are already in record: ')
    print(tabulate(books,headers='firstrow',tablefmt='fancy_grid'))
    return books


def adminBooks(): #tabulates the pre-existing lists of details
    books=fetchBooks()
    books.insert(0,['ID','Book Name', 'Author','Availability']) #inserting the headers for the table
    print('The following books are already in record: ')
    print(tabulate(books,headers='firstrow',tablefmt='fancy_grid'))
    adminPage()

    
def addHeader(LIST):
    LIST.insert(0,['ID','Name','Author','Availability'])
    print(tabulate(LIST,headers='firstrow',tablefmt='fancy_grid'))


def addBooks(): #staff function to add user determined number of books to the database
    books=tableBooks()
    qn=int(input('Enter the number of books you want to enter: '))
    for x in range(qn): 
        existing_id=[x[0] for x in books]
        existing_name=[x[1] for x in books]
        loop1=True
        while loop1: #validating the new ID
            ID=int(input('Enter ID of the book: '))
            if ID in existing_id:
                print('ID already exists')
            else:
                loop1=False
        loop2=True
        while loop2: #validating the new name of the book
            name=input('Enter the name of the book: ')
            if name in existing_name:
                print('Book already exists')
                loop2=True
            else:
                loop2=False
        
        author=input("Enter the book's author: ")
        avail='available' 
        mycursor.execute("INSERT INTO LIBRARY_BOOKS VALUES(%s, '%s', '%s','%s')"%(ID,name,author,avail)) #creating an entry for the new book in the database
        conn.commit()
        print('Book added')
        print('------------------------------------------------')
        books=fetchBooks() #updating the value of the lists to accomodate the newly entered details
    staffPage()
    

def updateName(): #staff function to update the book's name 
    books=tableBooks()
    existing_name=[x[1] for x in books]
    ID=validateoldID()
    loop=True
    while loop: #validating the new name (checking if it exists in previous records)
        new_name=input('Enter the new name of the book: ')
        if new_name in existing_name:
            print('Book already exists')
        else:
            loop=False
            mycursor.execute("UPDATE LIBRARY_BOOKS SET NAME='%s' WHERE BOOKID=%s"%(new_name,ID)) #creating an entry for the updated book name in the table "library_books"
            mycursor.execute("UPDATE ISSUED_BOOKS SET BOOKNAME='%s' WHERE BOOKID=%s"%(new_name,ID)) #creating an entry for the updated book name in the table "issued_books"
            conn.commit()
            print('Book name updated')
            print('------------------------------------------------')
            staffPage()
            

def updateAuthor(): #staff function to update a book's author
    books=tableBooks()
    loop=True
    existing_name=[x[1] for x in books]
    ID=validateoldID()
    new_author=input("Enter the updated author's name: ")
    mycursor.execute("UPDATE LIBRARY_BOOKS SET AUTHOR='%s' WHERE BOOKID=%s"%(new_author,ID)) #creating an entry for the updated author name in the table "library_books"
    mycursor.execute("UPDATE ISSUED_BOOKS SET AUTHOR='%s' WHERE BOOKID=%s"%(new_author,ID)) #creating an entry for the updated author name in the table "issued_books"
    conn.commit()
    print('Author name updated')
    print('------------------------------------------------')
    staffPage()


def deleteBook(): #staff function to delete a book's entry from the database
    tableBooks()
    ID=validateoldID()
    mycursor.execute("DELETE FROM ISSUED_BOOKS WHERE BOOKID=%s"%(ID))
    mycursor.execute("DELETE FROM LIBRARY_BOOKS WHERE BOOKID=%s"%(ID))
    conn.commit()
    print('Book deleted')
    print('------------------------------------------------')
    staffPage()


def editBooks(): #staff function encases functions to edit a book's details
    print('1. Update book name')
    print('2. Update author name')
    print('3. Delete book from logs')
    print('4. Go Back')
    choice=input('Choose a function from above by entering the number (1,2..): ')
    if choice=='1':
        updateName()
    if choice=='2':
        updateAuthor()
    if choice=='3':
        deleteBook()
    if choice=='4':
        staffPage()
        
        
def borrowBook():
    mycursor.execute("SELECT * FROM LIBRARY_BOOKS WHERE AVAILABILITY='available'")
    details=mycursor.fetchall()
    addHeader(details)
    stid=input('Enter your username: ')
    ID=availID()
    mycursor.execute("SELECT NAME,AUTHOR FROM LIBRARY_BOOKS WHERE BOOKID=%s"%(ID))
    data=mycursor.fetchall()
    name=data[0][0]
    auth=data[0][1]
    doi=datetime.date.today()
    time=datetime.datetime.now().strftime("%H:%M:%S")
    returned_by='not returned'
    date_returned=''
    time_returned=''
    mycursor.execute("UPDATE LIBRARY_BOOKS SET AVAILABILITY='inavailable' WHERE BOOKID=%s"%(ID))
    mycursor.execute("INSERT INTO ISSUED_BOOKS VALUES(%s,'%s','%s','%s','%s','%s')"%(ID,name,auth,doi,time,stid))
    conn.commit()
    print('Book borrowed successfully. Return within 15 days')
    print('------------------------------------------------')
    studentPage()

    
def returnBook():
    mycursor.execute("SELECT BOOKID FROM ISSUED_BOOKS")
    details=[x[0] for x in mycursor.fetchall()]
    viewIssuedBooks2()
    ID_inavail=inavailID()
    mycursor.execute("DELETE FROM ISSUED_BOOKS WHERE BOOKID=%s"%(ID_inavail))
    mycursor.execute("UPDATE LIBRARY_BOOKS SET AVAILABILITY='available' WHERE BOOKID=%s"%(ID_inavail))
    conn.commit()
    print('Book returned successfully')
    print('------------------------------------------------')
    studentPage()
        

def BrowseorBorrow():
    ask=input("Enter '1' if you want to borrow a book or any key if you want to go back to Student Page: ")
    if ask=='1':
        borrowBook()
    else:
        studentPage()
    
    
def browseBooks(): #student function which provides access to the Book IDs
    books=fetchBooks()
    addHeader(books)
    print('1. Browse by name')
    print('2. Browse by author')
    print('3. Browse by availability')
    print('4. Go Back')
    ask=input('Choose an option from above (1,2,3): ')
    if ask=='1':
        browsebyName()
    elif ask=='2':
        browsebyAuthor()
    elif ask=='3':
        browsebyAvail()
    if ask=='4':
        studentPage()
    else:
        pass
        

def browsebyName():
    mycursor.execute("SELECT * FROM LIBRARY_BOOKS")
    names=[x[1] for x in mycursor.fetchall()]
    loop=True
    while loop:
        name=input('Enter the book name: ')
        if name in names:
            loop=False
        else:
            print('Book does not exist')
            loop=True
    mycursor.execute("SELECT BOOKID,NAME,AUTHOR,AVAILABILITY FROM LIBRARY_BOOKS WHERE NAME='%s'"%(name))
    details=mycursor.fetchall()
    addHeader(details)
    conn.commit()
    BrowseorBorrow()
    

def browsebyAuthor():
    mycursor.execute('SELECT * FROM LIBRARY_BOOKS')
    authors=[x[2] for x in mycursor.fetchall()]
    loop=True
    while loop:
        author=input("Enter the author's name: ")
        if author in authors:
            loop=False
        else:
            print('Author not found')
            loop=True
    mycursor.execute("SELECT BOOKID,NAME,AUTHOR,AVAILABILITY FROM LIBRARY_BOOKS WHERE AUTHOR='%s'"%(author))
    details=mycursor.fetchall()
    addHeader(details)
    conn.commit()
    BrowseorBorrow()


def browsebyAvail():
    mycursor.execute("SELECT BOOKID,NAME,AUTHOR,AVAILABILITY FROM LIBRARY_BOOKS WHERE AVAILABILITY='available'")
    avail=mycursor.fetchall()
    addHeader(avail)
    conn.commit()
    BrowseorBorrow()
    
    
def viewIssuedBooks1():
    mycursor.execute("SELECT * FROM ISSUED_BOOKS")
    details=mycursor.fetchall()
    details.insert(0,['ID','Name','Author','Date Issued','Time Issued','Issued To'])
    print(tabulate(details,headers='firstrow',tablefmt='fancy_grid'))
    adminPage()

def viewIssuedBooks2():
    mycursor.execute("SELECT * FROM ISSUED_BOOKS")
    details=mycursor.fetchall()
    details.insert(0,['ID','Name','Author','Date Issued','Time Issued','Issued To'])
    print(tabulate(details,headers='firstrow',tablefmt='fancy_grid'))  
    
def staffPage():
    print('----------------------------------------------')
    print('1. Add Books')
    print('2. Edit Books Information')
    print('3. Exit')
    print('4. Log In Page')
    option=input('Choose a function from above by entering the number (1,2..): ')
    print('----------------------------------------------')
    if option=='1':
        addBooks()
    if option=='2':
        editBooks()
    if option=='3':
        exit(0)
    if option=='4':
        login()
    
def studentPage():
    print('-----------------------------------------------')
    print('1. Browse books')
    print('2. Borrow book')
    print('3. Return book')
    print('4. Exit')
    print('5. Log In Page')
    option=input('Enter a function from above by entering the number (1,2..): ')
    print('-----------------------------------------------')
    if option=='1':
        browseBooks()
    if option=='2':
        borrowBook()
    if option=='3':
        returnBook()
    if option=='4':
        exit(0)
    if option=='5':
        login()

def adminPage():
    print('------------------------------------------------')
    print('1. Check Book in Library')
    print('2. Check Books Issued')
    print('3. Exit')
    print('4. Log In Page')
    option=input('Enter a function from above by entering the number (1,2..): ')
    print('------------------------------------------------')
    if option=='1':
        adminBooks()
    if option=='2':
        viewIssuedBooks1()
        pass
    if option=='3':
        exit(0)
    if option=='4':
        login()

    
#main program 
login()
