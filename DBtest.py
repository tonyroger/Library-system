import sqlite3
import datetime

BORROW_TIME_PERIOD = 14
LATE_CHARGE = 0.25
DATABASE = 'Database.db'

def initDB(sqlite_file = DATABASE):
    bookTable = 'Books'
    userTable = 'Users'
    borrowedBookTable = 'BorrowedBooks'
    holdBookTable = 'Holds'
    searchTable = 'Search'
    dailyReportTable = 'Reports'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} ( `ID` INTEGER, `Name` TEXT, `Author` TEXT, `Description` TEXT, `Subject` TEXT, `Type` TEXT, `Language` TEXT, `Status` TEXT, `Hold Requested` TEXT )'\
              .format(tn=bookTable))
    c.execute('CREATE TABLE {tn} ( `Name` TEXT, `Author` TEXT, `Description` TEXT, `Subject` TEXT, `Type` TEXT, `Language` TEXT, `Status` TEXT )'\
              .format(tn=searchTable))
    c.execute('CREATE TABLE {tn} ( `Book ID` INTEGER, `Borrower ID` INTEGER, `Name` TEXT, `Due Date` REAL)'\
              .format(tn=borrowedBookTable))
    c.execute('CREATE TABLE {tn} ( `Book ID` INTEGER, `Borrower ID` INTEGER, `Name` TEXT)'\
              .format(tn=holdBookTable))
    c.execute('CREATE TABLE {tn} ( `ID` INTEGER, `Username` TEXT, `Password` TEXT, `User Level` INTEGER, `Name` TEXT, `Phone Number` TEXT, `Address` TEXT, `Email` TEXT, `Late Fees` INTEGER  )'\
              .format(tn=userTable))
    c.execute('CREATE TABLE {tn} ( `Book ID` INTEGER, `Borrower ID` INTEGER, `Check Out Date` REAL, `Check In Date` REAL)'\
              .format(tn=dailyReportTable))
    conn.commit()
    conn.close()

def fillBookDB(sqlite_file = DATABASE):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    books = [(1, "The Great Gatsby", "Francis Scott Key Fitzgerald", "A book about the roaring twenties in America.", "Romance", "Book", "English", "Available", "No"),
             (2, "The Grapes of Wrath", "John Steinbeck", "A book about living during the Great Depression", "Historical Fiction", "Book", "English", "Available", "No"),
             (3, "Nineteen Eighty-Four", "George Orwell", "A book about a potential dystopia", "Science Fiction", "Book", "English", "Available", "No"),
             (4, "Ulysses", "James Joyce", "A popular modernist book.", "Literary Fiction", "Book", "English", "Available", "No"),
             (5, "Catch-22", "Joseph Heller", "A satirical novel.", "Historical Fiction", "Book", "English", "Available", "No"),
             (6, "The Fellowship of the Ring", "J.R.R. Tolkien", "A popular fantasy novel.", "Science Fiction", "Book", "English", "Available", "No"),
             (7, "The Two Towers", "J.R.R. Tolkien", "A popular fantasy novel.", "Science Fiction", "Book", "English", "Available", "No"),
             (8, "The Return of the King", "J.R.R. Tolkien", "A popular fantasy novel.", "Science Fiction", "Book", "English", "Available", "No"),
             (9, "The Silmarillion", "J.R.R. Tolkien", "The worldmyth of a popular fantasy novel.", "Science Fiction", "Book", "English", "Available", "No"),
             (10, "Brave New World", "Aldous Huxley", "A book about a potential dystopia.", "Science Fiction", "Book", "English", "Available", "No"),
             (11, "Un di Velt Hot Geshvign", "Elie Wiesel", "A book about the horrors of the Holocaust.", "Biography", "Book", "Yiddish", "Available", "No"),
             (12, "The bishop's pawn", "Steve Berry", "Audiobook.", "Suspense Fiction", "CD", "English", "Available", "No"),
             (13, "Bon Appetit", "-", "Cooking and food magazine", "Culinary Arts", "Magazine", "English", "Available", "No"),
             (14, "Discover", "-", "Science magazine", "Science and Technology", "Magazine", "English", "Available", "No"),
             (15, "People en Espanol", "-", "Celebrity gossip", "Gossip", "Magazine", "Spanish", "Available", "No")
        ]
    for book in books:
        c.execute('INSERT INTO Books values (?,?,?,?,?,?,?,?,?)', book)
    conn.commit()
    conn.close()
    return 0

