#Sih1291

import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time 


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'bramharoopasaraswati108'

# Function to create SQLite database and tables
def create_tables():
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reported_problems 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT, landmark TEXT, 
                 location_description TEXT, issue_image TEXT, issue_description TEXT, 
                 email TEXT, date TEXT, lat REAL, lng REAL, assigned_to TEXT, status TEXT)''')  # Add lat and lng columns
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (employee_id TEXT PRIMARY KEY, password TEXT, role TEXT,
                 email TEXT, mobile_no TEXT, tasks_reviewed INTEGER DEFAULT 0,
                 tasks_completed INTEGER DEFAULT 0)''')  # Add employee table
    # c.execute("INSERT INTO employees VALUES ('manager1', 'password', 'Manager', 'manager1@example.com', '9380142763', 0, 0)")
    # c.execute("INSERT INTO employees VALUES ('inspector1', 'password', 'Water Inspector', 'inspector1@example.com', '9113518404', 0, 0)")
    
    conn.commit()
    conn.close()


# Create SQLite database and tables
create_tables()

@app.route('/')
def index():
    """Render the index page."""
    # Fetch top 5 reported problems from the SQLite database
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reported_problems ORDER BY id DESC LIMIT 5")
    top_problems = c.fetchall()
    conn.close()
    return render_template('index.html', top_problems=top_problems)


