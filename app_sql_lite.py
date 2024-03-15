from flask import Flask, redirect, url_for, request,render_template,session, flash,jsonify, make_response

import smtplib
import sqlite3
import binascii
import secrets
import string
from decimal import Decimal
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt
from codecs import open
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hinfo@123'
PASSWORD = 'Dhanu@123'
WAREHOUSE = 'COMPUTE_WH'
USER ='dhanu'
ACCOUNT ='LDWIECU-WK50439'
DATABASE ='IOT'
SCHEMA ='IOT'
# IOT_env\Scripts\activate.bat

sqlfile = 'table_list_of_iot_sql_lite.sql'
# connect = sqlite3.connect('database.db') 
# with sqlite3.connect('database.db') as connect:
#         cursor = connect.cursor()
# cursor = connect.cursor() 

def table_creation_sqllite(sql_file_name):
    with sqlite3.connect('database.db') as connect:
        cursor = connect.cursor()
        with open(sql_file_name, 'r') as file:
            queries = file.read()
        split_queries = queries.split('-')
        for query in split_queries:
            if query.strip():
                cursor.execute(query)
                # result = cursor.fetchall() 
    print("Table checking and creating process completed")
    

def testing_database():
    sql_insert = "INSERT INTO vendor(name, Email_id, Address, Telephone, Password) VALUES (?, ?, ?, ?, ?)"

    value = ('sethu', 'sethuraman542@gmail.com', "cmr", "12345","Sethu")
    name = 'sethu'
    email = 'sethuraman542@gmail.com'
    address = "cmr"
    phone = "12345"
    hashed_password = "Sethu"

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql_insert, (name, email, address, phone,hashed_password))
    connect.commit()
    connect.close()


    query = f"SELECT * FROM vendor WHERE Email_id = 'sethuraman542@gmail.com'"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(query)

    print("-----------result-----------------")
    results = cursor.fetchall()
    print("-----------result-----------------")
    connect.commit()
    connect.close()
    print(results)

table_creation_sqllite(sqlfile)

# testing_database()
@app.route('/')
@app.route('/<name>',methods=['GET','POST'])
def main(name=None):
    return render_template('main_page.html',session=session,text=name)

@app.route('/vendor',methods=['GET','POST'])
def index(name=None):
    return render_template('Homepage.html',session=session,text=name)

@app.route('/purchaser',methods=['GET','POST'])
def purchaser(name=None):
    return render_template('purchaser_login.html',session=session,text=name)

# @app.route('/dummy',methods=['GET','POST'])
# def dummy(name=None):
#     return render_template('dummy.html',session=session,text=name)

@app.route('/success/<name>',methods=['GET','POST'])
def success(name):
    return name

@app.route('/successfully',methods=['GET','POST'])
def successfully():
    return success

@app.route('/signuppage',methods=['GET','POST'])
def signuppage():
   return render_template('SignUp.html')

@app.route('/forgotpassword',methods=['GET','POST'])
@app.route('/forgotpassword/<name>')
def forgotpassword(name=None):
   return render_template('Forgot.html',text=name)

@app.route('/rfid_login',methods=['GET','POST'])

def rfid_login():
    if request.method == 'GET':
        rfid = int(request.json['num1'])
        query =("select * from token where ID = ?"% (rfid))
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(query)
        results = cursor.fetchall()


        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()

        if results:
            available = 1
            return f'{available}'
        else:
            available = 0
            return f'{available}'

@app.route('/purchaser_details',methods = ['POST', 'GET'])
def purchaser_details():
        query = ("select User_Rf_Id, User_Name, Email_id, User_Address, Telephone from purchaser_details")
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # curs = conns.cursor().execute(query)
        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()

        return render_template('purchaser_details.html',rows=results,)

