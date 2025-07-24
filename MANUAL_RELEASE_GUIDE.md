# 手动发布指南

如果GitHub Actions构建遇到问题，可以使用以下方法手动创建发布版本。

## 🚀 方法1：使用本地构建

### 步骤1：本地构建所有平台（如果可能）

```bash
# 在当前平台构建
python build.py

# 或使用PyInstaller直接构建
pyinstaller --onefile --noconsole --name "SRT转ASS字幕转换器" toAss.py
```

### 步骤2：检查构建结果

```bash
ls -la dist/
```

你应该看到生成的可执行文件。

### 步骤3：手动创建GitHub Release

1. 访问：https://github.com/senvenluckys/toAss/releases/new
2. 填写以下信息：
   - **Tag version**: `v1.0.4`
   - **Release title**: `Release v1.0.4`
   - **Description**:
     ```markdown
     ## SRT转ASS字幕转换器 v1.0.4
     
     ### 功能特性
     - 支持 SRT → ASS 转换
     - 支持 VTT → ASS 转换  
     - 支持 ASS → ASS 样式修改
     - 支持繁体中文转换
     - 支持自定义字幕样式和颜色
     - 支持批量文件处理
     - 现代化的用户界面
     
     ### 安装说明
     1. 下载对应平台的可执行文件
     2. 双击运行即可使用
     
     ### 从源码运行
     ```bash
     git clone https://github.com/senvenluckys/toAss.git
     cd toAss
     pip install -r requirements.txt
     python toAss.py
     ```
     ```

3. 上传文件：
   - 将`dist/`目录中的可执行文件拖拽到"Attach binaries"区域
   - 重命名文件（如果需要）

4. 点击"Publish release"

## 🛠️ 方法2：使用GitHub CLI

如果你安装了GitHub CLI：

```bash
# 创建release
gh release create v1.0.4 \
  --title "Release v1.0.4" \
  --notes "SRT转ASS字幕转换器 v1.0.4 - 支持多种字幕格式转换" \
  dist/*
```

## 📋 方法3：分步骤发布

### 步骤1：创建空的Release

1. 访问：https://github.com/senvenluckys/toAss/releases/new
2. 创建一个没有文件的release

### 步骤2：编辑Release添加文件

1. 进入刚创建的release页面
2. 点击"Edit release"
3. 上传构建的文件

## 🔧 构建不同平台版本

### Windows（在Windows系统上）
```cmd
pip install PyQt5 pysubs2 requests pyinstaller
pyinstaller --onefile --noconsole --name "SRT转ASS字幕转换器" toAss.py
```

### macOS（在macOS系统上）
```bash
pip install PyQt5 pysubs2 requests pyinstaller
pyinstaller --onefile --noconsole --name "SRT转ASS字幕转换器" toAss.py
```

### Linux（在Linux系统上）
```bash
pip install PyQt5 pysubs2 requests pyinstaller
pyinstaller --onefile --name "SRT转ASS字幕转换器" toAss.py
```

## 📊 当前状态

- ✅ 代码完全正常，可以直接运行
- ✅ 本地构建成功（macOS版本已完成）
- ✅ 项目结构专业完整
- ⚠️ GitHub Actions需要调试

## 🎯 推荐方案

1. **立即可用**：使用`python toAss.py`直接运行程序
2. **分享给他人**：手动创建GitHub Release上传本地构建的文件
3. **长期方案**：继续调试GitHub Actions自动构建

## 🔗 有用链接

- 创建Release: https://github.com/senvenluckys/toAss/releases/new
- 仓库主页: https://github.com/senvenluckys/toAss
- Actions状态: https://github.com/senvenluckys/toAss/actions

---

你的项目已经完全可用！即使自动构建有问题，手动发布也是一个完全可行的方案。
