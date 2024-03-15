-- Database : 'IOT';

DROP TABLE IF EXISTS user,user_address,user_payment,shoppping_session,cart_item,order_detils,order_item,payment_details,product,product_category,product_inventory,discount;

CREATE TABLE user (
    ID int (50) NOT NULL,
    username varchar(100) NOT NULL,
    first_name decimal(100) NOT NULL,
    last_name varchar(100) NOT NULL,
    telephone int (20) NOT NULL,
    create_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_address(
    ID int (50) NOT NULL,
    user_id int (50)  NOT NULL,
    address_line1 varchar(250)  NOT NULL,
    address_line2 varchar(250)  NOT NULL,
    city varchar(200) NOT NULL,
    postal_code varchar(6) NOT NULL,
    country varchar(50) NOT NULL, 
    telephone int(20) NOT NULL,
    mobile int(10) NOT NULL
);

-- CREATE TABLE user_payment(
--     ID int (50) NOT NULL,
--     user_id int (50)  NOT NULL,
--     payment_type varchar(100) NOT NULL,
--     provider varchar(100) NOT NULL,
--     account_no int(50) NOT NULL,
--     expiry_date int(50) NOT NULL
-- );

-- CREATE TABLE shoppping_session(
--     ID int (50) NOT NULL,
--     user_id int (50)  NOT NULL,
--     total int(50)  NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE cart_item(
--     ID int (50) NOT NULL,
--     session_id int(50) NOT NULL,
--     product_id int(50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE order_detils(
--     ID int (50) NOT NULL,
--     user_id int (50) NOT NULL,
--     total int (50) NOT NULL,
--     payment_id int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE order_item(
--     ID int (50) NOT NULL,
--     order_id int(50) NOT NULL,
--     product_id int(50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE payment_details(
--     ID int (50) NOT NULL,
--     order_id int(50) NOT NULL,
--     amount int(50) NOT NULL,
--     provider varchar(100) NOT NULL,
--     status varchar(100) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product(
--     ID int (50) NOT NULL,
--     name varachar(100) NOT NULL,
--     desc varchar(250) NOT NULL,
--     SKU varchar(100) NOT NULL,
--     category_id int(50) NOT NULL,
--     inventory_id int(50) NOT NULL,
--     price int(50) NOT NULL,
--     discount_id int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product_category(
--     ID int (50) NOT NULL,
--     name varachar(100) NOT NULL,
--     desc varchar(250) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE product_inventory(
--     ID int (50) NOT NULL,
--     quantity int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- CREATE TABLE discount(
--     ID int (50) NOT NULL,
--     name varchar(100) NOT NULL,
--     desc varchar(100) NOT NULL,
--     discount_percent int(50) NOT NULL,
--     create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );



create or replace table purchaser1(
    ID numeric,
    USERNAME varchar,
    EMAIL_ID varchar
    );

INSERT INTO purchaser1(ID,USERNAME,EMAIL_ID) VALUES
(1,'dummy','dd@gmail.com');

SELECT * from purchaser1;

create or replace table vendor1(
shopname text,
email_id varchar,
password varchar
);

INSERT INTO vendor1 (shopname,email_id,password) VALUES
('dummy','dummy@gmail.com',12345);

SELECT * from vendor1;
select email_id from vendor1;



create or replace table product1(
    ID INT PRIMARY KEY autoincrement start 100 increment 1 ,
    Product_Name text,
    Available_qty numeric,
    Price numeric
    );

INSERT INTO product1(Product_Name,Available_qty,Price) VALUES
('Apple',12,100),
('Orange',10,100),
('Daal',30,80),
('Dry fruit',20,150),
('Sugar',25,70),
('Dates',50,300),
('Soap',30,40),
('Biscuits',40,20);

SELECT * from product1;


create or replace table customer(
    Rfid_Id INT PRIMARY KEY autoincrement start 200 increment 1 ,
    User_Name varchar,
    Email_id text,
    User_Address text,
    Telephone text,
    Status boolean default false
    );

INSERT INTO customer(User_Name,Email_id,User_Address,Telephone) values
('Mani','mani@gmail.com','Attur',7374448899),
('John','john@gmail.com','Covai',5356368868),
('Peter','peter@gmail.com','chennai',1988328384);

SELECT * from customer;


create or replace table purchaser1(
    id text ,
    password varchar
    );


INSERT INTO purchaser1 (id,password) VALUES
('hinfo',12345);

SELECT * from purchaser1;


create or replace table purchaser_dashboard(
    ID INT PRIMARY KEY autoincrement start 1 increment 1 ,
    Description text,
    Total_items text,
    Quantity numeric,
    Money_transactions varchar
    );

INSERT INTO purchaser_dashboard (Description,Total_items,Quantity,Money_transactions) VALUES
('Apple',12,2,100),
('Orange',10,5,100),
('Daal',30,10,80),
('Dry fruit',20,5,150),
('Sugar',25,4,70),
('Dates',50,6,300),
('Soap',30,8,40),
('Biscuits',40,10,20);

SELECT * from purchaser_dashboard;


create or replace table purchasing_list(
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

INSERT INTO purchasing_list (DATE,ID,shopname,Items,Quantity,Total_price,Shop_address,Phone,Product_name,Product_MRP_Price,Product_discount_price,Qty) VALUES 
('2_5_23',100,'Adams','Shirt',50,60000,'Chennai',8989888889,'Shirt',80000,60000,50),
('2_5_23',101,'Bellstone','Shirt',100,80000,'covai',73733138189,'Shirt',90000,80000,100),
('2_5_23',102,'Pothys','Pant',70,150000,'covai',276372623726,'Pant',180000,150000,70),
('2_5_23',103,'Polo','Tshirt',80,200000,'chennai',2676383737,'Tshirt',220000,200000,80),
('2_5_23',104,'allen_selly','Shirt',100,100000,'chennai',762328237,'Shirt',130000,100000,100),
('2_5_23',105,'Adams','Shirt',60,60000,'chennai',52531376376,'Shirt',80000,60000,60),
('2_5_23',106,'Maxx','Shirt',100,150000,'trichy',573876378632,'Shirt',200000,150000,100);

SELECT DISTINCT
DATE,ID,shopname,Items,Quantity,Total_price,Shop_address,Phone,Product_name,Product_MRP_Price,Product_discount_price,Qty from purchasing_list;

select * from purchasing_list WHERE ID;
select Product_name,Product_MRP_Price,Product_discount_price,Qty from purchasing_list where ID;





create or replace table purchasing_view(
    ID INT PRIMARY KEY autoincrement start 100 increment 1,
    Shop_address text,
    Phone varchar,
    Product_name varchar ,
    Product_MRP_Price varchar,
    Product_discount_price varchar,
    Quantity numeric
    );

INSERT INTO purchasing_view
(Shop_address,Phone,Product_name,Product_MRP_Price,Product_discount_price,Quantity) VALUES
('Chennai',8989888889,'Shirt',80000,60000,50),
('covai',73733138189,'Shirt',90000,80000,100),
('covai',276372623726,'Pant',180000,150000,70),
('chennai',2676383737,'Tshirt',220000,200000,80),
('chennai',762328237,'Shirt',130000,100000,100),
('chennai',52531376376,'Shirt',80000,60000,60),
('trichy',573876378632,'Shirt',200000,150000,100);


select * from purchasing_view;
DROP table purchasing_view;



create or replace table admin(
    user_name text ,
    password varchar
    );


INSERT INTO admin (user_name,password) VALUES
('hinfo',12345);

SELECT * from admin;


create or replace table shop_list(
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

    
INSERT INTO shop_list
(ID,shop_name,owner,Address,phone,shop_starting_from,shop_last_update,Last_update_reason) VALUES
(100,'Adams','Peter','chennai',898889898,'2_3_22','29_5_23','sale'),
(101,'Bellstone','Luke','covai',44314134324,'4_1_23','29_5_23','sale'),
(102,'Pothys','John','trichy',365212525,'10_2_23','29_5_23','sale');

SELECT DISTINCT ID,shop_name,owner,Address,phone,shop_starting_from,shop_last_update,Last_update_reason from shop_list;







    