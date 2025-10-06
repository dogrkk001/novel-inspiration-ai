#!/usr/bin/env python3
"""
检索模块演示脚本

展示如何在 CLI 中使用检索模块的各种功能。
包括关键词搜索、源文件过滤、日期范围查询等。

Author: Assistant
Date: 2025-10-04
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.search import (
    search_inspirations,
    search_by_source,
    search_by_date_range,
    SearchError
)
from src.database import InspirationDatabase, DatabaseError


def setup_logging(verbose: bool = False) -> None:
    """配置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def create_sample_database(db_path: str) -> None:
    """创建示例数据库和数据"""
    print(f"创建示例数据库: {db_path}")
    
    try:
        db = InspirationDatabase(db_path)
        
        # 示例数据
        sample_data = [
            {
                "source_file": "科幻小说.txt",
                "chapter": "第一章 星际旅行",
                "raw_text": "宇宙飞船在星空中穿梭，闪烁的星光如同指引方向的明灯。船员们怀着对未知世界的好奇和勇气。",
                "idea": "通过星空描写营造科幻氛围，用光的意象象征希望和指引，展现探索精神。",
                "tags": "科幻,星空,勇气,探索"
            },
            {
                "source_file": "科幻小说.txt",
                "chapter": "第二章 新世界",
                "raw_text": "陌生的星球表面覆盖着奇异的植物，散发着淡蓝色的光芒，仿佛整个世界都在呼吸。",
                "idea": "创造性的外星环境描写，用颜色和生命感营造神秘而美丽的异世界。",
                "tags": "科幻,外星,环境描写,神秘"
            },
            {
                "source_file": "古典文学.txt",
                "chapter": "序章",
                "raw_text": "春风又绿江南岸，明月何时照我还。游子的思乡之情如潮水般涌起。",
                "idea": "经典的思乡主题，通过自然景物的变化表达时间流逝和情感变化。",
                "tags": "古典,思乡,自然,情感"
            },
            {
                "source_file": "现代都市.txt",
                "chapter": "第三章",
                "raw_text": "高楼大厦的霓虹灯在夜晚闪烁，城市的喧嚣中却有一种特殊的孤独感。",
                "idea": "现代都市生活的对比描写，繁华与孤独的反差能引起读者共鸣。",
                "tags": "都市,现代,孤独,对比"
            },
            {
                "source_file": "励志故事.txt",
                "chapter": "第一章 起点",
                "raw_text": "即使在最黑暗的夜晚，也要相信太阳会再次升起。坚持下去，就能看到希望的曙光。",
                "idea": "用日出日落的自然循环比喻人生的起伏，传达坚持和希望的主题。",
                "tags": "励志,希望,坚持,比喻"
            }
        ]
        
        record_ids = db.save_batch(sample_data)
        print(f"✅ 成功创建 {len(record_ids)} 条示例数据")
        
    except (DatabaseError, Exception) as e:
        print(f"❌ 创建示例数据失败: {e}")
        sys.exit(1)


def display_results(results: list, title: str) -> None:
    """显示搜索结果"""
    print(f"\n=== {title} ===")
    print(f"找到 {len(results)} 条记录\n")
    
    for i, result in enumerate(results, 1):
        print(f"【记录 {i}】")
        print(f"ID: {result['id']}")
        print(f"源文件: {result['source_file']}")
        print(f"章节: {result['chapter'] or '无'}")
        print(f"原文: {result['raw_text'][:80]}...")
        print(f"创意: {result['idea'][:80]}...")
        print(f"标签: {result['tags'] or '无'}")
        print(f"创建时间: {result['created_at']}")
        print("-" * 50)


def demo_keyword_search(db_path: str) -> None:
    """演示关键词搜索"""
    keywords = ["希望", "描写", "科幻", "现代"]
    
    for keyword in keywords:
        try:
            results = search_inspirations(db_path, keyword, limit=3)
            display_results(results, f"关键词搜索: '{keyword}'")
        except SearchError as e:
            print(f"❌ 关键词搜索失败: {e}")


def demo_source_search(db_path: str) -> None:
    """演示源文件搜索"""
    sources = ["科幻小说.txt", "古典文学.txt", "不存在的文件.txt"]
    
    for source in sources:
        try:
            results = search_by_source(db_path, source)
            display_results(results, f"源文件搜索: '{source}'")
        except SearchError as e:
            print(f"❌ 源文件搜索失败: {e}")


