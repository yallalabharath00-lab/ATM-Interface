from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for sessions

# In-memory data
user_balance = 1000.00
user_pin = None  # Will store the PIN after set

@app.route('/')
def index():
    return render_template('index.html', balance=user_balance, pin_set=(user_pin is not None))

@app.route('/set_pin', methods=['POST'])
def set_pin():
    global user_pin
    pin = request.form.get('pin')
    if not pin or len(pin) != 4 or not pin.isdigit():
        return jsonify({"success": False, "message": "PIN must be exactly 4 digits."})
    user_pin = pin
    session['authenticated'] = True
    return jsonify({"success": True, "message": "PIN set successfully!"})

@app.route('/authenticate_pin', methods=['POST'])
def authenticate_pin():
    pin = request.form.get('pin')
    if pin == user_pin:
        session['authenticated'] = True
        return jsonify({"success": True, "message": "PIN correct!"})
    else:
        return jsonify({"success": False, "message": "Incorrect PIN, please try again."})

@app.route('/deposit', methods=['POST'])
def deposit():
    global user_balance
    if not session.get('authenticated'):
        return jsonify({"success": False, "message": "Please authenticate PIN first."})

    amount = float(request.form.get('amount', 0))
    if amount <= 0:
        return jsonify({"success": False, "message": "Invalid deposit amount."})

    user_balance += amount
    session['authenticated'] = False  # Require re-auth for next transaction
    return jsonify({"success": True, "balance": user_balance, "message": "Deposit successful! Thank you for coming."})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    global user_balance
    if not session.get('authenticated'):
        return jsonify({"success": False, "message": "Please authenticate PIN first."})

    amount = float(request.form.get('amount', 0))
    if amount <= 0:
        return jsonify({"success": False, "message": "Invalid withdrawal amount."})
    if amount > user_balance:
        return jsonify({"success": False, "message": "Insufficient funds."})

    user_balance -= amount
    session['authenticated'] = False  # Require re-auth for next transaction
    return jsonify({"success": True, "balance": user_balance, "message": "Withdrawal successful! Thank you for coming."})

if __name__ == '__main__':
    app.run(debug=True)
