import PySimpleGUI as gui

gui.theme('DarkGrey2')

logged_in = 0

start_layout = [ [gui.Text('Welcome to Look Inna Book')], [gui.Button('Customer Mode')], [gui.Button('Owner Mode')] ]


def open_customer_window():
    customer_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Login')], [gui.Button('Order Tracking'), gui.InputText()], [gui.Button('Help')] ] 
    customer_window = gui.Window('Look Inna Book', customer_layout)
    while True:
        event, values = customer_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Login':
            login_window()
        elif event == 'Order Tracking':
            track(values[1])
        elif event == 'Help':
            open_help_window(0)
    customer_window.close()

def open_owner_window():
    owner_layout = [ [gui.Text('Search:'), gui.InputText()], [gui.Button('Add Publisher')], [gui.Button('View Reports')], [gui.Button('Help')] ]
    owner_window = gui.Window('Look Inna Book', owner_layout)
    while True:
        event, values = owner_window.read()
        if event == gui.WIN_CLOSED:
            break
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
            logged_in = 1
        elif event == 'No Account?':
            register_window()
    login_window.close()

def register_window():
    reg = [ [gui.Text('Enter Username:'), gui.InputText()], [gui.Text('Enter Password:'), gui.InputText()], [gui.Text('Enter Billing Address:'), gui.InputText()], [gui.Text('Enter Shipping Address:'), gui.InputText()], [gui.Button('Create Account')]]
    reg_window = gui.Window('Register', reg)
    while True:
        event, values = reg_window.read()
        if event == gui.WIN_CLOSED:
            break
        elif event == 'Create Account':
            logged_in = 1
    reg_window.close()

def track(i):
    i = 5

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


def main():
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
