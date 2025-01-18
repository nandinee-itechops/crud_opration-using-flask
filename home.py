import mysql.connector
from datetime import datetime

class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Empty password as per your configuration
            database="crudapplication"  # Updated database name
        )
        self.cursor = self.conn.cursor(dictionary=True)  # Use dictionary cursor

    def fetch_all_employees(self):
        try:
            query = "SELECT * FROM employees"
            self.cursor.execute(query)
            employees = self.cursor.fetchall()
            # Format dates for JSON
            for emp in employees:
                if emp['dob']:
                    emp['dob'] = emp['dob'].strftime('%Y-%m-%d')
            return {'status': 'success', 'data': employees}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def add_employee(self, employee):
        try:
            query = "INSERT INTO employees (name, email, phone, address, dob, position) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (
                employee['name'],
                employee['email'],
                employee['phone'],
                employee['address'],
                employee['dob'],
                employee['position']
            ))
            self.conn.commit()
            return {'status': 'success'}
        except mysql.connector.Error as e:
            self.conn.rollback()
            if e.errno == 1062:  # Duplicate entry error
                return {'status': 'error', 'message': 'Email already exists!'}
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            self.conn.rollback()
            return {'status': 'error', 'message': str(e)}

    def get_employee(self, employee_id):
        try:
            query = "SELECT * FROM employees WHERE id = %s"
            self.cursor.execute(query, (employee_id,))
            employee = self.cursor.fetchone()
            if employee and employee['dob']:
                employee['dob'] = employee['dob'].strftime('%Y-%m-%d')
            return {'status': 'success', 'data': employee} if employee else {'status': 'error', 'message': 'Employee not found'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def update_employee(self, employee):
        try:
            query = """UPDATE employees SET name = %s, email = %s, phone = %s, address = %s, dob = %s, position = %s WHERE id = %s"""
            self.cursor.execute(query, (
                employee['name'],
                employee['email'],
                employee['phone'],
                employee['address'],
                employee['dob'],
                employee['position'],
                employee['id']
            ))
            self.conn.commit()
            return {'status': 'success'}
        except mysql.connector.Error as e:
            self.conn.rollback()
            return {'status': 'error', 'message': str(e)}
        except Exception as e:
            self.conn.rollback()
            return {'status': 'error', 'message': f'Update failed: {str(e)}'}

    def delete_employee(self, employee_id):
        try:
            query = "DELETE FROM employees WHERE id = %s"
            self.cursor.execute(query, (employee_id,))
            self.conn.commit()
            return {'status': 'success'}
        except Exception as e:
            self.conn.rollback()
            return {'status': 'error', 'message': str(e)}