def demo_date_search(db_path: str) -> None:
    """演示日期范围搜索"""
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    date_ranges = [
        (today, today, "今天"),
        (yesterday, today, "昨天到今天"),
        ("2023-01-01", "2023-12-31", "2023年全年")
    ]
    
    for start, end, description in date_ranges:
        try:
            results = search_by_date_range(db_path, start, end)
            display_results(results, f"日期范围搜索: {description} ({start} 到 {end})")
        except SearchError as e:
            print(f"❌ 日期搜索失败: {e}")


def demo_error_handling(db_path: str) -> None:
    """演示错误处理"""
    print(f"\n=== 错误处理演示 ===")
    
    # 1. 测试无效数据库路径
    try:
        search_inspirations("/nonexistent/path.db", "test")
    except SearchError as e:
        print(f"✅ 正确捕获数据库路径错误: {e}")
    
    # 2. 测试空关键词
    try:
        search_inspirations(db_path, "")
    except SearchError as e:
        print(f"✅ 正确捕获空关键词错误: {e}")
    
    # 3. 测试无效日期格式
    try:
        search_by_date_range(db_path, "invalid-date", "2023-01-01")
    except SearchError as e:
        print(f"✅ 正确捕获日期格式错误: {e}")
    
    # 4. 测试日期范围错误
    try:
        search_by_date_range(db_path, "2023-01-02", "2023-01-01")
    except SearchError as e:
        print(f"✅ 正确捕获日期范围错误: {e}")


def interactive_search(db_path: str) -> None:
    """交互式搜索模式"""
    print(f"\n=== 交互式搜索模式 ===")
    print("输入 'quit' 退出")
    
    while True:
        print(f"\n请选择搜索类型:")
        print("1. 关键词搜索")
        print("2. 源文件搜索")
        print("3. 日期范围搜索")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == '4' or choice.lower() == 'quit':
            break
        elif choice == '1':
            keyword = input("请输入搜索关键词: ").strip()
            if keyword:
                try:
                    limit = int(input("请输入结果限制数量 (默认10): ") or "10")
                    results = search_inspirations(db_path, keyword, limit=limit)
                    display_results(results, f"关键词搜索: '{keyword}'")
                except (SearchError, ValueError) as e:
                    print(f"❌ 搜索失败: {e}")
        elif choice == '2':
            source = input("请输入源文件名: ").strip()
            if source:
                try:
                    results = search_by_source(db_path, source)
                    display_results(results, f"源文件搜索: '{source}'")
                except SearchError as e:
                    print(f"❌ 搜索失败: {e}")
        elif choice == '3':
            start = input("请输入开始日期 (YYYY-MM-DD): ").strip()
            end = input("请输入结束日期 (YYYY-MM-DD): ").strip()
            if start and end:
                try:
                    results = search_by_date_range(db_path, start, end)
                    display_results(results, f"日期范围搜索: {start} 到 {end}")
                except SearchError as e:
                    print(f"❌ 搜索失败: {e}")
        else:
            print("无效选择，请重新输入")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="检索模块演示脚本")
    parser.add_argument("--db", default="demo_inspirations.db", help="数据库文件路径")
    parser.add_argument("--create-sample", action="store_true", help="创建示例数据")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    parser.add_argument("--interactive", action="store_true", help="交互式搜索模式")
    parser.add_argument("--verbose", action="store_true", help="详细日志输出")
    
    args = parser.parse_args()
    
    # 配置日志
    setup_logging(args.verbose)
    
    db_path = args.db
    
    try:
        # 创建示例数据
        if args.create_sample:
            create_sample_database(db_path)
        
        # 检查数据库是否存在
        if not Path(db_path).exists():
            print(f"数据库文件不存在: {db_path}")
            print("使用 --create-sample 创建示例数据")
            return
        
        # 运行演示
        if args.demo:
            print(f"🔍 检索模块演示开始 (数据库: {db_path})")
            demo_keyword_search(db_path)
            demo_source_search(db_path)
            demo_date_search(db_path)
            demo_error_handling(db_path)
            print(f"\n🎉 演示完成!")
        
        # 交互式模式
        if args.interactive:
            interactive_search(db_path)
        
        # 如果没有指定任何操作，显示帮助
        if not any([args.create_sample, args.demo, args.interactive]):
            parser.print_help()
            print(f"\n示例用法:")
            print(f"  python {sys.argv[0]} --create-sample --demo")
            print(f"  python {sys.argv[0]} --interactive")
            
    except KeyboardInterrupt:
        print(f"\n\n👋 用户中断，再见!")
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()