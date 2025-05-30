from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dummy user credentials
dummy_user = {'username': 'admin', 'password': 'admin'}

# Dummy audit records
audit_records = [
    {'date': '2025-04-12', 'user': 'Ramu', 'action': 'login', 'hash': 'abc123defg'},
    {'date': '2025-04-12', 'user': 'Sita', 'action': 'view_data', 'hash': 'def456ghij'},
    {'date': '2025-04-06', 'user': 'Ramu', 'action': 'logout', 'hash': 'ghi789jklm'},
    
    # New entries
    {'date': '2025-04-11', 'user': 'Ramu', 'action': 'edit_profile', 'hash': 'mno321qrst'},
    {'date': '2025-04-11', 'user': 'Sita', 'action': 'download_report', 'hash': 'uvw654xyza'},
    {'date': '2025-04-10', 'user': 'Lakshmi', 'action': 'login', 'hash': 'bcd987efgh'},
    {'date': '2025-04-10', 'user': 'Lakshmi', 'action': 'submit_form', 'hash': 'hij321klmn'},
    {'date': '2025-04-09', 'user': 'Krishna', 'action': 'logout', 'hash': 'rst654uvwx'},
    {'date': '2025-04-08', 'user': 'Ramu', 'action': 'upload_file', 'hash': 'opq123lmno'},
    {'date': '2025-04-07', 'user': 'Sita', 'action': 'change_password', 'hash': 'klm789stuv'}
]


# Allowed IPs and Locations (Expanded)
org_ip_range = [
    '192.168.1.1', '192.168.1.100', '192.168.1.101', '192.168.1.102',
    '192.168.2.1', '10.0.0.1', '10.0.0.2', '172.16.0.1'
]

org_locations = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Delhi',
    'Chennai', 'Pune', 'Kolkata', 'Ahmedabad'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == dummy_user['username'] and password == dummy_user['password']:
            session['user'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return render_template('logout.html')

@app.route('/auditform', methods=['GET', 'POST'])
def auditform():
    if request.method == 'POST':
        user = request.form.get('auditUser')
        action = request.form.get('auditAction')
        date = request.form.get('auditDate')
        if not user or not action or not date:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('auditform'))
        record_str = f"{user}{action}{date}{datetime.now()}"
        record_hash = hashlib.sha256(record_str.encode()).hexdigest()[:10]
        new_record = {
            'date': date,
            'user': user,
            'action': action,
            'hash': record_hash
        }
        audit_records.append(new_record)
        flash('Audit record added successfully!', 'success')
        return redirect(url_for('audit'))
    return render_template('auditform.html')

@app.route('/audit')
def audit():
    return render_template('auditrecords1.html', records=audit_records)

@app.route('/delete_audit/<hash>', methods=['POST'])
def delete_audit(hash):
    global audit_records
    initial_count = len(audit_records)
    audit_records = [r for r in audit_records if r['hash'] != hash]
    if len(audit_records) < initial_count:
        flash("Audit record deleted successfully.", "success")
    else:
        flash("Audit record not found.", "danger")
    return redirect(url_for('audit'))

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

        if not hash_input:
            hash_str = f"{user}{timestamp}{datetime.now()}"
            hash_generated = hashlib.sha256(hash_str.encode()).hexdigest()[:10]
        else:
            hash_generated = hash_input

        anomaly_reason = []

        # Future timestamp check
        try:
            user_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')
            if user_time > datetime.now():
                anomaly_reason.append("Future timestamp detected")
        except Exception:
            anomaly_reason.append("Invalid timestamp format")

        # Action mismatch
        if not any(r['user'] == user and r['action'] == action for r in audit_records):
            anomaly_reason.append(f"User '{user}' not authorized for action '{action}'")

        # IP check
        if ip_address not in org_ip_range:
            anomaly_reason.append("IP address is outside the organization range")

        # Location check
        if location not in org_locations:
            anomaly_reason.append("Unusual device location")

        # Status check
        if status.lower() == 'failed':
            anomaly_reason.append("Login status failed")

        prediction_result = "Anomaly Detected" if anomaly_reason else "No Anomaly Detected"

        # Add to audit log
        audit_records.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'user': user,
            'action': action,
            'hash': hash_generated
        })

        result = {
            'timestamp': timestamp,
            'user': user,
            'action': action,
            'status': status,
            'ip_address': ip_address,
            'location': location,
            'device': device,
            'hash': hash_generated,
            'prediction': prediction_result,
            'anomaly_reasons': anomaly_reason
        }

        return render_template('result1.html', result=result)

    return render_template('predictionform.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    flash("Signup functionality is not implemented.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
