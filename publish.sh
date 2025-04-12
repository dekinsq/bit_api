#!/bin/bash
set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}开始发布 bitnet-api 包...${NC}"

# 清理旧的构建文件
echo -e "${GREEN}清理旧的构建文件...${NC}"
rm -rf dist/ build/ *.egg-info/

# 构建包
echo -e "${GREEN}开始构建包...${NC}"
python -m build

# 检查 twine 是否安装
if ! command -v twine &> /dev/null; then
    echo -e "${RED}twine 未安装，正在安装...${NC}"
    pip install twine
fi

# 检查构建文件
echo -e "${GREEN}检查构建文件...${NC}"
twine check dist/*

# 提示确认发布
echo -e "${YELLOW}准备发布到 PyPI...${NC}"
read -p "确认发布到 PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}正在上传到 PyPI...${NC}"
    twine upload dist/*
    echo -e "${GREEN}发布完成！新版本已成功上传到 PyPI.${NC}"
    
    # 获取当前版本号
    VERSION=$(grep -o 'version = "[^"]*"' pyproject.toml | cut -d'"' -f2)
    echo -e "${GREEN}发布的版本: ${YELLOW}$VERSION${NC}"
    echo -e "${GREEN}包地址: ${YELLOW}https://pypi.org/project/bitnet-api/${VERSION}/${NC}"
else
    echo -e "${RED}发布已取消${NC}"
fi 