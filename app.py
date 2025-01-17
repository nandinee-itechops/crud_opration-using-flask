from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import logging
from home import DB

app = Flask(__name__)
app.secret_key = 'many random bytes'

@app.route('/')
def index():
    db = DB()
    result = db.fetch_all_employees()
    return render_template('index.html', employees=result.get('data', []))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    dob = request.form['dob']
    position = request.form['position']

    cur = mysql.connection.cursor()
    try:
        cur.execute(""" 
            INSERT INTO employees (name, email, phone, address, dob, position) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, address, dob, position))
        
        mysql.connection.commit()
        return jsonify({'status': 'success'})
    except MySQLdb.IntegrityError as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'status': 'error', 'message': 'Email already exists!'})
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cur.close()

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    db = DB()
    if request.method == 'GET':
        result = db.get_employee(id)
        response = jsonify(result)
        response.headers['Content-Type'] = 'application/json'
        return response, 200 if result['status'] == 'success' else 404

    # Handle POST request
    try:
        employee = {
            'id': id,
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'dob': request.form['dob'],
            'position': request.form['position']
        }
        
        app.logger.debug(f"Updating employee with data: {employee}")
        
        result = db.update_employee(employee)
        if result['status'] == 'success':
            return jsonify({'status': 'success'})
        else:
            app.logger.error(f"Error updating employee: {result['message']}")
            return jsonify(result), 500
            
    except Exception as e:
        app.logger.error(f"Error in edit route: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM employees WHERE id = %s", (id,))
        mysql.connection.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cur.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
