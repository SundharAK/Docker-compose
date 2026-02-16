from fastapi import FastAPI
import mysql.connector
import time

app = FastAPI()

def connect_db():
    while True:
        try:
            connection = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root123",
                database="testdb"
            )
            return connection
        except:
            print("Waiting for MySQL...")
            time.sleep(2)

# Create table automatically (runs when API starts)
@app.on_event("startup")
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50)
        )
    """)
    conn.commit()

@app.get("/")
def read_root():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    return {"Connected to database": db_name}

# API to insert data
@app.get("/add/{name}")
def add_user(name: str):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    return {"message": f"User {name} inserted successfully"}

@app.get("/users")
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return {"users": data}


volumes:
  mysql_data:
