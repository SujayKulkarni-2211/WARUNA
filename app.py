#SIH1423

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
# Function to create SQLite database and tables
def create_tables():
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reported_problems 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT, landmark TEXT, 
                 location_description TEXT, issue_image TEXT, issue_description TEXT, 
                 email TEXT, date TEXT, lat REAL, lng REAL, assigned_to TEXT, status TEXT)''')  # Add lat and lng columns
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (employee_id TEXT PRIMARY KEY, name TEXT, password TEXT, role TEXT,
                 email TEXT, mobile_no TEXT, tasks_reviewed INTEGER DEFAULT 0,
                 tasks_completed INTEGER DEFAULT 0)''')  # Add name column

    # Create a table for assigned tasks
    c.execute('''CREATE TABLE IF NOT EXISTS assigned_tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, inspector_id TEXT,
                 issue_id INTEGER,
                 FOREIGN KEY(inspector_id) REFERENCES employees(employee_id),
                 FOREIGN KEY(issue_id) REFERENCES reported_problems(id))''')
    # c.execute("INSERT INTO employees VALUES ('manager1','Manager 1', 'password', 'Manager', 'manager1@example.com', '9380142763', 0, 0)")
    # c.execute("INSERT INTO employees VALUES ('inspector1','Inspector 1', 'password', 'Water Inspector', 'inspector1@example.com', '9113518404', 0, 0)")
    
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        password = request.form.get('password')
        
        if not employee_id or not password:
            flash('Please enter both employee ID and password', 'error')
            return redirect(url_for('login'))

        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_password = user[2]  # Assuming password is in the third column (index 2)
            if password == stored_password:
                session['employee_id'] = employee_id
                session['role'] = user[3]  # Store role in session (index 3 is role)
                session['name'] = user[1]  # Store name in session (index 1 is name)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password', 'error')
                return redirect(url_for('login'))
        else:
            flash('Invalid employee ID', 'error')
            return redirect(url_for('login'))

        

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'employee_id' in session:
        name = session.get('name')
        if session['role'] == 'Manager':
            return render_template('manager_dashboard.html', name=name)
        elif session['role'] == 'Water Inspector':
            return render_template('inspector_dashboard.html', name=name)
    flash('Please log in to access this page', 'error')
    return redirect(url_for('login'))



    


# Function to handle logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Function to render dashboard based on role


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
        # time.sleep(30)
        return redirect(url_for('index'))

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

# Function to assign tasks to water inspectors
@app.route('/assign_tasks', methods=['GET', 'POST'])
def assign_tasks():
    issues_data = []
    water_inspectors=[]
    if request.method == 'POST':
        # Get the selected reported issue and water inspector from the form
        issue_id = request.form.get('issue_id')
        inspector_id = request.form.get('inspector_id')

        # Update the database to assign the task to the selected water inspector
        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("UPDATE reported_problems SET assigned_to = ?, status = 'assigned' WHERE id = ?", (inspector_id, issue_id))
        
        # Insert the assigned task into the assigned_tasks table
        c.execute("INSERT INTO assigned_tasks (inspector_id, issue_id) VALUES (?, ?)", (inspector_id, issue_id))
        
        conn.commit()
        conn.close()

        # Create a table for the inspector's tasks if not exists
        table_name=f"{inspector_id}_tasks"
        create_inspector_task_table(table_name)

        # Insert the assigned task into the inspector's task table
        insert_inspector_task(table_name, issue_id)
        #print(reported_issues)
        session['task_assigned'] = True
        # Redirect to the assign tasks page after updating the database
        return redirect(url_for('assign_tasks'))


    else:
        # Fetch reported issues and water inspectors from the database
        reported_issues = get_reported_issues()
        water_inspectors = get_water_inspectors()

        # Fetch already assigned issues to exclude them from the table
        assigned_issues = get_assigned_issues()

        # Combine issues and inspectors data
        issues_data = []
        for issue in reported_issues:
            if issue['id'] not in assigned_issues:
                issues_data.append(issue)

        if 'task_assigned' in session:
            flash('Task assigned successfully!', 'success')
            session.pop('task_assigned', None)
            
        return render_template('assign_tasks.html', issues=issues_data, inspectors=water_inspectors)


def create_inspector_task_table(table_name):
    """Create a table for the inspector's tasks if not exists."""
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS tasks_{table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, issue_id INTEGER)")
    conn.commit()
    conn.close()


def insert_inspector_task(table_name, issue_id):
    """Insert the assigned task into the inspector's task table."""
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO tasks_{table_name} (issue_id) VALUES (?)", (issue_id,))
    conn.commit()
    conn.close()


def get_assigned_issues():
    """Get a list of already assigned issue IDs."""
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("SELECT issue_id FROM assigned_tasks")
    assigned_issues = [row[0] for row in c.fetchall()]
    conn.close()
    return assigned_issues


