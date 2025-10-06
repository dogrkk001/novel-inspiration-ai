#!/usr/bin/env python3
"""
模型配置功能验证脚本
验证模型配置相关的核心功能是否正常工作
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_web_ui_endpoints():
    """测试Web界面的模型配置相关端点"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔧 开始验证模型配置功能...")
    
    # 1. 测试获取当前模型
    try:
        response = requests.get(f"{base_url}/config/current-model", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 当前模型: {data.get('current_model', 'unknown')}")
            print(f"   模型名称: {data.get('model_name', 'unknown')}")
            print(f"   提供商: {data.get('provider', 'unknown')}")
        else:
            print(f"❌ 获取当前模型失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
        print("   请确保Web服务器正在运行 (python demo_web_ui.py)")
        return False
    
    # 2. 测试获取可用模型列表
    try:
        response = requests.get(f"{base_url}/config/available-models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            available = data.get('available_models', [])
            all_models = data.get('all_models', [])
            print(f"✅ 可用模型: {available}")
            print(f"   所有模型: {all_models}")
        else:
            print(f"❌ 获取可用模型失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取可用模型失败: {e}")
        return False
    
    # 3. 测试主页面加载
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ 主页面加载正常")
            # 检查是否包含模型配置相关内容
            if "模型配置" in response.text:
                print("✅ 主页面包含模型配置功能")
            else:
                print("⚠️  主页面可能缺少模型配置UI")
        else:
            print(f"❌ 主页面加载失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 主页面加载失败: {e}")
        return False
    
    return True

def check_file_structure():
    """检查文件结构是否完整"""
    print("\n📁 检查文件结构...")
    
    required_files = {
        "templates/index.html": "HTML模板",
        "static/style.css": "CSS样式",
        "static/app.js": "JavaScript逻辑",
        "src/web_ui.py": "Web界面核心",
        "src/llm_manager.py": "LLM管理器",
        "tests/test_model_config.py": "模型配置测试",
        "demo_web_ui.py": "演示脚本",
        "WEB_UI_SUMMARY.md": "技术文档"
    }
    
    all_exist = True
    for filepath, description in required_files.items():
        path = Path(filepath)
        if path.exists():
            print(f"✅ {filepath} - {description}")
        else:
            print(f"❌ {filepath} - {description} (缺失)")
            all_exist = False
    
    return all_exist

def check_llm_config():
    """检查LLM配置文件"""
    print("\n⚙️  检查LLM配置...")
    
    config_file = Path("llm_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"✅ 配置文件存在: {config_file}")
            print(f"   配置的模型数量: {len(config)}")
            
            for model_id, model_config in config.items():
                provider = model_config.get('provider', 'unknown')
                model_name = model_config.get('model_name', 'unknown')
                print(f"   - {model_id}: {provider} / {model_name}")
            
            return True
        except Exception as e:
            print(f"❌ 配置文件解析失败: {e}")
            return False
    else:
        print(f"⚠️  配置文件不存在: {config_file}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 小说灵感提取系统 - 模型配置功能验证")
    print("=" * 60)
    
    # 检查文件结构
    files_ok = check_file_structure()
    
    # 检查配置文件
    config_ok = check_llm_config()
    
    # 测试Web接口
    web_ok = test_web_ui_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 验证结果总结:")
    print(f"   文件结构: {'✅ 完整' if files_ok else '❌ 不完整'}")
    print(f"   配置文件: {'✅ 正常' if config_ok else '❌ 异常'}")
    print(f"   Web接口: {'✅ 正常' if web_ok else '❌ 异常'}")
    
    if files_ok and config_ok and web_ok:
        print("\n🎉 所有验证通过！模型配置功能已成功实现")
        print("\n💡 使用建议:")
        print("   1. 启动Web服务: python demo_web_ui.py")
        print("   2. 浏览器访问: http://127.0.0.1:8000")
        print("   3. 在「模型配置」区域添加您的API密钥")
        print("   4. 上传小说文件开始体验")
        return 0
    else:
        print("\n❌ 部分验证失败，请检查上述错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())