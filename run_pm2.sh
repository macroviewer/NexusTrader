#!/bin/bash

# 检查是否提供了参数
if [ $# -lt 2 ]; then
    echo "请提供要运行的进程编号列表和等待时间"
    echo "使用方法: ./run_pm2.sh <wait_time_seconds> <number1> <number2> ..."
    exit 1
fi

# 获取等待时间（第一个参数）
wait_time="$1"
shift  # 移除第一个参数，剩下的都是进程编号

# 验证等待时间是否为数字
if ! [[ "$wait_time" =~ ^[0-9]+$ ]]; then
    echo "错误: 等待时间必须是一个正整数"
    exit 1
fi

# 遍历所有传入的进程编号
for process_number in "$@"
do
    echo "启动进程 $process_number"
    pm2 restart "$process_number"
    
    echo "等待 $wait_time 秒..."
    sleep "$wait_time"
done

echo "所有进程已启动完成"
