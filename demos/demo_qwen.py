#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
千问（Qwen）模型演示脚本

演示如何使用千问模型进行：
1. 文本生成
2. 小说灵感提取
3. 创意写作

Author: Assistant
Date: 2025-10-04
"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent))

from src.llm_manager import LLMManager

def main():
    print("🌟 千问（Qwen）模型演示")
    print("=" * 50)
    
    # 初始化管理器
    try:
        manager = LLMManager()
        print("✓ LLM管理器初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 检查千问模型
    try:
        qwen = manager.get_model('qwen')
        print("✓ 千问模型加载成功")
        
        # 显示模型信息
        info = qwen.get_model_info()
        print(f"  - 提供商: {info['provider']}")
        print(f"  - 模型名: {info['model_name']}")
        print(f"  - API地址: {info.get('api_base', 'N/A')}")
        print(f"  - 可用性: {'✓ 可用' if qwen.is_available() else '❌ 不可用'}")
        
    except Exception as e:
        print(f"❌ 千问模型加载失败: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # 测试1: 基础对话
    print("🗣️  测试1: 基础对话")
    print("-" * 30)
    try:
        prompt = "你好！请用一句话介绍一下你自己。"
        print(f"输入: {prompt}")
        
        response = qwen.generate_text(prompt, max_tokens=100)
        print(f"千问回复: {response}")
        
    except Exception as e:
        print(f"❌ 对话测试失败: {e}")
    
    print("\n" + "-" * 50)
    
    # 测试2: 小说灵感生成
    print("📚 测试2: 小说灵感生成")
    print("-" * 30)
    try:
        prompt = """请根据以下文本片段，生成小说创作灵感，用JSON格式返回：

文本片段：
"李明站在悬崖边上，手中紧握着那把传说中的神剑。山风呼啸，云海翻腾，远处的雷声隆隆作响。他知道，今天就是决定命运的时刻。"

请提取：
- theme: 主题
- characters: 角色
- world_elements: 世界设定元素
- raw_excerpt: 原文片段

用JSON格式返回。"""
        
        print("输入: 小说片段灵感提取任务")
        
        response = qwen.generate_text(prompt, max_tokens=300)
        print(f"千问生成的灵感:\n{response}")
        
        # 尝试解析JSON
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            else:
                json_str = response
                
            data = json.loads(json_str)
            print("\n📋 解析结果:")
            for key, value in data.items():
                print(f"  {key}: {value}")
                
        except json.JSONDecodeError:
            print("⚠️  JSON解析失败，但文本生成成功")
        
    except Exception as e:
        print(f"❌ 灵感生成测试失败: {e}")
    
    print("\n" + "-" * 50)
    
    # 测试3: 创意写作
    print("✍️  测试3: 创意写作")
    print("-" * 30)
    try:
        prompt = "请写一个关于人工智能觉醒的科幻小说开头，大约150字。"
        print(f"输入: {prompt}")
        
        response = qwen.generate_text(prompt, max_tokens=200, temperature=0.8)
        print(f"千问创作:\n{response}")
        
    except Exception as e:
        print(f"❌ 创意写作测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 千问模型演示完成！")
    
    # 显示使用指南
    print("\n📖 使用指南:")
    print("=" * 30)
    print("1. 在代码中使用:")
    print("   from src.llm_manager import LLMManager")
    print("   manager = LLMManager()")
    print("   result = manager.generate_text('你的提示词', model_name='qwen')")
    print()
    print("2. 命令行使用:")
    print("   python demo_pipeline.py --model qwen --input your_file.txt")
    print()
    print("3. API密钥配置:")
    print("   - 在 llm_config.json 中配置 qwen.api_key")
    print("   - 或设置环境变量 QWEN_API_KEY")

if __name__ == "__main__":
    main()