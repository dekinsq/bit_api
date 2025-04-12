#!/usr/bin/env python3
"""
Client test for Bitnet API Python SDK with mock server
"""

import time
import sys
import os
from bitnet_api import BitnetClient, BrowserFingerPrint
from mock_server import MockServer

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_health_check(client):
    """Test health check API"""
    print("\n=== Testing Health Check API ===")
    response = client.health_check()
    print(f"Health check response: {response}")
    assert response.success is True
    print("Health check test passed!")


def test_browser_management(client):
    """Test browser management APIs"""
    print("\n=== Testing Browser Management APIs ===")
    
    # Test create browser
    print("\nCreating a browser...")
    fingerprint = BrowserFingerPrint(
        core_version="104",
        os="windows",
        os_version="10"
    )
    create_response = client.create_or_update_browser(
        browser_fingerprint=fingerprint,
        proxy_type="noproxy"
    )
    print(f"Create response: {create_response}")
    assert create_response.success is True
    assert create_response.data is not None
    browser_id = create_response.data.id
    print(f"Created browser with ID: {browser_id}")
    
    # Test get browser detail
    print("\nGetting browser details...")
    detail_response = client.get_browser_detail(id=browser_id)
    print(f"Detail response: {detail_response}")
    assert detail_response.success is True
    assert detail_response.data is not None
    assert detail_response.data.id == browser_id
    print("Browser detail test passed!")
    
    # Test update browser
    print("\nUpdating browser...")
    update_response = client.create_or_update_browser(
        id=browser_id,
        proxy_type="http",
        host="example.com",
        port="8080",
        proxy_username="user",
        proxy_password="pass",
        browser_fingerprint=fingerprint
    )
    print(f"Update response: {update_response}")
    assert update_response.success is True
    assert update_response.data is not None
    assert update_response.data.id == browser_id
    assert update_response.data.proxy_type == "http"
    print("Browser update test passed!")
    
    # Test open browser
    print("\nOpening browser...")
    open_response = client.open_browser(id=browser_id)
    print(f"Open response: {open_response}")
    assert open_response.success is True
    assert open_response.data is not None
    assert open_response.data.ws is not None
    assert open_response.data.http is not None
    print("Browser open test passed!")
    
    # Test list browsers
    print("\nListing browsers...")
    list_response = client.browser_list()
    print(f"List response: {list_response}")
    assert list_response.success is True
    assert list_response.content is not None
    assert len(list_response.content) > 0
    print("Browser list test passed!")
    
    # Test close browser
    print("\nClosing browser...")
    close_response = client.close_browser(id=browser_id)
    print(f"Close response: {close_response}")
    assert close_response.success is True
    print("Browser close test passed!")
    
    # Test delete browser
    print("\nDeleting browser...")
    delete_response = client.delete_browser(id=browser_id)
    print(f"Delete response: {delete_response}")
    assert delete_response.success is True
    print("Browser delete test passed!")
    
    print("\nAll browser management tests passed!")


def test_group_management(client):
    """Test group management APIs"""
    print("\n=== Testing Group Management APIs ===")
    
    # Test create group
    print("\nCreating a group...")
    group_name = f"Test Group {int(time.time())}"
    create_response = client.add_group(group_name=group_name)
    print(f"Create response: {create_response}")
    assert create_response.success is True
    assert create_response.data is not None
    group_id = create_response.data.id
    assert create_response.data.group_name == group_name
    print(f"Created group with ID: {group_id}")
    
    # Test get group detail
    print("\nGetting group details...")
    detail_response = client.get_group_detail(id=group_id)
    print(f"Detail response: {detail_response}")
    assert detail_response.success is True
    assert detail_response.data is not None
    assert detail_response.data.id == group_id
    print("Group detail test passed!")
    
    # Test list groups
    print("\nListing groups...")
    list_response = client.get_group_list()
    print(f"List response: {list_response}")
    assert list_response.success is True
    assert list_response.content is not None
    assert len(list_response.content) > 0
    print("Group list test passed!")
    
    # Test delete group
    print("\nDeleting group...")
    delete_response = client.delete_group(id=group_id)
    print(f"Delete response: {delete_response}")
    assert delete_response.success is True
    print("Group delete test passed!")
    
    print("\nAll group management tests passed!")


def test_proxy_check(client):
    """Test proxy check API"""
    print("\n=== Testing Proxy Check API ===")
    
    response = client.check_proxy(
        host="example.com",
        port=8080,
        proxy_type="http",
        proxy_username="user",
        proxy_password="pass"
    )
    print(f"Proxy check response: {response}")
    assert response.success is True
    assert response.data is not None
    assert response.data.ip is not None
    assert response.data.country_name is not None
    
    print("Proxy check test passed!")


def main():
    """Run all client tests"""
    print("==== Bitnet API Client Tests ====\n")
    
    # Start the mock server
    server = MockServer(port=55055)
    try:
        server.start()
        time.sleep(1)  # Give the server time to start
        
        # Create a client
        client = BitnetClient(host="127.0.0.1", port=55055)
        
        # Run tests
        try:
            test_health_check(client)
            test_browser_management(client)
            test_group_management(client)
            test_proxy_check(client)
            print("\n==== All client tests passed successfully! ====")
        except AssertionError as e:
            print(f"\nTest failed: {e}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")
    finally:
        server.stop()


if __name__ == "__main__":
    main() 