import mysql.connector

class DB:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="crudapplication"
            )
            print("DB connected")
        except mysql.connector.Error as e:
            print("Error:", e)
            self.con = None

    def getRecord(self):
        if not self.con:
            print("Database connection not established.")
            return []
        try:
            cur = self.con.cursor()
            query = "SELECT * FROM employees"  # Corrected table name
            cur.execute(query)
            response = cur.fetchall()
            cur.close()
            print(response)
            return response
        except mysql.connector.Error as e:
            print("Error executing query:", e)
            return []

dbHelper = DB()
dbHelper.getRecord()
