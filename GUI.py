import PySimpleGUI as gui
import sqlite3 

global logged_in
gui.theme('DarkGrey2')

start_layout = [ [gui.Text('Welcome to Look Inna Book')], [gui.Button('Customer Mode')], [gui.Button('Owner Mode')] ]

def link_database(db):
    """
    Connects to the database using sqlite3 library funcitonality
    """
    connection = None
    try:
        connection = sqlite3.connect(db)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    return connection

def open_customer_window(db):
    """
    Opens a window allowing for login or order tracking
    """
    customer_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Login')], [gui.Button('Order Tracking'), gui.InputText()], [gui.Button('Help')] ] 
    customer_window = gui.Window('Look Inna Book', customer_layout)
    while True:
        event, values = customer_window.read()
        if event == gui.WIN_CLOSED:
            break
        if event == 'Search':
            results = search(values[0], 0, db)
        elif event == 'Login':
            login_window(db)
        elif event == 'Order Tracking':
            track(values[1], db)
        elif event == 'Help':
            open_help_window(0)
    customer_window.close()

def open_owner_window(db):
    """
    Opens store owner window allowing for adding publisher, adding/removing books and viewing reports
    """
    owner_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Add Publisher')], [gui.Button('Add Books')], [gui.Button('Remove Books')], [gui.Button('View Reports')], [gui.Button('Help')] ]
    owner_window = gui.Window('Look Inna Book', owner_layout)
    while True:
        event, values = owner_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Add Publisher':
            add_publisher(db)
        elif event == 'Add Books':
            change_books(0, db)
        elif event == 'Remove Books':
            change_books(1, db)
        elif event == 'Help':
            open_help_window(1)
    owner_window.close()

def login_window(db):
    """
    Logs in to a user by querying database for user inputted user_id and password fields
    """
    login = [ [gui.Text('Enter Username:'), gui.InputText()], [gui.Text('Enter Password:'), gui.InputText()], [gui.Button('Login')], [gui.Button('No Account?')]]
    login_window = gui.Window('Login', login)
    while True:
        event, values = login_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Login':
            cur = db.cursor()
            query_login ="SELECT * FROM Users WHERE user_id=" + values[0] + " AND password=" + values[1] 
            try:
                cur.execute(query_login)
            except:
                print("Error, could not find elements " + values[0] + "," + values[1])
            
            result = cur.fetchall()
            if result is not None:
                logged_in = 1
        elif event == 'No Account?':
            register_window(db)
    login_window.close()

def open_help_window(i):
    """
    Displays a help message
    """
    customer_help = [ [gui.Text('Search allows you to enter the name or ISBN number of a book to search for it. \nLogin allows you to enter your information to be save your account, it is also required for purchasing books. \nOrder tracking allows you to enter your order number to check its status.')]]
    owner_help = [ [gui.Text('Search allows you to enter the name or ISBN number of a book to search for it to check inventory, order more, etc.\n Add Publisher allows you add the information about a new publisher.\n View reports allows you to brose data about sales.')] ]
    if i == 0:
        help_window = gui.Window('Help', customer_help)
    else:
        help_window = gui.Window('Help', owner_help)
    while True:
        event, values = help_window.read()
        if event == gui.WIN_CLOSED:
            break
    help_window.close()

def search(search, mode, db):
    """
    Queries database for book given isbn, title, genre or author
    """
    cur = db.cursor()
    cur.execute("SELECT ISBN, Title, Genre, Author Name FROM Books WHERE ISBN=?, Title=?, Genre=?, Author Name=?", search)

    results = cur.fetchall()
    #for rows in results:
    #search_window = gui.Window('Search Results', search_layout)

