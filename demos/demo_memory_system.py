#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目记忆系统演示脚本
展示如何使用记忆模块来记录和管理项目开发进度

运行方式:
    python demos/demo_memory_system.py
"""

import sys
import json
from pathlib import Path

try:
    from src.memory_module import (
        ProjectMemory, MemoryType, Priority,
        quick_log_progress, quick_log_bug_fix, export_session_context
    )
except ImportError as e:
    # 如果直接导入失败，尝试通过路径添加方式导入
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    try:
        from src.memory_module import (
            ProjectMemory, MemoryType, Priority,
            quick_log_progress, quick_log_bug_fix, export_session_context
        )
    except ImportError as e2:
        print(f"❌ 导入错误: {e2}")
        print("请确保在项目根目录运行此脚本")
        sys.exit(1)


def demo_basic_usage():
    """演示基本使用方法"""
    print("🎯 演示1: 基本记忆管理")
    print("=" * 50)
    
    # 创建记忆管理器
    memory = ProjectMemory()
    
    # 添加项目信息记忆
    project_id = memory.add_memory(
        memory_type=MemoryType.PROJECT_INFO,
        title="小说灵感AI项目初始化",
        content="""
        完成了小说灵感AI项目的基础架构搭建：
        - 前后端分离设计
        - Next.js + React前端
        - Python Flask后端
        - SQLite数据库
        - 模块化架构设计
        """,
        tags=["项目初始化", "架构设计", "技术栈"],
        priority=Priority.HIGH,
        context={
            "version": "1.0.0",
            "tech_stack": ["Python", "Next.js", "React", "SQLite"],
            "start_date": "2025-10-05"
        },
        file_references=[
            "src/",
            "src/ui/",
            "src/database.py",
            "src/web_ui.py"
        ]
    )
    print(f"✅ 添加项目信息记忆: {project_id}")
    
    # 添加开发进度记忆
    progress_id = memory.add_memory(
        memory_type=MemoryType.DEV_PROGRESS,
        title="完成UI界面重构",
        content="""
        根据用户反馈，将原有的IDE风格界面重构为ChatGPT风格：
        1. 删除复杂的多页面设计
        2. 实现极简聊天模式和完整工作台模式
        3. 优化动画效果和交互体验
        4. 增强错误处理和网络状态检测
        5. 实现流畅的视觉反馈系统
        """,
        tags=["UI重构", "用户体验", "动画优化"],
        priority=Priority.CRITICAL,
        context={
            "user_feedback": "界面过于复杂，需要简化",
            "design_style": "ChatGPT风格",
            "key_features": ["极简模式", "沉浸式对话", "流畅动画"]
        },
        file_references=[
            "src/ui/src/components/enhanced-workspace.js",
            "src/ui/src/app/globals.css",
            "src/ui/src/app/page.js"
        ]
    )
    print(f"✅ 添加开发进度记忆: {progress_id}")
    
    # 添加BUG修复记忆
    bug_id = memory.add_memory(
        memory_type=MemoryType.BUG_FIXES,
        title="修复CSS @apply错误",
        content="""
        问题: Tailwind CSS配置中出现"Unknown at rule @apply"错误
        原因: 重复的@tailwind指令和无效的@apply使用
        解决方案:
        1. 移除重复的@tailwind指令
        2. 修复自定义样式中的@apply语法
        3. 优化CSS结构和组织方式
        """,
        tags=["BUG修复", "CSS", "Tailwind"],
        priority=Priority.HIGH,
        file_references=[
            "src/ui/src/app/globals.css",
            "src/ui/tailwind.config.js"
        ]
    )
    print(f"✅ 添加BUG修复记忆: {bug_id}")
    
    print(f"\n📊 当前记忆统计:")
    summary = memory.get_project_summary()
    print(f"   总记忆数: {summary['total_memories']}")
    print(f"   类型分布: {summary['type_distribution']}")


def demo_search_functionality():
    """演示搜索功能"""
    print("\n🔍 演示2: 记忆搜索功能")
    print("=" * 50)
    
    memory = ProjectMemory()
    
    # 搜索开发进度记忆
    dev_memories = memory.search_memories(
        memory_type=MemoryType.DEV_PROGRESS,
        limit=5
    )
    print(f"🚀 找到 {len(dev_memories)} 条开发进度记忆:")
    for record in dev_memories:
        print(f"   📝 {record.title} ({record.timestamp[:10]})")
    
    # 搜索高优先级记忆
    critical_memories = memory.search_memories(
        priority=Priority.CRITICAL,
        limit=5
    )
    print(f"\n⚡ 找到 {len(critical_memories)} 条关键记忆:")
    for record in critical_memories:
        print(f"   🎯 {record.title} ({record.memory_type.value})")
    
    # 搜索最近记忆
    recent_memories = memory.get_recent_memories(days=30, limit=10)
    print(f"\n🕒 最近30天的 {len(recent_memories)} 条记忆:")
    for record in recent_memories:
        print(f"   📅 {record.title} - {record.timestamp[:10]}")


def demo_context_export():
    """演示上下文导出功能"""
    print("\n📤 演示3: 新对话上下文导出")
    print("=" * 50)
    
    # 导出上下文
    context = export_session_context()
    
    print("🚀 新对话上下文摘要:")
    print(f"   📈 总记忆数: {context['project_summary']['total_memories']}")
    print(f"   🎯 关键项目数: {len(context['critical_items'])}")
    print(f"   📋 最近进度数: {len(context['recent_progress'])}")
    print(f"   🏗️  架构决策数: {len(context['architecture_decisions'])}")
    
    # 保存到文件
    context_file = Path("memories/session_context.json")
    context_file.parent.mkdir(exist_ok=True)
    
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 上下文已保存到: {context_file}")
    
    # 显示关键项目
    print("\n🎯 关键项目概览:")
    for item in context['critical_items'][:3]:
        print(f"   ⚡ {item['title']}")
        print(f"      📄 {item['content'][:100]}...")
        if item['files']:
            print(f"      📁 {', '.join(item['files'][:3])}")


def demo_quick_functions():
    """演示快捷函数"""
    print("\n⚡ 演示4: 快捷记录功能")
    print("=" * 50)
    
    # 快速记录开发进度
    progress_id = quick_log_progress(
        title="实现记忆模块核心功能",
        content="""
        完成了项目记忆模块的核心功能开发:
        - 实现SQLite数据库存储
        - 支持多种记忆类型和优先级
        - 提供搜索和筛选功能
        - 支持上下文导出和恢复
        - 创建CLI管理工具
        """,
        files=[
            "src/memory_module.py",
            "src/memory_cli.py", 
            "demos/demo_memory_system.py"
        ]
    )
    print(f"✅ 快速记录开发进度: {progress_id}")
    
    # 快速记录BUG修复
    bug_id = quick_log_bug_fix(
        title="修复类型注解错误",
        content="""
        问题: Python类型检查器报告Optional类型使用错误
        解决: 将None默认参数的类型注解修改为Optional[Type]
        影响: 提高代码类型安全性和IDE支持
        """,
        files=["src/memory_module.py"]
    )
    print(f"✅ 快速记录BUG修复: {bug_id}")


def demo_cli_usage():
    """演示CLI工具使用方法"""
    print("\n💻 演示5: CLI工具使用说明")
    print("=" * 50)
    
    print("🔧 记忆管理CLI工具命令示例:")
    print("""
    # 添加开发进度记忆
    python src/memory_cli.py add --type dev_progress --title "完成功能X" --content "详细描述..."
    
    # 快速记录开发进度
    python src/memory_cli.py progress --title "优化性能" --content "提升了50%的响应速度"
    
    # 搜索记忆
    python src/memory_cli.py search --type dev_progress --limit 5 --verbose
    
    # 查看项目摘要
    python src/memory_cli.py summary
    
    # 导出新对话上下文
    python src/memory_cli.py export --output memories/new_session.json
    
    # 查看最近记忆
    python src/memory_cli.py recent --days 7 --limit 10
    
    # 备份记忆数据
    python src/memory_cli.py backup
    """)


def main():
    """主演示函数"""
    print("🧠 项目记忆系统演示")
    print("=" * 60)
    print("这个演示将展示如何使用记忆模块来管理项目开发进度和上下文")
    print()
    
    try:
        # 运行各个演示
        demo_basic_usage()
        demo_search_functionality()
        demo_context_export()
        demo_quick_functions()
        demo_cli_usage()
        
        print("\n🎉 演示完成!")
        print("=" * 60)
        print("💡 记忆模块的主要优势:")
        print("   ✅ 自动记录开发进度和决策")
        print("   ✅ 快速恢复项目上下文")
        print("   ✅ 支持多维度搜索和筛选")
        print("   ✅ 提供CLI工具便于日常使用")
        print("   ✅ 数据持久化和备份机制")
        print()
        print("📚 下一步建议:")
        print("   1. 在开发过程中持续记录关键进展")
        print("   2. 定期导出上下文用于新对话会话")
        print("   3. 使用CLI工具进行日常记忆管理")
        print("   4. 根据项目需要扩展记忆类型和功能")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()