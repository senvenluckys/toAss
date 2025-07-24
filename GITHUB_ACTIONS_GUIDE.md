# GitHub Actions 自动构建指南

本文档介绍如何使用GitHub Actions为SRT转ASS字幕转换器项目设置自动构建和发布。

## 📋 前提条件

1. **GitHub仓库**: 确保你的代码已推送到GitHub仓库
2. **权限设置**: 确保仓库有Actions权限（默认启用）
3. **分支保护**: 建议设置main/master分支保护规则

## 🚀 快速开始

### 1. 推送代码到GitHub

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: SRT转ASS字幕转换器"

# 添加远程仓库
git remote add origin https://github.com/senvenluckys/toAss.git

# 推送到GitHub
git push -u origin main
```

### 2. 启用GitHub Actions

1. 进入你的GitHub仓库
2. 点击 "Actions" 标签页
3. 如果是第一次使用，点击 "I understand my workflows, go ahead and enable them"

### 3. 触发构建

构建会在以下情况自动触发：

- **推送代码**到main/master分支
- **创建Pull Request**到main/master分支
- **创建版本标签**（如v1.0.0）

## 🏗️ 构建流程

### 自动构建

每次推送代码时，GitHub Actions会：

1. **多平台构建**: 在Windows、macOS、Linux上构建
2. **依赖安装**: 自动安装Python依赖
3. **代码检查**: 运行基本的导入测试
4. **生成可执行文件**: 使用PyInstaller打包
5. **上传构件**: 将生成的文件作为构件保存

### 查看构建状态

1. 进入仓库的 "Actions" 页面
2. 查看最新的工作流运行状态
3. 点击具体的运行查看详细日志

## 📦 发布版本

### 创建发布版本

有两种方式创建发布版本：

#### 方式1: 使用版本管理脚本

```bash
# 查看当前版本
python version.py current

# 增加版本号（patch: 1.0.0 -> 1.0.1）
python version.py bump patch

# 增加版本号（minor: 1.0.0 -> 1.1.0）
python version.py bump minor

# 增加版本号（major: 1.0.0 -> 2.0.0）
python version.py bump major

# 创建发布（会自动创建标签并推送）
python version.py release 1.0.0
```

#### 方式2: 手动创建标签

```bash
# 创建并推送标签
git tag v1.0.0
git push origin v1.0.0
```

### 发布流程

当推送版本标签时（如v1.0.0），GitHub Actions会：

1. **触发发布工作流**
2. **下载所有平台的构建文件**
3. **创建GitHub Release**
4. **上传可执行文件**作为发布资产

## 📁 构建产物

### 构件下载

对于每次构建，你可以：

1. 进入Actions页面
2. 点击具体的工作流运行
3. 在"Artifacts"部分下载构建文件

### 发布文件

发布版本会包含以下文件：

- `SRT转ASS字幕转换器-windows.exe` - Windows可执行文件
- `SRT转ASS字幕转换器-macos` - macOS可执行文件  
- `SRT转ASS字幕转换器-linux` - Linux可执行文件

## ⚙️ 自定义配置

### 修改构建配置

编辑 `.github/workflows/build.yml` 文件来自定义：

- **Python版本**: 修改`python-version`
- **操作系统**: 修改`matrix.include`部分
- **构建参数**: 修改PyInstaller命令
- **发布内容**: 修改release部分的描述

### 添加构建步骤

可以在工作流中添加：

```yaml
- name: Run tests
  run: |
    python -m pytest tests/

- name: Code quality check
  run: |
    pip install flake8
    flake8 toAss.py
```

## 🔧 故障排除

### 常见问题

1. **构建失败**
   - 检查依赖是否正确安装
   - 查看构建日志中的错误信息
   - 确保代码在本地能正常运行

2. **发布失败**
   - 检查标签格式是否正确（v1.0.0）
   - 确保有推送标签的权限
   - 检查GITHUB_TOKEN权限

3. **文件上传失败**
   - 检查文件路径是否正确
   - 确保构建成功生成了文件

### 调试技巧

1. **查看详细日志**
   ```yaml
   - name: Debug info
     run: |
       echo "Current directory: $(pwd)"
       echo "Files in dist:"
       ls -la dist/
   ```

2. **本地测试构建**
   ```bash
   python build.py
   ```

## 📊 监控和通知

### 构建状态徽章

在README.md中添加构建状态徽章：

```markdown
[![Build Status](https://github.com/senvenluckys/toAss/actions/workflows/build.yml/badge.svg)](https://github.com/senvenluckys/toAss/actions/workflows/build.yml)
```

### 通知设置

可以在GitHub仓库设置中配置：

1. 进入仓库 Settings > Notifications
2. 设置Actions失败时的通知方式

## 🔐 安全考虑

1. **敏感信息**: 不要在代码中包含API密钥等敏感信息
2. **权限控制**: 使用最小权限原则
3. **依赖安全**: 定期更新依赖包

## 📚 更多资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [PyInstaller文档](https://pyinstaller.readthedocs.io/)
- [工作流语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

如果遇到问题，请在仓库中创建Issue或查看Actions页面的详细日志。
