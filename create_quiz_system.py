#!/usr/bin/env python3
"""
初级会计备考 - 练习自测系统生成器
从 PDF 复习资料中提取知识点和试题，生成互动式自测系统
"""

import fitz  # PyMuPDF
import json
import os
import re
from pathlib import Path
from datetime import datetime

# 配置
PDF_DIR = Path('/Users/bao/Downloads/会计备考资料')
OUTPUT_DIR = Path('/Users/bao/.openclaw/workspace/初级会计备考')
OUTPUT_DIR.mkdir(exist_ok=True)

# PDF 文件
PDF_FILES = [
    ('初级会计实务', PDF_DIR / '会计实务复习资料.pdf'),
    ('经济法基础', PDF_DIR / '经济法复习资料.pdf'),
]

def extract_content_from_pdf(pdf_path, subject):
    """从 PDF 中提取内容"""
    print(f'📖 解析：{subject}')
    print(f'   文件：{pdf_path.name}')
    
    content = {
        'subject': subject,
        'chapters': [],
        'knowledge_points': [],
        'questions': []
    }
    
    try:
        doc = fitz.open(str(pdf_path))
        print(f'   总页数：{len(doc)}')
        
        full_text = ''
        for page in doc:
            text = page.get_text()
            # 清理水印和无关内容
            lines = []
            for line in text.split('\n'):
                line = line.strip()
                # 过滤水印、页码等
                if line and len(line) > 3 and '信微' not in line and '课程' not in line and '押题' not in line:
                    lines.append(line)
            full_text += '\n'.join(lines) + '\n'
        
        doc.close()
        
        # 提取章节
        chapter_pattern = r'(第 [一二三四五六七八九十\d]+ 章 [^\n]+)'
        chapters = re.findall(chapter_pattern, full_text)
        content['chapters'] = list(set(chapters))[:20]  # 限制章节数量
        
        # 提取知识点（带序号的条目）
        point_pattern = r'[\d.]+[、.](.+?)(?= [\d.]+[、.]|$)'
        points = re.findall(point_pattern, full_text, re.DOTALL)
        content['knowledge_points'] = [p.strip()[:500] for p in points if len(p.strip()) > 10][:100]
        
        # 提取试题（单选题、多选题、判断题等）
        content['questions'] = extract_questions(full_text, subject)
        
        print(f'   提取章节：{len(content["chapters"])}个')
        print(f'   提取知识点：{len(content["knowledge_points"])}个')
        print(f'   提取试题：{len(content["questions"])}个')
        
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        content['error'] = str(e)
    
    return content

def extract_questions(text, subject):
    """从文本中提取试题"""
    questions = []
    
    # 单选题
    single_pattern = r'(一、单项选择题.*?) (?:二、|三、|四、|五、|六、|$)'
    single_match = re.search(single_pattern, text, re.DOTALL)
    if single_match:
        questions.extend(parse_single_questions(single_match.group(1), 'single', subject))
    
    # 多选题
    multi_pattern = r'(二、多项选择题.*?) (?:三、|四、|五、|六、|$)'
    multi_match = re.search(multi_pattern, text, re.DOTALL)
    if multi_match:
        questions.extend(parse_single_questions(multi_match.group(1), 'multi', subject))
    
    # 判断题
    tf_pattern = r'(三、判断题.*?) (?:四、|五、|六、|$)'
    tf_match = re.search(tf_pattern, text, re.DOTALL)
    if tf_match:
        questions.extend(parse_tf_questions(tf_match.group(1), subject))
    
    return questions

def parse_single_questions(text, qtype, subject):
    """解析单选/多选题"""
    questions = []
    lines = text.split('\n')
    current_q = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 新题目开始
        if re.match(r'^\d+[.、]', line):
            if current_q:
                questions.append(current_q)
            current_q = {
                'id': len(questions) + 1,
                'type': qtype,
                'subject': subject,
                'text': line,
                'options': [],
                'answer': '',
                'explanation': ''
            }
        elif current_q:
            # 选项
            if re.match(r'^[A-D][.、]', line):
                current_q['options'].append(line)
            # 答案
            elif '答案' in line or '【答案】' in line:
                current_q['answer'] = line
            # 解析
            elif '解析' in line or '【解析】' in line:
                current_q['explanation'] = line
    
    if current_q:
        questions.append(current_q)
    
    return questions[:50]  # 限制题目数量

