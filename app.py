# from flask import Flask, render_template, request, redirect, url_for, flash
# import pymysql

# app = Flask(__name__)
# app.secret_key = "smart_parking_secret"


# db= pymysql.connect(
#     host="localhost",
#     user="postgres",
#     password="Pakha@2578",
#     database="software_eng1"
# )
# cursor=db.cursor()


# DB_CONFIG = {
#     "dbname": "software_eng1",
#     "user": "postgres",
#     "password": "Pakha@2578",
#     "host": "localhost",
#     "port": "5432"
# }

# def get_parking_data():
#     """Fetch parking slots from database."""
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()
#     cur.execute("SELECT lot_name, status FROM parking_lots;")
#     parking_lot = {row[0]: row[1] == "Available" for row in cur.fetchall()}
#     cur.close()
#     conn.close()
#     return parking_lot



# @app.route('/')
# def home():
#     parking_lot = get_parking_data()
#     return render_template('index1.html')


# @app.route('/login', methods=['POST'])
# # def redirect():
# #   user_id=request.form.get('user_id')
# #   pw=request.form.get('password')
# #   if user_id=="software" and  pw=="shrulep":
# #     return render_template('index.html', parking_lot=parking_lot)
    

# #   else:
# #     return render_template('index1.html')
# def redirect():
#     user_id=request.form.get('user_id')
#     pw=request.form.get('password')

#     cursor.execute("select * FROM users WHERE name=%s and password=%s",(user_id,pw))

#     user=cursor.fetchone()

#     if user:
#         return render_template('index.html',parking_lot=parking_lot)
#     else:
#         flash("Invalid login credentials.","error")
#         return render_template('index1.html')

# @app.route('/signup',methods=['POST'])
# def signup():
#     user_id=request.form.get('new_user_id')
#     pw=request.form.get('new_password')

#     cursor.execute("SELECT * FROM users where name=%s",(user_id,))
#     user=cursor.fetchone()

#     if user:
#         flash("user already exits","error")
#         return render_template('index1.html')
#     else:
#         cursor.execute("INSERT INTO users (name,password) VALUES (%s,%s)",(user_id,pw))
#         db.commit()
#         flash("new user created susccessfully","sucess")
#         return render_template('index1.html')




  
# @app.route('/logout',methods=['POST'])
# def logout():
#     return render_template('index1.html')
  
# @app.route('/book', methods=['POST'])
# def book_slot():
#     slot = request.form.get('slot')
    
#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()
    
#     cur.execute("SELECT status FROM parking_lots WHERE lot_name = %s;", (slot,))
#     row = cur.fetchone()
#     if not row:
#         flash(f"Error: Slot '{slot}' does not exist.", 'error')
#     elif row[0] == "Occupied":
#         flash(f"Slot {slot} is already occupied. It can't be booked.", 'error')
#     else:
#         cur.execute("UPDATE parking_lots SET status = 'Occupied' WHERE lot_name = %s;", (slot,))
#         conn.commit()
#         flash(f"Slot {slot} successfully booked!", 'success')
#     parking_lot = get_parking_data()
#     cur.close()
#     conn.close()
    
#     return render_template("index.html", parking_lot=parking_lot)


# @app.route('/release', methods=['POST'])
# def release_slot():
#     slot = request.form.get('slot')

#     conn = psycopg2.connect(**DB_CONFIG)
#     cur = conn.cursor()

    
#     cur.execute("SELECT status FROM parking_lots WHERE lot_name = %s;", (slot,))
#     row = cur.fetchone()
    
#     if not row:
#         flash(f"Error: Slot '{slot}' does not exist.", 'error')
#     elif row[0] == "Available":
#         flash(f"Slot {slot} is already available.", 'info')
#     else:
#         cur.execute("UPDATE parking_lots SET status = 'Available' WHERE lot_name = %s;", (slot,))
#         conn.commit()
#         flash(f"Slot {slot} has been released.", 'success')
#     parking_lot = get_parking_data()
#     cur.close()
#     conn.close()
    
#     return render_template("index.html", parking_lot=parking_lot)
  
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "smart_parking_secret"

# PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "software_eng1",
    "user": "postgres",
    "password": "Pakha@2578",
    "host": "localhost",
    "port": "5432"
}

# Function to get database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Fetch parking slot data
def get_parking_data():
    """Fetch parking slots from database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT lot_name, status FROM parking_lots;")
    parking_lot = {row[0]: row[1] == "Available" for row in cur.fetchall()}
    cur.close()
    conn.close()
    return parking_lot

@app.route('/')
def home():
    parking_lot = get_parking_data()
    return render_template('index1.html', parking_lot=parking_lot)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    pw = request.form.get('password')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (user_id, pw))
    user = cur.fetchone()

    cur.close()
    conn.close()

    parking_lot = get_parking_data()

    if user:
        return render_template('index.html', parking_lot=parking_lot)
    else:
        flash("Invalid login credentials.", "error")
        return render_template('index1.html')

@app.route('/signup', methods=['POST'])
def signup():
    user_id = request.form.get('new_user_id')
    pw = request.form.get('new_password')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE name = %s", (user_id,))
    user = cur.fetchone()

    if user:
        flash("User already exists", "error")
    else:
        cur.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (user_id, pw))
        conn.commit()
        flash("New user created successfully", "success")

    cur.close()
    conn.close()

    return render_template('index1.html')

@app.route('/logout', methods=['POST'])
def logout():
    return render_template('index1.html')

@app.route('/book', methods=['POST'])
def book_slot():
    slot = request.form.get('slot')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT status FROM parking_lots WHERE lot_name = %s;", (slot,))
    row = cur.fetchone()

    if not row:
        flash(f"Error: Slot '{slot}' does not exist.", 'error')
    elif row[0] == "Occupied":
        flash(f"Slot {slot} is already occupied.", 'error')
    else:
        cur.execute("UPDATE parking_lots SET status = 'Occupied' WHERE lot_name = %s;", (slot,))
        conn.commit()
        flash(f"Slot {slot} successfully booked!", 'success')

    cur.close()
    conn.close()

    parking_lot = get_parking_data()
    return render_template("index.html", parking_lot=parking_lot)

@app.route('/release', methods=['POST'])
def release_slot():
    slot = request.form.get('slot')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT status FROM parking_lots WHERE lot_name = %s;", (slot,))
    row = cur.fetchone()

    if not row:
        flash(f"Error: Slot '{slot}' does not exist.", 'error')
    elif row[0] == "Available":
        flash(f"Slot {slot} is already available.", 'info')
    else:
        cur.execute("UPDATE parking_lots SET status = 'Available' WHERE lot_name = %s;", (slot,))
        conn.commit()
        flash(f"Slot {slot} has been released.", 'success')

    cur.close()
    conn.close()

    parking_lot = get_parking_data()
    return render_template("index.html", parking_lot=parking_lot)

if __name__ == "__main__":
    app.run(debug=True)
