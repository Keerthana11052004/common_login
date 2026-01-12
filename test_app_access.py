from app_access import AppAccess

def test_app_access():
    """Test the app access functionality"""
    app_access = AppAccess()
    
    # Example usage:
    print("Testing App Access functionality:")
    
    # Get project accesses for an employee
    # accesses = app_access.get_project_accesses(1, "project1")
    # print(f"Project Accesses: {accesses}")
    
    # Check if project is allowed for an employee
    # allowed = app_access.is_project_allowed(1, "project1")
    # print(f"Project Allowed: {allowed}")
    
    # Grant project access to an employee
    # result = app_access.grant_project_access(1, "project1", "read")
    # print(f"Grant Access Result: {result}")

if __name__ == "__main__":
    test_app_access()