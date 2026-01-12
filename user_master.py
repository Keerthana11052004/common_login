import json
from typing import Dict, List, Optional, Any, Union
from sql_processor import SQLProcessor
from datetime import datetime

class UserMaster:
    """Business logic for user master operations"""
    
    def __init__(self):
        self.sql_processor = SQLProcessor()
    
    def get_username(self, user_id: int) -> Optional[str]:
        """Get username by user ID"""
        return self.sql_processor.get_username(user_id)
    
    def get_full_name(self, user_id: int) -> Optional[Dict[str, str]]:
        """Get full name (first name and last name) by user ID"""
        return self.sql_processor.get_full_name(user_id)
    
    def get_department(self, user_id: int) -> Optional[str]:
        """Get department by user ID"""
        return self.sql_processor.get_department(user_id)
    
    def get_left_date(self, user_id: int) -> Optional[str]:
        """Get left date by user ID"""
        return self.sql_processor.get_left_date(user_id)
    
    def get_user_data_json(self, user_id: Optional[int] = None) -> str:
        """Get user data in JSON format"""
        user_data = self.sql_processor.get_user_data(user_id)
        if user_data is not None:
            return json.dumps(user_data, default=str, ensure_ascii=False)
        return json.dumps([])
    
    def edit_master_data(self, user_id: int, **kwargs) -> bool:
        """Edit user master data"""
        return self.sql_processor.update_user_master(user_id, **kwargs)
    
    def check_and_update_user_status(self) -> bool:
        """Automatically update user status from active to inactive if left date has passed"""
        return self.sql_processor.check_and_update_user_status()
    
    def get_all_users(self) -> str:
        """Get all users data in JSON format"""
        return self.get_user_data_json()
    
    def get_user_by_id(self, user_id: int) -> str:
        """Get specific user data by ID in JSON format"""
        return self.get_user_data_json(user_id)
    
    def update_user_status_based_on_left_date(self) -> bool:
        """Public method to check and update user status based on left date"""
        return self.check_and_update_user_status()