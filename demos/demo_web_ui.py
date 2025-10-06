"""
Web界面演示脚本 - 展示如何启动和使用Web界面

本脚本演示：
1. 如何启动Web服务
2. 如何配置不同的数据库
3. 如何访问不同的功能

Usage:
    python demo_web_ui.py --port 8000 --db web_demo.db
    python demo_web_ui.py --help
"""

import argparse
import sys
import os
import threading
import time
import webbrowser
from pathlib import Path

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    import uvicorn
    from src.web_ui import create_web_app
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所需依赖：")
    print("pip install fastapi uvicorn jinja2 python-multipart aiofiles")
    sys.exit(1)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="小说灵感提取系统 Web 界面演示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python demo_web_ui.py                          # 使用默认配置启动
  python demo_web_ui.py --port 8080              # 指定端口
  python demo_web_ui.py --db my_database.db      # 指定数据库
  python demo_web_ui.py --host 0.0.0.0           # 允许外部访问
  python demo_web_ui.py --no-browser             # 启动后不自动打开浏览器
  python demo_web_ui.py --dev                    # 开发模式（自动重载）

访问地址: http://localhost:8000
        """
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器主机地址 (默认: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--db",
        default="web_ui_demo.db",
        help="数据库文件路径 (默认: web_ui_demo.db)"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="启动后不自动打开浏览器"
    )
    
    parser.add_argument(
        "--dev",
        action="store_true",
        help="开发模式（启用自动重载）"
    )
    
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        help="日志级别 (默认: info)"
    )
    
    return parser.parse_args()


def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                   📚 小说灵感提取系统                          ║
    ║                      Web界面演示                              ║
    ║                                                              ║
    ║  基于AI的智能小说灵感提取与检索平台                           ║
    ║  支持 TXT/PDF/EPUB 文件上传和智能分析                        ║
    ║  提供关键词检索和语义检索功能                                  ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_system_info(args):
    """打印系统信息"""
    print(f"🔧 配置信息:")
    print(f"   主机地址: {args.host}")
    print(f"   端口号: {args.port}")
    print(f"   数据库: {args.db}")
    print(f"   开发模式: {'是' if args.dev else '否'}")
    print(f"   日志级别: {args.log_level}")
    print("")


def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("jinja2", "Jinja2"),
        ("aiofiles", "aiofiles")
    ]
    
    missing_packages = []
    
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ 所有依赖项已安装")
    return True


def check_database(db_path):
    """检查数据库状态"""
    print(f"🗄️  检查数据库: {db_path}")
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"   ✅ 数据库文件存在 (大小: {size:,} 字节)")
        
        # 简单检查表结构
        try:
            import sqlite3
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"   📋 包含表: {', '.join([t[0] for t in tables])}")
                
                # 检查灵感记录数量
                if ('inspirations',) in tables:
                    cursor.execute("SELECT COUNT(*) FROM inspirations;")
                    count = cursor.fetchone()[0]
                    print(f"   📊 灵感记录数: {count:,}")
        except Exception as e:
            print(f"   ⚠️  数据库检查失败: {e}")
    else:
        print("   🆕 数据库文件不存在，将创建新数据库")


def open_browser_delayed(url, delay=2):
    """延迟打开浏览器"""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 已在浏览器中打开: {url}")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            print(f"请手动访问: {url}")
    
    thread = threading.Thread(target=_open, daemon=True)
    thread.start()


def print_usage_tips():
    """打印使用提示"""
    tips = """
    💡 使用提示:
    
    📤 文件上传:
       • 支持 TXT、PDF、EPUB 格式
       • 最大文件大小: 50MB
       • 可选择不同AI模型进行分析
    
    ⚙️ 模型配置:
       • 支持多种厂商: 通义千问、OpenAI、Claude、DeepSeek
       • 安全保存API密钥到本地配置文件
       • 支持连接测试和动态切换
       • 配置后立即生效，无需重启
    
    🔍 智能检索:
       • 关键词匹配: 基于文本关键词搜索
       • 语义检索: 基于AI理解的语义相似度搜索
       • 混合检索: 结合关键词和语义的综合搜索
    
    📊 结果导出:
       • 支持JSON格式导出
       • 包含完整的搜索结果和评分信息
    
    ⚙️  系统配置:
       • 可在界面中查看当前模型状态
       • 支持动态切换AI模型
       • 实时显示处理进度
    
    🎆 模型配置演示:
       1. 点击「模型配置」区域
       2. 选择厂商（推荐：通义千问）
       3. 输入您的API密钥
       4. 点击「测试连接」验证配置
       5. 点击「保存配置」完成设置
       6. 上传文件即可使用新模型进行灵感提取
    
    🆘 获取帮助:
       • 按 Ctrl+C 停止服务
       • 查看控制台日志了解系统状态
       • 检查浏览器开发者工具排查前端问题
    """
    print(tips)


def main():
    """主函数"""
    args = parse_arguments()
    
    print_banner()
    print_system_info(args)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    print("")
    
    # 检查数据库
    check_database(args.db)
    print("")
    
    # 创建Web应用
    print("🚀 创建Web应用...")
    try:
        app = create_web_app(args.db)
        print("✅ Web应用创建成功")
    except Exception as e:
        print(f"❌ Web应用创建失败: {e}")
        sys.exit(1)
    
    # 准备启动参数
    server_url = f"http://{args.host}:{args.port}"
    
    print(f"🌐 启动Web服务器...")
    print(f"   访问地址: {server_url}")
    print("")
    
    # 打印使用提示
    print_usage_tips()
    
    # 延迟打开浏览器
    if not args.no_browser:
        print("🌐 将在2秒后自动打开浏览器...")
        open_browser_delayed(server_url)
    else:
        print(f"🌐 请手动访问: {server_url}")
    
    print("")
    print("=" * 60)
    print("服务器启动中... 按 Ctrl+C 停止服务")
    print("=" * 60)
    print("")
    
    # 启动服务器
    try:
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level=args.log_level,
            reload=args.dev,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n")
        print("👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()