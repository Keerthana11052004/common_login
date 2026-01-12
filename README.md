# Common Login Backend

This is the backend for the common_login project that manages user master data in a MySQL database.

## Features

- Get username by user ID
- Get full name (first name and last name) by user ID
- Get department by user ID
- Get left date by user ID
- Automatically update user status from active to inactive when left date is reached
- Edit user master data
- Get user data in JSON format
- Get employee units with '|' separator
- Add employee units
- Remove employee units
- Get unit description by unit code
- Get project accesses (employee_id, project)
- Check if project is allowed for employee
- Grant project access with auth type
- RESTful API endpoints

## Database Configuration

The application connects to a MySQL database with the following configuration stored in `.env` file:

```
DB_HOST=localhost
DB_NAME=common_login
DB_USER=root
DB_PASSWORD=Violin@12
DB_PORT=3306
```

## Files Structure

- `.env` - Database credentials
- `sql_processor.py` - Database connection and SQL operations
- `user_master.py` - Business logic for user master operations
- `app.py` - Flask API application
- `test_user_master.py` - Test script for user master functionality
- `requirements.txt` - Project dependencies

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have a MySQL server running with the `common_login` database and `user_master` table.

3. Update the `.env` file with your database credentials if different.

## API Endpoints

- `GET /user/<id>/username` - Get username by user ID
- `GET /user/<id>/fullname` - Get full name by user ID
- `GET /user/<id>/department` - Get department by user ID
- `GET /user/<id>/leftdate` - Get left date by user ID
- `GET /user/<id>` - Get all user data by ID
- `GET /users` - Get all users data
- `PUT /user/<id>` - Update user data
- `POST /update-user-status` - Manually trigger user status update based on left date
- `GET /employee/<id>/units` - Get employee units using '|' separator
- `PUT /employee/<id>/units` - Add units to employee
- `PUT /employee/<id>/units/remove` - Remove units from employee
- `GET /unit/<unit_code>/description` - Get unit description by unit code
- `GET /project-access/<emp_id>/<project>` - Get project accesses for an employee
- `GET /project-allowed/<emp_id>/<project>` - Check if project is allowed for employee
- `POST /project-access` - Grant project access with auth type
- `/` - Login page
- `/dashboard` - User dashboard after successful login
- `/api/login` - Login API endpoint
- `/api/signup` - Signup API endpoint

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`