@app.route("/create_purchaser", methods=['GET', 'POST'])
def create_purchaser():
    def generate_random_password():
        # Define the character set from which to generate the password
        characters = string.digits  # Use digits (0-9)

        # Generate a 6-digit random password
        password = ''.join(secrets.choice(characters) for _ in range(6))

        return password

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_rf_id = request.form['user_rf_id']
        address = request.form['address']
        phone = request.form['phone']
        password = generate_random_password()

        # Check any field is empty
        if not name or not email or not address or not phone:
            flash('Please fill out all required fields', 'error')
        else:
            # Check if email already exists
            check_sql = "SELECT * FROM purchaser_details WHERE Email_id = ?"
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            cursor.execute(check_sql)
            existing_customer = cursor.fetchall()
            
            # curs = conns.cursor()
            # curs.execute(check_sql, (email,))
            # existing_customer = curs.fetchone()

            if existing_customer:
                flash('Provided email already exists', 'error')
            else:
                sql = "INSERT INTO purchaser_details(User_Name, Email_id,User_Rf_Id, User_Address, Telephone, Password) VALUES (?, ?, ?, ?, ?, ?)"
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                value = (name, email, user_rf_id, address, phone,hashed_password)
                connect = sqlite3.connect('database.db')
                cursor = connect.cursor()
                cursor.execute(sql, value)
                
                # curs.execute(sql, value)
                # conns.commit()
                flash('purchaser added successfully', 'success')
                # Call the send_email function to send an email to the newly created vendor
                sender_email = 'hinfo123456@gmail.com'
                sender_password = 'kpfg emev ekjg zmus'
                recipient_email = email
                subject = 'Welcome to our platform'
                message = f"Dear {name},\n\n"
                message += "Your purchaser account has been created with the following credentials:\n"
                message += f"Email: {email}\n"
                message += f"Password: {password}\n\n"
                message += "Please keep your password secure.\n\n"
                message += "Thank you for joining as a purchaser.\n"
                send_email(sender_email, sender_password, recipient_email, subject, message)

                return redirect(url_for("purchaser_details"))
    return render_template("create_purchaser.html")

@app.route('/edit_purchaser/<string:id>',methods = ['POST','GET'])
def edit_purchaser(id):
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        task = "update purchaser_details set User_Name = ?, Email_id = ?,User_Address = ?,Telephone = ? WHERE User_Rf_Id = ?"
        value = (name,email,address,phone,id)
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(task,value)
        
        # curs=conns.cursor()
        # curs = conns.cursor().execute(task,value)
        flash('customer updated successfully','success')
        return redirect (url_for('purchaser_details'))

    if request.method=='GET':
        sql="select * from purchaser_details where User_Rf_Id= ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(sql,[id])
        results = cursor.fetchall()

        
        # curs=conns.cursor()
        # curs = conns.cursor().execute(sql,[id])
        # results = curs.fetchone()
        print("---------------test-----------")
        print(results)
        return render_template("edit_purchaser.html", results = results)


@app.route('/activate_purchaser/<string:id>',methods = ['POST','GET'])
def activate_purchaser(id):
    sql="update purchaser_details set Status = 'True' WHERE User_Rf_Id = ?"
    connect = sqlite3.connect('database.db')

    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("purchaser_details"))

@app.route('/deactivate_purchaser/<string:id>',methods = ['POST','GET'])
def deactivate_purchaser(id):
    sql="update purchaser_details set Status = 'False' WHERE User_Rf_Id = ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("purchaser_details"))


@app.route('/delete_purchaser/<string:id>',methods = ['POST', 'GET'])
def delete_purchaser(id):
    sql="delete from purchaser_details where User_Rf_Id=?"
    connect = sqlite3.connect('database.db')

    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    flash('customer deleted successfully','success')
    return redirect(url_for("purchaser_details"))

@app.route('/purchaser_dashboard', methods=['GET', 'POST'])
def purchaser_dashboard():
    if request.method == 'POST':
        purchase_email = request.form['purchase_email']
        pwd1 = request.form['Password']

        if not purchase_email or not pwd1:
            flash("Any of the fields cannot be left blank", 'error')
            return redirect(url_for('purchaser'))

        query = "SELECT * FROM purchaser_details WHERE Email_id = ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(query, (purchase_email))
        result = cursor.fetchall()

        # curs = conns.cursor().execute(query, (purchase_email))
        # result = curs.fetchone()

        if result:
            # Check if the password matches the stored hashed password
            stored_hashed_password = result[8]  # Assuming password is in the 8th index column
            if bcrypt.checkpw(pwd1.encode('utf-8'), bytes(stored_hashed_password)):
                # Password matches, user authenticated
                return render_template('purchaser_dashboard.html')
            else:
                flash("Password is incorrect!", 'error')
        else:
            flash("Usermail/Password is incorrect!", 'error')

    return render_template('purchaser_login.html')



@app.route('/purchasing_list',methods = ['POST', 'GET'])
def purchasing_list():
    sql="select * from purchasing_list"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql)
    # results = curs.fetchall()
    print(results)
    mytuple = sorted(results)
    return render_template("purchasing_list.html", rows = mytuple)

