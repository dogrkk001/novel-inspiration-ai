"""
Web界面快速验证脚本
验证Web界面模块的基本功能
"""

import sys
import tempfile
import os
from pathlib import Path
import sqlite3

# 添加源代码路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_web_ui_creation():
    """测试Web应用创建"""
    print("🧪 测试Web应用创建...")
    
    # 创建临时数据库
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    try:
        # 初始化数据库
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE inspirations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_file TEXT NOT NULL,
                    chapter TEXT,
                    raw_text TEXT NOT NULL,
                    idea TEXT NOT NULL,
                    tags TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        
        # 导入并创建Web应用
        from src.web_ui import create_web_app
        
        app = create_web_app(db_path)
        print("✅ Web应用创建成功")
        
        # 检查路由
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/upload", "/search", "/export/{format}"]
        
        for expected in expected_routes:
            if any(expected.replace("{format}", "json") in route or expected == route for route in routes):
                print(f"✅ 路由 {expected} 已注册")
            else:
                print(f"⚠️  路由 {expected} 未找到")
        
        return True
        
    except Exception as e:
        print(f"❌ Web应用创建失败: {e}")
        return False
    finally:
        # 清理
        if os.path.exists(db_path):
            os.unlink(db_path)

def test_template_files():
    """测试模板文件存在性"""
    print("🧪 检查模板文件...")
    
    files_to_check = [
        "templates/index.html",
        "static/style.css", 
        "static/app.js"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} (大小: {size:,} 字节)")
        else:
            print(f"❌ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def test_llm_adapter():
    """测试LLM适配器"""
    print("🧪 测试LLM适配器...")
    
    try:
        from src.web_ui import LLMAdapter
        
        # 创建模拟LLM
        class MockLLM:
            def generate_text(self, prompt):
                return f"Mock response for: {prompt}"
            
            def get_model_info(self):
                return {"provider": "test", "model_name": "test-model"}
        
        mock_llm = MockLLM()
        adapter = LLMAdapter(mock_llm)
        
        # 测试generate方法
        result = adapter.generate("测试提示")
        assert "Mock response" in result
        print("✅ generate方法工作正常")
        
        # 测试get_model_name方法
        model_name = adapter.get_model_name()
        assert model_name == "test-test-model"
        print("✅ get_model_name方法工作正常")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM适配器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 Web界面模块验证开始")
    print("=" * 50)
    
    tests = [
        ("Web应用创建", test_web_ui_creation),
        ("模板文件检查", test_template_files), 
        ("LLM适配器", test_llm_adapter)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
            print(f"🎉 {test_name} 通过")
        else:
            print(f"💥 {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎊 所有测试通过！Web界面模块可以正常工作。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关模块。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)