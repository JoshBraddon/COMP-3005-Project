CREATE TABLE Store (
    store_name VARCHAR(50) PRIMARY KEY NOT NULL,
    owner_name VARCHAR(50) NOT NULL
);

CREATE TABLE Book (
    isbn  CHAR(13) PRIMARY KEY NOT NULL,
    title VARCHAR(50) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    price DECIMAL(8, 2) NOT NULL,
    num_of_pages INTEGER NOT NULL,
    publisher_pay_percent DECIMAL (3, 2),
    author_name VARCHAR(50) NOT NULL,
    publisher_name VARCHAR(50) NOT NULL,
    num_in_stock INTEGER NOT NULL,
    num_bought_last_month INTEGER NOT NULL,
    store_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (publisher_name)
        REFERENCES Publisher (publisher_name),
    FOREIGN KEY (store_name)
        REFERENCES Store (store_name)
);

CREATE TABLE Order_Info (
    order_id INTEGER PRIMARY KEY NOT NULL,
    destination VARCHAR(50) NOT NULL,
    current_location VARCHAR(50) NOT NULL
);

CREATE TABLE Publisher (
    publisher_name VARCHAR(50) PRIMARY KEY NOT NULL,
    address VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_num VARCHAR(11) NOT NULL,
    bank_account_num VARCHAR(17) NOT NULL
);

CREATE TABLE User_Info (
    user_id INTEGER PRIMARY KEY NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    billing_info VARCHAR(50) NOT NULL,
    shipping_info VARCHAR(50) NOT NULL
);

CREATE TABLE User_Orders (
    order_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES Order (order_id),
    FOREIGN KEY (user_id)
        REFERENCES User (user_id)
);

CREATE TABLE Order_Books (
    order_id INTEGER PRIMARY KEY NOT NULL,
    isbn VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES Order (order_id),
    FOREIGN KEY (isbn)
        REFERENCES Book (isbn)
)
