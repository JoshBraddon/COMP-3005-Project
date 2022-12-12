CREATE TABLE Stores (
    store_name VARCHAR(50) PRIMARY KEY NOT NULL,
    owner_name VARCHAR(50) NOT NULL
);

CREATE TABLE Books (
    isbn  VARCHAR(13) PRIMARY KEY NOT NULL,
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
        REFERENCES Publishers (publisher_name),
    FOREIGN KEY (store_name)
        REFERENCES Stores (store_name)
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY NOT NULL,
    destination VARCHAR(50) NOT NULL,
    current_location VARCHAR(50) NOT NULL
);

CREATE TABLE Publishers (
    publisher_name VARCHAR(50) PRIMARY KEY NOT NULL,
    address VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_num VARCHAR(15) NOT NULL,
    bank_account_num INTEGER NOT NULL
);

CREATE TABLE Users (
    user_id VARCHAR(50) PRIMARY KEY NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    billing_info VARCHAR(50) NOT NULL,
    shipping_info VARCHAR(50) NOT NULL
);

CREATE TABLE User_Orders (
    order_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES Orders (order_id),
    FOREIGN KEY (user_id)
        REFERENCES Users (user_id)
);

CREATE TABLE Order_Books (
    order_id INTEGER PRIMARY KEY NOT NULL,
    isbn VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES Orders (order_id),
    FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
);
