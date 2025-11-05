#!/usr/bin/env python3
"""
Script to change a user's password in the database.
Usage: python change_password.py <email> <new_password>
"""

import os
import sys
import hashlib
from dotenv import load_dotenv
from library_system.database.connection import DatabaseConnection

load_dotenv()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def change_password(email: str, new_password: str):
    """Change a user's password."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
        sys.exit(1)
    
    db = DatabaseConnection(url, key)
    client = db.get_client()
    
    # Check if user exists
    result = client.table('user').select('user_id, email, role').eq('email', email).execute()
    
    if not result.data:
        print(f"Error: User with email '{email}' not found.")
        sys.exit(1)
    
    user = result.data[0]
    password_hash = hash_password(new_password)
    
    # Update password
    client.table('user').update({'password_hash': password_hash}).eq('user_id', user['user_id']).execute()
    
    print(f"✓ Password updated for {user['email']} ({user['role']})")
    print(f"  New password: {new_password}")
    print(f"  Password hash: {password_hash}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python change_password.py <email> <new_password>")
        print("\nExample:")
        print("  python change_password.py julia.roberts@example.com mynewpassword")
        sys.exit(1)
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    change_password(email, new_password)

