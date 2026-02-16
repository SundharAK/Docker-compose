from fastapi import FastAPI
import mysql.connector

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host="mysql",        # important: service name from docker-compose
        user="root",
        password="root123",
        database="testdb"
    )

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

if __name__ == "__main__":
     app.run(host='0.0.0.0', port=8000)