@app.route('/purchasing_order',methods = ['POST', 'GET'])
def purchasing_order():
    sql="select * from product"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql)
    # results = curs.fetchall()
    print(results)
    mytuple = sorted(results)
    return render_template("purchasing_order.html", rows = mytuple)


@app.route('/purchaser_view/<string:id>',methods = ['POST', 'GET'])
def purchaser_view(id):
    sql="select * from purchasing_list WHERE ID= ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    # results = curs.fetchall()
    print(results)
    return render_template("purchaser_view.html", rows=results)


@app.route('/vendor_dashboard', methods=['GET', 'POST'])
def vendor_dashboard():
    if request.method == 'POST':
        user_mail = request.form['UserMail']
        pwd1 = request.form['Password']

        if not user_mail or not pwd1:
            flash("Any of the fields cannot be left blank", 'error')
            return redirect(url_for('admin'))

        
        query = f"SELECT * FROM vendor WHERE Email_id = '{user_mail}'"
        print(query)
        connect = sqlite3.connect('database.db')

        cursor = connect.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        print("-----------testing---------------------")
        print(result)
        print("-----------testing---------------------")


        # curs = conns.cursor().execute(query, (user_mail))
        # result = curs.fetchone()
        if result:
            # Check if the password matches the stored hashed password
            stored_hashed_password = result[3]  # Assuming password is in the 4th index
            print("----------------------------------------")
            print(stored_hashed_password)
            print("----------------------------------------")

            # if bcrypt.checkpw(pwd1.encode('utf-8'), bytes(stored_hashed_password)):
            if stored_hashed_password:

                # Password matches, user authenticated
                return render_template('index.html')
            else:
                flash("Password is incorrect!", 'error')
        else:
            flash("Usermail/Password is incorrect!", 'error')

    return render_template('Homepage.html')


@app.route('/purchasersignup', methods=['GET', 'POST'])
def purchasersignup():
    return render_template('Purchaser_signup.html')

@app.route('/updateproducts', methods=['GET', 'POST'])
def updateproducts():
    id=request.form.get('ID')
    product_name=request.form.get('NAME')
    product_price=request.form.get('PRICE')
    prd_qty=request.form.get('QUANTITY')
    task = (id, product_name, product_price, prd_qty)
    sql = "update GradeTable set MidTerm1 = ?, MidTerm2 = ?, MidTerm3 = ?, FinalGrade = ? where SID = ? and FID = ? and CourseId = ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    a = result.rowcount
   
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql)
    # a = curs.rowcount

    if a == 0:
        return 'no update happen'
    else:
        sql =("")
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(sql)
        
        # curs=conns.cursor()
        # curs = conns.cursor().execute(sql)
        return render_template('product_update.html')


@app.route('/callhtml/<a>/<b>/<c>/<d>/<e>' , methods=['GET', 'POST'])
def callhtml(a,b,c,d,e):
    return render_template('update.html',a=a,b=b,c=c,d=d,e=e)


@app.route('/clear')
def clearsession():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))

@app.route('/clear_purchaser')
def clearsession_purchaser():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('purchaser'))

@app.route('/clear_admin')
def clearsession_admin():
    # Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('admin'))


@app.route('/signup', methods=['GET', 'POST'])

def signup():

    # Connecting to the database file
    # curs=conns.cursor()
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()


    name = request.form['Name']
    action = request.form.get('action', '')
    user1 = request.form['UserName']
    user=user1
    email = request.form['email']

    # validate if all fields are entered
    if not action:
        error = "Any of the fields cannot be left blank"
        return redirect(url_for('success', name=error))

    if action == 'Add':
        if not action or not user or not email or not name:
            error = "Any of the fields cannot be left blank"
            return redirect(url_for('success', name=error))

        query =("select * from purchaser_details where ID = ?"% (user1))

        cursor.execute(query)
        results = cursor.fetchall()

        # curs = conns.cursor().execute(query)
        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()

        if results:
            msg = "User already exists"
        else:
            cursor.execute("INSERT INTO purchaser_details(ID, User_Name,Email_id) ""VALUES(?, ?, ?)", (user,name,email))
            # curs.execute("INSERT INTO purchaser_details(ID, User_Name,Email_id) ""VALUES(?, ?, ?)", (user,name,email))
            msg = "User has been registered successfully"

        return redirect(url_for('success', name=msg))
    elif action == 'Remove':
        if not user:
            error = "Enter user and name fields cannot be left blank"
            return redirect(url_for('success', name=error))
        query =("select * from purchaser_details where ID = ?"% (user1))
        
        cursor.execute(query)
        results = cursor.fetchall()

        # curs = conns.cursor().execute(query)
        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()

        if results:
            cursor.execute("DELETE FROM purchaser_details where ID = ?"%(user))
            # curs.execute("DELETE FROM purchaser_details where ID = ?"%(user))
            msg = "User has been removed successfully"
        else:
            msg = "User doesn't exists"
        return redirect(url_for('success', name=msg))

