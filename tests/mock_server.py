#!/usr/bin/env python3
"""
Mock HTTP server to simulate Bitnet API for testing
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
import uuid
import time
import threading


class MockBitnetAPIHandler(BaseHTTPRequestHandler):
    """Mock HTTP request handler for Bitnet API"""
    
    # Store some data for the mock API
    browsers = {
        "test-browser-1": {
            "id": "test-browser-1",
            "name": "Test Browser 1",
            "remark": "For testing",
            "seq": 1,
            "groupId": "test-group-1",
            "ws": "ws://127.0.0.1:12345/abc",
            "http": "127.0.0.1:12345",
            "coreVersion": "104",
            "pid": 12345,
            "browserFingerPrint": {
                "coreVersion": "104",
                "os": "windows",
                "osVersion": "10"
            }
        }
    }
    
    groups = {
        "test-group-1": {
            "id": "test-group-1",
            "groupName": "Test Group 1",
            "sortNum": 1
        }
    }
    
    def _set_headers(self):
        """Set common headers for all responses"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    
    def do_POST(self):
        """Handle all POST requests"""
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        request_json = {}
        
        try:
            if content_length > 0:
                request_json = json.loads(request_data.decode('utf-8'))
        except json.JSONDecodeError:
            self._send_error("Invalid JSON")
            return
        
        path = urlparse(self.path).path
        
        # Route requests to appropriate handlers
        handlers = {
            '/health': self._handle_health,
            '/browser/update': self._handle_browser_update,
            '/browser/list': self._handle_browser_list,
            '/browser/list/concise': self._handle_browser_list,
            '/browser/detail': self._handle_browser_detail,
            '/browser/open': self._handle_browser_open,
            '/browser/close': self._handle_browser_close,
            '/browser/delete': self._handle_browser_delete,
            '/group/add': self._handle_group_add,
            '/group/list': self._handle_group_list,
            '/group/detail': self._handle_group_detail,
            '/group/delete': self._handle_group_delete,
            '/checkagent': self._handle_check_agent
        }
        
        if path in handlers:
            handlers[path](request_json)
        else:
            self._send_error(f"Unsupported endpoint: {path}")
    
    def _send_success(self, data=None):
        """Send a success response"""
        self._set_headers()
        response = {
            "success": True,
            "data": data
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _send_error(self, message):
        """Send an error response"""
        self._set_headers()
        response = {
            "success": False,
            "msg": message
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_health(self, request_data):
        """Handle health check endpoint"""
        self._send_success({"message": "API is healthy"})
    
    def _handle_browser_update(self, request_data):
        """Handle browser update (create or update) endpoint"""
        browser_id = request_data.get("id")
        
        # Create new browser if ID is not provided
        if not browser_id:
            browser_id = str(uuid.uuid4())
        
        self.browsers[browser_id] = {
            "id": browser_id,
            "name": request_data.get("name", ""),
            "remark": request_data.get("remark", ""),
            "seq": len(self.browsers) + 1,
            "groupId": request_data.get("groupId", ""),
            "proxyMethod": request_data.get("proxyMethod", 2),
            "proxyType": request_data.get("proxyType", "noproxy"),
            "host": request_data.get("host", ""),
            "port": request_data.get("port", ""),
            "proxyUserName": request_data.get("proxyUserName", ""),
            "proxyPassword": request_data.get("proxyPassword", ""),
            "browserFingerPrint": request_data.get("browserFingerPrint", {})
        }
        
        self._send_success(self.browsers[browser_id])
    
    def _handle_browser_list(self, request_data):
        """Handle browser list endpoint"""
        page = request_data.get("page", 0)
        page_size = request_data.get("pageSize", 10)
        group_id = request_data.get("groupId")
        
        browser_list = list(self.browsers.values())
        
        # Filter by group if specified
        if group_id:
            browser_list = [b for b in browser_list if b.get("groupId") == group_id]
        
        # Handle pagination
        start_idx = page * page_size
        end_idx = start_idx + page_size
        content = browser_list[start_idx:end_idx]
        
        result = {
            "content": content,
            "totalElements": len(browser_list),
            "totalPages": (len(browser_list) + page_size - 1) // page_size,
            "number": page,
            "size": page_size
        }
        
        self._send_success(result)
    
    def _handle_browser_detail(self, request_data):
        """Handle browser detail endpoint"""
        browser_id = request_data.get("id")
        if browser_id in self.browsers:
            self._send_success(self.browsers[browser_id])
        else:
            self._send_error(f"Browser not found: {browser_id}")
    
    def _handle_browser_open(self, request_data):
        """Handle browser open endpoint"""
        browser_id = request_data.get("id")
        if browser_id in self.browsers:
            browser = self.browsers[browser_id]
            # Add runtime information
            browser["ws"] = f"ws://127.0.0.1:12345/{uuid.uuid4()}"
            browser["http"] = "127.0.0.1:12345"
            browser["pid"] = 10000 + int(time.time()) % 10000
            self._send_success(browser)
        else:
            self._send_error(f"Browser not found: {browser_id}")
    
    def _handle_browser_close(self, request_data):
        """Handle browser close endpoint"""
        browser_id = request_data.get("id")
        if browser_id in self.browsers:
            # Just remove runtime information
            browser = self.browsers[browser_id]
            if "ws" in browser:
                del browser["ws"]
            if "http" in browser:
                del browser["http"]
            if "pid" in browser:
                del browser["pid"]
            self._send_success()
        else:
            self._send_error(f"Browser not found: {browser_id}")
    
    def _handle_browser_delete(self, request_data):
        """Handle browser delete endpoint"""
        browser_id = request_data.get("id")
        if browser_id in self.browsers:
            del self.browsers[browser_id]
            self._send_success()
        else:
            self._send_error(f"Browser not found: {browser_id}")
    
    def _handle_group_add(self, request_data):
        """Handle group add endpoint"""
        group_name = request_data.get("groupName", "")
        sort_num = request_data.get("sortNum", 0)
        group_id = str(uuid.uuid4())
        
        self.groups[group_id] = {
            "id": group_id,
            "groupName": group_name,
            "sortNum": sort_num
        }
        
        self._send_success(self.groups[group_id])
    
    def _handle_group_list(self, request_data):
        """Handle group list endpoint"""
        page = request_data.get("page", 0)
        page_size = request_data.get("pageSize", 10)
        
        group_list = list(self.groups.values())
        
        # Handle pagination
        start_idx = page * page_size
        end_idx = start_idx + page_size
        content = group_list[start_idx:end_idx]
        
        result = {
            "content": content,
            "totalElements": len(group_list),
            "totalPages": (len(group_list) + page_size - 1) // page_size,
            "number": page,
            "size": page_size
        }
        
        self._send_success(result)
    
    def _handle_group_detail(self, request_data):
        """Handle group detail endpoint"""
        group_id = request_data.get("id")
        if group_id in self.groups:
            self._send_success(self.groups[group_id])
        else:
            self._send_error(f"Group not found: {group_id}")
    
    def _handle_group_delete(self, request_data):
        """Handle group delete endpoint"""
        group_id = request_data.get("id")
        if group_id in self.groups:
            del self.groups[group_id]
            self._send_success()
        else:
            self._send_error(f"Group not found: {group_id}")
    
    def _handle_check_agent(self, request_data):
        """Handle proxy check endpoint"""
        # Always return a successful proxy check
        proxy_info = {
            "success": True,
            "data": {
                "ip": "1.2.3.4",
                "countryName": "United States",
                "stateProv": "California",
                "countryCode": "US",
                "region": "CA",
                "city": "San Francisco",
                "languages": "en-US",
                "timeZone": "America/Los_Angeles",
                "offset": "-7",
                "longitude": "-122.4194",
                "latitude": "37.7749",
                "zip": "94102",
                "status": 1,
                "used": False,
                "usedTime": None
            }
        }
        self._send_success(proxy_info)


class MockServer:
    """Mock HTTP server for Bitnet API"""
    
    def __init__(self, host="127.0.0.1", port=55055):
        self.host = host
        self.port = port
        self.server = HTTPServer((host, port), MockBitnetAPIHandler)
        self.server_thread = None
    
    def start(self):
        """Start the server in a background thread"""
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"Mock Bitnet API server started at http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Mock Bitnet API server stopped")


if __name__ == "__main__":
    # Run the mock server directly
    server = MockServer()
    server.start()
    
    try:
        print("Press Ctrl+C to stop the server...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop() 