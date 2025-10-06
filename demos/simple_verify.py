"""
简单的Web界面验证脚本
"""

import sys
from pathlib import Path

# 添加源代码路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    print("🧪 简单验证开始...")
    
    # 检查文件存在
    files = [
        "src/web_ui.py",
        "templates/index.html", 
        "static/style.css",
        "static/app.js",
        "tests/test_web_ui.py",
        "demo_web_ui.py",
        "WEB_UI_SUMMARY.md"
    ]
    
    print("📁 检查文件存在性:")
    for file_path in files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size:,} 字节)")
        else:
            print(f"❌ {file_path} 不存在")
    
    # 尝试导入模块
    print("\n📦 检查模块导入:")
    try:
        print("  导入 FastAPI...")
        import fastapi
        print(f"  ✅ FastAPI {fastapi.__version__}")
        
        print("  导入 Uvicorn...")
        import uvicorn
        print(f"  ✅ Uvicorn {uvicorn.__version__}")
        
        print("  导入 Jinja2...")
        import jinja2
        print(f"  ✅ Jinja2 {jinja2.__version__}")
        
        print("  导入 aiofiles...")
        import aiofiles
        print(f"  ✅ aiofiles")
        
    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        return False
    
    print("\n🎉 基础验证完成！")
    print("\n💡 要启动Web界面，请运行:")
    print("   python demo_web_ui.py")
    
    return True

if __name__ == "__main__":
    main()