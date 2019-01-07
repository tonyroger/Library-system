from DBtest import *
from tkinter import *

# global variables
currentUser = ''
isLogged = False
listBooks = []

# currentUser = 'Matt'
# isLogged = True

currentState = {
"BookBorrow": 'disabled',
"BookOnHold": 'disabled',
"BookRenew": 'disabled',
"BookReturn": 'disabled'
}

listBorrowedBooksState = {
"BookBorrow": 'disabled',
"BookOnHold": 'disabled',
"BookRenew": 'active',
"BookReturn": 'active'
}

listBooksState = {
"BookBorrow": 'active',
"BookOnHold": 'active',
"BookRenew": 'disabled',
"BookReturn": 'disabled'
}

# book lists
def GUIListBooks():
    global listBooks
    global currentState

    if isLogged:
        s = searchDB(user=(currentUser,))
        if type(s) == int: listboxResponse.insert(END,'[GUIListBooks] not successful: '+str(s))
        else:
            currentState = listBooksState
            GUIFillMenu()
            listboxBooks.delete(0,END)
            listBooks = s
            i=0
            for record in s:
                listboxBooks.insert(END,str(i+1)+ '. ['+record[5]+'] ' + ' "' + record[0] + '", ' + record[1])
                if record[6]=='Borrowed':
                    listboxBooks.itemconfig(END,fg="gray")
                i+=1
            #listboxBooks.selection_set()
    else:
        listboxResponse.insert(END,'[GUIListBooks] not logged in')

def GUIListBorrowedBooks():
    global listBooks
    global currentState

    if isLogged:
        s = userReport(user=(currentUser,))
        if type(s) == int: listboxResponse.insert(END,'[GUIListBorrowedBooks] not successful: '+str(s))
        else:
            currentState = listBorrowedBooksState
            GUIFillMenu()
            listboxBooks.delete(0,END)
            listBooks = s[0]
            i=0
            for record in s[0]:
                listboxBooks.insert(END,str(i+1) + '. [due date '+record[1]+'] ' + ' "' + record[0]+'"')
                #listboxBooks.itemconfig(END, {'fg':('lightgray','black')['Available'==record[6]]})
                i+=1
    else:
        listboxResponse.insert(END,'[GUIListBorrowedBooks] not logged in')

# book menu functions
def GUIBookRenew():
    if isLogged:
        entry = listBooks[listboxBooks.curselection()[0]]
        result = renewBook(books=(entry[0],),user=(currentUser,))
        #print(result)
        if result != 0:
            listboxResponse.insert(END,'[GUIListBookRenew] not successful: '+str(result))
        else:
            listboxResponse.insert(END,'[GUIListBookRenew] selected book renewed')
            GUIListBorrowedBooks()
    else:
        listboxResponse.insert(END,'[GUIListBookRenew] not logged in')

def GUIBookReturn():
    if isLogged:
        entry = listBooks[listboxBooks.curselection()[0]]
        #print(entry[0])
        result = checkIn(books=(entry[0],),user=(currentUser,))
        #print(result)
        if result != 0:
            listboxResponse.insert(END,'[GUIBookReturn] not successful: '+str(result))
        else:
            listboxResponse.insert(END,'[GUIBookReturn] selected book returned')
            GUIListBorrowedBooks()
    else:
        listboxResponse.insert(END,'[GUIBookReturn] not logged in')

def GUIBookBorrow():
    if isLogged:

        entry = listBooks[listboxBooks.curselection()[0]]
        if entry[6]!="Borrowed": result = checkOut(books=(entry[0],),user=(currentUser,))
        else: result = -1
        if result != 0:
            listboxResponse.insert(END,'[GUIBookBorrow] not successful: '+str(result))
        else:
            listboxResponse.insert(END,'[GUIBookBorrow] selected book borrowed')
            GUIListBooks()
    else:
        listboxResponse.insert(END,'[GUIBookBorrow] not logged in')

def GUIBookOnHold():
    listboxResponse.insert(END,'[GUIBookOnHold] not implemented!')

