import sqlite3
connection = sqlite3.connect('database.db')

def init_db():
    db = get_db()
    with current_app.open_resource("demo.sql") as f:
        db.executescript(f.read().decode("utf-8"))

cursor = connection.cursor()

cursor.execute('''CREATE TABLE Items
        (ID INT    NOT NULL,
        user_name    TEXT    NOT NULL,
        first_name   TEXT    NOT NULL,
        last_name   TEXT    NOT NULL, 
        telephone int NOT NULL);''')

connection.commit()
connection.close()