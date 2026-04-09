#!/bin/bash
# 初级会计备考 - GitHub Pages 部署脚本

echo "======================================"
echo "📚 初级会计备考 - GitHub Pages 部署"
echo "======================================"

# 配置
REPO_NAME="primary-accounting-exam"
USER_NAME="your-github-username"
BRANCH="gh-pages"

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

# 创建部署目录
DEPLOY_DIR="/tmp/$REPO_NAME-deploy"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# 复制文件
echo "📂 复制文件到部署目录..."
cp *.html "$DEPLOY_DIR/"
cp *.json "$DEPLOY_DIR/"
cp *.md "$DEPLOY_DIR/"
cp -r images "$DEPLOY_DIR/" 2>/dev/null || true

# 创建 index.html
cat > "$DEPLOY_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>初级会计备考 - 在线学习系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { text-align: center; color: white; margin-bottom: 30px; }
        .card { background: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .card p { color: #666; line-height: 1.8; margin-bottom: 15px; }
        .btn { display: block; padding: 15px 30px; background: #667eea; color: white; text-align: center; text-decoration: none; border-radius: 8px; margin: 10px 0; transition: all 0.3s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .btn-success { background: #4CAF50; }
        .btn-warning { background: #ff9800; }
        .stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
        .stat-item { background: #f5f5f5; padding: 15px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; color: #667eea; }
        .footer { text-align: center; color: white; margin-top: 30px; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 初级会计备考 - 在线学习系统</h1>
        
        <div class="card">
            <h2>📊 系统概览</h2>
            <div class="stats">
                <div class="stat-item"><div class="stat-number">125</div><div>总题数</div></div>
                <div class="stat-item"><div class="stat-number">4</div><div>题型</div></div>
                <div class="stat-item"><div class="stat-number">2</div><div>科目</div></div>
                <div class="stat-item"><div class="stat-number">4</div><div>系统</div></div>
            </div>
        </div>
        
        <div class="card">
            <h2>🎯 选择系统</h2>
            <a href="进阶版自测系统.html" class="btn">🚀 进阶版自测系统（推荐）</a>
            <a href="最终版自测系统.html" class="btn">📖 最终版自测系统</a>
            <a href="模拟考试系统.html" class="btn btn-success">📝 模拟考试系统</a>
            <a href="题库编辑器.html" class="btn btn-warning">✏️ 题库编辑器</a>
        </div>
        
        <div class="card">
            <h2>📖 使用说明</h2>
            <p><strong>1. 进阶版自测系统</strong> - 包含错题本、收藏、学习分析功能，适合系统复习</p>
            <p><strong>2. 最终版自测系统</strong> - 基础练习系统，适合日常刷题</p>
            <p><strong>3. 模拟考试系统</strong> - 90 分钟限时考试，随机抽取 50 道题</p>
            <p><strong>4. 题库编辑器</strong> - 管理题库，添加/编辑/删除题目</p>
        </div>
        
        <div class="card">
            <h2>📱 设备支持</h2>
            <p>✅ 电脑（推荐） | ✅ 平板 | ✅ 手机</p>
            <p>💡 建议使用 Chrome、Safari 或 Firefox 浏览器</p>
        </div>
        
        <div class="footer">
            <p>🦐 初级会计备考系统 | 版本 1.0 | 2026-04-08</p>
            <p>GitHub: <a href="https://github.com/$USER_NAME/$REPO_NAME" style="color: white;">github.com/$USER_NAME/$REPO_NAME</a></p>
        </div>
    </div>
</body>
</html>
EOF

# 检查是否已有 Git 仓库
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git 仓库..."
    git init
    git remote add origin "https://github.com/$USER_NAME/$REPO_NAME.git"
fi

# 切换到 gh-pages 分支
cd "$DEPLOY_DIR"
git init
git checkout -b "$BRANCH"
git add .
git commit -m "📚 部署初级会计备考系统 v1.0"

# 推送
echo "🚀 推送到 GitHub..."
git remote add origin "https://github.com/$USER_NAME/$REPO_NAME.git"
git push -f origin "$BRANCH"

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "📱 访问地址："
echo "   https://$USER_NAME.github.io/$REPO_NAME/"
echo ""
echo "🔧 如需更新，重新运行此脚本即可"
echo ""