# login function
def GUILogin():
    global isLogged
    global currentUser

    result = login(username=entryUser.get(),password=entryPassword.get())

    if result==0:

        isLogged = True
        currentUser = entryUser.get()

        listboxResponse.insert(END,'login successful')
        report = userDetails((entryUser.get(),))

        labelCurrentUserNameData['text'] = entryUser.get()
        labelCurrentFullNameData['text'] = report[0][0]
        labelCurrentPhoneData['text'] = report[0][1]
        labelCurrentAddressData['text'] = report[0][2]
        labelCurrentEmailData['text'] = report[0][3]
        labelCurrentLateFeesData['text'] = report[0][4]

    else:
        listboxResponse.insert(END,'login not successful: '+str(result))

    entryUser.delete(0,END)
    entryPassword.delete(0,END)

# search function
def GUISearch():
    global listBooks
    global currentState

    if isLogged:

        search = entrySearch.get()
        s = searchDB(user=(currentUser,), Bookname=search)

        if type(s) == int: listboxResponse.insert(END,'[GUISearch] not successful: '+str(s))
        else:
            listboxResponse.insert(END,'[GUISearch] search successful')
            currentState = listBooksState
            GUIFillMenu()
            listboxBooks.delete(0,END)
            listBooks = s
            i=0
            for record in s:
                listboxBooks.insert(END,str(i+1)+ '. ['+record[5]+'] ' + ' "' + record[0] + '", ' + record[1])
                if record[6]=='Borrowed':
                    listboxBooks.itemconfig(END,fg="gray")
                i+=1
            #listboxBooks.selection_set()
    else:
        listboxResponse.insert(END,'[GUISearch] not logged in')

def GUIChangePassword():
    if isLogged:
        result = updateUserInformation(user=(currentUser,),Password=entryChangePassword.get());
        if result != 0: listboxResponse.insert(END,'[GUIChangePassword] not successful: '+str(result))
        else:
            entryChangePassword.delete(0,END)
            listboxResponse.insert(END,'[GUIChangePassword] password changed')

    else:
        listboxResponse.insert(END,'[GUIChangePassword] not logged in')


# draw menu function
def GUIFillMenu():
    global menubar
    menubar.delete(0,END)
    menuGeneral = Menu(menubar,tearoff=0)
    menuGeneral.add_command(label="Exit",command = root.quit)

    menuBook = Menu(menubar, tearoff=0)
    menuBook.add_command(label="Borrow", command=GUIBookBorrow, state=currentState['BookBorrow'])
    menuBook.add_command(label="Put on hold", command=GUIBookOnHold, state=currentState['BookOnHold'])
    menuBook.add_command(label="Renew", command=GUIBookRenew, state=currentState['BookRenew'])
    menuBook.add_command(label="Return", command=GUIBookReturn, state=currentState['BookReturn'])

    menuLists = Menu(menubar,tearoff=0)
    menuLists.add_command(label="List books", command=GUIListBooks)
    menuLists.add_command(label="List borrowed books", command=GUIListBorrowedBooks)
    #menuLists.add_command(label="History", command=GUIListHistory)

    menubar.add_cascade(label="General", menu=menuGeneral)
    menubar.add_cascade(label="Lists", menu=menuLists)
    menubar.add_cascade(label="Book", menu=menuBook)

root = Tk()
root.geometry("1000x700")
root.title("BookApp")
root.resizable(width=FALSE, height=FALSE)

# setup frames
frameTop = Frame(root)
frameBottom = Frame(root)
frameBottomLeft = Frame(frameBottom)
frameBottomRight = Frame(frameBottom)
frameResponse = Frame(root)

# setup the root grid
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# setup the Bottom grid
frameBottom.grid_rowconfigure(0, weight=1)
frameBottom.grid_columnconfigure(2, weight=1)

# setup the BottomLeft grid
frameBottomLeft.grid_rowconfigure(4, weight=1)
frameBottomLeft.grid_columnconfigure(3, weight=1)

# setup the BottomRight grid
frameBottomRight.grid_rowconfigure(0, weight=1)
frameBottomRight.grid_columnconfigure(0, weight=1)

# setup Menu
menubar = Menu(root)
GUIFillMenu()

# setup Login module
labelUser = Label(frameTop, text='User:')
labelPassword = Label(frameTop, text='Password:')
entryUser = Entry(frameTop)
entryPassword = Entry(frameTop, show="*")
buttonLogin = Button(frameTop,text='Login',command=GUILogin)

# setup Books module
labelBooks = Label(frameBottomLeft,text='Book list:')
scrollbarBooks = Scrollbar(frameBottomLeft)
listboxBooks = Listbox(frameBottomLeft,height=35,width=100, yscrollcommand=scrollbarBooks.set)

