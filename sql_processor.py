import mysql.connector
from mysql.connector import Error
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

class DatabaseConnection:
    """Database connection handler for MySQL operations"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'common_login')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'Violin@12')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None
    
    def connect(self):
        """Create a database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[List[Dict]]:
        """Execute a SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            if self.connection:
                cursor = self.connection.cursor(dictionary=True)
            else:
                return None
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            cursor.close()
            # Type check disabled for fetchall result
            return result  # type: ignore
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_non_query(self, query: str, params: Optional[tuple] = None) -> bool:
        """Execute an INSERT, UPDATE, or DELETE query"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            if self.connection:
                cursor = self.connection.cursor()
            else:
                return False
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if self.connection:
                self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing non-query: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def close_connection(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")


class SQLProcessor:
    """Handles SQL operations for user master"""
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_username(self, user_id: int) -> Optional[str]:
        """Get username by user ID"""
        query = "SELECT username FROM user_master WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        if result and len(result) > 0:
            return result[0]['username']
        return None
    
    def get_full_name(self, user_id: int) -> Optional[Dict[str, str]]:
        """Get first name and last name by user ID"""
        query = "SELECT first_name, last_name FROM user_master WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        if result and len(result) > 0:
            return {
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name']
            }
        return None
    
    def get_department(self, user_id: int) -> Optional[str]:
        """Get department by user ID"""
        query = "SELECT department FROM user_master WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        if result and len(result) > 0:
            return result[0]['department']
        return None
    
    def get_left_date(self, user_id: int) -> Optional[str]:
        """Get left date by user ID"""
        query = "SELECT left_date FROM user_master WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        if result and len(result) > 0:
            return str(result[0]['left_date']) if result[0]['left_date'] else None
        return None
    
    def get_user_data(self, user_id: Optional[int] = None) -> Optional[List[Dict]]:
        """Get all user data in JSON format"""
        if user_id:
            query = "SELECT * FROM user_master WHERE id = %s"
            params = (user_id,)
        else:
            query = "SELECT * FROM user_master"
            params = None
        
        result = self.db.execute_query(query, params)
        return result
    
    def update_user_master(self, user_id: int, **kwargs) -> bool:
        """Update user master data"""
        # Build dynamic update query
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['username', 'first_name', 'last_name', 'department', 'left_date', 'active_status']:
                fields.append(f"{key} = %s")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(user_id)  # For WHERE clause
        query = f"UPDATE user_master SET {', '.join(fields)} WHERE id = %s"
        
        return self.db.execute_non_query(query, tuple(values))
    
    def check_and_update_user_status(self) -> bool:
        """Check left date and update user status from active to inactive if left date has passed"""
        try:
            # Get all users with left_date set
            query = "SELECT id, left_date, active_status FROM user_master WHERE left_date IS NOT NULL"
            result = self.db.execute_query(query)
            
            if not result:
                return True
            
            today = datetime.now().date()
            updated_count = 0
            
            for user in result:
                if user['left_date'] and user['active_status'] == 1:  # If user is currently active
                    left_date = user['left_date'] if isinstance(user['left_date'], datetime) else datetime.strptime(str(user['left_date']), '%Y-%m-%d').date()
                    
                    if left_date <= today:
                        # Update user status to inactive
                        update_query = "UPDATE user_master SET active_status = 0 WHERE id = %s"
                        if self.db.execute_non_query(update_query, (user['id'],)):
                            updated_count += 1
            
            print(f"Updated {updated_count} users to inactive status based on left date")
            return True
        except Exception as e:
            print(f"Error checking and updating user status: {e}")
            return False
    
    def get_employee_units(self, emp_id: int) -> Optional[str]:
        """Get units for an employee using '|' as separator"""
        query = "SELECT units FROM employee_unit WHERE emp_id = %s"
        result = self.db.execute_query(query, (emp_id,))
        if result and len(result) > 0:
            return result[0]['units']
        return None
    
    def add_employee_units(self, emp_id: int, units: List[str]) -> bool:
        """Add units to an employee"""
        # Get current units
        current_units_str = self.get_employee_units(emp_id)
        
        if current_units_str:
            current_units = current_units_str.split('|')
        else:
            current_units = []
        
        # Add new units that are not already present
        for unit in units:
            if unit not in current_units:
                current_units.append(unit)
        
        # Join units with '|'
        new_units_str = '|'.join(current_units)
        
        # Update the database
        query = "UPDATE employee_unit SET units = %s WHERE emp_id = %s"
        return self.db.execute_non_query(query, (new_units_str, emp_id))
    
    def get_unit_description(self, unit_code: str) -> Optional[str]:
        """Get unit description by unit code"""
        query = "SELECT description FROM unit_master WHERE unit_code = %s"
        result = self.db.execute_query(query, (unit_code,))
        if result and len(result) > 0:
            return result[0]['description']
        return None
    
    def get_project_accesses(self, emp_id: int, project: str) -> Optional[List[Dict]]:
        """Get project accesses for an employee"""
        query = "SELECT emp_id, project, auth_type FROM app_access WHERE emp_id = %s AND project = %s"
        return self.db.execute_query(query, (emp_id, project))
    
    def is_project_allowed(self, emp_id: int, project: str) -> bool:
        """Check if a project is allowed for an employee (at least one access exists)"""
        query = "SELECT COUNT(*) as count FROM app_access WHERE emp_id = %s AND project = %s"
        result = self.db.execute_query(query, (emp_id, project))
        if result and len(result) > 0:
            return result[0]['count'] > 0
        return False
    
    def grant_project_access(self, emp_id: int, project: str, auth_type: str) -> bool:
        """Grant project access to an employee with specific auth type"""
        # Check if access already exists
        query = "SELECT id FROM app_access WHERE emp_id = %s AND project = %s AND auth_type = %s"
        result = self.db.execute_query(query, (emp_id, project, auth_type))
        
        if result and len(result) > 0:
            # Update existing access
            query = "UPDATE app_access SET auth_type = %s WHERE emp_id = %s AND project = %s AND auth_type = %s"
            return self.db.execute_non_query(query, (auth_type, emp_id, project, auth_type))
        else:
            # Insert new access
            query = "INSERT INTO app_access (emp_id, project, auth_type) VALUES (%s, %s, %s)"
            return self.db.execute_non_query(query, (emp_id, project, auth_type))
    
    def get_all_project_accesses(self, emp_id: int) -> Optional[List[Dict]]:
        """Get all project accesses for an employee"""
        query = "SELECT emp_id, project, auth_type FROM app_access WHERE emp_id = %s"
        return self.db.execute_query(query, (emp_id,))
    
    def remove_employee_units(self, emp_id: int, units_to_remove: List[str]) -> bool:
        """Remove units from an employee"""
        # Get current units
        current_units_str = self.get_employee_units(emp_id)
        
        if not current_units_str:
            return True  # Nothing to remove
        
        current_units = current_units_str.split('|')
        
        # Remove specified units
        for unit in units_to_remove:
            if unit in current_units:
                current_units.remove(unit)
        
        # Join remaining units with '|'
        new_units_str = '|'.join(current_units)
        
        # Update the database
        query = "UPDATE employee_unit SET units = %s WHERE emp_id = %s"
        return self.db.execute_non_query(query, (new_units_str, emp_id))