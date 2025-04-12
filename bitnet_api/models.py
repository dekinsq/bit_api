from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class BaseResponse:
    """Base class for all API responses"""
    success: bool
    msg: Optional[str] = None


@dataclass
class BrowserFingerPrint:
    """Browser fingerprint configuration"""
    core_version: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserFingerPrint':
        """Create a BrowserFingerPrint object from API response dictionary"""
        if not data:
            return cls()
        
        return cls(
            core_version=data.get('coreVersion'),
            os=data.get('os'),
            os_version=data.get('osVersion')
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API requests"""
        result = {}
        if self.core_version:
            result['coreVersion'] = self.core_version
        if self.os:
            result['os'] = self.os
        if self.os_version:
            result['osVersion'] = self.os_version
        return result


@dataclass
class Browser:
    """Browser window details"""
    id: Optional[str] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    seq: Optional[int] = None
    group_id: Optional[str] = None
    ws: Optional[str] = None
    http: Optional[str] = None
    core_version: Optional[str] = None
    pid: Optional[int] = None
    proxy_method: Optional[int] = None
    proxy_type: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
    proxy_user_name: Optional[str] = None
    proxy_password: Optional[str] = None
    browser_finger_print: Optional[BrowserFingerPrint] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Browser':
        """Create a Browser object from API response dictionary"""
        browser_finger_print = None
        if 'browserFingerPrint' in data:
            browser_finger_print = BrowserFingerPrint.from_dict(data['browserFingerPrint'])
            
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            remark=data.get('remark'),
            seq=data.get('seq'),
            group_id=data.get('groupId'),
            ws=data.get('ws'),
            http=data.get('http'),
            core_version=data.get('coreVersion'),
            pid=data.get('pid'),
            proxy_method=data.get('proxyMethod'),
            proxy_type=data.get('proxyType'),
            host=data.get('host'),
            port=data.get('port'),
            proxy_user_name=data.get('proxyUserName'),
            proxy_password=data.get('proxyPassword'),
            browser_finger_print=browser_finger_print
        )


@dataclass
class Group:
    """Browser group details"""
    id: str
    group_name: str
    sort_num: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Group':
        """Create a Group object from API response dictionary"""
        return cls(
            id=data['id'],
            group_name=data.get('groupName', ''),
            sort_num=data.get('sortNum', 0)
        )


@dataclass
class PageInfo:
    """Pagination information"""
    total_elements: int
    total_pages: int
    number: int
    size: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PageInfo':
        """Create a PageInfo object from API response dictionary"""
        return cls(
            total_elements=data.get('totalElements', 0),
            total_pages=data.get('totalPages', 0),
            number=data.get('number', 0),
            size=data.get('size', 0)
        )


@dataclass
class PagedResult(BaseResponse):
    """Base class for paged results"""
    page_info: Optional[PageInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict, content_type, content_key: str = 'content') -> 'PagedResult':
        """Create a PagedResult object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        
        result = cls(success=success, msg=msg)
        
        if 'data' in data and isinstance(data['data'], dict):
            if content_key in data['data']:
                result.content = [content_type.from_dict(item) for item in data['data'][content_key]]
            
            # Extract pagination info if available
            if all(key in data['data'] for key in ['totalElements', 'totalPages', 'number', 'size']):
                result.page_info = PageInfo.from_dict(data['data'])
        
        return result


@dataclass
class BrowserListResponse(PagedResult):
    """Response for browser list API"""
    content: List[Browser] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserListResponse':
        """Create a BrowserListResponse object from API response dictionary"""
        result = super().from_dict(data, Browser, 'content')
        if result.content is None:
            result.content = []
        return result


@dataclass
class GroupListResponse(PagedResult):
    """Response for group list API"""
    content: List[Group] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GroupListResponse':
        """Create a GroupListResponse object from API response dictionary"""
        result = super().from_dict(data, Group, 'content')
        if result.content is None:
            result.content = []
        return result


@dataclass
class HealthResponse(BaseResponse):
    """Response for health check API"""
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HealthResponse':
        """Create a HealthResponse object from API response dictionary"""
        return cls(
            success=data.get('success', False),
            msg=data.get('msg')
        )


@dataclass
class BrowserResponse(BaseResponse):
    """Response containing a single browser"""
    data: Optional[Browser] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserResponse':
        """Create a BrowserResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        browser_data = None
        # print(f'BrowserResponse raw: {data}')
        
        if success and 'data' in data and isinstance(data['data'], dict):
            browser_data = Browser.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=browser_data)


@dataclass
class GroupResponse(BaseResponse):
    """Response containing a single group"""
    data: Optional[Group] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GroupResponse':
        """Create a GroupResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        group_data = None
        
        if success and 'data' in data and isinstance(data['data'], dict):
            if 'id' in data['data']:
                group_data = Group.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=group_data)


@dataclass
class ProxyCheckInfo:
    """Proxy check information"""
    ip: str
    country_name: str
    state_prov: str
    country_code: str
    region: str
    city: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyCheckInfo':
        """Create a ProxyCheckInfo object from API response dictionary"""
        return cls(
            ip=data.get('ip', ''),
            country_name=data.get('countryName', ''),
            state_prov=data.get('stateProv', ''),
            country_code=data.get('countryCode', ''),
            region=data.get('region', ''),
            city=data.get('city', '')
        )


@dataclass
class ProxyCheckResponse(BaseResponse):
    """Response for proxy check API"""
    data: Optional[ProxyCheckInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyCheckResponse':
        """Create a ProxyCheckResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        proxy_data = None
        
        if success and 'data' in data:
            if isinstance(data['data'], dict):
                if data['data'].get('success') and 'data' in data['data']:
                    proxy_data = ProxyCheckInfo.from_dict(data['data']['data'])
        
        return cls(success=success, msg=msg, data=proxy_data)


@dataclass
class BrowserPidInfo:
    """Browser PID information"""
    browser_ids: Dict[str, str]  # Maps browser_id to PID
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserPidInfo':
        """Create a BrowserPidInfo object from API response dictionary"""
        return cls(browser_ids=data or {})


@dataclass
class BrowserPidResponse(BaseResponse):
    """Response for browser PID API"""
    data: Optional[BrowserPidInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserPidResponse':
        """Create a BrowserPidResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        pid_data = None
        
        if success and 'data' in data:
            pid_data = BrowserPidInfo.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=pid_data)


@dataclass
class GenericResponse(BaseResponse):
    """Generic response for API calls that don't return specific data"""
    data: Any = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GenericResponse':
        """Create a GenericResponse object from API response dictionary"""
        return cls(
            success=data.get('success', False),
            msg=data.get('msg'),
            data=data.get('data')
        ) 