from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "smart_parking_secret"

parking_lot = {"A1": False, "A2": True, "B1": True, "B2": False}  # True = Available, False = Occupied

@app.route('/')
def home():
    return render_template('index1.html')


@app.route('/login', methods=['POST'])
def redirect():
  user_id=request.form.get('user_id')
  pw=request.form.get('password')
  if user_id=="software" and  pw=="shrulep":
    return render_template('index.html', parking_lot=parking_lot)
    

  else:
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