# 📚 初级会计备考 - 在线学习系统

> 基于 OCR 技术从 PDF 复习资料中提取题目，生成的互动式练习自测系统

**在线版**: https://your-username.github.io/primary-accounting-exam/  
**题库规模**: 125 道题  
**支持题型**: 单选题、多选题、判断题、计算分析题

---

## 🚀 快速开始

### 在线版（推荐）

直接访问 GitHub Pages：
```
https://your-username.github.io/primary-accounting-exam/
```

### 本地版

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/primary-accounting-exam.git
cd primary-accounting-exam

# 2. 启动本地服务器
python3 start_local_server.py

# 3. 访问系统
浏览器打开：http://localhost:8000
```

### 局域网访问

启动本地服务器后，同一 WiFi 下的其他设备可访问：
```
http://你的局域网 IP:8000
```

---

## 📂 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| **进阶版自测系统.html** | 🚀 主系统 | 错题本 + 收藏 + 学习分析 |
| **最终版自测系统.html** | 📖 基础版 | 完整题库练习 |
| **模拟考试系统.html** | 📝 模拟测试 | 90 分钟限时考试 |
| **题库编辑器.html** | ✏️ 编辑工具 | 题库管理 |
| **优化题库_完整版.json** | 📄 题库数据 | JSON 格式 |
| **start_local_server.py** | 🔧 本地服务器 | 局域网访问 |

---

## 📊 题库统计

| 指标 | 数值 |
|------|------|
| 总题数 | **125 道** |
| 单选题 | 104 道 |
| 多选题 | 2 道 |
| 判断题 | 2 道 |
| 计算分析题 | 17 道 |
| 会计实务 | 95 道 |
| 经济法 | 30 道 |

---

## 🎯 功能特性

### 进阶版自测系统

- ✅ **科目切换**: 会计实务 / 经济法
- ✅ **题型筛选**: 单选 / 多选 / 判断 / 计算分析
- ✅ **错题本**: 自动记录错题
- ✅ **收藏夹**: 手动收藏重点题目
- ✅ **学习分析**: 答题统计、题型掌握情况
- ✅ **进度追踪**: 已答/正确/错误统计
- ✅ **本地存储**: 学习数据自动保存
- ✅ **导出报告**: JSON 格式学习报告

### 模拟考试系统

- ✅ **随机抽题**: 每次考试随机抽取 50 道题
- ✅ **限时考试**: 90 分钟倒计时
- ✅ **答题导航**: 题目编号导航栏
- ✅ **自动交卷**: 时间到自动提交
- ✅ **成绩统计**: 得分、正确率、用时

### 题库编辑器

- ✅ **加载题库**: 从 JSON 文件加载
- ✅ **添加题目**: 支持所有题型
- ✅ **编辑题目**: 修改内容、选项、答案
- ✅ **删除题目**: 移除不需要的题目
- ✅ **搜索筛选**: 按科目、题型、关键词
- ✅ **导出/导入**: JSON 格式

---

## 💻 部署说明

### GitHub Pages 部署

```bash
# 1. 修改 deploy_github.sh 中的用户名
# 将 YOUR_USERNAME 替换为你的 GitHub 用户名

# 2. 运行部署脚本
chmod +x deploy_github.sh
./deploy_github.sh

# 3. 访问
https://YOUR_USERNAME.github.io/primary-accounting-exam/
```

### 本地部署

```bash
# 方法 1: Python 内置服务器
python3 -m http.server 8000

# 方法 2: 使用提供的脚本
python3 start_local_server.py

# 方法 3: Node.js
npx http-server -p 8000
```

### Vercel 部署

1. Fork 本仓库
2. 在 Vercel 导入项目
3. 自动部署完成

### Netlify 部署

1. Fork 本仓库
2. 在 Netlify 导入项目
3. 设置发布目录为根目录
4. 自动部署完成

---

## 📱 设备支持

| 设备 | 支持 | 推荐浏览器 |
|------|------|------------|
| 💻 电脑 | ✅ | Chrome, Safari, Firefox |
| 📱 手机 | ✅ | Chrome, Safari |
| 📱 平板 | ✅ | Chrome, Safari |
| 🖥️ 智能电视 | ✅ | 内置浏览器 |

---

## 🔧 技术栈

- **前端**: HTML5 + CSS3 + JavaScript (ES6)
- **数据存储**: localStorage + IndexedDB
- **OCR**: pytesseract + pdf2image
- **图像处理**: PIL (Pillow)
- **部署**: GitHub Pages + Python HTTP Server

---

## 📖 使用指南

### 日常练习

1. 打开 **进阶版自测系统**
2. 选择科目和题型
3. 开始答题
4. 提交答案查看解析
5. 错题自动加入错题本

### 模拟考试

1. 打开 **模拟考试系统**
2. 点击"开始考试"
3. 90 分钟内完成 50 道题
4. 提交试卷查看成绩

### 题库管理

1. 打开 **题库编辑器**
2. 加载题库
3. 添加/编辑/删除题目
4. 导出题库备份

---

## 🎓 备考建议

| 阶段 | 时间 | 任务 | 目标 |
|------|------|------|------|
| 基础 | 1-2 周 | 系统学习 | 掌握基础 |
| 强化 | 3-4 周 | 大量刷题 | 熟悉题型 |
| 冲刺 | 5-6 周 | 模拟考试 | 提高速度 |

**每日任务**:
- 📖 每日至少 20 道题
- 📝 记录错题
- ⏰ 限时练习
- 🎯 重点突破

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交题目

1. Fork 仓库
2. 编辑 `优化题库_完整版.json`
3. 提交 PR

### 报告 Bug

1. 创建 Issue
2. 描述问题
3. 提供截图

### 功能建议

1. 创建 Issue
2. 描述功能
3. 说明用途

---

## 📄 许可证

本项目仅供学习交流使用，不得用于商业用途。

---

## 📞 联系方式

- 📧 Email: your-email@example.com
- 💬 微信：your-wechat
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/primary-accounting-exam/issues)

---

**🦐 祝学习进步，考试顺利！**
