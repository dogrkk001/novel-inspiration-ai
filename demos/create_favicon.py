#!/usr/bin/env python3
"""创建简单的favicon.ico文件"""

import base64
from pathlib import Path

# 这是一个简单的16x16像素书本图标的ico文件的base64编码
favicon_data = """
AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAAEAA
AABAAAAAAAAAAAACoFAACkBQAAqAUAAKQFAAAqBQAApAUAAKgFAACoFQAAqAUAAKQFAAAqBQAAKg
UAACoFAAAKBQAACgUAAKRQAAAqBQAAFQUAAKQFAACoFQAAAqBQAAKRQAAAqBQAAqAUAAKgFAAAqB
QAAKgFAACoFQAAKgUAACoFAAAKBQAACgUAAKRQAAAqBQAAFQUAAKQFAACoFQAAAqBQAAKRQAAAqB
QAAqAUAAKgFAAAqBQAAKgFAACoFQAAKgUAACoFAAAKBQAACgUAAKRQAAAqBQAAFQUAAKQDAACoFQA
AAqBQAAKRQAAAqBQAAqAUAAKgFAAAqBQAAKgFAACoFQAAKgUAACoFAAAKBQAACgUAAKRQAAAqBQA
"""

def create_favicon():
    """创建favicon.ico文件"""
    
    # 更简单的方法：创建一个包含📚图标的SVG favicon
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <text y=".9em" font-size="80">📚</text>
</svg>'''
    
    # 保存为SVG favicon（现代浏览器支持）
    favicon_path = Path("static/favicon.svg")
    favicon_path.parent.mkdir(exist_ok=True)
    
    with open(favicon_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✅ 创建favicon文件: {favicon_path}")
    
    # 同时创建一个空的ico文件避免404错误
    ico_path = Path("static/favicon.ico")
    
    # 最小的有效ICO文件头
    ico_data = bytes([
        0x00, 0x00,  # Reserved
        0x01, 0x00,  # Type (1 = ICO)
        0x01, 0x00,  # Number of images
        # Image directory entry
        0x10,        # Width (16)
        0x10,        # Height (16)
        0x00,        # Colors in palette (0 = no palette)
        0x00,        # Reserved
        0x01, 0x00,  # Color planes
        0x04, 0x00,  # Bits per pixel
        0x28, 0x01, 0x00, 0x00,  # Size of image data
        0x16, 0x00, 0x00, 0x00,  # Offset to image data
        # Bitmap header
        0x28, 0x00, 0x00, 0x00,  # Size of this header
        0x10, 0x00, 0x00, 0x00,  # Width
        0x20, 0x00, 0x00, 0x00,  # Height (2x for ICO)
        0x01, 0x00,              # Planes
        0x04, 0x00,              # Bits per pixel
        0x00, 0x00, 0x00, 0x00,  # Compression
        0x00, 0x01, 0x00, 0x00,  # Image size
        0x00, 0x00, 0x00, 0x00,  # X pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Y pixels per meter
        0x00, 0x00, 0x00, 0x00,  # Colors used
        0x00, 0x00, 0x00, 0x00,  # Important colors
        # Color palette (16 colors for 4bpp)
    ] + [0x00] * 64 + [  # 16 palette entries * 4 bytes each
        # Bitmap data (128 bytes for 16x16 at 4bpp)
    ] + [0x00] * 128 + [
        # AND mask (32 bytes for 16x16 at 1bpp)
    ] + [0x00] * 32)
    
    with open(ico_path, 'wb') as f:
        f.write(ico_data)
    
    print(f"✅ 创建ICO文件: {ico_path}")

if __name__ == "__main__":
    create_favicon()