from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import hashlib
import joblib
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Use environment variable for security
CORS(app)

# Initialize Blockchain (ensure blockchain_utils.py exists with Blockchain class)
from blockchain_utils import Blockchain

# Initialize the Blockchain object
blockchain = Blockchain()

# Load ML Model and Preprocessing Objects
model = joblib.load("model/anomaly_model.pkl")
label_encoders = joblib.load("model/label_encoders.pkl")
scaler = joblib.load("model/scaler.pkl")

# Dummy user credentials for login simulation
users = {'admin': generate_password_hash('password')}  # Store hashed password

# Store audit records (For demo purposes)
audit_records = []

def generate_hash(user, action):
    """Generate a unique hash using SHA-256 based on user and action."""
    hash_input = f"{user}{action}{datetime.utcnow()}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the username exists and if the password is correct
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user session
    flash('Logged out successfully.', 'success')  
    return render_template('logout.html')  # Show logout.html

@app.route('/auditform', methods=['GET', 'POST'])
def auditform():
    if request.method == 'POST':
        user = request.form.get('auditUser')
        action = request.form.get('auditAction')
        date = request.form.get('auditDate')
        if not user or not action or not date:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('auditform'))
        # Generate a short dummy hash for the record
        record_str = f"{user}{action}{date}{datetime.now()}"
        record_hash = hashlib.sha256(record_str.encode()).hexdigest()[:10]
        
        # Create a new blockchain block for this audit record
        block_data = f"{user}{action}{date}"
        previous_block = blockchain.get_previous_block()
        proof = blockchain.proof_of_work(previous_block['proof'])
        previous_hash = blockchain.hash(previous_block)
        blockchain.create_block(proof, previous_hash)  # Add the block to the blockchain
        
        new_record = {
            'date': date,
            'user': user,
            'action': action,
            'hash': record_hash
        }
        audit_records.append(new_record)
        flash('Audit record added successfully!', 'success')
        return redirect(url_for('audit'))
    return render_template('audit.html')

@app.route('/audit')
def audit():
    return render_template('auditrecords.html', records=audit_records)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        timestamp = request.form.get('Timestamp')
        user = request.form.get('user')
        action = request.form.get('Action')
        status = request.form.get('Status')
        ip_address = request.form.get('IP_Address')
        location = request.form.get('Location')
        device = request.form.get('Device')
        hash_input = request.form.get('Hash')
        
        # Generate hash if none provided
        if not hash_input:
            hash_str = f"{user}{timestamp}{datetime.now()}"
            hash_generated = hashlib.sha256(hash_str.encode()).hexdigest()[:10]
        else:
            hash_generated = hash_input
        
        # Dummy prediction logic: if status is 'Failed', flag an anomaly
        if status.lower() == 'failed':
            prediction_result = "Anomaly Detected"
        else:
            prediction_result = "No Anomaly Detected"
        
        result = {
            'timestamp': timestamp,
            'user': user,
            'action': action,
            'status': status,
            'ip_address': ip_address,
            'location': location,
            'device': device,
            'hash': hash_generated,
            'prediction': prediction_result
        }
        return render_template('result.html', result=result)
    return render_template('predictionform.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    flash("Signup functionality is not implemented.", "info")
    return redirect(url_for('login'))

if __name__== '__main__':
    app.run(debug=True)