#!/usr/bin/env python3
"""输入模块功能演示"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.input_module import InputModule

def demo_input_module():
    """演示输入模块的功能"""
    print("=== 小说灵感提取 Agent - 输入模块演示 ===\n")
    
    # 创建输入模块实例
    input_module = InputModule()
    
    # 显示支持的格式
    print("支持的文件格式:", input_module.get_supported_formats())
    
    # 测试示例小说文件
    print("\n=== 处理示例小说文件 ===")
    try:
        # 按段落切分
        result = input_module.process_file(
            '../data/sample_novel.txt',
            split_method='paragraphs',
            enable_segmentation=True
        )
        
        print(f"文件路径: {result['file_path']}")
        print(f"文本总长度: {result['total_length']} 字符")
        print(f"段落数量: {result['chunks_count']}")
        print(f"切分方式: {result['split_method']}")
        print(f"是否启用分词: {result['segmentation_enabled']}")
        
        print("\n前3个段落:")
        for i, chunk in enumerate(result['chunks'][:3]):
            print(f"\n段落 {i+1}:")
            print(f"  标题: {chunk['title']}")
            print(f"  内容: {chunk['content'][:100]}...")
            if 'keywords' in chunk:
                print(f"  关键词: {chunk['keywords'][:5]}")
        
        # 按章节切分
        print("\n=== 按章节切分 ===")
        result = input_module.process_file(
            '../data/sample_novel.txt',
            split_method='chapters',
            enable_segmentation=False
        )
        
        print(f"章节数量: {result['chunks_count']}")
        
        for i, chapter in enumerate(result['chunks']):
            print(f"\n章节 {i+1}:")
            print(f"  标题: {chapter['title']}")
            print(f"  内容: {chapter['content'][:150]}...")
            
    except Exception as e:
        print(f"处理文件时出错: {e}")

if __name__ == "__main__":
    demo_input_module()