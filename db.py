import mysql.connector
import os

# Establish a connection to MySQL
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST", "localhost"),
    user=os.getenv("MYSQLUSER", "root"),
    password=os.getenv("MYSQLPASSWORD", "Admin@123"),
    database=os.getenv("MYSQLDATABASE", "Bank_Management"),
    port=os.getenv("MYSQLPORT", 3306)
)

# Create a cursor object
cursor = db.cursor()

# Example query to check connection
cursor.execute("SHOW DATABASES")
for db in cursor:
    print(db)

db.close()
