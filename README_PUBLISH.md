# bitnet-api 发布工具使用文档

该项目提供了多种发布工具，用于简化 bitnet-api 包的版本管理和发布流程。

## 发布工具概览

| 工具 | 类型 | 功能 |
|-----|------|------|
| `publish.sh` | Shell脚本 | 简单的发布流程自动化 |
| `publish.py` | Python脚本 | 功能完整的发布工具，带参数解析和测试发布支持 |
| `bump_version.py` | Python脚本 | 独立的版本号更新工具 |

## 使用说明

### 1. 使用 `publish.py`（推荐）

这是功能最完整的发布工具，提供了版本管理和发布的所有功能。

```bash
# 增加补丁版本号并发布
python publish.py patch

# 增加次要版本号并发布
python publish.py minor

# 增加主要版本号并发布
python publish.py major

# 增加版本号并发布到测试PyPI
python publish.py patch --test

# 增加版本号并发布时跳过确认提示
python publish.py patch --no-confirm
```

**参数说明：**

- `patch|minor|major`: 指定要增加的版本部分
- `--no-confirm`: 跳过确认步骤
- `--test`: 上传到TestPyPI而不是正式PyPI

### 2. 使用 `publish.sh`

这是一个简单的Shell脚本，提供基本的发布功能。

```bash
./publish.sh
```

脚本会：
- 清理旧的构建文件
- 构建源码包和轮子包
- 检查构建文件格式
- 上传包到PyPI（需要确认）

### 3. 使用 `bump_version.py`

如果只想更新版本号而不发布，可以使用这个工具。

```bash
# 增加补丁版本号
python bump_version.py patch

# 增加次要版本号
python bump_version.py minor

# 增加主要版本号
python bump_version.py major
```

## 配置说明

### PyPI 配置

发布工具需要使用 `~/.pypirc` 文件进行认证。该文件应包含以下内容：

```
[pypi]
username = __token__
password = your-pypi-token

[testpypi]
username = __token__
password = your-testpypi-token
```

请将 `your-pypi-token` 和 `your-testpypi-token` 替换为您的实际令牌。

### 获取PyPI令牌

1. 注册或登录PyPI账户：访问 https://pypi.org 并登录
2. 访问账户设置：点击右上角的用户名，然后选择"Account settings"
3. 创建API令牌：
   - 滚动到"API tokens"部分
   - 点击"Add API token"
   - 给令牌起个名称（如"bitnet-api-publish"）
   - 可选择设置令牌的作用域
   - 点击"Create token"按钮
4. 保存令牌：创建后立即复制令牌（只显示一次）

### 获取TestPyPI令牌

如果需要在TestPyPI上测试发布，请：

1. 注册或登录TestPyPI账户：访问 https://test.pypi.org 并登录
2. 按照与PyPI相同的步骤获取令牌

## 最佳实践

1. **先测试，后发布**：首次发布时，建议先使用 `--test` 选项发布到TestPyPI
2. **保持版本号语义化**：遵循[语义化版本规范](https://semver.org/lang/zh-CN/)
3. **发布前检查**：确保代码已经通过测试，并且所有更改已记录在文档中
4. **备份凭据**：确保安全地保存您的PyPI令牌

## 问题排查

### 常见错误

- **版本冲突**：PyPI不允许重复发布相同版本，确保每次发布都增加版本号
- **认证失败**：检查 `~/.pypirc` 文件中的令牌是否正确
- **构建失败**：确保安装了所需的构建工具（build, wheel, setuptools）

### 找到帮助

如有问题，请查阅：
- [PyPI帮助文档](https://pypi.org/help/)
- [Python打包用户指南](https://packaging.python.org/) 