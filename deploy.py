#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速部署脚本
用于将项目推送到GitHub并设置自动构建
"""

import os
import sys
import subprocess
import json

REPO_URL = "https://github.com/senvenluckys/toAss.git"
REPO_NAME = "toAss"

def run_command(cmd, cwd=None, check=True):
    """运行命令"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(f"输出: {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"错误: {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stdout:
            print(f"标准输出: {e.stdout}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        return False

def check_git():
    """检查Git是否安装"""
    if not run_command("git --version", check=False):
        print("错误: Git未安装或不在PATH中")
        print("请先安装Git: https://git-scm.com/")
        return False
    return True

def init_git_repo():
    """初始化Git仓库"""
    print("初始化Git仓库...")
    
    # 检查是否已经是Git仓库
    if os.path.exists('.git'):
        print("Git仓库已存在")
        return True
    
    # 初始化仓库
    if not run_command("git init"):
        return False
    
    # 设置默认分支为main
    run_command("git branch -M main")
    
    return True

def setup_gitignore():
    """确保.gitignore文件存在且正确"""
    if not os.path.exists('.gitignore'):
        print("创建.gitignore文件...")
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# 项目特定文件
sub.json
settings.json
*.ico
*.icns

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db
"""
        try:
            with open('.gitignore', 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print(".gitignore文件已创建")
        except Exception as e:
            print(f"创建.gitignore文件失败: {e}")
            return False
    else:
        print(".gitignore文件已存在")
    return True

def add_remote_origin():
    """添加远程仓库"""
    print("设置远程仓库...")
    
    # 检查是否已有远程仓库
    result = subprocess.run("git remote get-url origin", shell=True, 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        current_url = result.stdout.strip()
        if current_url == REPO_URL:
            print(f"远程仓库已正确设置: {REPO_URL}")
            return True
        else:
            print(f"更新远程仓库URL: {current_url} -> {REPO_URL}")
            return run_command(f"git remote set-url origin {REPO_URL}")
    else:
        print(f"添加远程仓库: {REPO_URL}")
        return run_command(f"git remote add origin {REPO_URL}")

def commit_and_push():
    """提交并推送代码"""
    print("准备提交代码...")
    
    # 检查工作目录状态
    result = subprocess.run("git status --porcelain", shell=True, 
                          capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("没有需要提交的更改")
        return True
    
    # 添加所有文件
    if not run_command("git add ."):
        return False
    
    # 提交代码
    commit_message = "Setup GitHub Actions for automated builds"
    if not run_command(f'git commit -m "{commit_message}"'):
        return False
    
    # 推送到GitHub
    print("推送代码到GitHub...")
    if not run_command("git push -u origin main"):
        print("推送失败，可能需要先在GitHub上创建仓库")
        print(f"请访问: https://github.com/new")
        print(f"仓库名称: {REPO_NAME}")
        return False
    
    print("代码推送成功！")
    return True

def create_first_release():
    """创建第一个发布版本"""
    print("\n是否创建第一个发布版本？")
    print("这将触发GitHub Actions构建所有平台的可执行文件")
    
    create = input("创建v1.0.0发布版本? (y/N): ").lower().strip()
    if create not in ['y', 'yes']:
        return True
    
    # 创建标签
    if not run_command("git tag v1.0.0"):
        return False
    
    # 推送标签
    if not run_command("git push origin v1.0.0"):
        return False
    
    print("发布标签已创建并推送！")
    print("GitHub Actions将自动构建并创建Release")
    return True

def show_next_steps():
    """显示后续步骤"""
    print("\n" + "=" * 60)
    print("🎉 部署完成！")
    print("=" * 60)
    
    print(f"\n📍 仓库地址: {REPO_URL}")
    print(f"📍 Actions页面: https://github.com/senvenluckys/toAss/actions")
    print(f"📍 Releases页面: https://github.com/senvenluckys/toAss/releases")
    
    print("\n🔄 后续操作:")
    print("1. 访问GitHub仓库确认代码已推送")
    print("2. 检查Actions页面查看构建状态")
    print("3. 如果创建了标签，等待自动发布完成")
    
    print("\n⚙️ 本地开发命令:")
    print("  python toAss.py          # 运行程序")
    print("  python build.py          # 本地构建")
    print("  python version.py        # 版本管理")
    
    print("\n📝 版本发布:")
    print("  python version.py bump patch    # 增加补丁版本")
    print("  python version.py release 1.0.1 # 创建新发布")
    
    print("=" * 60)

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 SRT转ASS字幕转换器 - GitHub部署脚本")
    print("=" * 60)
    
    print(f"目标仓库: {REPO_URL}")
    print(f"当前目录: {os.getcwd()}")
    
    # 检查必要文件
    required_files = ['toAss.py', 'requirements.txt', '.github/workflows/build.yml']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"错误: 缺少必要文件: {', '.join(missing_files)}")
        print("请确保在正确的项目目录中运行此脚本")
        return False
    
    # 执行部署步骤
    steps = [
        ("检查Git", check_git),
        ("初始化Git仓库", init_git_repo),
        ("设置.gitignore", setup_gitignore),
        ("添加远程仓库", add_remote_origin),
        ("提交并推送代码", commit_and_push),
        ("创建发布版本", create_first_release),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{'-' * 40}")
        print(f"步骤: {step_name}")
        print(f"{'-' * 40}")
        
        if not step_func():
            print(f"步骤 '{step_name}' 失败")
            return False
    
    show_next_steps()
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
