#!/bin/bash

# 设置错误时脚本退出
set -e

# 下载 TA-Lib 源码
wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz

# 解压
tar -xzf ta-lib-0.6.4-src.tar.gz

# 进入源码目录
cd ta-lib-0.6.4/

# 配置
./configure --prefix=/usr

# 编译
make

# 安装 (需要 sudo 权限)
sudo make install

# 更新动态链接库缓存
sudo ldconfig

# 清理临时文件
cd ..
rm -rf ta-lib-0.6.4/ ta-lib-0.6.4-src.tar.gz

echo "TA-Lib is successfully installed in /usr"
