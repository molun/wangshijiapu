# -*- coding: utf-8 -*-
"""
Parse the family tree PDF into structured JSON data.
临县堡则峪王氏宗谱 - 利支
"""
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')
from pypdf import PdfReader

PDF_PATH = r'D:\molun\Desktop\家谱2025年9月10日利支06.pdf'

def extract_all_text():
    reader = PdfReader(PDF_PATH)
    all_text = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text.append(text)
    return '\n'.join(all_text)

def parse_persons(text):
    """Extract person records from the text.
    
    Pattern: Names like 王XX followed by optional wife info (X氏) and son count (X子)
    """
    persons = []
    # Match patterns like: 王克明, 王受仓, etc.
    # Also match wife patterns: 薛氏一子, 李薛氏二子, 高氏五子
    # And relational patterns: 高祖XX曾祖XX祖XX父XX
    
    lines = text.split('\n')
    
    # Extract all 王X names
    name_pattern = re.compile(r'王[\u4e00-\u9fff]{1,3}')
    wife_pattern = re.compile(r'([^\s]{1,4}氏)\s*(\d+子|一子|二子|三子|四子|五子|六子|七子|少亡|无后|无考)?')
    relation_pattern = re.compile(r'(高祖|曾祖|祖|父)(王[\u4e00-\u9fff]{1,3})')
    
    current_ancestors = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for ancestor chain patterns
        rel_matches = relation_pattern.findall(line)
        if rel_matches:
            for rel_type, rel_name in rel_matches:
                current_ancestors[rel_type] = rel_name
        
        # Check for person names
        names = name_pattern.findall(line)
        for name in names:
            if name.startswith('王') and len(name) >= 2:
                persons.append({
                    'name': name,
                    'raw_line': line[:100]
                })
    
    return persons

def build_tree_data():
    """Build a structured tree from the PDF content."""
    text = extract_all_text()
    
    # We'll create a simpler structured representation
    # Based on the generational information we extracted
    
    # The key structure from the PDF:
    # - Family: 临县堡则峪王氏
    # - Branches: 元支, 亨支, 利支
    # - Generations: 一世 through 三十世
    # - Each person has: name, wife(s), sons count, notes
    
    # Extract all unique names and their context
    all_names = set()
    lines = text.split('\n')
    
    name_pattern = re.compile(r'王[\u4e00-\u9fff]{1,4}')
    
    for line in lines:
        names = name_pattern.findall(line)
        for name in names:
            if 2 <= len(name) <= 5:
                all_names.add(name)
    
    print(f"Total unique names found: {len(all_names)}")
    return sorted(all_names)

def extract_structured_data():
    """More structured extraction preserving generational info."""
    reader = PdfReader(PDF_PATH)
    
    # Build page-by-page extraction with generation markers
    pages_data = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
            
        page_info = {
            'page': i + 1,
            'text': text,
            'generations': [],
            'branch': None
        }
        
        # Detect branch
        if '元支' in text:
            page_info['branch'] = '元支'
        elif '亨支' in text:
            page_info['branch'] = '亨支'
        elif '利支' in text:
            page_info['branch'] = '利支'
        
        # Detect generation ranges
        gen_pattern = re.compile(r'([一二三四五六七八九十百]+世)')
        gens = gen_pattern.findall(text)
        if gens:
            page_info['generations'] = gens
        
        pages_data.append(page_info)
    
    return pages_data

def build_json_data():
    """Build the final JSON structure for the website."""
    reader = PdfReader(PDF_PATH)
    
    # Extract all text and build person list with relationships
    persons = []
    seen_names = {}  # Track names to handle duplicates
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        
        branch = '利支'  # Default from the PDF title
        if '元支' in text:
            branch = '元支'
        elif '亨支' in text:
            branch = '亨支'
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse ancestor chain: 高祖XX曾祖XX祖XX父XX
            chain_match = re.search(r'(高祖|曾祖|祖|父)([^\s高曾祖父]{1,8})', line)
            
            # Parse wife info: X氏N子
            wife_match = re.search(r'([\u4e00-\u9fff]{1,3}氏)\s*(\d+子|[一二三四五六七八九十]+子)?', line)
            
            # Parse person name: 王XX
            name_match = re.search(r'(王[\u4e00-\u9fff]{1,4})', line)
            
            if name_match:
                name = name_match.group(1)
                person = {
                    'name': name,
                    'page': page_num + 1,
                    'branch': branch,
                }
                if wife_match:
                    person['wife'] = wife_match.group(1)
                    if wife_match.group(2):
                        person['sons'] = wife_match.group(2)
                
                # Handle duplicate names by adding page context
                if name in seen_names:
                    seen_names[name] += 1
                    person['occurrence'] = seen_names[name]
                else:
                    seen_names[name] = 1
                    person['occurrence'] = 1
                
                persons.append(person)
    
    return {
        'family': '临县堡则峪王氏',
        'source': '家谱2025年9月10日利支06.pdf',
        'updated': '二零二五年续修',
        'branches': ['元支', '亨支', '利支'],
        'total_persons': len(persons),
        'persons': persons[:2000]  # Limit for initial version
    }

if __name__ == '__main__':
    data = build_json_data()
    
    # Write JSON
    output_path = r'C:\Users\molun\.qclaw\workspace\jiapu\data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {data['total_persons']} persons")
    print(f"Written to {output_path}")
