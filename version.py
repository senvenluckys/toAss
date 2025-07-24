#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本管理脚本
用于管理项目版本号和创建发布标签
"""

import os
import sys
import subprocess
import re
from datetime import datetime

# 版本信息
VERSION_FILE = 'toAss.py'
CURRENT_VERSION = '1.0.0'

def get_current_version():
    """从代码中获取当前版本号"""
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # 查找版本号
            match = re.search(r'setApplicationVersion\(["\']([^"\']+)["\']\)', content)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"无法读取版本号: {e}")
    return CURRENT_VERSION

def update_version(new_version):
    """更新代码中的版本号"""
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换版本号
        content = re.sub(
            r'setApplicationVersion\(["\']([^"\']+)["\']\)',
            f'setApplicationVersion("{new_version}")',
            content
        )
        
        with open(VERSION_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"版本号已更新为: {new_version}")
        return True
    except Exception as e:
        print(f"更新版本号失败: {e}")
        return False

def run_git_command(cmd):
    """运行git命令"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git命令执行失败: {e}")
        return None

def create_release_tag(version):
    """创建发布标签"""
    tag_name = f"v{version}"
    
    # 检查标签是否已存在
    existing_tags = run_git_command("git tag -l")
    if existing_tags and tag_name in existing_tags.split('\n'):
        print(f"标签 {tag_name} 已存在")
        return False
    
    # 检查是否有未提交的更改
    status = run_git_command("git status --porcelain")
    if status:
        print("有未提交的更改，请先提交所有更改")
        print("未提交的文件:")
        print(status)
        return False
    
    # 创建标签
    commit_message = f"Release version {version}"
    
    # 提交版本更新
    if not run_git_command("git add ."):
        return False
    
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("没有需要提交的更改")
    
    # 创建标签
    if not run_git_command(f'git tag -a {tag_name} -m "{commit_message}"'):
        return False
    
    print(f"标签 {tag_name} 创建成功")
    
    # 询问是否推送
    push = input("是否推送到远程仓库? (y/N): ").lower().strip()
    if push in ['y', 'yes']:
        if run_git_command("git push origin main") and run_git_command(f"git push origin {tag_name}"):
            print("推送成功")
            return True
        else:
            print("推送失败")
            return False
    
    return True

def bump_version(version_type='patch'):
    """增加版本号"""
    current = get_current_version()
    parts = current.split('.')
    
    if len(parts) != 3:
        print(f"无效的版本格式: {current}")
        return None
    
    major, minor, patch = map(int, parts)
    
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    else:
        print(f"无效的版本类型: {version_type}")
        return None
    
    return f"{major}.{minor}.{patch}"

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python version.py current                    # 显示当前版本")
        print("  python version.py bump [major|minor|patch]   # 增加版本号")
        print("  python version.py set <version>              # 设置版本号")
        print("  python version.py release [version]          # 创建发布")
        return
    
    command = sys.argv[1]
    
    if command == 'current':
        current = get_current_version()
        print(f"当前版本: {current}")
    
    elif command == 'bump':
        version_type = sys.argv[2] if len(sys.argv) > 2 else 'patch'
        new_version = bump_version(version_type)
        if new_version:
            print(f"当前版本: {get_current_version()}")
            print(f"新版本: {new_version}")
            confirm = input("确认更新版本号? (y/N): ").lower().strip()
            if confirm in ['y', 'yes']:
                update_version(new_version)
    
    elif command == 'set':
        if len(sys.argv) < 3:
            print("请指定版本号")
            return
        new_version = sys.argv[2]
        print(f"当前版本: {get_current_version()}")
        print(f"新版本: {new_version}")
        confirm = input("确认更新版本号? (y/N): ").lower().strip()
        if confirm in ['y', 'yes']:
            update_version(new_version)
    
    elif command == 'release':
        version = sys.argv[2] if len(sys.argv) > 2 else get_current_version()
        print(f"准备创建发布: v{version}")
        confirm = input("确认创建发布? (y/N): ").lower().strip()
        if confirm in ['y', 'yes']:
            # 更新版本号
            update_version(version)
            # 创建标签
            create_release_tag(version)
    
    else:
        print(f"未知命令: {command}")

if __name__ == '__main__':
    main()
