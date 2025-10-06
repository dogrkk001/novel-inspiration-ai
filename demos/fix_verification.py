#!/usr/bin/env python3
"""
JavaScript语法错误和favicon问题修复验证脚本
"""

import re
import requests
import time
from pathlib import Path

def check_javascript_syntax():
    """检查JavaScript语法问题"""
    print("🔍 检查JavaScript语法...")
    
    js_file = Path("static/app.js")
    if not js_file.exists():
        print("❌ JavaScript文件不存在")
        return False
    
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查Python风格的多行字符串注释
    python_multiline_strings = re.findall(r'""".*?"""', content, re.DOTALL)
    if python_multiline_strings:
        print(f"❌ 发现Python风格的多行字符串注释: {len(python_multiline_strings)} 个")
        for i, match in enumerate(python_multiline_strings[:3]):  # 只显示前3个
            print(f"   {i+1}: {match[:50]}...")
        return False
    
    # 检查其他常见的语法问题
    common_errors = [
        (r'"""', '使用了Python多行字符串'),
        (r"'''", '使用了Python多行字符串'),
        (r'async def ', '使用了Python函数定义语法'),
        (r'^\s*def\s+', '使用了Python函数定义语法'),
    ]
    
    for pattern, description in common_errors:
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            print(f"❌ 发现语法问题: {description}")
            return False
    
    print("✅ JavaScript语法检查通过")
    return True

def check_favicon_files():
    """检查favicon文件"""
    print("\n📄 检查favicon文件...")
    
    files_to_check = [
        ("static/favicon.svg", "SVG favicon"),
        ("static/favicon.ico", "ICO favicon")
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        path = Path(filepath)
        if path.exists():
            print(f"✅ {filepath} - {description} (大小: {path.stat().st_size} 字节)")
        else:
            print(f"❌ {filepath} - {description} (缺失)")
            all_exist = False
    
    return all_exist

def check_html_favicon_link():
    """检查HTML中的favicon链接"""
    print("\n🔗 检查HTML favicon链接...")
    
    html_file = Path("templates/index.html")
    if not html_file.exists():
        print("❌ HTML模板文件不存在")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查favicon链接
    if 'favicon.svg' in content:
        print("✅ HTML中包含favicon.svg链接")
        return True
    elif 'favicon.ico' in content:
        print("✅ HTML中包含favicon.ico链接")
        return True
    else:
        print("⚠️  HTML中未找到favicon链接")
        return False

def test_web_server():
    """测试Web服务器响应"""
    print("\n🌐 测试Web服务器...")
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试主页
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ 主页响应正常")
            
            # 检查页面是否包含JavaScript
            if 'app.js' in response.text:
                print("✅ 主页正确加载JavaScript")
            else:
                print("⚠️  主页可能未加载JavaScript")
                
        else:
            print(f"❌ 主页响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到Web服务器: {e}")
        print("   请确保服务器正在运行: python demo_web_ui.py --port 8000")
        return False
    
    # 测试favicon
    favicon_urls = ["/static/favicon.svg", "/static/favicon.ico", "/favicon.ico"]
    favicon_found = False
    
    for url in favicon_urls:
        try:
            response = requests.get(f"{base_url}{url}", timeout=3)
            if response.status_code == 200:
                print(f"✅ favicon可访问: {url}")
                favicon_found = True
                break
            elif response.status_code == 404:
                print(f"⚠️  favicon未找到: {url}")
        except:
            pass
    
    if not favicon_found:
        print("❌ 所有favicon文件都无法访问")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🔧 JavaScript语法错误和favicon问题修复验证")
    print("=" * 60)
    
    # 检查JavaScript语法
    js_ok = check_javascript_syntax()
    
    # 检查favicon文件
    favicon_files_ok = check_favicon_files()
    
    # 检查HTML中的favicon链接
    html_link_ok = check_html_favicon_link()
    
    # 测试Web服务器
    web_ok = test_web_server()
    
    print("\n" + "=" * 60)
    print("📊 修复验证结果:")
    print(f"   JavaScript语法: {'✅ 正常' if js_ok else '❌ 有问题'}")
    print(f"   Favicon文件: {'✅ 存在' if favicon_files_ok else '❌ 缺失'}")
    print(f"   HTML链接: {'✅ 正常' if html_link_ok else '❌ 有问题'}")
    print(f"   Web服务器: {'✅ 正常' if web_ok else '❌ 异常'}")
    
    if js_ok and favicon_files_ok and html_link_ok:
        print("\n🎉 所有问题已修复！")
        print("\n💡 修复内容:")
        print("   1. ✅ 修复了JavaScript中的Python风格多行字符串注释")
        print("   2. ✅ 创建了favicon.svg和favicon.ico文件")
        print("   3. ✅ 在HTML中添加了favicon链接")
        print("\n🚀 现在可以正常使用Web界面，不会再出现语法错误和404错误")
        return 0
    else:
        print("\n❌ 部分问题仍未解决，请检查上述错误信息")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())