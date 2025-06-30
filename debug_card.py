#!/usr/bin/env python3
"""Debug script for qBittorrent Tasks Card loading issues."""

import os
import sys

def check_files():
    """Check if all required files exist."""
    base_path = "custom_components/qbittorrent_tasks"
    required_files = [
        "manifest.json",
        "__init__.py",
        "frontend.py",
        "www/qbittorrent-tasks-card.js"
    ]
    
    print("=== File Check ===")
    for file in required_files:
        full_path = os.path.join(base_path, file)
        exists = os.path.exists(full_path)
        print(f"{'✓' if exists else '✗'} {full_path}")
        if not exists:
            print(f"  ERROR: Missing required file: {full_path}")
    print()

def check_manifest():
    """Check manifest.json configuration."""
    manifest_path = "custom_components/qbittorrent_tasks/manifest.json"
    print("=== Manifest Check ===")
    
    if not os.path.exists(manifest_path):
        print("✗ manifest.json not found")
        return
    
    try:
        import json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        print(f"✓ Domain: {manifest.get('domain', 'NOT SET')}")
        print(f"✓ Name: {manifest.get('name', 'NOT SET')}")
        print(f"✓ Version: {manifest.get('version', 'NOT SET')}")
        
        if manifest.get('frontend'):
            print("✓ Frontend: enabled")
        else:
            print("⚠ Frontend: not explicitly enabled (this might cause issues)")
            
    except Exception as e:
        print(f"✗ Error reading manifest.json: {e}")
    print()

def check_js_file():
    """Check JavaScript file."""
    js_path = "custom_components/qbittorrent_tasks/www/qbittorrent-tasks-card.js"
    print("=== JavaScript File Check ===")
    
    if not os.path.exists(js_path):
        print("✗ JavaScript file not found")
        return
    
    try:
        with open(js_path, 'r') as f:
            content = f.read()
        
        # Check for key components
        checks = [
            ("customElements.define", "Custom element definition"),
            ("QBittorrentTasksCard", "Main class"),
            ("setConfig", "setConfig method"),
            ("set hass", "hass setter"),
            ("window.customCards", "Card registration")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✓ {description}: found")
            else:
                print(f"✗ {description}: missing")
                
        print(f"✓ File size: {len(content)} bytes")
        
    except Exception as e:
        print(f"✗ Error reading JavaScript file: {e}")
    print()

def generate_troubleshooting_steps():
    """Generate troubleshooting steps."""
    print("=== Troubleshooting Steps ===")
    print("1. 重启Home Assistant")
    print("2. 清除浏览器缓存 (Ctrl+Shift+R 或 Cmd+Shift+R)")
    print("3. 检查Home Assistant日志中的错误信息")
    print("4. 在浏览器开发者工具中检查网络请求:")
    print("   - 打开F12开发者工具")
    print("   - 查看Network标签")
    print("   - 刷新页面")
    print("   - 查找qbittorrent-tasks-card.js的请求状态")
    print("5. 检查浏览器控制台是否有JavaScript错误")
    print("6. 验证集成是否正确安装和配置")
    print()
    
    print("=== Manual URL Test ===")
    print("在浏览器中访问以下URL来测试JavaScript文件是否可访问:")
    print("http://your-ha-ip:8123/qbittorrent_tasks/qbittorrent-tasks-card.js")
    print("(将your-ha-ip替换为你的Home Assistant IP地址)")
    print()

if __name__ == "__main__":
    print("qBittorrent Tasks Card Debug Tool")
    print("=" * 40)
    
    check_files()
    check_manifest()
    check_js_file()
    generate_troubleshooting_steps()
