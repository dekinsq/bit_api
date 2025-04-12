#!/usr/bin/env python3
"""
bitnet-api 包发布工具

此脚本提供了完整的包发布流程，包括：
1. 版本号更新
2. 清理旧的构建文件
3. 构建新的分发包
4. 检查构建文件
5. 上传到PyPI

使用方法:
    python publish.py [major|minor|patch] [--no-confirm] [--test]

参数:
    major|minor|patch: 指定要增加的版本部分
    --no-confirm: 跳过确认步骤
    --test: 上传到TestPyPI而不是正式PyPI

示例:
    python publish.py patch        # 增加补丁版本并发布
    python publish.py minor --test # 增加次要版本并发布到TestPyPI
"""

import os
import re
import sys
import shutil
import subprocess
import argparse
from typing import Tuple, Optional


PYPROJECT_PATH = "pyproject.toml"
TEST_PYPI_REPO = "testpypi"
COLORS = {
    "green": "\033[0;32m",
    "yellow": "\033[1;33m",
    "red": "\033[0;31m",
    "blue": "\033[0;34m",
    "nc": "\033[0m",  # No Color
}


def colored(text: str, color: str) -> str:
    """返回带颜色的文本"""
    return f"{COLORS.get(color, '')}{text}{COLORS['nc']}"


def get_current_version() -> str:
    """获取当前版本号"""
    with open(PYPROJECT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        print(colored("无法在 pyproject.toml 中找到版本号", "red"))
        sys.exit(1)
    
    return match.group(1)


def bump_version(version: str, part: str) -> str:
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
        print(colored(f"无效的版本部分: {part}", "red"))
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"


def update_pyproject(new_version: str) -> None:
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


def run_command(command: str) -> Tuple[int, str]:
    """运行命令并返回退出代码和输出"""
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    output, _ = process.communicate()
    return process.returncode, output


def clean_build_files() -> None:
    """清理旧的构建文件"""
    print(colored("清理旧的构建文件...", "blue"))
    
    for path in ["dist", "build", "*.egg-info"]:
        try:
            if "*" in path:
                for item in os.listdir("."):
                    if item.endswith(path.replace("*", "")):
                        shutil.rmtree(item)
            elif os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            print(colored(f"清理 {path} 时出错: {str(e)}", "yellow"))


def build_package() -> bool:
    """构建包"""
    print(colored("开始构建包...", "blue"))
    
    # 检查 build 是否安装
    returncode, _ = run_command("pip show build")
    if returncode != 0:
        print(colored("build 包未安装，正在安装...", "yellow"))
        returncode, output = run_command("pip install build")
        if returncode != 0:
            print(colored(f"安装 build 失败: {output}", "red"))
            return False
    
    # 构建包
    returncode, output = run_command("python -m build")
    if returncode != 0:
        print(colored(f"构建失败: {output}", "red"))
        return False
    
    return True


def check_distribution() -> bool:
    """检查构建文件"""
    print(colored("检查构建文件...", "blue"))
    
    # 检查 twine 是否安装
    returncode, _ = run_command("pip show twine")
    if returncode != 0:
        print(colored("twine 未安装，正在安装...", "yellow"))
        returncode, output = run_command("pip install twine")
        if returncode != 0:
            print(colored(f"安装 twine 失败: {output}", "red"))
            return False
    
    # 检查构建文件
    returncode, output = run_command("twine check dist/*")
    if returncode != 0:
        print(colored(f"检查失败: {output}", "red"))
        return False
    
    print(colored("检查通过!", "green"))
    return True


def upload_to_pypi(test: bool = False) -> bool:
    """上传包到PyPI"""
    repo_option = f"--repository {TEST_PYPI_REPO}" if test else ""
    repo_name = "TestPyPI" if test else "PyPI"
    
    print(colored(f"正在上传到 {repo_name}...", "blue"))
    
    command = f"twine upload {repo_option} dist/*"
    returncode, output = run_command(command)
    
    if returncode != 0:
        print(colored(f"上传失败: {output}", "red"))
        return False
    
    print(colored("上传成功!", "green"))
    
    # 提取包地址
    if "View at:" in output:
        url = output.split("View at:")[1].strip()
        print(colored(f"包地址: {url}", "yellow"))
    
    return True


def main() -> None:
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="bitnet-api 包发布工具")
    parser.add_argument("version_part", choices=["major", "minor", "patch"], 
                        help="要增加的版本部分")
    parser.add_argument("--no-confirm", action="store_true", 
                        help="跳过确认步骤")
    parser.add_argument("--test", action="store_true", 
                        help="上传到TestPyPI而不是正式PyPI")
    
    args = parser.parse_args()
    
    # 更新版本号
    current_version = get_current_version()
    new_version = bump_version(current_version, args.version_part)
    
    print(colored(f"当前版本: {current_version}", "yellow"))
    print(colored(f"新版本: {new_version}", "green"))
    
    # 确认更新
    if not args.no_confirm:
        confirm = input(colored("确认更新版本号并发布? (y/n): ", "yellow")).lower()
        if confirm != "y":
            print(colored("操作已取消", "red"))
            return
    
    # 更新版本号
    update_pyproject(new_version)
    print(colored(f"版本已更新至 {new_version}", "green"))
    
    # 构建和发布流程
    clean_build_files()
    
    if not build_package():
        return
    
    if not check_distribution():
        return
    
    # 最终确认上传
    if not args.no_confirm:
        destination = "TestPyPI" if args.test else "PyPI"
        confirm = input(colored(f"确认上传到 {destination}? (y/n): ", "yellow")).lower()
        if confirm != "y":
            print(colored("上传已取消", "red"))
            return
    
    upload_to_pypi(args.test)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n操作已取消", "red"))
        sys.exit(1) 