import mysql.connector
import os
import dotenv


dotenv.load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWRD")
)

mycursor = conn.cursor()
mycursor.execute("CREATE DATABASE climatewise")