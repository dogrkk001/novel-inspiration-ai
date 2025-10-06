#!/usr/bin/env python3
"""
使用千问模型启动Web界面的简化脚本
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    print("🚀 启动小说灵感提取系统 (使用千问模型)")
    print("=" * 50)
    
    # 检查.env文件
    env_file = project_root / ".env"
    if not env_file.exists():
        print("❌ 找不到.env文件")
        print("💡 请先在项目根目录创建.env文件并配置QWEN_API_KEY")
        print("   可以复制.env.template文件并修改")
        return
    
    # 读取.env文件检查千问密钥
    with open(env_file, 'r', encoding='utf-8') as f:
        env_content = f.read()
        
    if 'QWEN_API_KEY=请在此处填入你的千问API密钥' in env_content or 'QWEN_API_KEY=your_qwen_api_key_here' in env_content:
        print("❌ 请先在.env文件中配置你的千问API密钥")
        print(f"   编辑文件: {env_file}")
        print("   将 QWEN_API_KEY= 后面填入你的真实API密钥")
        return
    
    print("✅ 找到千问API密钥配置")
    
    # 创建数据库目录
    db_dir = project_root / "data" / "demo_dbs"
    db_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = db_dir / "web_ui_demo.db"
    print(f"📀 数据库路径: {db_path}")
    
    # 启动Web界面
    try:
        from src.web_ui import create_web_app
        import uvicorn
        
        print("🔧 创建Web应用...")
        app = create_web_app(str(db_path))
        
        print("🌐 启动Web服务器...")
        print("   访问地址: http://127.0.0.1:8000")
        print("   使用 Ctrl+C 停止服务")
        print("")
        
        # 启动服务器
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("💡 请安装所需依赖:")
        print("   pip install fastapi uvicorn jinja2 python-multipart aiofiles")
    except KeyboardInterrupt:
        print("\n⏹️  用户停止服务")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()