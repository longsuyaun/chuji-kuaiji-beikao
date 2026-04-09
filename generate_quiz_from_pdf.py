#!/usr/bin/env python3
"""
初级会计备考 - PDF 解析 + 练习自测系统生成器
使用 OCR 从扫描版 PDF 提取文字，自动生成练习题目
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 尝试导入 OCR 相关库
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR 库未安装，将使用示例题目")

# 配置
PDF_DIR = Path('/Users/bao/Downloads/会计备考资料')
OUTPUT_DIR = Path('/Users/bao/.openclaw/workspace/初级会计备考')
OUTPUT_DIR.mkdir(exist_ok=True)

# PDF 文件
PDF_FILES = [
    ('初级会计实务', PDF_DIR / '会计实务复习资料.pdf'),
    ('经济法基础', PDF_DIR / '经济法复习资料.pdf'),
]

def extract_text_with_ocr(pdf_path):
    """使用 OCR 从 PDF 提取文本"""
    if not OCR_AVAILABLE:
        return ""
    
    print(f'   使用 OCR 解析：{pdf_path.name}')
    
    try:
        # 将 PDF 转换为图片
        images = convert_from_path(str(pdf_path), dpi=200)
        print(f'   共{len(images)}页')
        
        full_text = ''
        for i, img in enumerate(images[:5]):  # 只解析前 5 页作为示例
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            full_text += f'\n--- 第{i+1}页 ---\n{text}'
            print(f'   第{i+1}页：{len(text)}字符')
        
        return full_text
    
    except Exception as e:
        print(f'   ❌ OCR 错误：{e}')
        return ""

def extract_questions_from_text(text, subject):
    """从文本中提取试题"""
    questions = []
    
    if not text:
        return questions
    
    # 匹配题目模式
    # 单选题：1. 题目内容 A. B. C. D.
    single_pattern = r'(\d+)[.、](.+?)(?=\d+[.、]|$)'
    
    lines = text.split('\n')
    current_q = None
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
        
        # 新题目
        if re.match(r'^\d+[.、]', line):
            if current_q and len(current_q['text']) > 10:
                questions.append(current_q)
            
            # 判断题型
            qtype = 'single'
            if '多选' in line or '下列各项中，属于' in line:
                qtype = 'multi'
            elif '判断' in line or '正确' in line or '错误' in line:
                qtype = 'true_false'
            
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
            elif '答案' in line:
                current_q['answer'] = line
            # 解析
            elif '解析' in line:
                current_q['explanation'] = line
            # 题目 continuation
            elif len(line) > 10 and not line.startswith(('一、', '二、', '三、')):
                current_q['text'] += ' ' + line
    
    if current_q and len(current_q['text']) > 10:
        questions.append(current_q)
    
    return questions[:20]  # 限制题目数量

def generate_sample_questions(subject):
    """生成示例题目（当 OCR 不可用时）"""
    samples = {
        '初级会计实务': [
            {
                'id': 1, 'type': 'single', 'subject': subject,
                'text': '下列各项中，属于企业资产的是（ ）',
                'options': ['A. 应付账款', 'B. 预收账款', 'C. 应收账款', 'D. 短期借款'],
                'answer': 'C', 'explanation': '应收账款属于资产，其他为负债。'
            },
            {
                'id': 2, 'type': 'single', 'subject': subject,
                'text': '企业收到投资者投入的资本，应贷记的会计科目是（ ）',
                'options': ['A. 银行存款', 'B. 实收资本', 'C. 资本公积', 'D. 盈余公积'],
                'answer': 'B', 'explanation': '收到投资应贷记"实收资本"。'
            },
            {
                'id': 3, 'type': 'true_false', 'subject': subject,
                'text': '企业的资产总额等于负债总额加上所有者权益总额。（ ）',
                'options': ['✓ 正确', '✗ 错误'],
                'answer': '✓ 正确', 'explanation': '会计基本等式：资产 = 负债 + 所有者权益。'
            },
            {
                'id': 4, 'type': 'multi', 'subject': subject,
                'text': '下列各项中，属于流动资产的有（ ）',
                'options': ['A. 货币资金', 'B. 应收账款', 'C. 存货', 'D. 固定资产'],
                'answer': 'A、B、C', 'explanation': '固定资产属于非流动资产。'
            },
            {
                'id': 5, 'type': 'single', 'subject': subject,
                'text': '会计核算的基本前提是（ ）',
                'options': ['A. 会计主体', 'B. 持续经营', 'C. 会计分期', 'D. 货币计量'],
                'answer': 'A', 'explanation': '会计主体是基本前提。'
            }
        ],
        '经济法基础': [
            {
                'id': 1, 'type': 'single', 'subject': subject,
                'text': '下列各项中，属于法律关系主体的是（ ）',
                'options': ['A. 自然人', 'B. 物', 'C. 行为', 'D. 智力成果'],
                'answer': 'A', 'explanation': '自然人是主体，其他是客体。'
            },
            {
                'id': 2, 'type': 'true_false', 'subject': subject,
                'text': '会计档案的保管期限分为永久和定期两类。（ ）',
                'options': ['✓ 正确', '✗ 错误'],
                'answer': '✓ 正确', 'explanation': '会计档案分为永久和定期保管。'
            },
            {
                'id': 3, 'type': 'single', 'subject': subject,
                'text': '票据权利包括（ ）',
                'options': ['A. 付款请求权和追索权', 'B. 只有付款请求权', 'C. 只有追索权', 'D. 以上都不对'],
                'answer': 'A', 'explanation': '票据权利包括付款请求权和追索权。'
            },
            {
                'id': 4, 'type': 'multi', 'subject': subject,
                'text': '下列各项中，属于会计职业道德内容的有（ ）',
                'options': ['A. 爱岗敬业', 'B. 诚实守信', 'C. 廉洁自律', 'D. 客观公正'],
                'answer': 'A、B、C、D', 'explanation': '四项都是会计职业道德内容。'
            },
            {
                'id': 5, 'type': 'single', 'subject': subject,
                'text': '根据《会计法》规定，我国会计年度自（ ）',
                'options': ['A. 公历 1 月 1 日起至 12 月 31 日止', 'B. 农历 1 月 1 日起至 12 月 31 日止', 'C. 公历 4 月 1 日起至次年 3 月 31 日止', 'D. 农历 4 月 1 日起至次年 3 月 31 日止'],
                'answer': 'A', 'explanation': '我国会计年度采用公历制。'
            }
        ]
    }
    
    return samples.get(subject, [])

def generate_html(data):
    """生成 HTML 自测系统"""
    print('\n🎯 生成练习自测系统...')
    
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
        .info {{ text-align: center; color: white; margin-bottom: 30px; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 28px; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; margin-top: 5px; font-size: 14px; }}
        .main-content {{ display: grid; grid-template-columns: 280px 1fr; gap: 20px; }}
        .sidebar {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .content {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .subject-tabs {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .tab {{ padding: 10px 20px; background: #f0f0f0; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; transition: all 0.3s; }}
        .tab:hover {{ background: #e0e0e0; }}
        .tab.active {{ background: #667eea; color: white; }}
        .question-types {{ display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }}
        .type-btn {{ padding: 6px 14px; background: #e0e0e0; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }}
        .type-btn.active {{ background: #764ba2; color: white; }}
        .question-card {{ background: #f9f9f9; padding: 20px; margin-bottom: 20px; border-radius: 8px; border-left: 4px solid #667eea; }}
        .question-text {{ font-size: 16px; margin-bottom: 15px; line-height: 1.6; color: #333; }}
        .options {{ list-style: none; }}
        .options li {{ padding: 10px 14px; margin: 6px 0; background: white; border-radius: 6px; cursor: pointer; transition: all 0.3s; border: 2px solid #e0e0e0; font-size: 15px; }}
        .options li:hover {{ background: #f0f7ff; border-color: #667eea; }}
        .options li.selected {{ background: #667eea; color: white; border-color: #667eea; }}
        .options li.correct {{ background: #4CAF50; color: white; border-color: #4CAF50; }}
        .options li.incorrect {{ background: #f44336; color: white; border-color: #f44336; }}
        .answer-section {{ margin-top: 15px; padding: 15px; background: #e8f5e9; border-radius: 6px; display: none; font-size: 14px; }}
        .answer-section.show {{ display: block; }}
        .btn {{ padding: 10px 24px; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 15px; }}
        .btn:hover {{ background: #5568d3; }}
        .btn-secondary {{ background: #9e9e9e; }}
        .score {{ font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; }}
        .progress {{ height: 10px; background: #e0e0e0; border-radius: 5px; margin: 20px 0; }}
        .progress-bar {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.5s; }}
        .action-buttons {{ display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }}
        .tip {{ background: #e3f2fd; padding: 12px; border-radius: 6px; margin: 10px 0; font-size: 14px; border-left: 3px solid #2196F3; }}
        @media (max-width: 768px) {{ .main-content {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 初级会计备考 - 练习自测系统</h1>
        <div class="info">
            <p><strong>📂 PDF 源文件：</strong>/Users/bao/Downloads/会计备考资料/</p>
            <p><strong>📄 解析时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card"><div class="stat-number">{len(data)}</div><div class="stat-label">科目</div></div>
            <div class="stat-card"><div class="stat-number" id="stat-questions">{total_questions}</div><div class="stat-label">试题数</div></div>
            <div class="stat-card"><div class="stat-number" id="stat-answered">0</div><div class="stat-label">已答</div></div>
            <div class="stat-card"><div class="stat-number" id="stat-accuracy">0%</div><div class="stat-label">正确率</div></div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <h3 style="margin-bottom: 15px;">📑 导航</h3>
                <ul style="list-style: none;">
                    <li style="padding: 8px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">💼 初级会计实务</li>
                    <li style="padding: 8px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">⚖️ 经济法基础</li>
                    <li style="padding: 8px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">📝 单选题</li>
                    <li style="padding: 8px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">☑️ 多选题</li>
                    <li style="padding: 8px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">✓ 判断题</li>
                </ul>
                
                <h3 style="margin: 20px 0 10px;">💡 备考建议</h3>
                <div class="tip">📖 每日至少完成 20 道题</div>
                <div class="tip">📝 记录错题并定期复习</div>
                <div class="tip">⏰ 模拟考试环境答题</div>
            </div>
            
            <div class="content">
                <div class="subject-tabs">
                    <button class="tab active" data-subject="初级会计实务">💼 初级会计实务</button>
                    <button class="tab" data-subject="经济法基础">⚖️ 经济法基础</button>
                </div>
                
                <div class="question-types">
                    <button class="type-btn active" data-type="all">全部</button>
                    <button class="type-btn" data-type="single">单选</button>
                    <button class="type-btn" data-type="multi">多选</button>
                    <button class="type-btn" data-type="true_false">判断</button>
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
        
        function renderQuestions() {{
            const container = document.getElementById('questions-container');
            container.innerHTML = '';
            selectedAnswers = {{}};
            
            const subjectData = questionsData.find(d => d.subject === currentSubject);
            if (!subjectData || !subjectData.questions) {{
                container.innerHTML = '<p style="text-align:center;color:#999;padding:50px;">暂无试题</p>';
                return;
            }}
            
            let questions = subjectData.questions;
            if (currentType !== 'all') {{
                questions = questions.filter(q => q.type === currentType);
            }}
            questions = questions.slice(0, 50);
            totalQuestions = questions.length;
            document.getElementById('stat-questions').textContent = totalQuestions;
            
            if (questions.length === 0) {{
                container.innerHTML = '<p style="text-align:center;color:#999;padding:50px;">该题型暂无试题</p>';
                return;
            }}
            
            questions.forEach((q, index) => {{
                const card = document.createElement('div');
                card.className = 'question-card';
                card.innerHTML = `
                    <div class="question-text">${{index + 1}}. ${{q.text}}</div>
                    <ul class="options" data-question="${{index}}">
                        ${{q.options.map((opt, i) => `<li data-option="${{i}}">${{opt}}</li>`).join('')}}
                    </ul>
                    <div class="answer-section" id="answer-${{index}}">
                        <strong>✅ 正确答案：</strong> ${{q.answer}}<br>
                        ${{q.explanation ? `<strong>📝 解析：</strong> ${{q.explanation}}` : ''}}
                    </div>
                `;
                container.appendChild(card);
            }});
            
            document.querySelectorAll('.options li').forEach(li => {{
                li.addEventListener('click', function() {{
                    const qIdx = this.parentElement.dataset.question;
                    const oIdx = this.dataset.option;
                    this.parentElement.querySelectorAll('li').forEach(l => l.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedAnswers[qIdx] = oIdx;
                    updateProgress();
                }});
            }});
            
            updateProgress();
        }}
        
        function updateProgress() {{
            const answered = Object.keys(selectedAnswers).length;
            const percent = totalQuestions > 0 ? (answered / totalQuestions) * 100 : 0;
            document.querySelector('.progress-bar').style.width = percent + '%';
            document.getElementById('stat-answered').textContent = answered;
        }}
        
        function checkAnswers() {{
            document.querySelectorAll('.answer-section').forEach(a => a.classList.add('show'));
            let correct = 0, total = 0;
            
            document.querySelectorAll('.options').forEach(ul => {{
                const qIdx = ul.dataset.question;
                const selected = selectedAnswers[qIdx];
                if (selected !== undefined) {{
                    total++;
                    const opts = ul.querySelectorAll('li');
                    if (opts[selected]) {{
                        opts[selected].classList.add('correct');
                        correct++;
                    }}
                }}
            }});
            
            const accuracy = total > 0 ? ((correct / total) * 100).toFixed(1) : 0;
            document.querySelector('.score').textContent = `得分：${{correct}} / ${{total}} | 正确率：${{accuracy}}%`;
            document.getElementById('stat-accuracy').textContent = accuracy + '%';
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
            document.getElementById('stat-answered').textContent = '0';
            document.getElementById('stat-accuracy').textContent = '0%';
            renderQuestions();
        }}
        
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
        
        document.querySelectorAll('.type-btn').forEach(btn => {{
            btn.addEventListener('click', function() {{
                document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentType = this.dataset.type;
                resetQuiz();
            }});
        }});
        
        renderQuestions();
    </script>
</body>
</html>
'''
    
    html_file = OUTPUT_DIR / '练习自测系统.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ 自测系统：{html_file}')

def main():
    """主函数"""
    print('=' * 60)
    print('📚 初级会计备考 - PDF 解析 + 自测系统生成')
    print('=' * 60)
    print(f'时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    all_data = []
    
    for subject, pdf_path in PDF_FILES:
        print(f'\n📖 处理：{subject}')
        
        if not pdf_path.exists():
            print(f'   ❌ 文件不存在')
            continue
        
        # 尝试 OCR 解析
        text = extract_text_with_ocr(pdf_path)
        
        # 提取或直接使用示例题目
        if text and len(text) > 100:
            questions = extract_questions_from_text(text, subject)
            print(f'   ✅ 提取{len(questions)}道题')
        else:
            questions = generate_sample_questions(subject)
            print(f'   📝 使用示例题目{len(questions)}道')
        
        all_data.append({
            'subject': subject,
            'pdf': pdf_path.name,
            'pages': 0,
            'knowledge_points': [],
            'questions': questions
        })
    
    # 保存解析结果
    json_file = OUTPUT_DIR / '备考资料解析.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ 解析保存：{json_file}')
    
    # 生成自测系统
    generate_html(all_data)
    
    print(f'\n📂 输出目录：{OUTPUT_DIR}')
    print('=' * 60)
    print('✅ 完成！')

if __name__ == '__main__':
    main()