def fillUserDB(sqlite_file = DATABASE):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    users = [(1, "Matt", "password12345", 1, "Matthew Carpenter", "555-555-5555", "1234 Example Street", "email@email.com", 0),
             (2, "Bryan", "password12345", 1, "Bryan Washington", "554-555-5555", "1233 Example Street", "email2@email.com", 0),
             (3, "Anthony", "password12345", 1, "Anthony Rogers", "553-555-5555", "1232 Example Street", "email3@email.com", 0),
        ]
    for user in users:
        c.execute('INSERT INTO Users values (?,?,?,?,?,?,?,?,?)', user)
    conn.commit()
    conn.close()
    return 0

def createUser(Username = None, Password = None, Name = None, PhoneNumber = None, Address = None, Email = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No username provided.
    errorCode2 = 2 #No password provided.
    errorCode3 = 3 #Invalid username provided.
    errorCode4 = 4 #Invalid password provided.
    errorCode5 = 5 #Username already in use.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(Username == None):
        conn.close()
        return errorCode1
    if(Password == None):
        conn.close()
        return errorCode2
    if("%" in Username):
        conn.close()
        return errorCode3
    if("%" in Password):
        conn.close()
        return errorCode4
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?', (Username,))
    u = c.fetchone()
    if u:
        conn.close()
        return errorCode5
    if not Name:
        na = ""
    else:
        na = Name
    if not PhoneNumber:
        pn = ""
    else:
        pn = PhoneNumber
    if not Address:
        ad = ""
    else:
        ad = Address
    if not Email:
        em = ""
    else:
        em = email
    highestID = c.execute('SELECT MAX(ID) FROM Users')
    h = c.fetchone()
    newID = h[0] + 1
    user = [(newID, Username, Password, 0, na, pn, ad, em, 0)]
    c.execute('INSERT INTO Users values (?,?,?,?,?,?,?,?,?)', user[0])
    conn.commit()
    conn.close()
    return 0

def removeUser(Username = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No username provided.
    errorCode4 = 4 #Username not found.
    errorCode5 = 5 #Attempted to delete own account.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if u[3] == 0:
        conn.close()
        return errorCode2
    if not Username:
        conn.close()
        return errorCode3
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',(Username,))
    u2 = c.fetchone()
    if not u2:
        conn.close()
        return errorCode4
    if (Username,) == user:
        conn.close()
        return errorCode5
    c.execute('DELETE FROM Users WHERE Username=?', (Username,))
    c.execute('DELETE FROM BorrowedBooks WHERE "User ID" = ?', (Username,))
    c.execute('DELETE FROM Holds WHERE "User ID" = ?', (Username,))
    c.execute('DELETE FROM Reports WHERE "User ID" = ?', (Username,))

    conn.commit()
    conn.close()
    return 0

def forgotUsername(email = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No email provided.
    errorCode2 = 1 #Invalid email provided.
    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(email == None):
        conn.close()
        return errorCode1
    if("%" in email):
        conn.close()
        return errorCode2
    userInformation = c.execute('SELECT * FROM Users WHERE email=?', (email,))
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    conn.close()
    return u[1]

def forgotPassword(username = None, email = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No username/email provided.
    errorCode2 = 2 #Invalid username/email provided.
    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(username == None or email == None):
        conn.close()
        return errorCode1
    if("%" in username or "%" in email):
        conn.close()
        return errorCode2
    userInformation = c.execute('SELECT * FROM Users WHERE email=? AND username=?', (email,), (username,))
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    conn.close()
    return u[2]

def searchUsers(name = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No search results found.
    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if u[3] == 0:
        conn.close()
        return errorCode2
    n = ('%') + name
    searchResult = c.execute('SELECT Name FROM Users WHERE "Name" LIKE ?', (n,))
    s = c.fetchall()

    conn.close()
    return s

def searchDB(Bookname = None, Author = None, Description = None, Subject = None, Type = None, Language = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No search results found.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not Bookname and not Author and not Subject:
        searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books')
        s2 = c.fetchall()
        return s2
    #Pseudo switch-case block.
    while True:
        if Bookname and Author and Subject:
            b = ('%') + Bookname + ('%')
            s = ('%') + Subject + ('%')
            a = ('%') + Author + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Name" LIKE ? AND "Author" LIKE ? AND "Subject" LIKE ?', (b,), (a,), (s,))
            break
        if Bookname and Author:
            b = ('%') + Bookname + ('%')
            a = ('%') + Author + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Name" LIKE ? AND "Author" LIKE ?', (b,), (a,))
            break
        if Bookname and Subject:
            b = ('%') + Bookname + ('%')
            s = ('%') + Subject + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Name" LIKE ? AND "Subject" LIKE ?', (b,), (s,))
            break
        if Subject and Author:
            s = ('%') + Subject + ('%')
            a = ('%') + Author + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Author" LIKE ? AND "Subject" LIKE ?', (a,), (s,))
            break
        if Bookname:
            b = ('%') + Bookname + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Name" LIKE ?', (b,))
            break
        if Author:
            a = ('%') + Author + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Author" LIKE ?', (a,))
            break
        if Subject:
            s = ('%') + Subject + ('%')
            searchResult = c.execute('SELECT "Name", "Author", "Description", "Subject", "Type", "Language", "Status" FROM Books WHERE "Subject" LIKE ?', (s,))
            break
        return errorCode3

    s2 = c.fetchall()
    if not s2:
        return errorCode3
    for s in s2:
        c.execute('INSERT INTO Search values (?,?,?,?,?,?,?)', s)
    if(Description):
        d = ('%') + Description + "%"
        searchResult = c.execute('SELECT * FROM Search WHERE "Description" LIKE ?', (d,))
        s2 = c.fetchall()
        c.execute('DELETE FROM Search')
        for s in s2:
            c.execute('INSERT INTO Search values (?,?,?,?,?,?,?)', s)
    if(Type):
        t = ('%') + Type + "%"
        searchResult = c.execute('SELECT * FROM Search WHERE "Type" LIKE ?', (t,))
        s2 = c.fetchall()
        c.execute('DELETE FROM Search')
        for s in s2:
            c.execute('INSERT INTO Search values (?,?,?,?,?,?,?)', s)
    if(Language):
        l = ('%') + Language + "%"
        searchResult = c.execute('SELECT * FROM Search WHERE "Language" LIKE ?', (l,))
        s2 = c.fetchall()
        c.execute('DELETE FROM Search')
        for s in s2:
            c.execute('INSERT INTO Search values (?,?,?,?,?,?,?)', s)
    c.execute('DELETE FROM Search')
    conn.commit()
    conn.close()
    if not s2:
        return errorCode3
    else:
        return s2

def login(username = None, password = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No username provided.
    errorCode2 = 2 #No password provided.
    errorCode3 = 3 #Invalid username/password combination provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(username == None):
        conn.close()
        return errorCode1
    if(password == None):
        conn.close()
        return errorCode2
    c.execute("SELECT * FROM Users WHERE Username = ? and Password = ?", (username,password))
    u = c.fetchone()
    if u == None:
        conn.close()
        return errorCode3
    conn.close()
    return 0

def addBooks(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if u[3] == 0:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    for book in books:
        c.execute('INSERT INTO Books values (?,?,?,?,?,?,?,?)', book)
    conn.commit()
    conn.close()
    return 0

def removeBooks(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if u[3] == 0:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    for book in books:
        s = c.execute('SELECT "Status" FROM Books WHERE "ID"=?', (book,))
        status = c.fetchone()
        if status[0] == 'Borrowed':
            continue
        else:
            c.execute('DELETE FROM Books WHERE "ID"=?', (book,))
            c.execute('DELETE FROM BorrowedBooks WHERE "Book ID" = ?', (book,))
            c.execute('DELETE FROM Holds WHERE "Book ID" = ?', (book,))
            c.execute('DELETE FROM Reports WHERE "Book ID" = ?', (book,))
    conn.commit()
    conn.close()
    return 0

def checkOut(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books selected.
    errorCode4 = 4 #User has a high fee.
    borrow = ''' INSERT INTO BorrowedBooks("Book ID", "Borrower ID", "Name", "Due Date")
              VALUES(?,?,?,?) '''

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
    f = c.fetchone()
    if f[0] >= 5:
        conn.close()
        return errorCode4
    for book in books:
        b = c.execute('SELECT * FROM Books WHERE Name=?',(book,))
        currentBook = c.fetchone()
        if not currentBook:
            continue
        if(currentBook[7] != 'Available'):
            continue
        if(currentBook[8] == 'Yes'):
            bID = currentBook[0]
            allHolds = c.execute('SELECT * FROM Holds WHERE "Book ID"=?', (bID,))
            ah = c.fetchall()
            userHolds = c.execute('SELECT * FROM Holds WHERE "Book ID"=? and "Borrower ID"=?', (bID, u[0]))
            h = c.fetchone()
            if(u[0] != h[1]):
                continue
            else:
                c.execute('DELETE FROM Holds WHERE "Borrower ID"=?',(u[0],))
                if(len(ah) == 1):
                    c.execute('''UPDATE Books SET "Hold Requested" = ? WHERE ID = ?''', ('No', currentBook[0]))
        task = []
        report = []
        task.append(currentBook[0])
        report.append(currentBook[0])
        task.append(u[0])
        report.append(u[0])
        task.append(currentBook[1])
        now = datetime.datetime.now()
        duration = datetime.timedelta(days=BORROW_TIME_PERIOD)
        time = now + duration
        task.append(time)
        report.append(now)
        report.append("")
        c.execute(borrow, task)
        c.execute(''' INSERT INTO Reports values(?,?,?,?) ''', report)
        c.execute('''UPDATE Books SET Status = ? WHERE ID = ?''', ('Borrowed', task[0]))
    conn.commit()
    conn.close()
    return 0

def checkIn(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books selected.
    returnBook = 'DELETE FROM BorrowedBooks WHERE "Book ID"=?'

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    for book in books:
        b = c.execute('SELECT * FROM Books WHERE Name=?',(book,))
        currentBook = c.fetchone()
        bb = c.execute('SELECT * FROM BorrowedBooks WHERE Name=?',(book,))
        borrowedBook = c.fetchone()
        if not currentBook:
            continue
        if not borrowedBook:
            continue
        if borrowedBook[1] != u[0]:
            continue
        else:
            num = currentBook[0]
            task = []
            report = []
            task.append(currentBook[0])
            report.append(currentBook[0])
            report.append(u[0])
            date = c.execute('SELECT "Due Date" FROM BorrowedBooks WHERE "Book ID"=?',(num,))
            d = c.fetchone()
            now = datetime.datetime.now()
            report.append("")
            report.append(now)
            dt_obj = datetime.datetime.strptime(d[0], "%Y-%m-%d %H:%M:%S.%f")
            if(now > dt_obj):
                timeLate = now - dt_obj
                daysLate = timeLate.total_seconds() / 86400
                fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
                f = c.fetchone()
                newFee = f[0] + (int(daysLate) * LATE_CHARGE)
                c.execute('''UPDATE Users SET "Late Fees" = ? WHERE ID = ?''', (newFee, u[2]))
            c.execute(returnBook, task)
            c.execute(''' INSERT INTO Reports values(?,?,?,?) ''', report)
            c.execute('''UPDATE Books SET Status = ? WHERE ID = ?''', ('Available', task[0]))
    conn.commit()
    conn.close()
    return 0

def placeHold(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books selected.
    errorCode4 = 4 #User has a high fee.
    hold = ''' INSERT INTO Holds("Book ID", "Borrower ID", "Name")
              VALUES(?,?,?) '''

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
    f = c.fetchone()
    if f[0] >= 5:
        conn.close()
        return errorCode4
    for book in books:
        b = c.execute('SELECT * FROM Books WHERE Name=?',(book,))
        currentBook = c.fetchone()
        if not currentBook:
            continue
        h = c.execute('SELECT * FROM Holds WHERE "Borrower ID" =? and "Book ID" = ?', (u[0], currentBook[0]))
        holds = c.fetchone()
        if holds:
            continue
        else:
            task = []
            task.append(currentBook[0])
            task.append(u[0])
            task.append(currentBook[1])
            c.execute(hold, task)
            c.execute('''UPDATE Books SET "Hold Requested" = ? WHERE ID = ?''', ('Yes', task[0]))
    conn.commit()
    conn.close()
    return 0

def renewBook(books = [], user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No books selected.
    errorCode4 = 4 #User has a high fee.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not books:
        conn.close()
        return errorCode3
    fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
    f = c.fetchone()
    if f[0] >= 5:
        conn.close()
        return errorCode4
    #print('ssss')
    for book in books:
        b = c.execute('SELECT * FROM Books WHERE Name=?',(book,))
        currentBook = c.fetchone()
        if not currentBook:
            continue
        else:
            now = datetime.datetime.now()
            duration = datetime.timedelta(days=BORROW_TIME_PERIOD)
            time = now + duration

            c.execute('''UPDATE BorrowedBooks SET "Due Date" = ? WHERE "Book ID" = ?''', (time, currentBook[0]))

    conn.commit()
    conn.close()
    return 0

def updateUserInformation(PhoneNumber = None, Address = None, Email = None, Password = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if PhoneNumber:
        c.execute('''UPDATE Users SET "Phone Number" = ? WHERE ID = ?''', (PhoneNumber, u[0]))
    if Address:
        c.execute('''UPDATE Users SET "Address" = ? WHERE ID = ?''', (Address, u[0]))
    if Email:
        c.execute('''UPDATE Users SET "Email" = ? WHERE ID = ?''', (Email, u[0]))
    if Password:
        c.execute('''UPDATE Users SET "Password" = ? WHERE ID = ?''', (Password, u[0]))
    conn.commit()
    conn.close()
    return 0

def payFee(amount=0.0, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #Negative amount provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if amount < 0:
        conn.close()
        return errorCode3
    fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
    f = c.fetchone()
    newFee = f[0] - amount
    if newFee < 0:
        newFee = 0
    c.execute('''UPDATE Users SET "Late Fees" = ? WHERE ID = ?''', (newFee, u[0]))
    conn.commit()
    conn.close()
    return 0

def getFee(user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    fee = c.execute('SELECT "Late Fees" FROM Users WHERE Username=?',user)
    f = c.fetchone()
    conn.close()
    f0 = '${:,.2f}'.format(f[0])
    return f0

#Date format should be "YEAR-MONTH-DAY"
def dailyCheckoutReport(date = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No date provided.
    errorCode4 = 4 #No data for provided date.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not date:
        conn.close()
        return errorCode3
    d = date + ('%')
    c.execute('SELECT "Book ID", "Borrower ID" FROM Reports WHERE "Check Out Date" LIKE ?', (d,))
    r = c.fetchall()
    if not r:
        conn.close()
        return errorCode4
    r1 = []
    for b in r:
        c.execute('SELECT "Name" FROM Books WHERE ID=?', (b[0],))
        r1.append(c.fetchone())
        c.execute('SELECT "Name" FROM Users WHERE ID=?', (b[1],))
        r1.append(c.fetchone())
    conn.close()
    return r1

#Date format should be "YEAR-MONTH-DAY"
def dailyCheckinReport(date = None, user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.
    errorCode3 = 3 #No date provided.
    errorCode4 = 4 #No data for provided date.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    if not date:
        conn.close()
        return errorCode3
    d = date + ('%')
    c.execute('SELECT "Book ID", "Borrower ID" FROM Reports WHERE "Check In Date" LIKE ?', (d,))
    r = c.fetchall()
    if not r:
        conn.close()
        return errorCode4
    r1 = []
    for b in r:
        c.execute('SELECT "Name" FROM Books WHERE ID=?', (b[0],))
        r1.append(c.fetchone())
        c.execute('SELECT "Name" FROM Users WHERE ID=?', (b[1],))
        r1.append(c.fetchone())
    conn.close()
    return r1

def userReport(user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT * FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2
    borrowed = c.execute('SELECT "Name", "Due Date" FROM BorrowedBooks WHERE "Borrower ID"=?', (u[0],))
    b = c.fetchall()
    b2 = (b)
    held = c.execute('SELECT "Name" FROM Holds WHERE "Borrower ID"=?', (u[0],))
    h = c.fetchall()
    f = getFee(user)
    report = []
    #[0][x][y]
    if b2:
        report.append(b2)
    #[1][x]
    if h:
        report.append(h)
    report.append(f)
    conn.close()
    return report

def userDetails(user = None, sqlite_file = DATABASE):
    errorCode1 = 1 #No user provided.
    errorCode2 = 2 #Invalid user provided.

    conn = sqlite3.connect(sqlite_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    #user should look like this:
    #u = ('John Doe',)
    #note the comma.
    if(user == None):
        conn.close()
        return errorCode1
    userInformation = c.execute('SELECT Name, `Phone Number`, Address, Email, `Late Fees` FROM Users WHERE Username=?',user)
    u = c.fetchone()
    if not u:
        conn.close()
        return errorCode2

    details = []
    details.append(u)
    conn.close()
    return details
