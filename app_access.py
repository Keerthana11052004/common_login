from typing import Dict, List, Optional, Any
from sql_processor import SQLProcessor
import json

class AppAccess:
    """Business logic for app access (authentication) operations"""
    
    def __init__(self):
        self.sql_processor = SQLProcessor()
    
    def get_project_accesses(self, emp_id: int, project: str) -> Optional[List[Dict]]:
        """Get project accesses for an employee"""
        return self.sql_processor.get_project_accesses(emp_id, project)
    
    def get_all_project_accesses(self, emp_id: int) -> Optional[List[Dict]]:
        """Get all project accesses for an employee"""
        return self.sql_processor.get_all_project_accesses(emp_id)
    
    def is_project_allowed(self, emp_id: int, project: str) -> bool:
        """Check if a project is allowed for an employee (at least one access exists)"""
        return self.sql_processor.is_project_allowed(emp_id, project)
    
    def grant_project_access(self, emp_id: int, project: str, auth_type: str) -> bool:
        """Grant project access to an employee with specific auth type"""
        return self.sql_processor.grant_project_access(emp_id, project, auth_type)
    
    def get_project_accesses_json(self, emp_id: int, project: str) -> str:
        """Get project accesses in JSON format"""
        accesses = self.get_project_accesses(emp_id, project)
        if accesses is not None:
            return json.dumps({'emp_id': emp_id, 'project': project, 'accesses': accesses})
        return json.dumps({'emp_id': emp_id, 'project': project, 'accesses': []})
    
    def get_project_allowed_json(self, emp_id: int, project: str) -> str:
        """Get project allowed status in JSON format"""
        allowed = self.is_project_allowed(emp_id, project)
        return json.dumps({'emp_id': emp_id, 'project': project, 'allowed': allowed})