from typing import Dict, List, Optional, Any
from sql_processor import SQLProcessor
import json

class EmployeeUnit:
    """Business logic for employee unit operations"""
    
    def __init__(self):
        self.sql_processor = SQLProcessor()
    
    def get_units(self, emp_id: int) -> Optional[str]:
        """Get units for an employee using '|' as separator"""
        return self.sql_processor.get_employee_units(emp_id)
    
    def add_units(self, emp_id: int, units: List[str]) -> bool:
        """Add units to an employee"""
        return self.sql_processor.add_employee_units(emp_id, units)
    
    def remove_units(self, emp_id: int, units: List[str]) -> bool:
        """Remove units from an employee"""
        return self.sql_processor.remove_employee_units(emp_id, units)
    
    def get_units_json(self, emp_id: int) -> str:
        """Get employee units in JSON format"""
        units_str = self.get_units(emp_id)
        if units_str is not None:
            units_list = units_str.split('|') if units_str else []
            return json.dumps({'emp_id': emp_id, 'units': units_list})
        return json.dumps({'emp_id': emp_id, 'units': []})
    
    def get_units_raw(self, emp_id: int) -> Optional[str]:
        """Get raw units string for an employee"""
        return self.get_units(emp_id)