# setup Search module
labelSearch = Label(frameBottomLeft,text='Search')
buttonSearch = Button(frameBottomLeft,text='Search',command=GUISearch)
entrySearch = Entry(frameBottomLeft)

# setup UserDetails module
labelCurrentUser = Label(frameBottomRight,text='Current user details')

labelCurrentUserName = Label(frameBottomRight,text='User Name:')
labelCurrentFullName = Label(frameBottomRight,text='Full Name:')
labelCurrentPhone = Label(frameBottomRight,text='Phone Number:')
labelCurrentAddress = Label(frameBottomRight,text='Address:')
labelCurrentEmail = Label(frameBottomRight,text='Email:')
labelCurrentLateFees = Label(frameBottomRight,text='Late Fees:')

labelCurrentUserNameData = Label(frameBottomRight,text='')
labelCurrentFullNameData = Label(frameBottomRight,text='')
labelCurrentPhoneData = Label(frameBottomRight,text='')
labelCurrentAddressData = Label(frameBottomRight,text='')
labelCurrentEmailData = Label(frameBottomRight,text='')
labelCurrentLateFeesData = Label(frameBottomRight,text='')

buttonChangePassword = Button(frameBottomRight,text='Change password', command=GUIChangePassword)
entryChangePassword = Entry(frameBottomRight)
# setup BookDetails module
#labelBookDetails = Label(frameBottomRight,text='Book details')

# setup Response module
scrollbarResponse = Scrollbar(frameResponse)
listboxResponse = Listbox(frameResponse,height=10,width=80, yscrollcommand=scrollbarResponse.set)
scrollbarResponse.config(command=listboxResponse.yview)

# display the menu
root.config(menu=menubar)

#position all frames
frameTop.grid(row=0,column=0,sticky="w")
frameBottom.grid(row=1,column=0,sticky="ew")
frameResponse.grid(row=2,column=0,sticky="ew")
frameBottomLeft.grid(row=0,column=0,sticky="ew")
frameBottomRight.grid(row=0,column=1,sticky="n")


# frameTop

# position Login module
labelUser.grid(row=0,column=0,sticky='w')
labelPassword.grid(row=1,column=0,sticky='w')
entryUser.grid(row=0,column=1)
entryPassword.grid(row=1,column=1)
buttonLogin.grid(column=2,row=0,rowspan=2)

# frameBottomLeft

# position Books module
labelBooks.grid(row=0,column=0,columnspan=2)
scrollbarBooks.grid(row=1,column=2,sticky="ns")
listboxBooks.grid(row=1,column=0,columnspan=2)

# position Search module
#labelSearch.grid(row=2,column=0)
#entrySearch.grid(row=2,column=0)
entrySearch.grid(row=2,column=0,columnspan=2)
buttonSearch.grid(row=3,column=0,columnspan=2)

# frameBottomRight

# position UserDetails module
labelCurrentUser.grid(row=0,column=0,columnspan=2,sticky='w')
labelCurrentUserName.grid(row=2,column=0,sticky='w')
labelCurrentUserNameData.grid(row=2,column=1,sticky='w',columnspan=2)
labelCurrentFullName.grid(row=3,column=0,sticky='w')
labelCurrentFullNameData.grid(row=3,column=1,sticky='w',columnspan=2)
labelCurrentPhone.grid(row=4,column=0,sticky='w')
labelCurrentPhoneData.grid(row=4,column=1,sticky='w',columnspan=2)
labelCurrentAddress.grid(row=5,column=0,sticky='w')
labelCurrentAddressData.grid(row=5,column=1,sticky='w',columnspan=2)
labelCurrentEmail.grid(row=6,column=0,sticky='w')
labelCurrentEmailData.grid(row=6,column=1,sticky='w',columnspan=2)
labelCurrentLateFees.grid(row=7,column=0,sticky='w')
labelCurrentLateFeesData.grid(row=7,column=1,sticky='w',columnspan=2)
entryChangePassword.grid(row=8,column=0)
buttonChangePassword.grid(row=8, column=1)


# position BookDetails module
#labelBookDetails.grid(row=8,column=0,columnspan=2)

# frameResponse

# position Response module
scrollbarResponse.grid(row=0,column=1,sticky="ns")
listboxResponse.grid(row=0,column=0)



root.mainloop()
