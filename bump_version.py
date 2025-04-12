#!/usr/bin/env python3
"""
版本号更新工具
使用方法: python bump_version.py [major|minor|patch]
例如: python bump_version.py patch
"""

import re
import sys
import os

PYPROJECT_PATH = "pyproject.toml"

def get_current_version():
    """获取当前版本号"""
    with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print("无法在 pyproject.toml 中找到版本号")
        sys.exit(1)
    
    return match.group(1)

def bump_version(version, part):
    """更新版本号"""
    major, minor, patch = map(int, version.split("."))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"无效的版本部分: {part}")
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"

def update_pyproject(new_version):
    """更新 pyproject.toml 文件"""
    with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'(version\s*=\s*)"([^"]+)"', 
        rf'\g<1>"{new_version}"', 
        content
    )
    
    with open(PYPROJECT_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("使用方法: python bump_version.py [major|minor|patch]")
        sys.exit(1)
    
    part = sys.argv[1]
    current_version = get_current_version()
    new_version = bump_version(current_version, part)
    
    print(f"当前版本: {current_version}")
    print(f"新版本: {new_version}")
    
    confirm = input("确认更新版本号? (y/n): ").lower()
    if confirm == "y":
        update_pyproject(new_version)
        print(f"版本已更新至 {new_version}")
    else:
        print("操作已取消")

if __name__ == "__main__":
    main() 