def register_window(db):
    """
    Allows for registering a new user to the database using sql INSERT and passing in user inputted fields
    Checks that user input user_id is unique by querying database
    """
    reg = [ [gui.Text('Enter Username:'), gui.InputText()], [gui.Text('Enter Password:'), gui.InputText()], [gui.Text('Enter Email Address:'), gui.InputText()], [gui.Text('Enter Billing Address:'), gui.InputText()], [gui.Button('Create Account')]]
    reg_window = gui.Window('Register', reg)
    while True:
        event, values = reg_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Create Account':
            cur = db.cursor()
            query_user_id = "SELECT user_id FROM Users WHERE user_id=" + values[0]
            result = None
            try:
                cur = db.cursor()
                cur.execute(query_user_id)
                results = cur.fetch()
                
                info_window = gui.Window('Login Failed', [[gui.Text('This Username is already in use try another one.')]])
                while True:
                    event, values = info_window.read()
                    if event == gui.WIN_CLOSED:
                        break
            except:
                insert_string = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s)"
                cur.execute(insert_string, (values[0], values[1], values[2], values[3], values[3]))
                logged_in = 1
                
            
    reg_window.close()
    
def track(orderNo, db):
    """
    Returns current location allowing tracking of package by querying sql database using user inputted order number
    """
    cur = db.cursor()
    try:
        cur.execute("SELECT current_location FROM Orders WHERE order_id=" + str(orderNo)) 
        result = cur.fetchall()
        orderTracking = [ [gui.Text('Your is order in:')], [gui.Text(result)] ]
        tracking = gui.Window('Shipping Information', orderTracking)
        while True:
            event, values = tracking.read()
            if event == gui.WIN_CLOSED:
                break
            tracking.close()
    except:
        pass
    
    

def add_publisher(db):
    """
    Allows for adding a publisher to the database using sql INSERT and user inputted fields
    """
    publisher_layout = [[gui.Text('Enter Publisher Name:'), gui.InputText()], [gui.Text('Enter Publisher Address:'), gui.InputText()], [gui.Text('Enter Publisher Email:'), gui.InputText()], [gui.Text('Enter Publisher Phone Number:'), gui.InputText()], [gui.Text('Enter Publisher Shipping Info:'), gui.InputText()], [gui.Button('Submit')]]
    publisher_window = gui.Window('Publisher Informaition', publisher_layout)
    while True:
        event, values = publisher_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Submit':
            cur = db.cursor()
            insert_string = "INSERT INTO Publishers VALUES ({}, {}, {}, {}, {})".format(values[0], values[1], values[2], values[3], values[4])
            cur.execute(insert_string)
            break
    publisher_window.close()

def change_books(mode, db):
    """
    Allows for adding/removing books from the database using INSERT/DELETE sql actions and user inputted fields
    """
    if mode == 0:
        layout = [[gui.Text('Enter ISBN:'), gui.InputText()], [gui.Text('Enter Title:'), gui.InputText()], [gui.Text('Enter Genre:'), gui.InputText()], [gui.Text('Enter Price:'), gui.InputText()], [gui.Text('Enter Number of Pages:'), gui.InputText()], [gui.Text('Enter Publish Pay %:'), gui.InputText()], [gui.Text('Enter Author Name:'), gui.InputText()], [gui.Text('Enter Publisher Name:'), gui.InputText()], [gui.Text('Enter how many copies we have:'), gui.InputText()], [gui.Button('Submit')]]
    else:
        layout = [[gui.Text('Enter ISBN'), gui.InputText()], [gui.Button('Submit')]]
        
    stock_window = gui.Window('Change Inventory', layout)
    while True:
        event, values = stock_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Submit':
            if mode == 0:
                cur = db.cursor()
                insert_string = "INSERT INTO Books (isbn, title, genre, price, num_of_pages, publisher_pay_percent, author_name, publisher_name, num_in_stock, store_name) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, \"Look Inna Book\")".format(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
                cur.execute(insert_string)
    stock_window.close()


def main():
    logged_in = 0
    db = None
    database = r"bookstore.db"
    db = link_database(database)
    start_window = gui.Window('Mode Select', start_layout)

    while True:
        event, vales = start_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Customer Mode':
            open_customer_window(db)
        elif event == 'Owner Mode':
            open_owner_window(db)
    start_window.close()
    exit()
        
if __name__ == "__main__":
    main()
