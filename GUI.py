import PySimpleGUI as gui
import sqlite3 

global db
global logged_in
gui.theme('DarkGrey2')

start_layout = [ [gui.Text('Welcome to Look Inna Book')], [gui.Button('Customer Mode')], [gui.Button('Owner Mode')] ]

def link_databse(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
    except:
        print("Linking falied")
    return connection

def open_customer_window():
    customer_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Login')], [gui.Button('Order Tracking'), gui.InputText()], [gui.Button('Help')] ] 
    customer_window = gui.Window('Look Inna Book', customer_layout)
    while True:
        event, values = customer_window.read()
        if event == gui.WIN_CLOSED:
            break
        if event == 'Search':
            results = search(values[0], 0)
        elif event == 'Login':
            login_window()
        elif event == 'Order Tracking':
            track(values[1])
        elif event == 'Help':
            open_help_window(0)
    customer_window.close()

def open_owner_window():
    owner_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Add Publisher')], [gui.Button('Add Books')], [gui.Button('Remove Books')], [gui.Button('View Reports')], [gui.Button('Help')] ]
    owner_window = gui.Window('Look Inna Book', owner_layout)
    while True:
        event, values = owner_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Add Publisher':
            add_publisher()
        elif event == 'Add Books':
            change_books(0)
        elif event == 'Remove Books':
            change_books(1)
        elif event == 'Help':
            open_help_window(1)
    owner_window.close()

def login_window():
    login = [ [gui.Text('Enter Username:'), gui.InputText()], [gui.Text('Enter Password:'), gui.InputText()], [gui.Button('Login')], [gui.Button('No Account?')]]
    login_window = gui.Window('Login', login)
    while True:
        event, values = login_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Login':
            cur = db.cursor()
            cur.execute("SELECT * FROM Users WHERE user_id=? AND password=?", values[0], values[1]) 
            result = cur.fetchall()
            if result is not None:
                logged_in = 1
        elif event == 'No Account?':
            register_window()
    login_window.close()

def open_help_window(i):
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

def search(search, mode):
    cur = db.cursor()
    cur.execute("SELECT ISBN, Title, Genre, Author Name FROM Books WHERE ISBN=?, Title=?, Genre=?, Author Name=?", search)

    results = cur.fetchall()
    #for rows in results:
    #search_window = gui.Window('Search Results', search_layout)

def register_window():
    reg = [ [gui.Text('Enter Username:'), gui.InputText()], [gui.Text('Enter Password:'), gui.InputText()], [gui.Text('Enter Email Address:'), gui.InputText()], [gui.Text('Enter Billing Address:'), gui.InputText()], [gui.Button('Create Account')]]
    reg_window = gui.Window('Register', reg)
    while True:
        event, values = reg_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Create Account':
            cur = db.cursor()
            cur.execute("SELECT Id FROM Users WHERE Id=?", values[0])
            results = cur.fetch()
            if results is not None:
                info_window = gui.Window('Login Failed', [[gui.Text('This Username is already in use try another one.')]])
                while True:
                    event, values = info_window.read()
                    if event == gui.WIN_CLOSED:
                        break
            else:
                insert_string = values[0] + values[2] + values[1] + values[3] + values[3]
                cur.execute("INSERT INTO Users(Id, Email, Password, Billing Address, Shipping Address) VALUES (?) ", insert_string)
                logged_in = 1
            break
    reg_window.close()
    
def track(orderNo):
    cur = db.cursor()
    cur.execute("SELECT Current Location FROM Order_Info WHERE Order_id=?", orderNo) 
    result = cur.fetchall()
    orderTracking = [ [gui.Text('Your is order in:')], [gui.Text(result)] ]
    tracking = gui.Window('Shipping Information', orderTracking)
    while True:
        event, values = orderTracking.read()
        if event == gui.WIN_CLOSED:
            break
    orderTracking.close()

def add_publisher():
    publisher_layout = [[gui.Text('Enter Publisher Name:'), gui.InputText()], [gui.Text('Enter Publisher Address:'), gui.InputText()], [gui.Text('Enter Publisher Email:'), gui.InputText()], [gui.Text('Enter Publisher Phone Number:'), gui.InputText()], [gui.Text('Enter Publisher Shipping Info:'), gui.InputText()], [gui.Button('Submit')]]
    publisher_window = gui.Window('Publisher Informaition', publisher_layout)
    while True:
        event, values = publisher_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Submit':
            cur = db.cursor()
            cur.execute("INSERT INTO Publishers VALUES (?, ?, ?, ?, ?)", values[0], values[1], values[2], values[3], int(values[4]))
            break
    publisher_window.close()

def change_books(mode):
    if mode == 0:
        layout = [[gui.Text('Enter ISBN:'), gui.InputText()], [gui.Text('Enter Title:'), gui.InputText()], [gui.Text('Enter Genre:'), gui.InputText()], [gui.Text('Enter Price:'), gui.InputText()], [gui.Text('Enter Number of Pages:'), gui.InputText()], [gui.Text('Enter Publish Pay %:'), gui.InputText()], [gui.Text('Enter Author Name:'), gui.InputText()], [gui.Text('Enter Publisher Name:'), gui.InputText()], [gui.Text('Enter how many copies we have:'), gui.InputText()], [gui.Button('Submit')]]
    else:
        layout = [[gui.Text('Enter ISBN'), gui.InputText()], gui.Button('Submit')]
    stock_window = gui.Window('Change Inventory', layout)
    while True:
        event, values = stock_window.read()
        if event == gui.WIN_CLOSED:
            break
    stock_window.close()


def main():
    logged_in = 0
    database = r"\bokkstore.db"
    db = link_databse(database)
    start_window = gui.Window('Mode Select', start_layout)

    while True:
        event, vales = start_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Customer Mode':
            open_customer_window()
        elif event == 'Owner Mode':
            open_owner_window()
    start_window.close()
    exit()
        
if __name__ == "__main__":
    main()