@app.route('/admin',methods=['GET','POST'])
def admin(name=None):
    return render_template('admin_login.html',session=session,text=name)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        user_name = request.form['UserName']
        pwd1 = request.form['Password']

        if not user_name or not pwd1:
            flash("Any of the fields cannot be left blank", 'error')
            return redirect(url_for('admin'))

        user_name_hashed = user_name
        pwd_hashed = pwd1
        query = "SELECT * FROM admin WHERE user_name = ? AND password = ?"
        connect = sqlite3.connect('database.db')
        
        cursor = connect.cursor()
        cursor.execute(query, (user_name_hashed, pwd_hashed))
        results = cursor.fetchall()

        # curs = conns.cursor().execute(query, (user_name_hashed, pwd_hashed))
        # results = curs.fetchall()

        if results:
            return render_template('admin_dashboard.html')
        else:
            flash("Username/Password is incorrect!", 'error')

    return render_template('admin_login.html')

@app.route('/shop_list',methods = ['POST', 'GET'])
def shop_list():
    query = ("select * from shop_list")
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # curs = conns.cursor().execute(query)
    # query_id = curs.sfqid
    # curs.get_results_from_sfqid(query_id)
    # results = curs.fetchall()

    mytuple = sorted(results)
    print(results)
    return render_template('shop_list.html',rows=mytuple)

@app.route('/shop_view/<string:id>',methods = ['POST', 'GET'])
def shop_view(id):
    sql="select * from shop_list WHERE ID= ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()

    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    # results = curs.fetchall()
    print(results)
    return render_template("shop_view.html", rows=results)

@app.route('/activate_shop/<string:id>',methods = ['POST','GET'])
def activate_shop(id):
    sql="update shop_list set Status = 'True' WHERE ID = ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])

    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("shop_view"))

@app.route('/deactivate_shop/<string:id>',methods = ['POST','GET'])
def deactivate_shop(id):
    sql="update shop_list set Status = 'False' WHERE ID = ?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])

    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    return redirect(url_for("shop_view"))


@app.route('/delete_shop/<string:id>',methods = ['POST', 'GET'])
def delete_shop(id):
    sql="delete from shop_list where ID=?"
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    connect = sqlite3.connect('database.db')

    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    flash('customer deleted successfully','success')
    return redirect(url_for("shop_list"))

@app.route('/adminsignup',methods=['GET','POST'])
def adminsignup():
   return render_template('admin_signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('Homepage'))  # Redirect to the home page

@app.route('/get_data')
def get_data():
    # curs = conns.cursor()
    # curs.execute("SELECT COUNT(*) FROM purchaser_details")
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT COUNT(*) FROM purchaser_details")
    num_purchasers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM product")
    num_products = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(AVAILABLE_QTY) FROM product")
    total_quantity = cursor.fetchone()[0]


    cursor.close()

    data = {
        'num_purchasers': num_purchasers,
        'num_products':num_products,
        'total_quantity': total_quantity,
    }
    print(num_purchasers)
    print(total_quantity)
    return jsonify(data)

@app.route('/product_details',methods = ['POST', 'GET'])
def product_details():
        query = ("select id, Rf_reader,product_name,available_qty,price from product")
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # curs = conns.cursor().execute(query)
        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()

        mytuple = sorted(results)
        print(results)
        return render_template('product_details.html',rows=mytuple)


@app.route('/edit_product/<int:id>', methods=['POST', 'GET'])
def edit_product(id):
    if request.method == 'POST':
        productname = request.form['product_name']
        available_qty = request.form['available_qty']
        price = request.form['price']
        # Add other product attributes as needed
        task = "UPDATE product SET product_name = ?, available_qty = ?, price = ? WHERE id = ?"
        value = (productname, available_qty, price, id)
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(task, value)


        # curs = conns.cursor()
        # curs.execute(task, value)
        # conns.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('product_details'))

    if request.method == 'GET':
        sql = "SELECT * FROM product WHERE id = ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(sql, [id])
        results = cursor.fetchall()
        
        # curs = conns.cursor()
        # curs.execute(sql, [id])
        # results = curs.fetchone()
        print("---------------test-----------")
        print(results)
        return render_template("edit_product.html", results=results)

@app.route('/delete_product/<string:id>',methods = ['POST', 'GET'])
def delete_product(id):
    sql="delete from product where id=?"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql,[id])
    results = cursor.fetchall()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    flash('Product deleted successfully','success')
    return redirect(url_for("product_details"))

