from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = "smart_parking_secret"

parking_lot = {"A1": False, "A2": True, "B1": True, "B2": False}  # True = Available, False = Occupied


#db connection
db= pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_parking"
)
cursor=db.cursor()

@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/login', methods=['POST'])
# def redirect():
#   user_id=request.form.get('user_id')
#   pw=request.form.get('password')
#   if user_id=="software" and  pw=="shrulep":
#     return render_template('index.html', parking_lot=parking_lot)
    

#   else:
#     return render_template('index1.html')
def redirect():
    user_id=request.form.get('user_id')
    pw=request.form.get('password')

    cursor.execute("select * FROM users WHERE name=%s and password=%s",(user_id,pw))

    user=cursor.fetchone()

    if user:
        return render_template('index.html',parking_lot=parking_lot)
    else:
        flash("Invalid login credentials.","error")
        return render_template('index1.html')

@app.route('/signup',methods=['POST'])
def signup():
    user_id=request.form.get('new_user_id')
    pw=request.form.get('new_password')

    cursor.execute("SELECT * FROM users where name=%s",(user_id,))
    user=cursor.fetchone()

    if user:
        flash("user already exits","error")
        return render_template('index1.html')
    else:
        cursor.execute("INSERT INTO users (name,password) VALUES (%s,%s)",(user_id,pw))
        db.commit()
        flash("new user created susccessfully","sucess")
        return render_template('index1.html')




  
@app.route('/logout',methods=['POST'])
def logout():
    return render_template('index1.html')
  
@app.route('/book', methods=['POST'])
def book_slot():
    slot = request.form.get('slot')
    if slot not in parking_lot:
        flash(f"Error: Slot '{slot}' does not exist.", 'error')
    elif not parking_lot[slot]:
        flash(f"Slot {slot} is already occupied. It can't be booked.", 'error')
    else:
        parking_lot[slot] = False
        flash(f"Slot {slot} successfully booked!", 'success')
   
    return render_template('index.html', parking_lot=parking_lot)

@app.route('/release', methods=['POST'])
def release_slot():
    slot = request.form.get('slot')
    if slot not in parking_lot:
        flash(f"Error: Slot '{slot}' does not exist.", 'error')
    elif parking_lot[slot]:
        flash(f"Slot {slot} is already available.", 'info')
    else:
        parking_lot[slot] = True
        flash(f"Slot {slot} has been released.", 'success')
    return render_template('index.html', parking_lot=parking_lot)
  
if __name__ == "__main__":
    app.run(debug=True)