## Bitnet API Python SDK

Python SDK for interacting with the Bitnet Browser API, providing clean entity-based objects instead of raw dictionaries.

### Key Features
- Complete API wrapper with typed response objects
- Comprehensive documentation and examples
- Supports browser & window management, grouping, and proxy testing
- Simple error handling and type hints

### Quick Start
```bash
pip install bitnet-api
```
```python
from bitnet_api import BitnetClient

client = BitnetClient(host="127.0.0.1", port=54345)
response = client.health_check()
if response.success:
    print("API is connected!")
```

### Documentation
See the [full documentation](README.md) for detailed usage examples. 