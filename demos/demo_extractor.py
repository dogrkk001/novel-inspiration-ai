#!/usr/bin/env python3
"""
灵感提取模块功能演示
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 从 src 包中导入模块
from src.extractor import (
    MockLLM, OpenAIModel, ClaudeModel,
    InspirationExtractor, PromptTemplate
)
from src.input_module import InputModule


def demo_mock_llm():
    """演示MockLLM的功能"""
    print("=== MockLLM 演示 ===")
    
    # 创建MockLLM实例
    mock_llm = MockLLM()
    
    # 测试基本调用
    response = mock_llm.generate("请分析这段文本")
    print(f"模型名称: {mock_llm.get_model_name()}")
    print(f"调用次数: {mock_llm.call_count}")
    print(f"生成响应: {response[:100]}...")
    
    print()


def demo_inspiration_extractor():
    """演示灵感提取器的功能"""
    print("=== 灵感提取器演示 ===")
    
    # 创建提取器
    mock_llm = MockLLM()
    extractor = InspirationExtractor(mock_llm)
    
    # 测试文本
    test_texts = [
        "李云从小在山村长大，从未见过外面的世界。这一天，他终于决定走出大山，去寻找自己的命运。",
        "在老者的指导下，李云开始了艰苦的修炼。每天清晨，他都要在瀑布下打坐，感受天地间的灵气。",
        "",  # 空文本
        "短",  # 很短文本
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- 测试文本 {i} ---")
        print(f"原文: {repr(text)}")
        
        try:
            result = extractor.extract_inspiration(text)
            print(f"主题: {result['theme']}")
            print(f"人物: {result['characters']}")
            print(f"世界观: {result['world_elements']}")
            print(f"精华片段: {result['raw_excerpt']}")
        except Exception as e:
            print(f"提取失败: {e}")
    
    print()


def demo_custom_llm_response():
    """演示自定义LLM响应"""
    print("=== 自定义LLM响应演示 ===")
    
    # 自定义响应
    custom_response = '''```json
{
    "theme": "科幻，时间旅行",
    "characters": ["时间旅行者", "未来人类"],
    "world_elements": "时空机器，平行宇宙",
    "raw_excerpt": "时间的秘密即将揭开"
}
```'''
    
    mock_llm = MockLLM(fixed_response=custom_response)
    extractor = InspirationExtractor(mock_llm)
    
    test_text = "这是一个关于时间旅行的科幻故事，主角发明了时光机器，穿越到了未来世界。"
    result = extractor.extract_inspiration(test_text)
    
    print(f"测试文本: {test_text}")
    print(f"提取结果:")
    print(f"  主题: {result['theme']}")
    print(f"  人物: {result['characters']}")
    print(f"  世界观: {result['world_elements']}")
    print(f"  精华片段: {result['raw_excerpt']}")
    
    print()


def demo_structured_data():
    """演示结构化数据提取"""
    print("=== 结构化数据演示 ===")
    
    mock_llm = MockLLM()
    extractor = InspirationExtractor(mock_llm)
    
    test_text = "在魔法学院里，年轻的魔法师艾莉亚正在学习古老的咒语。她的导师告诉她，真正的魔法来自内心的力量。"
    
    # 提取为字典
    dict_result = extractor.extract_inspiration(test_text)
    print("字典格式结果:")
    for key, value in dict_result.items():
        print(f"  {key}: {value}")
    
    # 提取为结构化对象
    struct_result = extractor.extract_inspiration_structured(test_text)
    print(f"\n结构化对象结果:")
    print(f"  类型: {type(struct_result)}")
    print(f"  主题: {struct_result.theme}")
    print(f"  人物: {struct_result.characters}")
    print(f"  转换为字典: {struct_result.to_dict()}")
    
    print()


def demo_error_handling():
    """演示错误处理"""
    print("=== 错误处理演示 ===")
    
    # 测试无效JSON响应
    invalid_json_llm = MockLLM(fixed_response="这不是有效的JSON")
    extractor = InspirationExtractor(invalid_json_llm)
    
    test_text = "这是一段测试文本，用于验证错误处理。"
    result = extractor.extract_inspiration(test_text)
    
    print("无效JSON响应处理:")
    print(f"  主题: {result['theme']}")
    print(f"  人物: {result['characters']}")
    print(f"  世界观: {result['world_elements']}")
    
    # 测试LLM调用失败
    from src.extractor import LLMInterface
    
    class FailingLLM(LLMInterface):
        def generate(self, prompt: str) -> str:
            raise Exception("模拟API调用失败")
        
        def get_model_name(self) -> str:
            return "FailingLLM"
    
    failing_extractor = InspirationExtractor(FailingLLM())
    result = failing_extractor.extract_inspiration(test_text)
    
    print("\nLLM调用失败处理:")
    print(f"  主题: {result['theme']}")
    print(f"  世界观: {result['world_elements']}")
    
    print()


def demo_custom_prompt_template():
    """演示自定义提示词模板"""
    print("=== 自定义提示词模板演示 ===")
    
    # 创建自定义模板
    custom_template = """请仔细分析以下文本并提取关键信息：

