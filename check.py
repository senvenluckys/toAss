#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目状态检查脚本
检查项目配置和GitHub设置是否正确
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

REPO_OWNER = "senvenluckys"
REPO_NAME = "toAss"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"

def check_file_exists(filepath, description=""):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {filepath} {description}")
        return True
    else:
        print(f"✗ {filepath} 不存在 {description}")
        return False

def check_python_syntax():
    """检查Python语法"""
    print("\n检查Python语法...")
    try:
        result = subprocess.run([sys.executable, "-m", "py_compile", "toAss.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Python语法检查通过")
            return True
        else:
            print(f"✗ Python语法错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 语法检查失败: {e}")
        return False

def check_dependencies():
    """检查依赖是否可以导入"""
    print("\n检查依赖...")
    
    dependencies = {
        'PyQt5': 'PyQt5',
        'pysubs2': 'pysubs2', 
        'qfluentwidgets': 'qfluentwidgets',
        'requests': 'requests'
    }
    
    all_ok = True
    for name, module in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} 可以导入")
        except ImportError:
            print(f"✗ {name} 无法导入")
            all_ok = False
    
    return all_ok

def check_git_status():
    """检查Git状态"""
    print("\n检查Git状态...")
    
    if not os.path.exists('.git'):
        print("✗ 不是Git仓库")
        return False
    
    try:
        # 检查远程仓库
        result = subprocess.run(["git", "remote", "get-url", "origin"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            if REPO_URL in remote_url or f"{REPO_OWNER}/{REPO_NAME}" in remote_url:
                print(f"✓ 远程仓库设置正确: {remote_url}")
            else:
                print(f"⚠ 远程仓库URL不匹配: {remote_url}")
        else:
            print("✗ 没有设置远程仓库")
            return False
        
        # 检查当前分支
        result = subprocess.run(["git", "branch", "--show-current"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"✓ 当前分支: {branch}")
        
        # 检查工作目录状态
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout.strip():
                print("⚠ 有未提交的更改")
                print(result.stdout.strip())
            else:
                print("✓ 工作目录干净")
        
        return True
        
    except Exception as e:
        print(f"✗ Git检查失败: {e}")
        return False

def check_github_repo():
    """检查GitHub仓库状态"""
    print("\n检查GitHub仓库...")
    
    try:
        # 检查仓库是否存在
        response = requests.get(f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}", 
                              timeout=10)
        
        if response.status_code == 200:
            repo_info = response.json()
            print(f"✓ GitHub仓库存在: {repo_info['html_url']}")
            print(f"  描述: {repo_info.get('description', '无')}")
            print(f"  默认分支: {repo_info['default_branch']}")
            print(f"  最后更新: {repo_info['updated_at']}")
            
            # 检查Actions是否启用
            if repo_info.get('has_actions', False):
                print("✓ GitHub Actions已启用")
            else:
                print("⚠ GitHub Actions可能未启用")
            
            return True
        elif response.status_code == 404:
            print("✗ GitHub仓库不存在")
            print(f"请访问 https://github.com/new 创建仓库")
            return False
        else:
            print(f"✗ 无法访问GitHub仓库: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ 网络错误，无法检查GitHub仓库: {e}")
        return False

def check_github_actions():
    """检查GitHub Actions状态"""
    print("\n检查GitHub Actions...")
    
    try:
        # 检查工作流运行
        response = requests.get(
            f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs",
            timeout=10
        )
        
        if response.status_code == 200:
            runs = response.json()
            if runs['total_count'] > 0:
                latest_run = runs['workflow_runs'][0]
                print(f"✓ 找到 {runs['total_count']} 个工作流运行")
                print(f"  最新运行: {latest_run['status']} - {latest_run['conclusion']}")
                print(f"  分支: {latest_run['head_branch']}")
                print(f"  时间: {latest_run['created_at']}")
                
                if latest_run['conclusion'] == 'success':
                    print("✓ 最新构建成功")
                elif latest_run['conclusion'] == 'failure':
                    print("✗ 最新构建失败")
                    print(f"  查看详情: {latest_run['html_url']}")
                else:
                    print(f"⚠ 构建状态: {latest_run['status']}")
            else:
                print("⚠ 没有找到工作流运行")
                print("可能需要推送代码或创建标签来触发构建")
            
            return True
        else:
            print(f"✗ 无法获取Actions信息: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ 网络错误，无法检查GitHub Actions: {e}")
        return False

def check_releases():
    """检查GitHub Releases"""
    print("\n检查GitHub Releases...")
    
    try:
        response = requests.get(
            f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases",
            timeout=10
        )
        
        if response.status_code == 200:
            releases = response.json()
            if releases:
                print(f"✓ 找到 {len(releases)} 个发布版本")
                latest = releases[0]
                print(f"  最新版本: {latest['tag_name']}")
                print(f"  发布时间: {latest['published_at']}")
                print(f"  资产数量: {len(latest['assets'])}")
                
                if latest['assets']:
                    print("  可下载文件:")
                    for asset in latest['assets']:
                        size_mb = asset['size'] / 1024 / 1024
                        print(f"    - {asset['name']} ({size_mb:.1f} MB)")
                
                return True
            else:
                print("⚠ 没有找到发布版本")
                print("可以使用 'python version.py release 1.0.0' 创建发布")
                return True
        else:
            print(f"✗ 无法获取Releases信息: {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"✗ 网络错误，无法检查Releases: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 SRT转ASS字幕转换器 - 项目状态检查")
    print("=" * 60)
    
    print(f"项目目录: {os.getcwd()}")
    print(f"目标仓库: {REPO_URL}")
    
    # 检查项目文件
    print("\n📁 检查项目文件...")
    files_ok = all([
        check_file_exists("toAss.py", "- 主程序文件"),
        check_file_exists("requirements.txt", "- 依赖列表"),
        check_file_exists(".github/workflows/build.yml", "- GitHub Actions配置"),
        check_file_exists("README.md", "- 项目说明"),
        check_file_exists("LICENSE", "- 许可证"),
        check_file_exists(".gitignore", "- Git忽略文件"),
    ])
    
    # 执行各项检查
    checks = [
        ("Python语法", check_python_syntax),
        ("Python依赖", check_dependencies),
        ("Git状态", check_git_status),
        ("GitHub仓库", check_github_repo),
        ("GitHub Actions", check_github_actions),
        ("GitHub Releases", check_releases),
    ]
    
    results = {"files": files_ok}
    
    for check_name, check_func in checks:
        print(f"\n{'-' * 40}")
        print(f"🔍 {check_name}")
        print(f"{'-' * 40}")
        results[check_name] = check_func()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 检查结果总结")
    print("=" * 60)
    
    all_passed = True
    for name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20} {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有检查都通过了！项目配置正确。")
    else:
        print("\n⚠️  有一些问题需要解决。")
    
    print(f"\n🔗 有用的链接:")
    print(f"  仓库主页: {REPO_URL}")
    print(f"  Actions: {REPO_URL}/actions")
    print(f"  Releases: {REPO_URL}/releases")
    print(f"  Issues: {REPO_URL}/issues")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
