from typing import Dict, List, Optional, Any
from sql_processor import SQLProcessor
import json

class UnitMaster:
    """Business logic for unit master operations"""
    
    def __init__(self):
        self.sql_processor = SQLProcessor()
    
    def get_unit_description(self, unit_code: str) -> Optional[str]:
        """Get unit description by unit code"""
        return self.sql_processor.get_unit_description(unit_code)
    
    def get_unit_description_json(self, unit_code: str) -> str:
        """Get unit description in JSON format"""
        description = self.get_unit_description(unit_code)
        if description is not None:
            return json.dumps({'unit_code': unit_code, 'description': description})
        return json.dumps({'unit_code': unit_code, 'description': None})