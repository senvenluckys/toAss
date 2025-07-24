#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目设置脚本
用于快速设置开发环境和构建项目
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, cwd=None):
    """运行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 9):
        print("错误: 需要Python 3.9或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"Python版本检查通过: {sys.version}")
    return True

def install_dependencies():
    """安装依赖"""
    print("安装Python依赖...")
    
    # 升级pip
    if not run_command("python -m pip install --upgrade pip"):
        return False
    
    # 安装依赖
    if not run_command("pip install -r requirements.txt"):
        return False
    
    print("依赖安装完成")
    return True

def setup_git_hooks():
    """设置Git钩子"""
    hooks_dir = ".git/hooks"
    if not os.path.exists(hooks_dir):
        print("Git仓库未初始化，跳过钩子设置")
        return True
    
    # 创建pre-commit钩子
    pre_commit_hook = os.path.join(hooks_dir, "pre-commit")
    hook_content = """#!/bin/sh
# Pre-commit hook for Python project

echo "Running pre-commit checks..."

# Check Python syntax
python -m py_compile toAss.py
if [ $? -ne 0 ]; then
    echo "Python syntax check failed"
    exit 1
fi

echo "Pre-commit checks passed"
"""
    
    try:
        with open(pre_commit_hook, 'w') as f:
            f.write(hook_content)
        os.chmod(pre_commit_hook, 0o755)
        print("Git pre-commit钩子设置完成")
    except Exception as e:
        print(f"设置Git钩子失败: {e}")
    
    return True

def create_desktop_shortcut():
    """创建桌面快捷方式"""
    current_platform = platform.system()
    
    if current_platform == "Windows":
        # Windows快捷方式
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "SRT转ASS字幕转换器.lnk")
            target = os.path.join(os.getcwd(), "toAss.py")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.save()
            
            print(f"桌面快捷方式已创建: {path}")
        except ImportError:
            print("创建Windows快捷方式需要安装 pywin32 和 winshell")
        except Exception as e:
            print(f"创建快捷方式失败: {e}")
    
    elif current_platform == "Darwin":  # macOS
        # macOS应用程序包
        app_name = "SRT转ASS字幕转换器.app"
        app_path = os.path.join(os.path.expanduser("~/Desktop"), app_name)
        
        try:
            os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
            
            # 创建启动脚本
            launcher_script = f"""#!/bin/bash
cd "{os.getcwd()}"
python toAss.py
"""
            launcher_path = f"{app_path}/Contents/MacOS/launcher"
            with open(launcher_path, 'w') as f:
                f.write(launcher_script)
            os.chmod(launcher_path, 0o755)
            
            # 创建Info.plist
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.subtitleconverter.toass</string>
    <key>CFBundleName</key>
    <string>SRT转ASS字幕转换器</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
</dict>
</plist>"""
            
            with open(f"{app_path}/Contents/Info.plist", 'w') as f:
                f.write(plist_content)
            
            print(f"macOS应用程序包已创建: {app_path}")
        except Exception as e:
            print(f"创建macOS应用程序包失败: {e}")
    
    else:  # Linux
        # Linux桌面文件
        desktop_file = os.path.expanduser("~/Desktop/SRT转ASS字幕转换器.desktop")
        
        try:
            desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=SRT转ASS字幕转换器
Comment=字幕格式转换工具
Exec=python "{os.path.join(os.getcwd(), 'toAss.py')}"
Path={os.getcwd()}
Terminal=false
Categories=AudioVideo;
"""
            
            with open(desktop_file, 'w') as f:
                f.write(desktop_content)
            os.chmod(desktop_file, 0o755)
            
            print(f"Linux桌面文件已创建: {desktop_file}")
        except Exception as e:
            print(f"创建Linux桌面文件失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("SRT转ASS字幕转换器 - 项目设置")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 设置Git钩子
    setup_git_hooks()
    
    # 询问是否创建快捷方式
    create_shortcut = input("\n是否创建桌面快捷方式? (y/N): ").lower().strip()
    if create_shortcut in ['y', 'yes']:
        create_desktop_shortcut()
    
    print("\n" + "=" * 50)
    print("设置完成！")
    print("\n可用命令:")
    print("  python toAss.py          # 运行程序")
    print("  python build.py          # 构建可执行文件")
    print("  python version.py        # 版本管理")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
