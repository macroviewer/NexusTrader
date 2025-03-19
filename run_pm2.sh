#!/bin/bash

# 检查是否提供了参数
if [ $# -eq 0 ]; then
    echo "请提供要运行的进程编号列表"
    echo "使用方法: ./run_pm2.sh <number1> <number2> ..."
    exit 1
fi

# 遍历所有传入的参数
for process_number in "$@"
do
    echo "启动进程 $process_number"
    pm2 restart "$process_number"
    
    echo "等待3分钟..."
    sleep 120  # 300秒 = 5分钟
done

echo "所有进程已启动完成"