@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        rf_reader_id = request.form['rf_reader_id']
        available_qty = request.form['available_qty']
        price = request.form['price']

        task = "INSERT INTO product (product_name, Rf_reader, available_qty, price) VALUES (?, ?, ?, ?)"
        values = (product_name,rf_reader_id, available_qty, price)
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(task, values)
        results = cursor.fetchall()

        # curs = conns.cursor()
        # curs.execute(task, values)
        # conns.commit()


        response = {'status': 'success'}
        print(product_name,available_qty,price)
        return jsonify(response), 200, {'Cache-Control': 'no-store, no-cache, must-revalidate'}

    return render_template("add_product.html")

@app.route('/bill')
def bill():
    cart_items = []
    if 'cart' in session:
        for product_id in session['cart']:
            product = Product.query.get(product_id)
            if product:
                cart_items.append(product)
    return render_template('bill.html', cart_items=cart_items)

@app.route('/purchaser_cart', methods=['GET', 'POST'])
def add_cart():
    return render_template('Purchaser_add_to_cart.html')

#------------------------------------------------purchase_transaction------------
@app.route('/purchase', methods=['POST', 'GET'])
def purchase():
    if request.headers['Content-Type'] == 'application/json':
        # If the request contains JSON data
        data = request.get_json()
        user_rfid = data.get('Rf_id')
        product_id = data.get('Rf_reader')
    else:
        user_rfid = request.form['Rf_id']
        product_id = request.form['Rf_reader']

    if not user_rfid or not product_id:
        flash('Please fill in all the details.', 'error')
        return redirect(url_for('add_cart'))

    # Check  user RFID is valid
    # curs = conns.cursor()
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    # curs.execute("SELECT * FROM purchaser_details WHERE User_Rf_Id = %s", (user_rfid))
    # purchaser_details = curs.fetchone()

    cursor.execute("SELECT * FROM purchaser_details WHERE User_Rf_Id = ?", (user_rfid))
    purchaser_details = cursor.fetchone()


    if purchaser_details:
        # Check  the product exists and has available quantity
        cursor.execute("SELECT * FROM product WHERE Rf_reader = ?", (product_id))
        product_data = cursor.fetchone()

        if product_data:
            available_qty = product_data[3]  # column index 3  for available_qty in product table

            if available_qty > 0:
                product_price = product_data[4]  # column index 4 is for price in product table
                # Convert the product price to a decimal
                product_price_decimal = Decimal(str(product_price))

                 # column index 2 for account_balance in purchaser_details table
                if purchaser_details[2] >= product_price:
                    # Update user balance in the purchaser_details table
                    new_balance = purchaser_details[2] - product_price_decimal
                    cursor.execute("UPDATE purchaser_details SET account_balance = ? WHERE User_Rf_Id = ?", (new_balance, user_rfid))

                    # Update the available quantity in the product table
                    new_available_qty = available_qty - 1
                    cursor.execute("UPDATE product SET available_qty = ? WHERE Rf_reader = ?", (new_available_qty, product_id))

                    flash('Product purchased successfully!', 'success')
                    print(f"user_rfid: {user_rfid}")
                    print(f"product_price: {product_price}")
                    print(f"new_balance: {new_balance}")
                    if request.headers['Content-Type'] == 'application/json':
                        return make_response(jsonify({"status": "purchased_success"}), 200)
                else:
                    flash('Insufficient balance to purchase the product.', 'error')
                    return make_response(jsonify({"status": "Insufficient_balance"}), 200)
            else:
                flash('Product is out of stock.', 'error')
                return make_response(jsonify({"status": "Product_out_of_stock"}), 200)
        else:
            flash('Invalid RFID_Reader.', 'error')
    else:
        flash('Invalid user RFID.', 'error')
        return redirect(url_for('add_cart'))

    return render_template('purchaser_add_to_cart.html')

