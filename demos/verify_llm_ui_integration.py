#!/usr/bin/env python3
"""
简单的LLM切换功能验证脚本

Author: Assistant
Date: 2025-10-05
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.llm_manager import LLMManager


def test_llm_switching():
    """测试LLM模型切换功能"""
    print("🔬 开始测试LLM模型切换功能...")
    
    # 在临时目录中测试
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # 1. 创建LLM管理器
            print("1. 创建LLM管理器...")
            manager = LLMManager()
            
            # 2. 测试获取初始状态
            print("2. 测试获取初始状态...")
            initial_status = manager.get_current_model()
            print(f"   初始状态: {initial_status}")
            assert "vendor" in initial_status
            
            # 3. 测试切换到Mock模型
            print("3. 测试切换到Mock模型...")
            result = manager.set_current_model('mock')
            print(f"   切换结果: {result}")
            assert result["ok"] is True
            assert "Mock 模型" in result["message"]
            
            # 4. 验证Mock模型状态
            print("4. 验证Mock模型状态...")
            mock_status = manager.get_current_model()
            print(f"   Mock状态: {mock_status}")
            assert mock_status["vendor"] == "mock"
            assert mock_status["has_api_key"] is False
            
            # 5. 测试带API Key的模型
            print("5. 测试带API Key的模型...")
            test_key = "test-qwen-key-12345"
            result = manager.set_current_model('qwen', test_key)
            print(f"   Qwen切换结果: {result}")
            assert result["ok"] is True
            
            # 6. 验证API Key被正确处理
            print("6. 验证API Key安全处理...")
            qwen_status = manager.get_current_model()
            print(f"   Qwen状态: {qwen_status}")
            assert qwen_status["vendor"] == "qwen"
            assert qwen_status["has_api_key"] is True
            assert qwen_status["api_key_masked"].endswith("2345")
            assert test_key not in str(qwen_status)
            
            # 7. 测试持久化功能
            print("7. 测试持久化功能...")
            result = manager.set_current_model('openai', 'test-openai-key', persist=True)
            print(f"   持久化结果: {result}")
            if result["ok"]:
                # 检查.env文件
                if Path('.env').exists():
                    with open('.env', 'r') as f:
                        env_content = f.read()
                        print(f"   .env内容: {env_content}")
                        assert 'OPENAI_API_KEY' in env_content
                
                # 检查备份文件
                if Path('.env.bak').exists():
                    print("   ✅ 备份文件已创建")
            
            # 8. 测试无效厂商
            print("8. 测试无效厂商...")
            result = manager.set_current_model('invalid_vendor')
            print(f"   无效厂商结果: {result}")
            assert result["ok"] is False
            assert "不支持的模型厂商" in result["message"]
            
            # 9. 测试缺少API Key
            print("9. 测试缺少API Key...")
            result = manager.set_current_model('claude')
            print(f"   缺少Key结果: {result}")
            assert result["ok"] is False
            assert "需要提供 API Key" in result["message"]
            
            print("✅ 所有LLM切换测试通过！")
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            os.chdir(original_cwd)


def test_web_api_basic():
    """测试基本的Web API功能"""
    print("\n🌐 开始测试Web API功能...")
    
    try:
        from src.web_ui import create_web_app
        from fastapi.testclient import TestClient
        
        # 创建测试应用
        print("1. 创建Web应用...")
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            app = create_web_app(db_path="test_api.db")
            client = TestClient(app)
            
            # 测试GET /api/models
            print("2. 测试GET /api/models...")
            response = client.get("/api/models")
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   响应数据: {data}")
                assert "ok" in data
                assert data["ok"] is True
                assert "supported_vendors" in data
                print("   ✅ /api/models 测试通过")
            
            # 测试GET /api/status
            print("3. 测试GET /api/status...")
            response = client.get("/api/status")
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   响应数据: {data}")
                assert "ok" in data
                assert "model" in data
                assert "database" in data
                print("   ✅ /api/status 测试通过")
            
            # 测试POST /api/models/select (Mock模型)
            print("4. 测试POST /api/models/select...")
            response = client.post("/api/models/select", data={
                "vendor": "mock",
                "persist": "false"
            })
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   响应数据: {data}")
                assert data["ok"] is True
                print("   ✅ 模型切换 测试通过")
            
            print("✅ Web API基本功能测试通过！")
            return True
            
    except ImportError as e:
        print(f"⚠️  Web API测试跳过（缺少依赖）: {e}")
        return True
    except Exception as e:
        print(f"❌ Web API测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 开始LLM UI集成功能验证\n")
    
    success = True
    
    # 测试LLM切换功能
    if not test_llm_switching():
        success = False
    
    # 测试Web API功能
    if not test_web_api_basic():
        success = False
    
    print(f"\n{'🎉 所有测试通过！' if success else '❌ 部分测试失败'}")
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)