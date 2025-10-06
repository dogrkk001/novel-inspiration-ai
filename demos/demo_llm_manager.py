#!/usr/bin/env python3
"""
LLM 管理器演示脚本 - 展示通用 LLM 接口配置的使用

演示功能：
1. 从配置文件加载多种 LLM 配置
2. 展示不同 LLM 提供商的统一调用
3. 动态添加和管理 LLM 模型
4. 配置文件和环境变量的使用示例

Usage:
    python demo_llm_manager.py
    python demo_llm_manager.py --config llm_config.json
    python demo_llm_manager.py --list-models
    python demo_llm_manager.py --test-model openai
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, Any

# 添加 src 目录到 Python 路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from src.llm_manager import LLMManager, LLMConfig, LLMProvider


def demo_basic_usage():
    """演示基础用法"""
    print("🔧 LLM 管理器基础用法演示")
    print("=" * 50)
    
    # 创建 LLM 管理器
    manager = LLMManager()
    
    print(f"✓ 创建 LLM 管理器成功")
    print(f"  - 默认模型: {manager.default_model}")
    
    # 列出所有模型
    all_models = manager.list_models()
    print(f"  - 所有模型: {', '.join(all_models)}")
    
    # 获取可用模型
    available_models = manager.get_available_models()
    print(f"  - 可用模型: {', '.join(available_models)}")
    
    return manager


def demo_text_generation(manager: LLMManager):
    """演示文本生成"""
    print("\n📝 文本生成演示")
    print("=" * 30)
    
    prompt = "请用一句话描述人工智能的作用"
    
    # 使用默认模型
    print(f"📝 使用默认模型生成文本...")
    print(f"   提示词: {prompt}")
    
    try:
        result = manager.generate_text(prompt)
        print(f"   生成结果: {result[:100]}...")
        
        # 获取模型信息
        info = manager.get_model_info()
        print(f"   模型信息: {info['provider']}-{info['model_name']}")
        
    except Exception as e:
        print(f"   生成失败: {e}")


def demo_embedding_generation(manager: LLMManager):
    """演示嵌入向量生成"""
    print("\n🔢 嵌入向量演示")
    print("=" * 30)
    
    text = "人工智能是未来科技发展的重要方向"
    
    try:
        embedding = manager.get_embedding(text)
        print(f"📝 输入文本: {text}")
        print(f"🔢 嵌入向量长度: {len(embedding)}")
        print(f"🔢 向量示例: [{embedding[0]:.3f}, {embedding[1]:.3f}, ..., {embedding[-1]:.3f}]")
        
    except Exception as e:
        print(f"❌ 嵌入生成失败: {e}")


def demo_model_management(manager: LLMManager):
    """演示模型管理"""
    print("\n⚙️ 模型管理演示")
    print("=" * 30)
    
    # 动态添加模型
    print("➕ 动态添加自定义模型...")
    custom_config = LLMConfig(
        provider="mock",
        model_name="custom-demo-model",
        max_tokens=500,
        temperature=0.9
    )
    
    manager.add_model('custom_demo', custom_config)
    print(f"   ✓ 添加模型: custom_demo")
    
    # 测试新模型
    print("🧪 测试新添加的模型...")
    try:
        result = manager.generate_text("测试自定义模型", model_name='custom_demo')
        print(f"   ✓ 生成成功: {result[:50]}...")
        
        info = manager.get_model_info('custom_demo')
        print(f"   📊 模型信息: {info}")
        
    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
    
    # 移除模型
    print("➖ 移除自定义模型...")
    manager.remove_model('custom_demo')
    print(f"   ✓ 移除完成")


def demo_config_loading():
    """演示配置加载"""
    print("\n📋 配置加载演示")
    print("=" * 30)
    
    # 从配置文件加载
    config_file = Path("llm_config.json")
    if config_file.exists():
        print(f"📁 从配置文件加载: {config_file}")
        manager = LLMManager(config_path=str(config_file))
        
        configs = manager.configs
        print(f"   ✓ 加载了 {len(configs)} 个配置:")
        for name, config in configs.items():
            print(f"     - {name}: {config.provider} ({config.model_name})")
    else:
        print(f"⚠️ 配置文件不存在: {config_file}")
        print("   使用默认配置")
        manager = LLMManager()
    
    return manager


def demo_environment_variables():
    """演示环境变量配置"""
    print("\n🌍 环境变量配置演示")
    print("=" * 35)
    
    # 检查常见的环境变量
    env_vars = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY', 
        'QWEN_API_KEY',
        'DEEPSEEK_API_KEY'
    ]
    
    found_keys = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            found_keys.append(var)
            print(f"   ✓ {var}: {'*' * 8}{value[-4:] if len(value) > 4 else '****'}")
        else:
            print(f"   ❌ {var}: 未设置")
    
    if found_keys:
        print(f"\n🎉 检测到 {len(found_keys)} 个有效的 API key")
        print("   可以尝试使用 --use-llm 参数测试真实模型")
    else:
        print("\n💡 提示:")
        print("   - 设置环境变量以使用真实的 LLM 模型")
        print("   - 例如: export OPENAI_API_KEY='your-api-key'")


def test_specific_model(manager: LLMManager, model_name: str):
    """测试特定模型"""
    print(f"\n🧪 测试特定模型: {model_name}")
    print("=" * 40)
    
    try:
        # 检查模型是否存在
        if model_name not in manager.list_models():
            print(f"❌ 模型 '{model_name}' 不存在")
            print(f"   可用模型: {', '.join(manager.list_models())}")
            return
        
        # 获取模型信息
        info = manager.get_model_info(model_name)
        print(f"📊 模型信息:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # 检查可用性
        model = manager.get_model(model_name)
        is_available = model.is_available()
        print(f"🔍 可用性检查: {'✓ 可用' if is_available else '❌ 不可用'}")
        
        if is_available:
            # 测试文本生成
            print(f"📝 测试文本生成...")
            result = manager.generate_text("说一句鼓励的话", model_name=model_name)
            print(f"   结果: {result[:100]}...")
            
            # 测试嵌入（如果支持）
            try:
                print(f"🔢 测试嵌入向量...")
                embedding = manager.get_embedding("测试文本", model_name=model_name)
                print(f"   向量长度: {len(embedding)}")
            except NotImplementedError:
                print(f"   ⚠️ 该模型不支持嵌入向量")
            except Exception as e:
                print(f"   ❌ 嵌入测试失败: {e}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


def list_all_models(manager: LLMManager):
    """列出所有模型的详细信息"""
    print("\n📋 所有模型详细信息")
    print("=" * 40)
    
    models = manager.list_models()
    
    for i, model_name in enumerate(models, 1):
        print(f"\n[{i}] {model_name}")
        print("-" * 20)
        
        try:
            info = manager.get_model_info(model_name)
            model = manager.get_model(model_name)
            is_available = model.is_available()
            
            print(f"   提供商: {info.get('provider', 'unknown')}")
            print(f"   模型名: {info.get('model_name', 'unknown')}")
            print(f"   状态: {'✓ 可用' if is_available else '❌ 不可用'}")
            
            # 显示其他配置信息
            for key, value in info.items():
                if key not in ['provider', 'model_name']:
                    print(f"   {key}: {value}")
                    
        except Exception as e:
            print(f"   ❌ 获取信息失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="LLM 管理器演示脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 基础演示
  python demo_llm_manager.py
  
  # 指定配置文件
  python demo_llm_manager.py --config llm_config.json
  
  # 列出所有模型
  python demo_llm_manager.py --list-models
  
  # 测试特定模型
  python demo_llm_manager.py --test-model mock
  
  # 检查环境变量
  python demo_llm_manager.py --check-env
        """
    )
    
    parser.add_argument(
        '--config',
        help='指定配置文件路径'
    )
    
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='列出所有模型的详细信息'
    )
    
    parser.add_argument(
        '--test-model',
        help='测试特定模型'
    )
    
    parser.add_argument(
        '--check-env',
        action='store_true',
        help='检查环境变量配置'
    )
    
    args = parser.parse_args()
    
    print("🚀 LLM 管理器演示")
    print("=" * 50)
    
    try:
        if args.check_env:
            demo_environment_variables()
            return
        
        # 创建管理器
        if args.config:
            print(f"📁 使用配置文件: {args.config}")
            manager = LLMManager(config_path=args.config)
        else:
            manager = demo_config_loading()
        
        if args.list_models:
            list_all_models(manager)
            return
        
        if args.test_model:
            test_specific_model(manager, args.test_model)
            return
        
        # 完整演示
        demo_basic_usage()
        demo_text_generation(manager)
        demo_embedding_generation(manager)
        demo_model_management(manager)
        demo_environment_variables()
        
        print("\n🎉 演示完成！")
        print("\n💡 提示:")
        print("  - 使用 --list-models 查看所有模型")
        print("  - 使用 --test-model <name> 测试特定模型")
        print("  - 设置环境变量以使用真实的 LLM 模型")
        
    except KeyboardInterrupt:
        print(f"\n⏹ 用户中断演示")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 演示出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()