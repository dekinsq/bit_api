## 🚀 Bitnet API Python SDK

### Simple, type-safe API client for Bitnet Browser

```python
from bitnet_api import BitnetClient, BrowserFingerPrint

# Initialize client
client = BitnetClient(host="127.0.0.1", port=54345)

# Create a browser with custom fingerprint
fingerprint = BrowserFingerPrint(
    core_version="104",
    os="windows",
    os_version="10"
)

# Create and open a browser
browser_resp = client.create_or_update_browser(browser_fingerprint=fingerprint)
if browser_resp.success:
    browser_id = browser_resp.data.id
    open_resp = client.open_browser(id=browser_id)
    print(f"Browser opened with WebSocket URL: {open_resp.data.ws}")
```

### Key Features

✅ Entity-based responses with proper typing  
✅ Complete API coverage for all Bitnet endpoints  
✅ Comprehensive error handling  
✅ Example scripts and thorough documentation

### Installation

```bash
pip install bitnet-api
``` 