文本：{text_chunk}

请返回JSON格式，包含：
- 主要主题（简洁明了）
- 主要角色（列表格式）
- 背景设定
- 核心句子

格式：
```json
{{"theme": "主题", "characters": ["角色"], "world_elements": "背景", "raw_excerpt": "核心句子"}}
```"""
    
    prompt_template = PromptTemplate(template=custom_template)
    mock_llm = MockLLM()
    extractor = InspirationExtractor(mock_llm, prompt_template)
    
    test_text = "勇敢的骑士在龙的巢穴中寻找传说中的宝藏。"
    
    # 查看生成的提示词
    prompt = prompt_template.format(test_text)
    print("生成的提示词:")
    print(prompt[:200] + "...")
    
    # 执行提取
    result = extractor.extract_inspiration(test_text)
    print(f"\n提取结果: {result}")
    
    print()


def demo_integration_with_input_module():
    """演示与输入模块的集成"""
    print("=== 与输入模块集成演示 ===")
    
    try:
        # 创建输入模块和提取器
        input_module = InputModule()
        mock_llm = MockLLM()
        extractor = InspirationExtractor(mock_llm)
        
        # 处理示例文件
        result = input_module.process_file(
            '../data/sample_novel.txt',
            split_method='chapters',
            enable_segmentation=False
        )
        
        print(f"文件处理结果: {result['chunks_count']} 个章节")
        
        # 对每个章节提取灵感
        inspirations = []
        for i, chunk in enumerate(result['chunks'][:2]):  # 只处理前2章
            print(f"\n--- 处理章节: {chunk['title']} ---")
            inspiration = extractor.extract_inspiration(chunk['content'])
            inspirations.append({
                'chapter_title': chunk['title'],
                'inspiration': inspiration
            })
            
            print(f"主题: {inspiration['theme']}")
            print(f"人物: {inspiration['characters']}")
            print(f"世界观: {inspiration['world_elements'][:50]}...")
        
        print(f"\n总共提取了 {len(inspirations)} 个章节的灵感")
        
    except FileNotFoundError:
        print("示例文件不存在，跳过集成演示")
    except Exception as e:
        print(f"集成演示失败: {e}")
    
    print()


def demo_model_comparison():
    """演示不同模型的比较"""
    print("=== 模型比较演示 ===")
    
    test_text = "在遥远的星球上，外星文明正在计划一次重要的星际会议。"
    
    # 不同的模拟响应
    responses = {
        "GPT风格": '''```json
{
    "theme": "科幻，外交",
    "characters": ["外星外交官", "星际议会成员"],
    "world_elements": "遥远星球，星际政治",
    "raw_excerpt": "星际会议即将召开"
}
```''',
        "Claude风格": '''```json
{
    "theme": "星际文明，和平对话",
    "characters": ["智慧外星人", "和平使者"],
    "world_elements": "多元宇宙，文明交流",
    "raw_excerpt": "文明间的重要对话"
}
```''',
        "简化风格": '''```json
{
    "theme": "太空，会议",
    "characters": ["外星人"],
    "world_elements": "太空背景",
    "raw_excerpt": "外星会议"
}
```'''
    }
    
    for style_name, response in responses.items():
        print(f"--- {style_name} ---")
        mock_llm = MockLLM(fixed_response=response)
        extractor = InspirationExtractor(mock_llm)
        
        result = extractor.extract_inspiration(test_text)
        print(f"主题: {result['theme']}")
        print(f"人物: {result['characters']}")
        print(f"世界观: {result['world_elements']}")
        print()


def main():
    """主演示函数"""
    print("=== 小说灵感提取 Agent - 灵感提取模块演示 ===\n")
    
    # 运行所有演示
    demo_mock_llm()
    demo_inspiration_extractor()
    demo_custom_llm_response()
    demo_structured_data()
    demo_error_handling()
    demo_custom_prompt_template()
    demo_integration_with_input_module()
    demo_model_comparison()
    
    print("=== 演示完成 ===")
    print("\n使用说明:")
    print("1. MockLLM适用于测试和开发")
    print("2. OpenAIModel和ClaudeModel需要相应的API密钥")
    print("3. 所有模型都实现了LLMInterface接口，可以互换使用")
    print("4. InspirationExtractor提供了完整的错误处理机制")
    print("5. 提取结果可直接用于数据库存储")


if __name__ == "__main__":
    main()