@app.route('/all_stock_data')
def all_stock_data():
    try:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()

        cursor.execute("SELECT Rf_reader, product_name, available_qty FROM product WHERE available_qty = 0")
        out_of_stock_products = cursor.fetchall()

        cursor.execute("SELECT Rf_reader, product_name, available_qty FROM product WHERE available_qty <= 5 AND available_qty > 0")
        soon_out_of_stock_products = cursor.fetchall()

        # Convert the results to a list of dictionaries
        out_of_stock_products_data = [{'rfid': row[0], 'product_name': row[1],'quantity':row[2]} for row in out_of_stock_products]
        soon_out_of_stock_products_data = [{'rfid': row[0], 'product_name': row[1],'quantity':row[2]} for row in soon_out_of_stock_products]


        all_stock_data = {
            'out_of_stock_products': out_of_stock_products_data,
            'soon_out_of_stock_products': soon_out_of_stock_products_data
        }

        return jsonify(all_stock_data)
    except Exception as e:
        return jsonify({"error": str(e)})

def send_email(sender_email, sender_password, recipient_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Email could not be sent. Error: " + str(e))


@app.route("/create_vendor", methods=['GET', 'POST'])
def create_vendor():
    def generate_random_password():
        # Define the character set from which to generate the password
        characters = string.digits  # Use digits (0-9)

        # Generate a 6-digit random password
        # password = ''.join(secrets.choice(characters) for _ in range(6))
        password = 'Sethu'

        return password

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password = generate_random_password()

        # Check any field is empty
        if not name or not email or not address or not phone:
            flash('Please fill out all required fields', 'error')
        else:
            # Check if email already exists
            # curs = conns.cursor()
            connect = sqlite3.connect('database.db')
            cursor = connect.cursor()
            check_sql = "SELECT * FROM vendor WHERE Email_id = ?"
            cursor.execute(check_sql, (email,))
            existing_customer = cursor.fetchone()

            if existing_customer:
                flash('Provided email already exists', 'error')
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                sql = "INSERT INTO vendor(name, Email_id, Address, Telephone, Password) VALUES (?, ?, ?, ?, ?)"

                value = (name, email, address, phone,hashed_password)
                
                connect = sqlite3.connect('database.db')
                cursor = connect.cursor()
                cursor.execute(sql, (name, email, address, phone,hashed_password))
                connect.commit()
                connect.close()

                flash('vendor added successfully', 'success')
                # Call the send_email function to send an email to the newly created vendor
                sender_email = 'hinfo123456@gmail.com'
                sender_password = 'kpfg emev ekjg zmus'
                recipient_email = email
                subject = 'Welcome to our platform'
                message = f"Dear {name},\n\n"
                message += "Your vendor account has been created with the following credentials:\n"
                message += f"Email: {email}\n"
                message += f"Password: {password}\n\n"
                message += "Please keep your password secure.\n\n"
                message += "Thank you for joining as a vendor.\n"
                send_email(sender_email, sender_password, recipient_email, subject, message)

                return redirect(url_for("vendor_details"))
    return render_template("create_vendor.html")


@app.route('/vendor_details',methods = ['POST', 'GET'])
def vendor_details():
        query = ("select * from vendor")
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # query_id = curs.sfqid
        # curs.get_results_from_sfqid(query_id)
        # results = curs.fetchall()
        return render_template('vendor_details.html',rows=results,)

@app.route('/edit_vendor/<string:id>',methods = ['POST','GET'])
def edit_vendor(id):
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        # id = int(id)
        print("---------------test-----------")
        print(email)
        print("---------------test-----------")
        task = "UPDATE vendor SET name = ?, Email_id = ?,Address = ?,Telephone = ? WHERE Vendor_ID = ?;"
        value = (name,email,address,phone,id)
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(task,value)
        results = cursor.fetchall()
        
        # curs=conns.cursor()
        # curs = conns.cursor().execute(task,value)
        flash('vendor updated successfully','success')
        return redirect (url_for('vendor_details'))

    if request.method=='GET':
        sql="select * from vendor where Vendor_ID= ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(sql,[id])
        results = cursor.fetchone()
        
        # curs = conns.cursor().execute(sql,[id])
        # curs=conns.cursor()
        # results = curs.fetchone()
        print(results)
        return render_template("edit_vendor.html", results = results)

@app.route('/delete_vendor/<string:id>',methods = ['POST', 'GET'])
def delete_vendor(id):
    print("---------------test-----------")
    print(id)
    print("---------------test-----------")

    sql=f"delete from vendor where Vendor_ID={id}"
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(sql)
    results = cursor.fetchone()
    
    # curs=conns.cursor()
    # curs = conns.cursor().execute(sql,[id])
    flash('vendor deleted successfully','success')
    return redirect(url_for("vendor_details"))

@app.route('/reset_password', methods=['GET', 'POST'])

def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        source = request.args.get('source')
        check_vendor_sql = "SELECT * FROM vendor WHERE Email_id = ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(check_vendor_sql, (email,))
        vendor = cursor.fetchone()
        
        # curs = conns.cursor()
        # curs.execute(check_vendor_sql, (email,))
        # vendor = curs.fetchone()

        check_customer_sql = "SELECT * FROM purchaser_details WHERE Email_id = ?"
        cursor.execute(check_vendor_sql, (email,))
        customer = cursor.fetchone()


        # curs.execute(check_customer_sql, (email,))
        # customer = curs.fetchone()

        if source == 'vendor' and vendor :
            reset_token = secrets.token_urlsafe(20)
            expiration_timestamp = datetime.now() + timedelta(hours=1)


            # Store the reset token and expiration timestamp in the reset_tokens table
            insert_reset_token_sql = "INSERT INTO reset_tokens (email_id, token, expiration) VALUES (?, ?, ?)"
            
            cursor.execute(insert_reset_token_sql, (email, reset_token, expiration_timestamp))
            
            # curs.execute(insert_reset_token_sql, (email, reset_token, expiration_timestamp))
            # conns.commit()

            # Send an email to the user with the reset token
            send_reset_email(email, reset_token)

            flash('A password reset email has been sent to your email address', 'success')
            print("check the mail:{email}")
            return redirect(url_for('main'))

        elif source == 'customer' and customer :
            reset_token = secrets.token_urlsafe(20)
            expiration_timestamp = datetime.now() + timedelta(hours=1)

            print(f"email: {email}, reset_token: {reset_token}, expiration_timestamp: {expiration_timestamp}")

            # Store token datas in reset_tokens table
            insert_reset_token_sql = "INSERT INTO reset_tokens (email_id, token, expiration) VALUES (?, ?, ?)"
            
            cursor.execute(insert_reset_token_sql, (email, reset_token, expiration_timestamp))
            
            # curs.execute(insert_reset_token_sql, (email, reset_token, expiration_timestamp))
            # conns.commit()

            # Send an email to the user with the reset token
            send_reset_email(email, reset_token)

            flash('A password reset email has been sent to your email address', 'success')
            print("check the mail:{email}")
            return redirect(url_for('main'))
        else:
            flash('Email not found', 'error')

    return render_template('reset_password.html')


@app.route('/reset_password/<reset_token>', methods=['GET', 'POST'])
def reset_password_token(reset_token):
    if request.method == 'POST':
        new_password = request.form['new_password']

        check_reset_token_sql = "SELECT email_id, expiration FROM reset_tokens WHERE token = ?"
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute(check_reset_token_sql, (reset_token,))
        result = cursor.fetchone()
        
        # curs = conns.cursor()
        # curs.execute(check_reset_token_sql, (reset_token,))
        # result = curs.fetchone()
        print(new_password)
        if result:
            email, expiration_timestamp = result[0], result[1]
            now = datetime.now()

            if now <= expiration_timestamp:
                # Check if the email exists in the vendor or customer table
                check_vendor_sql = "SELECT * FROM vendor WHERE Email_id = ?"
                connect = sqlite3.connect('database.db')

                cursor = connect.cursor()
                cursor.execute(check_vendor_sql, (email,))
                vendor = cursor.fetchone()
                
                # curs.execute(check_vendor_sql, (email,))
                # vendor = curs.fetchone()

                check_customer_sql = "SELECT * FROM purchaser_details WHERE Email_id = ?"
                connect = sqlite3.connect('database.db')
                cursor = connect.cursor()
                cursor.execute(check_customer_sql, (email,))
                customer = cursor.fetchone()

                # curs.execute(check_customer_sql, (email,))
                # customer = curs.fetchone()
                print("vendor:{vendor}, customer:{customer}")
                if vendor:
                    vendor_id = vendor[0]
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    # Update the password in the vendor table
                    update_vendor_password_sql = "UPDATE vendor SET Password = ? WHERE Vendor_ID = ?"
                    cursor.execute(update_vendor_password_sql, (hashed_password, vendor_id))
                    # curs.execute(update_vendor_password_sql, (hashed_password, vendor_id))


                if customer:
                    rfid = customer[0]
                    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                    # Update the password in the customer table
                    update_customer_password_sql = "UPDATE purchaser_details SET Password = ? WHERE User_Rf_Id = ?"
                    cursor.execute(update_customer_password_sql, (hashed_password, rfid))
                    
                    # curs.execute(update_customer_password_sql, (hashed_password, rfid))

                # Delete the reset token
                delete_reset_token_sql = "DELETE FROM reset_tokens WHERE token = ?"
                cursor.execute(delete_reset_token_sql, (reset_token))

                # curs.execute(delete_reset_token_sql, (reset_token))

                flash('Password reset successful. You can now log in with your new password.', 'success')
                return redirect(url_for('main'))
            else:
                flash('Reset token has expired', 'error')
        else:
            flash('Invalid reset token', 'error')

    return render_template('reset_password_confirm.html', token=reset_token)


def send_reset_email(recipient_email, reset_token):
    sender_email = 'hinfo123456@gmail.com'
    sender_password = 'kpfg emev ekjg zmus'

    subject = 'Password Reset Request'
    message = f'You have requested a password reset.\n To reset your password, <a href="{request.url_root}reset_password/{reset_token}">Click here</a>.<br><br>'
    message += 'If you not request this password reset, please ignore this email.'

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    html_message = MIMEText(message, 'html')
    msg.attach(html_message)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f'Failed to send email: {str(e)}')

