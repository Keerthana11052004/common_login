from user_master import UserMaster
import json

def test_user_master():
    """Test the user master functionality"""
    user_master = UserMaster()
    
    # Example usage:
    print("Testing User Master functionality:")
    
    # Get username by ID (replace 1 with actual user ID from your database)
    # username = user_master.get_username(1)
    # print(f"Username: {username}")
    
    # Get full name by ID
    # full_name = user_master.get_full_name(1)
    # print(f"Full Name: {full_name}")
    
    # Get department by ID
    # department = user_master.get_department(1)
    # print(f"Department: {department}")
    
    # Get left date by ID
    # left_date = user_master.get_left_date(1)
    # print(f"Left Date: {left_date}")
    
    # Get all users data in JSON format
    # all_users_json = user_master.get_all_users()
    # print(f"All Users: {all_users_json}")
    
    # Get specific user data by ID in JSON format
    # user_json = user_master.get_user_by_id(1)
    # print(f"User Data: {user_json}")
    
    # Edit master data
    # result = user_master.edit_master_data(1, username="new_username", department="IT")
    # print(f"Update successful: {result}")
    
    # Check and update user status based on left date
    # status_updated = user_master.update_user_status_based_on_left_date()
    # print(f"Status updated: {status_updated}")

if __name__ == "__main__":
    test_user_master()