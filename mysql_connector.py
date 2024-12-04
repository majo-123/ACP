import mysql.connector
from mysql.connector import Error
import bcrypt

def connect_to_database():
    """Connect to the database and return the connection object."""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your database host
            user='root',  # Replace with your database username
            password='yhuan123',  # Replace with your database password
            database='project'  # Replace with your database name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def hash_password(password):
    """Hash a plain-text password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
import bcrypt

def check_password(plain_password, hashed_password):
    """Check if the plain-text password matches the hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
