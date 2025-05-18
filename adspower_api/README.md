# AdsPower API 客户端

这是一个用于与AdsPower浏览器指纹管理工具进行交互的Python客户端库。通过这个库，你可以创建、启动、停止、更新和删除浏览器环境，以及查询环境和分组信息。

## 安装

```bash
# 从项目目录安装
cd /path/to/bit_api
pip install -e .
```

## 快速开始

### 初始化客户端

```python
from adspower_api import AdsPowerClient

# 默认连接到本地AdsPower服务
client = AdsPowerClient(host="127.0.0.1", port=50325)
```

### 创建浏览器环境

```python
from adspower_api import AdsPowerClient, BrowserFingerprint, UserProxyConfig

# 初始化客户端
client = AdsPowerClient()

# 创建指纹配置
fingerprint = BrowserFingerprint(
    automatic_timezone="1",
    webrtc="proxy",
    language=["zh-CN", "en-US"],
    resolution="1920,1080",
    platform="win32"
)

# 创建代理配置
proxy_config = UserProxyConfig(
    proxy_soft="other",
    proxy_type="http",
    proxy_host="127.0.0.1",
    proxy_port="8080",
    proxy_user="username",
    proxy_password="password"
)

# 创建浏览器环境
response = client.create_browser(
    group_id="12345",  # 替换为实际的分组ID
    name="测试浏览器",
    remark="API创建的测试环境",
    fingerprint_config=fingerprint,
    user_proxy_config=proxy_config
)

if response.code == 0:
    print(f"创建成功，环境ID: {response.data.profile_id}")
else:
    print(f"创建失败: {response.msg}")
```

### 启动浏览器

```python
response = client.start_browser(
    profile_id="your_profile_id",
    headless="0",  # 非无头模式
    proxy_detection="0"  # 不打开代理检测页面
)

if response.code == 0:
    print(f"启动成功，调试地址: {response.data.ws}")
    print(f"浏览器地址: {response.data.webdriver}")
else:
    print(f"启动失败: {response.msg}")
```

### 查询浏览器环境列表

```python
response = client.list_browsers(page=1, limit=10)

if response.code == 0:
    print(f"总数: {response.data.page_info.total}")
    for browser in response.data.list:
        print(f"ID: {browser.profile_id}, 名称: {browser.name}, 状态: {browser.status}")
else:
    print(f"查询失败: {response.msg}")
```

### 查询分组列表

```python
response = client.list_groups(page=1, page_size=10)

if response.code == 0:
    print(f"总数: {response.data.page_info.total}")
    for group in response.data.list:
        print(f"ID: {group.group_id}, 名称: {group.group_name}")
else:
    print(f"查询失败: {response.msg}")
```

### 关闭浏览器

```python
response = client.stop_browser(profile_id="your_profile_id")

if response.code == 0:
    print("关闭成功")
else:
    print(f"关闭失败: {response.msg}")
```

### 更新浏览器环境

```python
response = client.update_browser(
    profile_id="your_profile_id",
    name="更新后的名称",
    remark="API更新的环境"
)

if response.code == 0:
    print("更新成功")
else:
    print(f"更新失败: {response.msg}")
```

### 删除浏览器环境

```python
response = client.delete_browser(profile_id=["your_profile_id"])

if response.code == 0:
    print("删除成功")
else:
    print(f"删除失败: {response.msg}")
```

## 更多示例

查看 `examples.py` 文件获取更多使用示例。

## API文档

### AdsPowerClient

主要的客户端类，用于与AdsPower API进行交互。

#### 初始化

```python
AdsPowerClient(host="127.0.0.1", port=50325)
```

#### 方法

- `create_browser(...)` - 创建新的浏览器环境
- `start_browser(...)` - 启动浏览器
- `stop_browser(...)` - 关闭浏览器
- `list_browsers(...)` - 查询环境列表
- `update_browser(...)` - 更新浏览器环境
- `delete_browser(...)` - 删除浏览器环境
- `check_browser_active(...)` - 检查浏览器活动状态
- `list_groups(...)` - 查询分组列表

### 数据模型

- `BaseResponse` - 基础响应类
- `BrowserResponse` - 浏览器操作响应类
- `BrowserListResponse` - 浏览器列表响应类
- `GroupListResponse` - 分组列表响应类
- `BrowserActiveResponse` - 浏览器活动状态响应类
- `Browser` - 浏览器环境类
- `Group` - 分组类
- `PageInfo` - 分页信息类
- `BrowserFingerprint` - 浏览器指纹配置类
- `UserProxyConfig` - 用户代理配置类