# Function to send confirmation email
def send_confirmation_email(email):
    sender_email = 'contact.dkulkarni@gmail.com'  # Update with your email address
    sender_password = 'Sujay&nidhiR1'  # Update with your email password
    subject = 'Confirmation: Water Issue Report Received'
    message = 'Thank you for reporting the water issue. We have received your report and will work on resolving it as soon as possible.'

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("Confirmation email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

# Function to handle login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        password = request.form['password']
        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE employee_id = ? AND password = ?", (employee_id, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['employee_id'] = employee_id
            session['role'] = user[2]  # Store role in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# Function to handle logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Function to render dashboard based on role
@app.route('/dashboard')
def dashboard():
    if 'employee_id' in session:
        if session['role'] == 'Manager':
            return render_template('manager_dashboard.html')
        elif session['role'] == 'Water Inspector':
            return render_template('inspector_dashboard.html')
    flash('Please log in to access this page', 'error')
    return redirect(url_for('login'))

# Function to submit a reported issue
@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    if request.method == 'POST':
        # Retrieve form data
        location = request.form.get('location')
        landmark = request.form.get('landmark')
        location_description = request.form.get('location_description')
        issue_image = request.files.get('issue_image')

        # Save the image if uploaded
        if issue_image:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], issue_image.filename)
            issue_image.save(image_filename)
        else:
            image_filename = None

        issue_description = request.form.get('issue_description')
        email = request.form.get('email')
        date = request.form.get('date')  

        # Extract latitude and longitude from location
        lat, lng = map(float, location.split(', '))

        # Save the issue data to the database
        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("INSERT INTO reported_problems (location, landmark, location_description, issue_image, issue_description, email, date, lat, lng) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (location, landmark, location_description, image_filename, issue_description, email, date, lat, lng))
        conn.commit()
        conn.close()

        # Send a confirmation email to the reporter
        send_confirmation_email(email)

        # Flash a success message
        flash('Thank you for reporting!', 'success')

        # Redirect to the dashboard after 30 seconds
        time.sleep(30)
        return redirect(url_for('dashboard'))

import csv
import random
import sqlite3

# Function to generate dummy IoT data and write it to a CSV file
def generate_dummy_iot_data(filename, num_entries):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Flow Rate', 'Pressure Level', 'Latitude', 'Longitude'])
        for _ in range(num_entries):
            timestamp = '2024-05-31 12:00:00'  # Dummy timestamp
            flow_rate = random.uniform(0.5, 10)  # Random flow rate
            pressure_level = random.uniform(10, 50)  # Random pressure level
            latitude = random.uniform(12.9, 13)  # Random latitude within specified range
            longitude = random.uniform(77.4, 77.6)  # Random longitude within specified range
            writer.writerow([timestamp, flow_rate, pressure_level, latitude, longitude])

# Function to read IoT data from a CSV file and detect problems based on specified conditions
def read_iot_data(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            #print(row)  # Here you can process each row as needed
            # Example: Detect problems based on specified conditions and add to reported problems database
            flow_rate = float(row['Flow Rate'])
            pressure_level = float(row['Pressure Level'])
            latitude = row['Latitude']
            longitude = row['Longitude']
            if flow_rate > 8.0:
                add_to_reported_problems('Abnormal Flow Rate', f'Flow rate is too high: {flow_rate}', latitude, longitude)
            elif pressure_level < 20.0:
                add_to_reported_problems('Low Pressure', f'Pressure level is too low: {pressure_level}', latitude, longitude)

# Function to add location coordinates to the reported problems database
def add_to_reported_problems(issue_type, issue_description, latitude, longitude):
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    loc=f"{latitude},{longitude}"
    issue_description=f"{issue_type}:{issue_description}"
    c.execute("INSERT INTO reported_problems (location, issue_description, lat, lng) VALUES (?, ?, ?, ?)",
              (loc, issue_description, latitude, longitude))
    conn.commit()
    conn.close()
generate_dummy_iot_data('data/dummy_iot_data.csv', 100)
read_iot_data('data/dummy_iot_data.csv')

# import pandas as pd
# import numpy as np

# def generate_dummy_geospatial_data(filename, num_points):
#     # Generate dummy geospatial data
#     data = pd.DataFrame()

#     # Generate random coordinates (latitude and longitude)
#     data['Latitude'] = np.random.uniform(low=-90, high=90, size=num_points)
#     data['Longitude'] = np.random.uniform(low=-180, high=180, size=num_points)

#     # Generate other dummy attributes such as water source type, infrastructure type, terrain features, etc.
#     data['Water_Source'] = np.random.choice(['River', 'Lake', 'Reservoir', 'Groundwater'], size=num_points)
#     data['Infrastructure_Type'] = np.random.choice(['Pipeline', 'Channel', 'Reservoir', 'Treatment Plant'], size=num_points)
#     data['Terrain_Features'] = np.random.choice(['Flat', 'Hilly', 'Mountainous'], size=num_points)
#     data['Land_Use'] = np.random.choice(['Urban', 'Suburban', 'Rural'], size=num_points)

#     # Save the generated data as a CSV file
#     data.to_csv(filename, index=False)

# # Example usage:
# generate_dummy_geospatial_data('data/dummy_geospatial_data.csv', 100)

# Function to fetch reported issues from the database
def get_reported_issues():
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("SELECT id, location, issue_description FROM reported_problems WHERE assigned_to IS NULL")
    issues = c.fetchall()
    conn.close()
    return issues

# Function to fetch water inspectors from the database
def get_water_inspectors():
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("SELECT employee_id, email FROM employees WHERE role = 'Water Inspector'")
    inspectors = c.fetchall()
    conn.close()
    return inspectors

# Function to assign tasks to water inspectors
@app.route('/assign_tasks', methods=['GET', 'POST'])
def assign_tasks():
    if request.method == 'POST':
        # Get the selected reported issue and water inspector from the form
        issue_id = request.form.get('issue_id')
        inspector_id = request.form.get('inspector_id')

        # Update the database to assign the task to the selected water inspector
        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("UPDATE reported_problems SET assigned_to = ?, status = 'assigned' WHERE id = ?", (inspector_id, issue_id))
        conn.commit()
        conn.close()

        # Redirect to the assign tasks page after updating the database
        return redirect(url_for('assign_tasks'))

    else:
        # Fetch reported issues and water inspectors from the database
        reported_issues = get_reported_issues()
        water_inspectors = get_water_inspectors()
        return render_template('assign_tasks.html', issues=reported_issues, inspectors=water_inspectors)


if __name__ == "__main__":
    app.run(port=5002, debug=True)  # Change the port number to 5001
