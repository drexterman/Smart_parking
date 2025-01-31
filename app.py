
from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "smart_parking_secret"

# PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "software_eng1",
    "user": "postgres",
    #removed password for security purposes
    "password":"root",
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

    cur.execute("SELECT notified FROM waiting_queue WHERE user_id = %s;", (user_id,))
    queue_status = cur.fetchone()

    cur.close()
    conn.close()

    parking_lot = get_parking_data()

    if user:
        # Check if any slot is available
        if any(parking_lot.values()):
            flash(f"A parking slot is now available! Book it quickly.", "success")

        # If the user has been notified due to the queue
        if queue_status and queue_status[0]:
            flash(f"A slot has been reserved for you, {user_id}! Hurry up and book.", "success")

            # Remove the user from the queue
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM waiting_queue WHERE user_id = %s;", (user_id,))
            conn.commit()
            cur.close()
            conn.close()

        return render_template('index.html', parking_lot=parking_lot, user_id=user_id)
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

        # Notify the next user
        notify_next_user()

    cur.close()
    conn.close()

    parking_lot = get_parking_data()
    return render_template("index.html", parking_lot=parking_lot)

def notify_next_user():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get the first user in the queue
    cur.execute("SELECT user_id FROM waiting_queue ORDER BY id ASC LIMIT 1;")
    next_user = cur.fetchone()

    if next_user:
        # Mark them as notified
        cur.execute("UPDATE waiting_queue SET notified = TRUE WHERE user_id = %s;", (next_user[0],))
        conn.commit()

    cur.close()
    conn.close()

@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    user_id = request.form.get('user_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if user is already in the queue
    cur.execute("SELECT * FROM waiting_queue WHERE user_id = %s;", (user_id,))
    existing = cur.fetchone()

    if existing:
        flash("You are already in the waiting queue.", "info")
    else:
        cur.execute("INSERT INTO waiting_queue (user_id) VALUES (%s);", (user_id,))
        conn.commit()
        flash("You have been added to the waiting queue.", "info")

    cur.close()
    conn.close()
    
    parking_lot = get_parking_data()
    return render_template("index.html", parking_lot=parking_lot)

@app.route('/remove_from_queue', methods=['POST'])
def remove_from_queue():
    user_id = request.form.get('user_id')

    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the user is in the queue
    cur.execute("SELECT * FROM waiting_queue WHERE user_id = %s;", (user_id,))
    existing = cur.fetchone()

    if existing:
        # Remove user from the queue
        cur.execute("DELETE FROM waiting_queue WHERE user_id = %s;", (user_id,))
        conn.commit()
        flash("You have been removed from the waiting queue.", "info")
    else:
        flash("You are not in the waiting queue.", "info")

    cur.close()
    conn.close()

    # Update the parking lot data and render the page again
    parking_lot = get_parking_data()
    return render_template("index.html", parking_lot=parking_lot, user_id=user_id)

if __name__ == "__main__":
    app.run(debug=True)
