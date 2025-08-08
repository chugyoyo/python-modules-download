#!/bin/bash
set -e

WORK_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "执行部署操作..."

# 1. 拷贝 index.html
cp "$WORK_DIR/index.html" /var/www/pymd/html/
echo "[OK] index.html 已复制到 /var/www/pymd/html/"

# 2. 结束旧进程
pkill -f "python3 -m http.server 8080" 2>/dev/null || true
pkill -f "$WORK_DIR/back-end/app.py" 2>/dev/null || true
echo "[OK] 已结束旧进程"

# 3. 启动新服务
nohup python3 -m http.server 8080 >> "$WORK_DIR/back-end/front.log" 2>&1 &
nohup python3 "$WORK_DIR/back-end/app.py" >> "$WORK_DIR/back-end/log.txt" 2>&1 &
echo "[OK] Python 服务已重启"