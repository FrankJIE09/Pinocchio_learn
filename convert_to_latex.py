#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将PDF转换的TXT文件转换为中文LaTeX格式
保留图片描述，但不包含图片本身
"""

import re
import sys
import time

def translate_to_chinese(text):
    """
    翻译函数，将英文转换为中文
    优先使用 deep-translator，如果不可用则使用 googletrans
    """
    if not text or not text.strip():
        return text
    
    # 尝试使用 deep-translator
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='en', target='zh-CN')
        # 限制文本长度以避免API限制
        if len(text) > 5000:
            # 分段翻译
            parts = []
            words = text.split()
            current_part = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) > 4500:
                    parts.append(' '.join(current_part))
                    current_part = [word]
                    current_length = len(word)
                else:
                    current_part.append(word)
                    current_length += len(word) + 1
            
            if current_part:
                parts.append(' '.join(current_part))
            
            translated_parts = []
            for part in parts:
                try:
                    translated = translator.translate(part)
                    translated_parts.append(translated)
                    time.sleep(0.1)  # 避免请求过快
                except Exception as e:
                    translated_parts.append(part)  # 翻译失败时保留原文
            
            return ' '.join(translated_parts)
        else:
            return translator.translate(text)
    except ImportError:
        # 尝试使用 googletrans
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, src='en', dest='zh-cn')
            return result.text
        except ImportError:
            # 如果都没有安装，使用简单替换
            translations = {
                'Abstract': '摘要',
                'Introduction': '引言',
                'Section': '章节',
                'Figure': '图',
                'Fig.': '图',
                'Table': '表',
                'References': '参考文献',
                'Conclusion': '结论',
                'Acknowledgement': '致谢',
            }
            for en, zh in translations.items():
                text = text.replace(en, zh)
            return text
    except Exception as e:
        # 翻译失败时返回原文
        print(f'翻译警告: {e}', file=sys.stderr)
        return text

def extract_figure_descriptions(text):
    """提取图片描述"""
    # 匹配图片引用，如 "Fig. 1", "Figure 2" 等
    figure_pattern = r'Fig\.?\s*\d+[\.:]?\s*[^\n]*'
    figures = re.findall(figure_pattern, text, re.IGNORECASE)
    return figures

def escape_latex(text):
    """转义LaTeX特殊字符"""
    special_chars = {
        '\\': '\\textbackslash{}',
        '{': '\\{',
        '}': '\\}',
        '$': '\\$',
        '&': '\\&',
        '%': '\\%',
        '#': '\\#',
        '^': '\\textasciicircum{}',
        '_': '\\_',
        '~': '\\textasciitilde{}',
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text

def convert_to_latex(txt_content):
    """将TXT内容转换为LaTeX格式"""
    lines = txt_content.split('\n')
    latex_lines = []
    current_paragraph = []
    in_code_block = False
    in_references = False
    
    # 添加LaTeX文档头部
    latex_lines.append('\\documentclass[12pt,a4paper]{article}')
    latex_lines.append('\\usepackage[UTF8]{ctex}')
    latex_lines.append('\\usepackage{graphicx}')
    latex_lines.append('\\usepackage{amsmath}')
    latex_lines.append('\\usepackage{hyperref}')
    latex_lines.append('\\usepackage{listings}')
    latex_lines.append('\\usepackage{xcolor}')
    latex_lines.append('\\begin{document}')
    latex_lines.append('')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        original_line = lines[i]
        
        # 检测标题和作者信息
        if i == 0 and line:
            title = translate_to_chinese(line)
            latex_lines.append('\\title{' + escape_latex(title) + '}')
            # 读取作者信息（接下来的几行）
            authors = []
            j = i + 1
            while j < len(lines) and j < i + 5 and not lines[j].strip().startswith('Abstract'):
                if lines[j].strip():
                    authors.append(lines[j].strip())
                j += 1
            if authors:
                author_line = ', '.join(authors)
                author_line = translate_to_chinese(author_line)
                latex_lines.append('\\author{' + escape_latex(author_line) + '}')
            latex_lines.append('\\maketitle')
            latex_lines.append('')
            i = j
            continue
        
        # 检测Abstract
        if line.startswith('Abstract'):
            latex_lines.append('\\begin{abstract}')
            abstract_lines = []
            i += 1
            while i < len(lines) and not re.match(r'^[IVX]+\.', lines[i].strip()):
                if lines[i].strip():
                    abstract_lines.append(lines[i].strip())
                i += 1
            abstract_text = ' '.join(abstract_lines)
            abstract_text = translate_to_chinese(abstract_text)
            latex_lines.append(escape_latex(abstract_text))
            latex_lines.append('\\end{abstract}')
            latex_lines.append('')
            continue
        
        # 检测章节标题（如 "I. INTRODUCTION"）
        section_match = re.match(r'^([IVX]+\.?|A\.|B\.|C\.|D\.|E\.|F\.|G\.|H\.|a\)|b\)|c\)|d\)|e\)|f\))\s+(.+)$', line)
        if section_match:
            # 先输出当前段落
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                para_text = translate_to_chinese(para_text)
                latex_lines.append(escape_latex(para_text))
                latex_lines.append('')
                current_paragraph = []
            
            level = section_match.group(1)
            title = section_match.group(2).strip()
            
            if level in ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']:
                latex_lines.append('\\section{' + escape_latex(translate_to_chinese(title)) + '}')
            elif level in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                latex_lines.append('\\subsection{' + escape_latex(translate_to_chinese(title)) + '}')
            elif level in ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']:
                latex_lines.append('\\subsubsection{' + escape_latex(translate_to_chinese(title)) + '}')
            latex_lines.append('')
            i += 1
            continue
        
        # 检测图片引用和描述
        fig_match = re.search(r'Fig\.?\s*(\d+)[\.:]?\s*(.*?)(?:\.|$)', line, re.IGNORECASE)
        if fig_match:
            # 先输出当前段落
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                para_text = translate_to_chinese(para_text)
                latex_lines.append(escape_latex(para_text))
                latex_lines.append('')
                current_paragraph = []
            
            fig_num = fig_match.group(1)
            fig_desc = fig_match.group(2).strip()
            # 尝试获取更多描述（下一行可能包含描述）
            if not fig_desc and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.match(r'^[IVX]+\.', next_line):
                    fig_desc = next_line
                    i += 1
            
            if fig_desc:
                fig_desc = translate_to_chinese(f'图 {fig_num}: {fig_desc}')
                latex_lines.append('\\begin{figure}[h]')
                latex_lines.append('\\centering')
                latex_lines.append('% 图片已省略')
                latex_lines.append('\\caption{' + escape_latex(fig_desc) + '}')
                latex_lines.append('\\label{fig:' + fig_num + '}')
                latex_lines.append('\\end{figure}')
                latex_lines.append('')
            i += 1
            continue
        
        # 检测代码块
        if line.startswith('import ') or (line and '=' in line and ('np.' in line or 'se3.' in line)):
            # 先输出当前段落
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                para_text = translate_to_chinese(para_text)
                latex_lines.append(escape_latex(para_text))
                latex_lines.append('')
                current_paragraph = []
            
            latex_lines.append('\\begin{lstlisting}[language=Python]')
            code_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^[IVX]+\.', lines[i].strip()):
                code_lines.append(lines[i])
                i += 1
            latex_lines.extend(code_lines)
            latex_lines.append('\\end{lstlisting}')
            latex_lines.append('')
            continue
        
        # 检测参考文献部分
        if line.startswith('REFERENCES') or line.startswith('R EFERENCES'):
            in_references = True
            # 先输出当前段落
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                para_text = translate_to_chinese(para_text)
                latex_lines.append(escape_latex(para_text))
                latex_lines.append('')
                current_paragraph = []
            
            latex_lines.append('\\section{' + escape_latex(translate_to_chinese('参考文献')) + '}')
            latex_lines.append('\\begin{thebibliography}{99}')
            i += 1
            continue
        
        # 处理参考文献条目
        if in_references:
            ref_match = re.match(r'^\[(\d+)\]\s+(.+)$', line)
            if ref_match:
                ref_num = ref_match.group(1)
                ref_text = ref_match.group(2).strip()
                # 继续读取直到下一个引用或空行
                ref_full = ref_text
                i += 1
                while i < len(lines) and lines[i].strip() and not re.match(r'^\[\d+\]', lines[i].strip()):
                    ref_full += ' ' + lines[i].strip()
                    i += 1
                latex_lines.append('\\bibitem{' + ref_num + '}')
                latex_lines.append(escape_latex(ref_full))
                latex_lines.append('')
                continue
        
        # 普通文本行
        if line:
            current_paragraph.append(line)
        else:
            # 空行，输出当前段落
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                para_text = translate_to_chinese(para_text)
                latex_lines.append(escape_latex(para_text))
                latex_lines.append('')
                current_paragraph = []
        
        i += 1
    
    # 输出最后一段
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        para_text = translate_to_chinese(para_text)
        latex_lines.append(escape_latex(para_text))
        latex_lines.append('')
    
    if in_references:
        latex_lines.append('\\end{thebibliography}')
    
    latex_lines.append('\\end{document}')
    return '\n'.join(latex_lines)

def main():
    input_file = 'The Pinocchio C++ library.txt'
    output_file = 'The Pinocchio C++ library.tex'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            txt_content = f.read()
        
        latex_content = convert_to_latex(txt_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f'成功将 {input_file} 转换为 {output_file}')
        print('注意：图片已省略，但保留了图片描述')
        
    except FileNotFoundError:
        print(f'错误：找不到文件 {input_file}')
        sys.exit(1)
    except Exception as e:
        print(f'错误：{e}')
        sys.exit(1)

if __name__ == '__main__':
    main()

