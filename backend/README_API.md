# API Server - Login Instructions

## Current Password Configuration

All user passwords have been set to: **`password123`**

### How to Login

Use any user email from your database with the password `password123`:

**Librarian Accounts (can manage books/members):**
- Email: `julia.roberts@example.com`
- Password: `password123`

- Email: `ivan.petrov@example.com`
- Password: `password123`

**Administrator Account:**
- Email: `kevin.spacey@example.com`
- Password: `password123`

**Member Accounts (regular users):**
- Any email from the `user` table
- Password: `password123`

## Changing Passwords

To change a specific user's password, use the `change_password.py` script:

```bash
cd backend
source venv/bin/activate  # if using virtual environment
python change_password.py <email> <new_password>
```

**Example:**
```bash
python change_password.py julia.roberts@example.com mySecurePassword123
```

## Understanding Password Hashing

**Important:** Passwords are stored as SHA-256 hashes in the database. This means:
- ✅ You can verify if a password is correct
- ❌ You cannot "get back" the original password from the hash
- ✅ You can change a password by providing a new one

The hash is one-way: `password123` → `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`

When you login:
1. You enter the plain text password: `password123`
2. The system hashes it: `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`
3. It compares this hash with the hash stored in the database
4. If they match, login succeeds

## Troubleshooting Login

If login is not working:

1. **Check API server is running:**
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return: `{"status":"healthy",...}`

2. **Check the endpoint exists:**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"julia.roberts@example.com","password":"password123"}'
   ```

3. **Restart the API server** if you made changes:
   ```bash
   cd backend
   python api_server.py
   ```

4. **Verify password hash in database:**
   - Check Supabase dashboard
   - The `password_hash` for all users should be: `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f`
   - If it's still `hashed_password_12` or similar, run the password fix script again

## Frontend Login

In the frontend, use:
- **API Base URL:** `http://localhost:8000`
- **Email:** Any user email (e.g., `julia.roberts@example.com`)
- **Password:** `password123`

