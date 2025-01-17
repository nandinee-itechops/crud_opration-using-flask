from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'many random bytes'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapplication'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = []
    data = cur.fetchall()
    
    # Convert tuple data to dictionary for easier template rendering
    for row in data:
        employee = {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'phone': row[3],
            'address': row[4],
            'dob': datetime.strptime(str(row[5]), '%Y-%m-%d'),
            'position': row[6]
        }
        employees.append(employee)
    
    cur.close()
    return render_template('index2.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']
        position = request.form['position']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO employees (name, email, phone, address, dob, position) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, address, dob, position))
        
        mysql.connection.commit()
        cur.close()
        
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']
        position = request.form['position']

        cur.execute("""
            UPDATE employees 
            SET name=%s, email=%s, phone=%s, address=%s, dob=%s, position=%s
            WHERE id=%s
        """, (name, email, phone, address, dob, position, id))
        
        mysql.connection.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # Get employee data for edit form
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    row = cur.fetchone()
    
    if row is None:
        flash('Employee not found!', 'danger')
        return redirect(url_for('index'))
    
    employee = {
        'id': row[0],
        'name': row[1],
        'email': row[2],
        'phone': row[3],
        'address': row[4],
        'dob': datetime.strptime(str(row[5]), '%Y-%m-%d'),
        'position': row[6]
    }
    
    cur.close()
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)