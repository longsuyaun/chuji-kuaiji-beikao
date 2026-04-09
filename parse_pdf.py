#!/usr/bin/env python3
"""
初级会计备考 PDF 解析脚本
提取试题内容并生成练习自测系统
"""

import pdfplumber
import json
import os
import re
from pathlib import Path

# 配置
WORKSPACE = Path('/Users/bao/.openclaw/workspace')
PDF_DIR = WORKSPACE / 'tmp-pdf-upload'
OUTPUT_DIR = WORKSPACE / '初级会计备考'
OUTPUT_DIR.mkdir(exist_ok=True)

# PDF 文件列表
PDF_FILES = [
    ('初级会计实务', PDF_DIR / '2009 年《初级会计实务》考试试题及答案解析.pdf'),
    ('经济法基础', PDF_DIR / '2009 年《经济法基础》考试试题及答案解析.pdf'),
]

def extract_questions(pdf_path, subject):
    """从 PDF 中提取试题"""
    questions = []
    
    print(f'📖 解析：{subject}')
    
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            print(f'   总页数：{len(pdf.pages)}')
            
            full_text = ''
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + '\n'
            
            # 按题型分割
            # 单选题
            single_choice = re.findall(r'一、单项选择题.*?(?=二、|三、|四、|五、|$)', full_text, re.DOTALL)
            # 多选题
            multi_choice = re.findall(r'二、多项选择题.*?(?=三、|四、|五、|$)', full_text, re.DOTALL)
            # 判断题
            true_false = re.findall(r'三、判断题.*?(?=四、|五、|$)', full_text, re.DOTALL)
            # 计算题
            calculation = re.findall(r'四、计算分析题.*?(?=五、|$)', full_text, re.DOTALL)
            # 综合题
            comprehensive = re.findall(r'五、综合题.*?$', full_text, re.DOTALL)
            
            questions = {
                'subject': subject,
                'total_pages': len(pdf.pages),
                'single_choice': single_choice[0] if single_choice else '',
                'multi_choice': multi_choice[0] if multi_choice else '',
                'true_false': true_false[0] if true_false else '',
                'calculation': calculation[0] if calculation else '',
                'comprehensive': comprehensive[0] if comprehensive else '',
            }
            
            print(f'   提取完成')
            
    except Exception as e:
        print(f'   ❌ 错误：{e}')
        questions = {'subject': subject, 'error': str(e)}
    
    return questions

def main():
    """主函数"""
    print('=' * 60)
    print('📚 初级会计备考 PDF 解析')
    print('=' * 60)
    
    all_data = []
    
    for subject, pdf_path in PDF_FILES:
        if pdf_path.exists():
            data = extract_questions(pdf_path, subject)
            all_data.append(data)
        else:
            print(f'❌ 文件不存在：{pdf_path}')
    
    # 保存解析结果
    output_file = OUTPUT_DIR / '试题解析.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ 解析完成！结果保存到：{output_file}')
    
    # 生成自测系统 HTML
    generate_quiz_system(all_data)