# @app.route("/reset_password", methods=['GET'])
# def reset_password():
#     email = request.args.get('email')
#     print(email)
#     return render_template('reset_password.html', email=email)

# @app.route("/reset_password", methods=['POST', 'GET'])
# def reset_password():
#     if request.method == 'GET':
#         email = request.args.get('email_id')
#         curs=conns.cursor()
#         sql=("select * from vendor where email_id = '%s' "%(email))
#         print("------------testingstart-----------")
#         print(sql)
#         print("------------testingend-----------")
#         curs = conns.cursor().execute(sql)
#         results = curs.fetchone()
#         print("------------testingstart-----------")
#         print(results)
#         print("------------testingend-----------")
#         return render_template('reset_password.html', email=email)


# @app.route('/resetpass', methods=['POST', 'GET'])
# def resetpass():
#     if request.method == 'POST':
#         mail = request.form['email']
#         passw = request.form['new_password']
#         # Hash the new password
#         hashed_password = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())

#         # Check if the email exists in the database
#         cursor = conns.cursor()
#         cursor.execute("SELECT * FROM vendor WHERE email_id = %s", (mail,))
#         result = cursor.fetchone()

#         if result:
#             # Update the password in the database
#             cursor.execute("UPDATE vendor SET password = %s WHERE email_id = %s", (hashed_password, mail))
#             conns.commit()
#             return render_template('reset_password.html', success="Password reset successful!")
#         else:
#             error = "Email is incorrect or does not exist."
#             return redirect(url_for('reset_password', error=error))

#     return render_template('reset_password.html')

    # print("------------testingstart-----------")
    # print(request.method)
    # print("------------testingend-----------")
    # curs=conns.cursor()
    # sql=("select * from vendor where shopname = '%s' "%(shopname))
    # print("------------testingstart-----------")
    # print(sql)
    # print("------------testingend-----------")
    # curs = conns.cursor().execute(sql)
    # results = curs.fetchone()
    # user=results['shopname']
    # user1=session['shopname']
    # if user == user1:
    #     return render_template('reset_password.html', results=results)
    # else:
    #     return redirect('/')
    # if request.method=='GET':
    #     print("------------testingstart-----------")
    #     print(request.method)
    #     print("------------testingend-----------")
    #     mail = request.form['email']
    #     print(mail)
    #     query = ("select email_id from vendor where shopname = '%s'"%(mail))
    #     curs = conns.cursor().execute(query)
    #     query_id = curs.sfqid
    #     curs.get_results_from_sfqid(query_id)
    #     results = curs.fetchone()
    #     print(results)
    #     return render_template('reset_password.html', results=results)


if __name__ == '__main__':
    app.run(use_reloader=True)
