from unit_master import UnitMaster

def test_unit_master():
    """Test the unit master functionality"""
    unit_master = UnitMaster()
    
    # Example usage:
    print("Testing Unit Master functionality:")
    
    # Get unit description by unit code
    # description = unit_master.get_unit_description("HR001")
    # print(f"Unit Description: {description}")
    
    # Get unit description in JSON format
    # description_json = unit_master.get_unit_description_json("HR001")
    # print(f"Unit Description JSON: {description_json}")

if __name__ == "__main__":
    test_unit_master()