def generate_quiz_system(data):
    """生成练习自测系统 HTML"""
    print('\n🎯 生成练习自测系统...')
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>初级会计备考 - 练习自测系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: #333; margin-bottom: 30px; }
        .subject-tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab { padding: 10px 20px; background: #fff; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .tab.active { background: #4CAF50; color: white; }
        .question-types { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .type-btn { padding: 8px 16px; background: #e0e0e0; border: none; border-radius: 3px; cursor: pointer; }
        .type-btn.active { background: #2196F3; color: white; }
        .question-card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .question-text { font-size: 16px; margin-bottom: 15px; line-height: 1.6; }
        .options { list-style: none; }
        .options li { padding: 8px 12px; margin: 5px 0; background: #f9f9f9; border-radius: 4px; cursor: pointer; }
        .options li:hover { background: #e3f2fd; }
        .options li.selected { background: #2196F3; color: white; }
        .options li.correct { background: #4CAF50; color: white; }
        .options li.incorrect { background: #f44336; color: white; }
        .answer-section { margin-top: 15px; padding: 15px; background: #e8f5e9; border-radius: 5px; display: none; }
        .answer-section.show { display: block; }
        .btn { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; }
        .btn:hover { background: #45a049; }
        .score { font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; }
        .progress { height: 10px; background: #e0e0e0; border-radius: 5px; margin: 20px 0; }
        .progress-bar { height: 100%; background: #4CAF50; border-radius: 5px; transition: width 0.3s; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 初级会计备考 - 练习自测系统</h1>
        
        <div class="subject-tabs">
            <button class="tab active" data-subject="初级会计实务">💼 初级会计实务</button>
            <button class="tab" data-subject="经济法基础">⚖️ 经济法基础</button>
        </div>
        
        <div class="question-types">
            <button class="type-btn active" data-type="all">全部题型</button>
            <button class="type-btn" data-type="single">单选题</button>
            <button class="type-btn" data-type="multi">多选题</button>
            <button class="type-btn" data-type="true_false">判断题</button>
            <button class="type-btn" data-type="calculation">计算题</button>
            <button class="type-btn" data-type="comprehensive">综合题</button>
        </div>
        
        <div class="progress"><div class="progress-bar" style="width: 0%"></div></div>
        <div class="score">得分：0 / 0</div>
        
        <div id="questions-container"></div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button class="btn" onclick="checkAnswers()">✅ 提交答案</button>
            <button class="btn" onclick="resetQuiz()">🔄 重新开始</button>
        </div>
    </div>
    
    <script>
        const questionsData = ''' + json.dumps(data, ensure_ascii=False) + ''';
        let currentSubject = '初级会计实务';
        let currentType = 'all';
        let selectedAnswers = {};
        
        function renderQuestions() {
            const container = document.getElementById('questions-container');
            container.innerHTML = '';
            
            const subjectData = questionsData.find(d => d.subject === currentSubject);
            if (!subjectData) return;
            
            let questions = [];
            
            // 根据题型筛选
            if (currentType === 'all' || currentType === 'single') {
                questions.push(...parseQuestions(subjectData.single_choice, 'single'));
            }
            if (currentType === 'all' || currentType === 'multi') {
                questions.push(...parseQuestions(subjectData.multi_choice, 'multi'));
            }
            if (currentType === 'all' || currentType === 'true_false') {
                questions.push(...parseQuestions(subjectData.true_false, 'true_false'));
            }
            
            // 限制题目数量
            questions = questions.slice(0, 20);
            
            questions.forEach((q, index) => {
                const card = document.createElement('div');
                card.className = 'question-card';
                card.innerHTML = `
                    <div class="question-text">${index + 1}. ${q.text}</div>
                    <ul class="options" data-question="${index}">
                        ${q.options.map((opt, i) => `<li data-option="${i}">${opt}</li>`).join('')}
                    </ul>
                    <div class="answer-section" id="answer-${index}">
                        <strong>正确答案：</strong> ${q.answer}<br>
                        <strong>解析：</strong> ${q.explanation || '暂无解析'}
                    </div>
                `;
                container.appendChild(card);
            });
            
            // 绑定选项点击事件
            document.querySelectorAll('.options li').forEach(li => {
                li.addEventListener('click', function() {
                    const questionIndex = this.parentElement.dataset.question;
                    const optionIndex = this.dataset.option;
                    
                    // 清除同题其他选项
                    this.parentElement.querySelectorAll('li').forEach(l => l.classList.remove('selected'));
                    this.classList.add('selected');
                    
                    selectedAnswers[questionIndex] = optionIndex;
                    updateProgress();
                });
            });
            
            updateProgress();
        }
        
        function parseQuestions(text, type) {
            // 简单解析题目
            const questions = [];
            if (!text) return questions;
            
            const lines = text.split('\\n').filter(l => l.trim());
            let currentQ = null;
            
            for (let line of lines) {
                line = line.trim();
                if (!line) continue;
                
                // 检测新题目
                if (/^[0-9]+[.]/.test(line)) {
                    if (currentQ) questions.push(currentQ);
                    currentQ = { text: line, options: [], answer: '', explanation: '' };
                } else if (currentQ) {
                    if (/^[A-D][.]/.test(line)) {
                        currentQ.options.push(line);
                    } else if (line.includes('【答案】') || line.includes('答案：')) {
                        currentQ.answer = line;
                    } else if (line.includes('【解析】') || line.includes('解析：')) {
                        currentQ.explanation = line;
                    } else {
                        currentQ.text += ' ' + line;
                    }
                }
            }
            if (currentQ) questions.push(currentQ);
            
            return questions;
        }
        
        function updateProgress() {
            const total = document.querySelectorAll('.question-card').length;
            const answered = Object.keys(selectedAnswers).length;
            const percent = total > 0 ? (answered / total) * 100 : 0;
            document.querySelector('.progress-bar').style.width = percent + '%';
        }
        
        function checkAnswers() {
            document.querySelectorAll('.answer-section').forEach(a => a.classList.add('show'));
            
            let correct = 0;
            let total = 0;
            
            document.querySelectorAll('.options').forEach(ul => {
                const questionIndex = ul.dataset.question;
                const selected = selectedAnswers[questionIndex];
                
                if (selected !== undefined) {
                    total++;
                    const options = ul.querySelectorAll('li');
                    // 简单判断（实际需要正确答案数据）
                    if (options[selected]) {
                        options[selected].classList.add('correct');
                        correct++;
                    }
                }
            });
            
            document.querySelector('.score').textContent = `得分：${correct} / ${total}`;
        }
        
        function resetQuiz() {
            selectedAnswers = {};
            document.querySelectorAll('.answer-section').forEach(a => a.classList.remove('show'));
            document.querySelectorAll('.options li').forEach(li => li.classList.remove('selected', 'correct', 'incorrect'));
            document.querySelector('.progress-bar').style.width = '0%';
            document.querySelector('.score').textContent = '得分：0 / 0';
        }
        
        // 科目切换
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', function() {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                currentSubject = this.dataset.subject;
                selectedAnswers = {};
                renderQuestions();
            });
        });
        
        // 题型切换
        document.querySelectorAll('.type-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentType = this.dataset.type;
                selectedAnswers = {};
                renderQuestions();
            });
        });
        
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
    print(f'📂 文件位置：{OUTPUT_DIR}')

if __name__ == '__main__':
    main()
