from flask import Flask, request, jsonify
from user_master import UserMaster
from employee_unit import EmployeeUnit
from unit_master import UnitMaster
from app_access import AppAccess
import os

app = Flask(__name__)
user_master = UserMaster()
emp_unit = EmployeeUnit()
unit_master = UnitMaster()
app_access = AppAccess()

@app.route('/user/<int:user_id>/username', methods=['GET'])
def get_username(user_id):
    """Get username by user ID"""
    try:
        username = user_master.get_username(user_id)
        if username is not None:
            return jsonify({'username': username})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/fullname', methods=['GET'])
def get_full_name(user_id):
    """Get full name by user ID"""
    try:
        full_name = user_master.get_full_name(user_id)
        if full_name is not None:
            return jsonify(full_name)
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/department', methods=['GET'])
def get_department(user_id):
    """Get department by user ID"""
    try:
        department = user_master.get_department(user_id)
        if department is not None:
            return jsonify({'department': department})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>/leftdate', methods=['GET'])
def get_left_date(user_id):
    """Get left date by user ID"""
    try:
        left_date = user_master.get_left_date(user_id)
        if left_date is not None:
            return jsonify({'left_date': left_date})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_data(user_id):
    """Get user data by ID in JSON format"""
    try:
        user_data = user_master.get_user_by_id(user_id)
        return jsonify(user_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users data in JSON format"""
    try:
        all_users = user_master.get_all_users()
        return jsonify(all_users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user_data(user_id):
    """Update user master data"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = user_master.edit_master_data(user_id, **data)
        if result:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'error': 'Failed to update user'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-user-status', methods=['POST'])
def update_user_status():
    """Manually trigger update of user status based on left date"""
    try:
        result = user_master.update_user_status_based_on_left_date()
        if result:
            return jsonify({'message': 'User status updated successfully'})
        else:
            return jsonify({'error': 'Failed to update user status'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employee/<int:emp_id>/units', methods=['GET'])
def get_employee_units(emp_id):
    """Get units for an employee using '|' as separator"""
    try:
        units = emp_unit.get_units(emp_id)
        if units is not None:
            return jsonify({'emp_id': emp_id, 'units': units.split('|')})
        else:
            return jsonify({'error': 'Employee not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employee/<int:emp_id>/units', methods=['PUT'])
def add_employee_units(emp_id):
    """Add units to an employee"""
    try:
        data = request.get_json()
        if not data or 'units' not in data:
            return jsonify({'error': 'Units list is required'}), 400
        
        units_to_add = data['units']
        if not isinstance(units_to_add, list):
            return jsonify({'error': 'Units must be provided as a list'}), 400
        
        result = emp_unit.add_units(emp_id, units_to_add)
        if result:
            return jsonify({'message': 'Units added successfully'})
        else:
            return jsonify({'error': 'Failed to add units'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employee/<int:emp_id>/units/remove', methods=['PUT'])
def remove_employee_units(emp_id):
    """Remove units from an employee"""
    try:
        data = request.get_json()
        if not data or 'units' not in data:
            return jsonify({'error': 'Units list is required'}), 400
        
        units_to_remove = data['units']
        if not isinstance(units_to_remove, list):
            return jsonify({'error': 'Units must be provided as a list'}), 400
        
        result = emp_unit.remove_units(emp_id, units_to_remove)
        if result:
            return jsonify({'message': 'Units removed successfully'})
        else:
            return jsonify({'error': 'Failed to remove units'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/unit/<unit_code>/description', methods=['GET'])
def get_unit_description(unit_code):
    """Get unit description by unit code"""
    try:
        description = unit_master.get_unit_description(unit_code)
        if description is not None:
            return jsonify({'unit_code': unit_code, 'description': description})
        else:
            return jsonify({'error': 'Unit not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/project-access/<int:emp_id>/<project>', methods=['GET'])
def get_project_accesses(emp_id, project):
    """Get project accesses for an employee"""
    try:
        accesses = app_access.get_project_accesses_json(emp_id, project)
        return accesses
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/project-allowed/<int:emp_id>/<project>', methods=['GET'])
def is_project_allowed(emp_id, project):
    """Check if a project is allowed for an employee"""
    try:
        result = app_access.get_project_allowed_json(emp_id, project)
        return result
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/project-access', methods=['POST'])
def grant_project_access():
    """Grant project access to an employee"""
    try:
        data = request.get_json()
        if not data or 'emp_id' not in data or 'project' not in data or 'auth_type' not in data:
            return jsonify({'error': 'Employee ID, project, and auth type are required'}), 400
        
        emp_id = data['emp_id']
        project = data['project']
        auth_type = data['auth_type']
        
        result = app_access.grant_project_access(emp_id, project, auth_type)
        if result:
            return jsonify({'message': 'Project access granted successfully'})
        else:
            return jsonify({'error': 'Failed to grant project access'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Import render_template for serving HTML templates
from flask import render_template
import re

# Ensure the templates folder exists
app.template_folder = 'templates'

@app.route('/')
def login_page():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/landing')
def landing():
    """Serve the landing page with all projects"""
    return render_template('landing.html')



# API endpoint to get project data
@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects from project_master table"""
    try:
        query = "SELECT project_code, project_name FROM project_master ORDER BY project_name ASC"
        projects = user_master.sql_processor.db.execute_query(query)
        
        if projects is not None:
            return jsonify({'status': 'success', 'projects': projects}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to retrieve projects'}), 500
            
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/app-access')
def app_access_management():
    """Serve the app access management page"""
    return render_template('app_access_management.html')

@app.route('/api/access/<employee_id>/<project_code>', methods=['GET'])
def get_access(employee_id, project_code):
    """Get access details for a specific employee and project"""
    try:
        query = "SELECT * FROM authentication WHERE employee_id = %s AND project_code = %s LIMIT 1"
        access = user_master.sql_processor.db.execute_query(query, (employee_id, project_code))
        
        if access:
            # Also get project name
            project_query = "SELECT project_name FROM project_master WHERE project_code = %s LIMIT 1"
            project_info = user_master.sql_processor.db.execute_query(project_query, (project_code,))
            
            result = access[0]
            if project_info:
                result['project_name'] = project_info[0]['project_name']
            
            return jsonify({'status': 'success', 'access': result}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No access found'}), 404
    
    except Exception as e:
        print(f"Error fetching access: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/access', methods=['POST'])
def update_access():
    """Update or create access for an employee and project"""
    try:
        data = request.get_json()
        
        if not data or 'employee_id' not in data or 'project_code' not in data or 'auth_type' not in data:
            return jsonify({'status': 'error', 'message': 'Employee ID, project code, and auth type are required'}), 400
        
        employee_id = data['employee_id']
        project_code = data['project_code']
        auth_type = data['auth_type']
        
        # Check if access already exists
        check_query = "SELECT * FROM authentication WHERE employee_id = %s AND project_code = %s LIMIT 1"
        existing_access = user_master.sql_processor.db.execute_query(check_query, (employee_id, project_code))
        
        if existing_access:
            # Update existing access
            update_query = "UPDATE authentication SET auth_type = %s, created_at = CURRENT_TIMESTAMP WHERE employee_id = %s AND project_code = %s"
            result = user_master.sql_processor.db.execute_non_query(update_query, (auth_type, employee_id, project_code))
            message = f'Access updated successfully to {auth_type}'
        else:
            # Create new access
            insert_query = "INSERT INTO authentication (employee_id, project_code, auth_type) VALUES (%s, %s, %s)"
            result = user_master.sql_processor.db.execute_non_query(insert_query, (employee_id, project_code, auth_type))
            message = f'Access created successfully as {auth_type}'
        
        if result:
            return jsonify({'status': 'success', 'message': message}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to update access'}), 500
    
    except Exception as e:
        print(f"Error updating access: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/access/<employee_id>/<project_code>', methods=['DELETE'])
def remove_access(employee_id, project_code):
    """Remove access for a specific employee and project"""
    try:
        query = "DELETE FROM authentication WHERE employee_id = %s AND project_code = %s"
        result = user_master.sql_processor.db.execute_non_query(query, (employee_id, project_code))
        
        if result:
            return jsonify({'status': 'success', 'message': 'Access removed successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No access found to remove'}), 404
    
    except Exception as e:
        print(f"Error removing access: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle user login with employee ID or email"""
    try:
        data = request.get_json()
        identifier = data.get('identifier', '').strip()
        password = data.get('password', '')
        
        if not identifier or not password:
            return jsonify({'status': 'error', 'message': 'Identifier and password are required'}), 400
        
        # Determine if identifier is an email or employee ID
        is_email = '@' in identifier
        
        # Validate email format if it's an email
        if is_email:
            email_pattern = r'^[^@]+@violintec\.com$'
            if not re.match(email_pattern, identifier):
                return jsonify({'status': 'error', 'message': 'Email must be in @violintec.com domain'}), 400
        
        # Check if employee exists and is active
        # First, try to find by employee ID if identifier looks like an ID
        if not is_email:
            # Employee ID can be varchar (numeric or character)
            emp_id = identifier
            # Query user_master by employee ID
            # Query user_master by employee ID - use the correct column based on table structure
            query = "SELECT * FROM user_master WHERE employee_id = %s LIMIT 1"
            user_result = user_master.sql_processor.db.execute_query(query, (emp_id,))
            
            if not user_result:
                return jsonify({'status': 'error', 'message': 'Invalid employee ID or user not found'}), 401
            
            user = user_result[0]
        else:
            # Query user_master by email (assuming there's an email column in user_master)
            query = "SELECT * FROM user_master WHERE email = %s LIMIT 1"
            user_result = user_master.sql_processor.db.execute_query(query, (identifier,))
            
            if not user_result:
                return jsonify({'status': 'error', 'message': 'Invalid email or user not found'}), 401
            
            user = user_result[0]
            # Try to get the ID field, using common alternatives if 'id' doesn't exist
            emp_id = user.get('id', user.get('employee_id', user.get('emp_id', identifier)))
        
        # Check if user is active
        if user['active_status'] == 0:
            return jsonify({'status': 'inactive', 'message': 'Account is inactive due to employment end'}), 401
        
        # Check if employee has left (left_date is in the past)
        if user['left_date']:
            from datetime import datetime
            today = datetime.now().date()
            left_date = user['left_date'] if isinstance(user['left_date'], datetime) else datetime.strptime(str(user['left_date']), '%Y-%m-%d').date()
            
            if left_date <= today:
                # Update user status to inactive
                # Try different common column names for the ID
                user_id = user.get('id', user.get('employee_id', user.get('emp_id', None)))
                if user_id is not None:
                    update_query = "UPDATE user_master SET active_status = 0 WHERE id = %s OR employee_id = %s OR emp_id = %s LIMIT 1"
                    # Use the found ID value for all possible column names
                    user_master.sql_processor.db.execute_non_query(update_query, (user_id, user_id, user_id))
                
                return jsonify({'status': 'inactive', 'message': 'Access denied: Your employment has ended'}), 401
        
        # Check for shared email accounts
        if is_email:
            query = "SELECT COUNT(*) as count FROM user_master WHERE email = %s"
            email_check_result = user_master.sql_processor.db.execute_query(query, (identifier,))
            if email_check_result and len(email_check_result) > 0 and email_check_result[0]['count'] > 1:
                return jsonify({'status': 'shared_email', 'message': 'Multiple accounts detected with this email. Please use your Employee ID to login instead.'}), 200
        
        # Verify password hash
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user['password_hash'] != password_hash:
            return jsonify({'status': 'error', 'message': 'Invalid password'}), 401
        
        # Get user units
        units_str = emp_unit.get_units_raw(emp_id)
        units = units_str.split('|') if units_str else []
        
        # Get user access information
        access_result = app_access.get_all_project_accesses(emp_id)  # Get all project accesses
        access = access_result if access_result else []
        
        # Prepare response data
        user_data = {
            'employee_id': emp_id,
            'title': user.get('title', ''),  # Get title from the database
            'first_name': user.get('first_name', ''),
            'last_name': user.get('last_name', ''),
            'units': units,
            'department': user.get('department', ''),
            'access': access
        }
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': user_data
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Handle user signup"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['empId', 'title', 'firstName', 'lastName', 'email', 'password']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({'status': 'error', 'message': f'{field.replace("Id", " ID").replace("firstName", "First Name").replace("lastName", "Last Name").replace("title", "Title")} is required'}), 400
        
        # Validate email format
        email = data['email'].strip()
        email_pattern = r'^[^@]+@violintec\.com$'
        if not re.match(email_pattern, email):
            return jsonify({'status': 'error', 'message': 'Email must be in @violintec.com domain'}), 400
        
        # Check if email or employee ID already exists
        emp_id = data['empId']  # No need to convert to int since it's varchar
        
        # Check if employee ID already exists
        # Try different common column names for employee ID
        try:
            check_emp_query = "SELECT id, emp_id, employee_id FROM user_master WHERE id = %s OR employee_id = %s OR emp_id = %s LIMIT 1"
            existing_emp = user_master.sql_processor.db.execute_query(check_emp_query, (emp_id, emp_id, emp_id))
            
            if existing_emp:
                return jsonify({'status': 'error', 'message': 'Employee ID already exists'}), 400
        except Exception as e:
            # If the query fails due to column names, try simpler approach
            try:
                check_emp_query = "SELECT * FROM user_master LIMIT 1"  # Just test if table exists
                user_master.sql_processor.db.execute_query(check_emp_query)
                # If this works, try to find by email only
                check_email_query = "SELECT * FROM user_master WHERE email = %s LIMIT 1"
                existing_email = user_master.sql_processor.db.execute_query(check_email_query, (email,))
                
                if existing_email:
                    return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
            except Exception as e2:
                return jsonify({'status': 'error', 'message': 'Database access error'}), 500
        
        # Check if email already exists
        try:
            check_email_query = "SELECT id, emp_id, employee_id FROM user_master WHERE email = %s LIMIT 1"
            existing_email = user_master.sql_processor.db.execute_query(check_email_query, (email,))
            
            if existing_email:
                return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
        except Exception as e:
            # If query fails due to column names, skip this check
            print(f"Email check failed: {str(e)}")
            pass
        
        # In a real application, you'd hash the password here
        # password_hash = hash_password(data['password'])
        
        # Insert new user based on the actual table structure
        # According to DESCRIBE: employee_id(PRI), title, first_name, last_name, email(UNI), password_hash, department, left_date, username, active_status
        # Required fields: employee_id, title, first_name, last_name, email, password_hash
        
        # Hash the password (using a simple approach for now - in production use proper hashing)
        import hashlib
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        try:
            # Insert with the actual required fields based on table structure
            insert_query = "INSERT INTO user_master (employee_id, title, first_name, last_name, email, password_hash, department, username, active_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            result = user_master.sql_processor.db.execute_non_query(insert_query, (
                emp_id,  # This is the primary key
                data['title'],  # Title field (enum: Mr, Miss, Mrs)
                data['firstName'],
                data['lastName'],
                email,
                password_hash,  # Need to add password hash
                'General',  # Default department
                f"emp_{str(emp_id)}",  # Username
                1  # Active status
            ))
        except Exception as e:
            # If the insert fails, it could be due to duplicate employee_id or email
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                if emp_id in error_msg:
                    return jsonify({'status': 'error', 'message': 'Employee ID already exists'}), 400
                elif email in error_msg:
                    return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
                else:
                    return jsonify({'status': 'error', 'message': 'Employee ID or Email already exists'}), 400
            else:
                # More detailed error logging
                print(f"Signup insert error: {error_msg}")
                return jsonify({'status': 'error', 'message': f'Database error during registration: {error_msg}'}), 500
        
        if not result:
            return jsonify({'status': 'error', 'message': 'Failed to create account due to database constraints. Please check that the Employee ID or Email is not already in use.'}), 500
        
        # If project access data is provided, insert into authentication table
        if 'access' in data and isinstance(data['access'], list):
            for access_item in data['access']:
                if 'projectCode' in access_item and 'authType' in access_item:
                    try:
                        # Insert access permissions into authentication table
                        auth_query = "INSERT INTO authentication (employee_id, project_code, auth_type, status) VALUES (%s, %s, %s, %s)"
                        auth_result = user_master.sql_processor.db.execute_non_query(auth_query, (
                            emp_id,
                            access_item['projectCode'],
                            access_item['authType'],
                            1  # Active status
                        ))
                    except Exception as auth_error:
                        print(f"Error inserting authentication record: {str(auth_error)}")
                        # Continue processing even if auth insertion fails
        
        if result:
            return jsonify({'status': 'success', 'message': 'Account created successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create account'}), 500
            
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)