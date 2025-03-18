# How to Run the Flask Project

## Steps to Run the Project

### 1. Clone the Repository
```sh
git clone <repository-url>
cd crud_operation_using_flask
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
```
Activate the virtual environment:
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```sh
  source venv/bin/activate
  ```

### 3. Install Required Libraries
```sh
pip install flask mysql-connector-python
```

### 4. Configure Database
Ensure MySQL is running and update `config.py` with your database credentials:
```python
self.conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
```

### 5. Run the Flask Application
```sh
python app.py
```

### 6. Open in Browser
Visit `http://127.0.0.1:5000/` to access the application.

## Troubleshooting
- If you get a `ModuleNotFoundError`, install the missing package using:
  ```sh
  pip install <missing_package>
  ```
- If MySQL fails to connect, ensure your MySQL service is running and check credentials in `config.py`.

