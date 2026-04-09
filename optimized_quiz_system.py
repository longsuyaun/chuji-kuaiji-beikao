#!/usr/bin/env python3
"""
初级会计备考 - 优化版自测系统生成器
将 OCR 提取的知识点转换为练习题目
"""

import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path('/Users/bao/.openclaw/workspace/初级会计备考')

# 加载解析结果
with open(OUTPUT_DIR / '备考资料解析.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 优化题目格式
def optimize_questions(raw_questions, subject):
    """将 OCR 提取的知识点转换为选择题"""
    optimized = []
    
    for i, q in enumerate(raw_questions[:30]):  # 限制 30 题
        text = q.get('text', '')
        if not text or len(text) < 10:
            continue
        
        # 清理文本
        text = text.replace('@® vaxssenm', '').replace('--- 第', '（第').strip()
        
        # 生成选项（如果没有）
        if not q.get('options'):
            options = [
                f'A. {text[:50]}...',
                f'B. 与{subject}相关',
                f'C. 会计基础知识',
                f'D. 以上都是'
            ]
        else:
            options = q['options']
        
        optimized.append({
            'id': i + 1,
            'type': 'single',
            'subject': subject,
            'text': f'【知识点】{text}',
            'options': options,
            'answer': 'D',
            'explanation': f'本题考查{subject}相关知识点。'
        })
    
    return optimized

# 优化所有题目
for item in data:
    subject = item['subject']
    raw_questions = item.get('questions', [])
    item['questions'] = optimize_questions(raw_questions, subject)
    print(f'{subject}: {len(item["questions"])}道题')

# 保存优化后的数据
with open(OUTPUT_DIR / '优化题库.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\n✅ 优化题库已保存：{OUTPUT_DIR / "优化题库.json"}')

# 统计
total = sum(len(item['questions']) for item in data)
print(f'📊 总题目数：{total}道')
