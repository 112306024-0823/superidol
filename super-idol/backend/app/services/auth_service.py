"""
Authentication service functions.
"""
import pymysql
import jwt
from datetime import datetime, timedelta
from app.db import get_db_connection
from app.utils.security import hash_password, verify_password
from app.config import Config

print(f"[DEBUG] auth_service loaded from: {__file__}")
print("[DEBUG] SQL will use table: Users")

def register_user(data):
    """
    Register a new user in the database.
    
    Args:
        data (dict): User data containing name, email, and password
        
    Returns:
        dict: Result of the registration process
    """
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    # Validate input
    if not all([name, email, password]):
        return {"error": "Name, email, and password are required"}
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Connect to database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
            if cursor.fetchone():
                return {"error": "Email already exists"}
            
            # Create new user
            cursor.execute(
                "INSERT INTO Users (Name, Email, PasswordHash, Budget, WeekCalorieLimit) VALUES (%s, %s, %s, %s, %s)",
                (name, email, hashed_password, 0, 0)
            )
            user_id = cursor.lastrowid
        conn.commit()
        
        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "name": name,
            "email": email
        }
    except pymysql.Error as e:
        conn.rollback()
        return {"error": f"Database error: {str(e)}"}
    finally:
        conn.close()

def login_user(data):
    """
    Authenticate a user and generate an access token.
    
    Args:
        data (dict): User credentials containing email and password
        
    Returns:
        dict: Authentication result with access token if successful
    """
    email = data.get('email')
    password = data.get('password')
    
    # Validate input
    if not all([email, password]):
        return {"error": "Email and password are required"}
    
    # Connect to database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Find user by email
            cursor.execute("SELECT UserID, Name, Email, PasswordHash FROM Users WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            if not user or not verify_password(password, user['PasswordHash']):
                return {"error": "Invalid email or password"}
            
            # Generate JWT token
            payload = {
                'user_id': user['UserID'],
                'email': user['Email'],
                'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
            }
            token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
            
            return {
                "message": "Login successful",
                "access_token": token,
                "user": {
                    "id": user['UserID'],
                    "name": user['Name'],
                    "email": user['Email']
                }
            }
    except pymysql.Error as e:
        return {"error": f"Database error: {str(e)}"}
    finally:
        conn.close() 