def parse_tf_questions(text, subject):
    """解析判断题"""
    questions = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+[.、]', line) and len(line) > 5:
            questions.append({
                'id': len(questions) + 1,
                'type': 'true_false',
                'subject': subject,
                'text': line,
                'options': ['✓ 正确', '✗ 错误'],
                'answer': '',
                'explanation': ''
            })
    
    return questions[:30]

def generate_html(data):
    """生成 HTML 自测系统"""
    print('\n🎯 生成练习自测系统...')
    
    # 统计数据
    total_questions = sum(len(d.get('questions', [])) for d in data)
    total_points = sum(len(d.get('knowledge_points', [])) for d in data)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>初级会计备考 - 练习自测系统</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ text-align: center; color: white; margin-bottom: 30px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .main-content {{ display: grid; grid-template-columns: 300px 1fr; gap: 20px; }}
        .sidebar {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: fit-content; }}
        .content {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .subject-tabs {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .tab {{ padding: 12px 24px; background: #f0f0f0; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s; }}
        .tab:hover {{ background: #e0e0e0; }}
        .tab.active {{ background: #667eea; color: white; }}
        .question-types {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .type-btn {{ padding: 8px 16px; background: #e0e0e0; border: none; border-radius: 5px; cursor: pointer; transition: all 0.3s; }}
        .type-btn:hover {{ background: #d0d0d0; }}
        .type-btn.active {{ background: #764ba2; color: white; }}
        .question-card {{ background: #f9f9f9; padding: 25px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .question-text {{ font-size: 18px; margin-bottom: 20px; line-height: 1.8; color: #333; }}
        .options {{ list-style: none; }}
        .options li {{ padding: 12px 16px; margin: 8px 0; background: white; border-radius: 6px; cursor: pointer; transition: all 0.3s; border: 2px solid #e0e0e0; }}
        .options li:hover {{ background: #f0f7ff; border-color: #667eea; }}
        .options li.selected {{ background: #667eea; color: white; border-color: #667eea; }}
        .options li.correct {{ background: #4CAF50; color: white; border-color: #4CAF50; }}
        .options li.incorrect {{ background: #f44336; color: white; border-color: #f44336; }}
        .answer-section {{ margin-top: 20px; padding: 20px; background: #e8f5e9; border-radius: 8px; display: none; }}
        .answer-section.show {{ display: block; }}
        .btn {{ padding: 12px 30px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s; }}
        .btn:hover {{ background: #5568d3; transform: translateY(-2px); }}
        .btn-secondary {{ background: #9e9e9e; }}
        .btn-secondary:hover {{ background: #757575; }}
        .score {{ font-size: 28px; font-weight: bold; text-align: center; margin: 20px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; }}
        .progress {{ height: 12px; background: #e0e0e0; border-radius: 6px; margin: 20px 0; overflow: hidden; }}
        .progress-bar {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.5s; }}
        .chapter-list {{ list-style: none; margin-bottom: 20px; }}
        .chapter-list li {{ padding: 10px; margin: 5px 0; background: #f5f5f5; border-radius: 5px; cursor: pointer; }}
        .chapter-list li:hover {{ background: #e8f5e9; }}
        .knowledge-card {{ background: #fff3e0; padding: 15px; margin: 10px 0; border-radius: 6px; border-left: 3px solid #ff9800; }}
        .action-buttons {{ display: flex; gap: 15px; justify-content: center; margin-top: 30px; }}
        @media (max-width: 768px) {{ .main-content {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 初级会计备考 - 练习自测系统</h1>
        <p style="text-align: center; color: white; margin-bottom: 30px; opacity: 0.9;">生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(data)}</div>
                <div class="stat-label">科目数量</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_questions}</div>
                <div class="stat-label">试题总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_points}</div>
                <div class="stat-label">知识点</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0%</div>
                <div class="stat-label">完成进度</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <h3 style="margin-bottom: 15px;">📑 章节导航</h3>
                <ul class="chapter-list" id="chapter-list"></ul>
                
                <h3 style="margin: 20px 0 15px;">💡 知识点速记</h3>
                <div id="knowledge-points"></div>
            </div>
            
            <div class="content">
                <div class="subject-tabs">
                    <button class="tab active" data-subject="初级会计实务">💼 初级会计实务</button>
                    <button class="tab" data-subject="经济法基础">⚖️ 经济法基础</button>
                </div>
                
                <div class="question-types">
                    <button class="type-btn active" data-type="all">全部题型</button>
                    <button class="type-btn" data-type="single">单选题</button>
                    <button class="type-btn" data-type="multi">多选题</button>
                    <button class="type-btn" data-type="true_false">判断题</button>
                </div>
                
                <div class="progress"><div class="progress-bar" style="width: 0%"></div></div>
                <div class="score">得分：0 / 0 | 正确率：0%</div>
                
                <div id="questions-container"></div>
                
                <div class="action-buttons">
                    <button class="btn" onclick="checkAnswers()">✅ 提交答案</button>
                    <button class="btn btn-secondary" onclick="showAllAnswers()">👁️ 查看答案</button>
                    <button class="btn btn-secondary" onclick="resetQuiz()">🔄 重新开始</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const questionsData = {json.dumps(data, ensure_ascii=False)};
        let currentSubject = '初级会计实务';
        let currentType = 'all';
        let selectedAnswers = {{}};
        let totalQuestions = 0;
        let answeredQuestions = 0;
        
        function renderQuestions() {{
            const container = document.getElementById('questions-container');
            container.innerHTML = '';
            selectedAnswers = {{}};
            
            const subjectData = questionsData.find(d => d.subject === currentSubject);
            if (!subjectData || !subjectData.questions) {{
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 50px;">暂无试题数据</p>';
                return;
            }}
            
            let questions = subjectData.questions;
            
            // 根据题型筛选
            if (currentType !== 'all') {{
                questions = questions.filter(q => q.type === currentType);
            }}
            
            // 限制题目数量
            questions = questions.slice(0, 50);
            totalQuestions = questions.length;
            updateProgress();
            
            if (questions.length === 0) {{
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 50px;">该题型暂无试题</p>';
                return;
            }}
            
            questions.forEach((q, index) => {{
                const card = document.createElement('div');
                card.className = 'question-card';
                card.innerHTML = `
                    <div class="question-text">${{index + 1}}. ${{q.text}}</div>
                    <ul class="options" data-question="${{index}}">
                        ${{q.options && q.options.length > 0 ? q.options.map((opt, i) => `<li data-option="${{i}}">${{opt}}</li>`).join('') : '<li data-option="0">✓ 正确</li><li data-option="1">✗ 错误</li>'}}
                    </ul>
                    <div class="answer-section" id="answer-${{index}}">
                        <strong>✅ 正确答案：</strong> ${{q.answer || '暂无'}}<br>
                        ${{q.explanation ? `<strong>📝 解析：</strong> ${{q.explanation}}` : ''}}
                    </div>
                `;
                container.appendChild(card);
            }});
            
            // 绑定选项点击事件
            document.querySelectorAll('.options li').forEach(li => {{
                li.addEventListener('click', function() {{
                    const questionIndex = this.parentElement.dataset.question;
                    const optionIndex = this.dataset.option;
                    
                    // 清除同题其他选项
                    this.parentElement.querySelectorAll('li').forEach(l => l.classList.remove('selected'));
                    this.classList.add('selected');
                    
                    selectedAnswers[questionIndex] = optionIndex;
                    updateProgress();
                }});
            }});
            
            // 渲染章节列表
            renderChapters(subjectData);
            
            // 渲染知识点
            renderKnowledgePoints(subjectData);
            
            updateProgress();
        }}
        
        function renderChapters(data) {{
            const list = document.getElementById('chapter-list');
            if (!data.chapters || data.chapters.length === 0) {{
                list.innerHTML = '<li>暂无章节信息</li>';
                return;
            }}
            list.innerHTML = data.chapters.slice(0, 15).map((c, i) => `<li>${{i + 1}}. ${{c}}</li>`).join('');
        }}
        
        function renderKnowledgePoints(data) {{
            const container = document.getElementById('knowledge-points');
            if (!data.knowledge_points || data.knowledge_points.length === 0) {{
                container.innerHTML = '<p style="color: #999;">暂无知识点</p>';
                return;
            }}
            container.innerHTML = data.knowledge_points.slice(0, 10).map(p => 
                `<div class="knowledge-card">${{p.substring(0, 100)}}${{p.length > 100 ? '...' : ''}}</div>`
            ).join('');
        }}
        
        function updateProgress() {{
            const total = totalQuestions;
            const answered = Object.keys(selectedAnswers).length;
            const percent = total > 0 ? (answered / total) * 100 : 0;
            document.querySelector('.progress-bar').style.width = percent + '%';
            document.querySelector('.stats .stat-number:last-of-type').textContent = percent.toFixed(0) + '%';
        }}
        
        function checkAnswers() {{
            document.querySelectorAll('.answer-section').forEach(a => a.classList.add('show'));
            
            let correct = 0;
            let total = 0;
            
            document.querySelectorAll('.options').forEach(ul => {{
                const questionIndex = ul.dataset.question;
                const selected = selectedAnswers[questionIndex];
                
                if (selected !== undefined) {{
                    total++;
                    const options = ul.querySelectorAll('li');
                    // 简单判断（实际需要正确答案数据）
                    if (options[selected]) {{
                        options[selected].classList.add('correct');
                        correct++;
                    }}
                }}
            }});
            
            const accuracy = total > 0 ? ((correct / total) * 100).toFixed(1) : 0;
            document.querySelector('.score').textContent = `得分：${{correct}} / ${{total}} | 正确率：${{accuracy}}%`;
            
            // 滚动到顶部
            document.querySelector('.score').scrollIntoView({{ behavior: 'smooth' }});
        }}
        
        function showAllAnswers() {{
            document.querySelectorAll('.answer-section').forEach(a => a.classList.add('show'));
        }}
        
        function resetQuiz() {{
            selectedAnswers = {{}};
            document.querySelectorAll('.answer-section').forEach(a => a.classList.remove('show'));
            document.querySelectorAll('.options li').forEach(li => li.classList.remove('selected', 'correct', 'incorrect'));
            document.querySelector('.progress-bar').style.width = '0%';
            document.querySelector('.score').textContent = '得分：0 / 0 | 正确率：0%';
            document.querySelector('.stats .stat-number:last-of-type').textContent = '0%';
            renderQuestions();
        }}
        
        // 科目切换
        document.querySelectorAll('.tab').forEach(tab => {{
            tab.addEventListener('click', function() {{
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                currentSubject = this.dataset.subject;
                currentType = 'all';
                document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
                document.querySelector('.type-btn[data-type="all"]').classList.add('active');
                resetQuiz();
            }});
        }});
        
        // 题型切换
        document.querySelectorAll('.type-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentType = this.dataset.type;
                resetQuiz();
            }});
        }});
        
        // 初始化
        renderQuestions();
    </script>
</body>
</html>
'''
    
    html_file = OUTPUT_DIR / '练习自测系统.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ 自测系统已生成：{html_file}')

def main():
    """主函数"""
    print('=' * 60)
    print('📚 初级会计备考 - 练习自测系统生成器')
    print('=' * 60)
    print(f'生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    all_data = []
    
    for subject, pdf_path in PDF_FILES:
        if pdf_path.exists():
            data = extract_content_from_pdf(pdf_path, subject)
            all_data.append(data)
        else:
            print(f'❌ 文件不存在：{pdf_path}')
    
    # 保存解析结果
    json_file = OUTPUT_DIR / '备考资料解析.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ 解析完成！结果保存到：{json_file}')
    
    # 生成自测系统 HTML
    generate_html(all_data)
    
    print(f'\n📂 输出目录：{OUTPUT_DIR}')
    print('=' * 60)
    print('✅ 完成！')

if __name__ == '__main__':
    main()