def get_reported_issues():
    """Fetch reported issues from the database."""
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reported_problems WHERE assigned_to IS NULL")
    reported_issues = [{'id': row[0], 'location': row[1], 'landmark': row[2], 'location_description': row[3], 'issue_image': row[4],
                        'issue_description': row[5], 'email': row[6], 'date': row[7], 'lat': row[8], 'lng': row[9]} for row in c.fetchall()]
    conn.close()
    return reported_issues


def get_water_inspectors():
    """Fetch water inspectors from the database along with the number of tasks assigned to each inspector."""
    conn = sqlite3.connect('waruna.db')
    c = conn.cursor()
    c.execute("""
        SELECT e.employee_id, e.name, COUNT(at.issue_id) AS tasks_assigned
        FROM employees e
        LEFT JOIN assigned_tasks at ON e.employee_id = at.inspector_id
        WHERE e.role = 'Water Inspector'
        GROUP BY e.employee_id, e.name
    """)
    water_inspectors = [{'employee_id': row[0], 'name': row[1], 'tasks_assigned': row[2]} for row in c.fetchall()]
    conn.close()
    return water_inspectors



@app.route('/view_profile')
def view_profile():
    if 'employee_id' in session:
        employee_id = session['employee_id']
        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("SELECT employee_id, name, role, email, mobile_no FROM employees WHERE employee_id = ?", (employee_id,))
        profile = c.fetchone()
        conn.close()
        return render_template('view_profile.html', profile=profile)
    flash('Please log in to access this page', 'error')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'employee_id' in session:
        if request.method == 'POST':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            employee_id = session['employee_id']

            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('change_password'))

            conn = sqlite3.connect('waruna.db')
            c = conn.cursor()
            c.execute("SELECT password FROM employees WHERE employee_id = ?", (employee_id,))
            stored_password = c.fetchone()[0]

            if stored_password != current_password:
                flash('Current password is incorrect', 'error')
                conn.close()
                return redirect(url_for('change_password'))

            c.execute("UPDATE employees SET password = ? WHERE employee_id = ?", (new_password, employee_id))
            conn.commit()
            conn.close()

            flash('Password successfully changed', 'success')
            return redirect(url_for('view_profile'))
        
        return render_template('change_password.html')

    flash('Please log in to access this page', 'error')
    return redirect(url_for('login'))

@app.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees (employee_id, name, email, password, mobile_no, role) VALUES (?, ?, ?, ?, ?, ?)",
                  (id, name, email, password, mobile, 'Manager'))
        conn.commit()
        conn.close()

        flash('Manager registered successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register_manager.html')


@app.route('/register_inspector', methods=['GET', 'POST'])
def register_inspector():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']

        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()
        c.execute("INSERT INTO employees (employee_id, name, email, password, mobile_no, role) VALUES (?, ?, ?, ?, ?, ?)",
                  (id, name, email, password, mobile, 'Water Inspector'))
        conn.commit()
        conn.close()

        flash('Inspector registered successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register_inspector.html')

def get_db_connection():
    conn = sqlite3.connect('waruna.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/manage_employees')
def manage_employees():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT employee_id, name, role, email, mobile_no, tasks_reviewed, tasks_completed FROM employees")
    employees = c.fetchall()
    conn.close()
    return render_template('manage_employees.html', employees=employees)

@app.route('/edit_employee_page/<employee_id>', methods=['GET', 'POST'])
def edit_employee_page(employee_id):
    conn = get_db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        tasks_reviewed = request.form.get('tasks_reviewed')
        tasks_completed = request.form.get('tasks_completed')

        c.execute('''UPDATE employees 
                     SET name = ?, password = ?, role = ?, email = ?, mobile_no = ?, 
                         tasks_reviewed = ?, tasks_completed = ? 
                     WHERE employee_id = ?''',
                  (name, password, role, email, mobile_number, tasks_reviewed, tasks_completed, employee_id))
        conn.commit()
        conn.close()
        flash('Employee data updated successfully', 'success')
        return redirect(url_for('manage_employees'))

    c.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = c.fetchone()
    conn.close()

    return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if the employee exists
    c.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    employee = c.fetchone()

    if employee:
        c.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        
        # Check if a table with the employee's name exists and delete it
        employee_table = f"tasks_{employee_id}_tasks"
        c.execute(f"DROP TABLE IF EXISTS {employee_table}")

        conn.commit()
        flash('Employee deleted successfully', 'success')
    else:
        flash('Employee does not exist', 'error')

    conn.close()
    return redirect(url_for('manage_employees'))

@app.route('/delete_task', methods=['GET', 'POST'])
def delete_task():
    if request.method == 'POST':
        issue_id = request.form.get('issue_id')

        conn = sqlite3.connect('waruna.db')
        c = conn.cursor()

        # Delete the task from the database
        c.execute("DELETE FROM reported_problems WHERE id = ?", (issue_id,))
        conn.commit()
        conn.close()

        flash('ISSUE deleted successfully', 'success')
        return redirect(request.referrer or url_for('assign_tasks'))
    else:
        
        return "This route only accepts POST requests. Go back and use a form to delete a task."

if __name__ == "__main__":
    app.run(port=5001, debug=True)  
