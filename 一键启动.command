#!/bin/bash
# 初级会计备考 - 一键启动脚本

echo "======================================"
echo "📚 初级会计备考系统 - 一键启动"
echo "======================================"
echo ""

# 进入目录
cd "$(dirname "$0")"

# 检查文件
echo "📂 检查文件..."
if [ ! -f "START_HERE.html" ]; then
    echo "❌ 文件缺失！"
    exit 1
fi

echo "✅ 文件检查通过"
echo ""

# 启动服务器
echo "🚀 启动服务器..."
echo ""
echo "访问地址："
echo "  📱 http://localhost:8080/"
echo "  📱 START_HERE.html"
echo ""
echo "🛑 停止：Ctrl + C"
echo ""
echo "======================================"

python3 -m http.server 8080
