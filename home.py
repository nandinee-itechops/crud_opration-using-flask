import mysql.connector
from datetime import datetime

class DB:
    def __init__(self):
        # Database configuration
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crudapplication"
            )
            self.con.autocommit = True
            self.cursor = self.con.cursor(dictionary=True)  # Use dictionary cursor for named columns
            self.create_table()  # Ensure table exists
            print("Database connected successfully")
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            self.con = None

    def create_table(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone VARCHAR(20) NOT NULL,
                address VARCHAR(200) NOT NULL,
                dob DATE NOT NULL,
                position VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.con.commit()
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")

    def getRecord(self):
        try:
            query = "SELECT id, name, email, phone, address, DATE_FORMAT(dob, '%Y-%m-%d') as dob, position FROM employees ORDER BY id DESC"
            self.cursor.execute(query)
            employees = self.cursor.fetchall()
            return employees
        except mysql.connector.Error as e:
            print(f"Error fetching records: {e}")
            return []

    def getEmployeeById(self, id):
        try:
            query = "SELECT id, name, email, phone, address, DATE_FORMAT(dob, '%Y-%m-%d') as dob, position FROM employees WHERE id = %s"
            self.cursor.execute(query, (id,))
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error fetching employee: {e}")
            return None

    def insertRecord(self, name, email, phone, address, dob, position):
        try:
            query = """
            INSERT INTO employees (name, email, phone, address, dob, position) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # Parse the date string to ensure valid format
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
            
            values = (name, email, phone, address, dob_date, position)
            self.cursor.execute(query, values)
            self.con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error inserting record: {e}")
            return False
        except ValueError as e:
            print(f"Invalid date format: {e}")
            return False

    def updateRecord(self, id, name, email, phone, address, dob, position):
        try:
            query = """
            UPDATE employees 
            SET name=%s, email=%s, phone=%s, address=%s, dob=%s, position=%s 
            WHERE id=%s
            """
            # Parse the date string to ensure valid format
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
            
            values = (name, email, phone, address, dob_date, position, id)
            self.cursor.execute(query, values)
            self.con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error updating record: {e}")
            return False
        except ValueError as e:
            print(f"Invalid date format: {e}")
            return False

    def deleteRecord(self, id):
        try:
            query = "DELETE FROM employees WHERE id = %s"
            self.cursor.execute(query, (id,))
            self.con.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error deleting record: {e}")
            return False

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'con') and self.con:
            self.con.close()