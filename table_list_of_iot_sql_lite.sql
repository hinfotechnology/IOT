
CREATE TABLE IF NOT EXISTS admin(
    user_name text ,
    password varchar
);

-

INSERT INTO admin (user_name,password) VALUES
('hinfo',12345);

-

CREATE TABLE IF NOT EXISTS purchaser_details (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_Rf_Id INTEGER NOT NULL,
    account_balance INTEGER,
    User_Name TEXT NOT NULL,
    Email_id TEXT NOT NULL,
    User_Address TEXT NOT NULL,
    Telephone INTEGER NOT NULL,
    Status BOOLEAN DEFAULT 0,
    Password BLOB,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-

CREATE TABLE IF NOT EXISTS vendor(
    Vendor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name text,
    Email_id varchar,
    Address varchar,
    Telephone varchar,
    Password BINARY(60)
);

-

CREATE TABLE IF NOT EXISTS product(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name text,
    Rf_reader varchar,
    available_qty numeric,
    price numeric
);

-

CREATE TABLE IF NOT EXISTS purchaser_dashboard(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Description text,
    Total_items text,
    Quantity numeric,
    Money_transactions varchar
);

-

CREATE TABLE IF NOT EXISTS purchasing_list(
    DATE text ,
    ID numeric,
    shopname text,
    Items text,
    Quantity numeric,
    Total_price varchar,
    Shop_address text,
    Phone varchar,
    Product_name varchar ,
    Product_MRP_Price varchar,
    Product_discount_price varchar,
    Qty numeric
);

-

CREATE TABLE IF NOT EXISTS purchasing_view(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Shop_address text,
    Phone varchar,
    Product_name varchar ,
    Product_MRP_Price varchar,
    Product_discount_price varchar,
    Quantity numeric
);

-

CREATE TABLE IF NOT EXISTS shop_list(
    ID numeric,
    shop_name text,
    owner text,
    Address text,
    phone varchar,
    Status boolean default false,
    shop_starting_from varchar,
    shop_last_update varchar,
    Last_update_reason varchar,
    shop_photo varchar
);
