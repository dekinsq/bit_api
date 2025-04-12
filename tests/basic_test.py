#!/usr/bin/env python3
"""
Basic test for Bitnet API Python SDK entities
"""

from bitnet_api import (
    BitnetClient, BaseResponse, BrowserFingerPrint, Browser, Group, 
    PageInfo, BrowserListResponse, GroupListResponse, 
    HealthResponse, BrowserResponse, GroupResponse, 
    ProxyCheckInfo, ProxyCheckResponse, BrowserPidInfo, 
    BrowserPidResponse, GenericResponse
)

def test_entity_creation():
    """Test that all entity classes can be instantiated correctly"""
    print("Testing entity creation...")
    
    # Test BaseResponse
    base_resp = BaseResponse(success=True, msg="Success")
    print(f"BaseResponse: {base_resp}")
    assert base_resp.success == True
    assert base_resp.msg == "Success"
    
    # Test BrowserFingerPrint
    fingerprint = BrowserFingerPrint(
        core_version="104",
        os="windows",
        os_version="10"
    )
    print(f"BrowserFingerPrint: {fingerprint}")
    assert fingerprint.core_version == "104"
    assert fingerprint.os == "windows"
    assert fingerprint.os_version == "10"
    
    # Test to_dict() method
    fingerprint_dict = fingerprint.to_dict()
    print(f"BrowserFingerPrint.to_dict(): {fingerprint_dict}")
    assert fingerprint_dict["coreVersion"] == "104"
    assert fingerprint_dict["os"] == "windows"
    assert fingerprint_dict["osVersion"] == "10"
    
    # Test from_dict() method
    fingerprint2 = BrowserFingerPrint.from_dict({
        "coreVersion": "110",
        "os": "linux",
        "osVersion": "ubuntu"
    })
    print(f"BrowserFingerPrint.from_dict(): {fingerprint2}")
    assert fingerprint2.core_version == "110"
    assert fingerprint2.os == "linux"
    assert fingerprint2.os_version == "ubuntu"
    
    # Test Browser
    browser = Browser(
        id="test-browser-id",
        name="Test Browser",
        seq=1,
        group_id="test-group-id",
        browser_finger_print=fingerprint
    )
    print(f"Browser: {browser}")
    assert browser.id == "test-browser-id"
    assert browser.name == "Test Browser"
    assert browser.browser_finger_print.core_version == "104"
    
    # Test Group
    group = Group(
        id="test-group-id",
        group_name="Test Group",
        sort_num=1
    )
    print(f"Group: {group}")
    assert group.id == "test-group-id"
    assert group.group_name == "Test Group"
    
    # Test PageInfo
    page_info = PageInfo(
        total_elements=100,
        total_pages=10,
        number=0,
        size=10
    )
    print(f"PageInfo: {page_info}")
    assert page_info.total_elements == 100
    assert page_info.size == 10
    
    # Test more complex response objects
    browser_response = BrowserResponse(
        success=True,
        msg="Success",
        data=browser
    )
    print(f"BrowserResponse: {browser_response}")
    assert browser_response.success == True
    assert browser_response.data.id == "test-browser-id"
    
    print("\nAll entity tests passed successfully!")
    return True

def test_fingerprint_conversions():
    """Test converting between fingerprint objects and dictionaries"""
    print("\nTesting fingerprint conversion...")
    
    # Create a fingerprint object
    fingerprint = BrowserFingerPrint(
        core_version="104",
        os="windows",
        os_version="10"
    )
    
    # Convert to dictionary
    fingerprint_dict = fingerprint.to_dict()
    print(f"Original fingerprint: {fingerprint}")
    print(f"As dictionary: {fingerprint_dict}")
    
    # Convert back to object
    fingerprint2 = BrowserFingerPrint.from_dict(fingerprint_dict)
    print(f"Converted back to object: {fingerprint2}")
    
    # Verify values match
    assert fingerprint.core_version == fingerprint2.core_version
    assert fingerprint.os == fingerprint2.os
    assert fingerprint.os_version == fingerprint2.os_version
    
    print("Fingerprint conversion test passed!")
    return True

def main():
    """Run all tests"""
    print("==== Bitnet API SDK Entity Tests ====\n")
    
    try:
        test_entity_creation()
        test_fingerprint_conversions()
        
        print("\n==== All tests passed successfully! ====")
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main() 