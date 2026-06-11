import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_MYSQL_PASSWORD",   # 👈 put your MySQL password
    database="student_db"
)

cursor = db.cursor()

print("Database connected successfully!")