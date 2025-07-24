#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地构建脚本
用于在本地环境中构建可执行文件
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True, encoding='utf-8')
        print(f"命令执行成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stdout:
            print(f"标准输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def check_dependencies():
    """检查依赖是否安装"""
    print("检查依赖...")
    
    required_packages = ['PyQt5', 'pysubs2', 'qfluentwidgets', 'requests', 'pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少以下依赖: {', '.join(missing_packages)}")
        print("正在安装缺少的依赖...")
        if not run_command(f"pip install {' '.join(missing_packages)}"):
            print("依赖安装失败，请手动安装")
            return False
    
    print("所有依赖检查完成")
    return True

def clean_build():
    """清理构建目录"""
    print("清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除 {dir_name}")
    
    # 清理 .pyc 文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 获取当前平台
    current_platform = platform.system()
    print(f"当前平台: {current_platform}")
    
    # 构建命令
    if os.path.exists('build.spec'):
        cmd = "pyinstaller build.spec"
    else:
        # 基本构建命令
        cmd = 'pyinstaller --onefile --windowed --name "SRT转ASS字幕转换器" toAss.py'
        
        # 添加图标（如果存在）
        if os.path.exists('icon.ico'):
            cmd += ' --icon=icon.ico'
    
    # 执行构建
    if not run_command(cmd):
        print("构建失败")
        return False
    
    print("构建完成")
    return True

def post_build():
    """构建后处理"""
    print("执行构建后处理...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("dist目录不存在")
        return False
    
    # 列出生成的文件
    print("生成的文件:")
    for file in dist_dir.iterdir():
        print(f"  {file.name} ({file.stat().st_size / 1024 / 1024:.1f} MB)")
    
    # 创建发布目录
    release_dir = Path('release')
    release_dir.mkdir(exist_ok=True)
    
    # 复制文件到发布目录
    current_platform = platform.system()
    for file in dist_dir.iterdir():
        if file.is_file():
            if current_platform == 'Windows':
                new_name = f"{file.stem}-windows{file.suffix}"
            elif current_platform == 'Darwin':
                new_name = f"{file.stem}-macos{file.suffix}"
            else:
                new_name = f"{file.stem}-linux{file.suffix}"
            
            shutil.copy2(file, release_dir / new_name)
            print(f"已复制到 release/{new_name}")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("SRT转ASS字幕转换器 - 本地构建脚本")
    print("=" * 50)
    
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("错误: 需要Python 3.9或更高版本")
        return False
    
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    
    # 检查主文件是否存在
    if not os.path.exists('toAss.py'):
        print("错误: 找不到 toAss.py 文件")
        return False
    
    # 执行构建步骤
    steps = [
        ("检查依赖", check_dependencies),
        ("清理构建目录", clean_build),
        ("构建可执行文件", build_executable),
        ("构建后处理", post_build),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'-' * 30}")
        print(f"步骤: {step_name}")
        print(f"{'-' * 30}")
        
        if not step_func():
            print(f"步骤 '{step_name}' 失败")
            return False
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print("可执行文件位于 dist/ 目录")
    print("发布文件位于 release/ 目录")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
