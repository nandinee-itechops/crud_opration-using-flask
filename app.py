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
    try:
        employee = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'dob': request.form['dob'],
            'position': request.form['position']
        }
        
        db = DB()
        result = db.add_employee(employee)
        if result['status'] == 'success':
            return jsonify({'status': 'success'})
        else:
            return jsonify(result), 400
    except Exception as e:
        app.logger.error(f"Error adding employee: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

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
    try:
        db = DB()
        result = db.delete_employee(id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
