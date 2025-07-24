# SRT转ASS字幕转换器

[![Build and Release](https://github.com/senvenluckys/toAss/actions/workflows/build.yml/badge.svg)](https://github.com/senvenluckys/toAss/actions/workflows/build.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

一个现代化的字幕格式转换工具，支持将SRT、VTT字幕文件转换为ASS格式，并提供丰富的自定义选项。

## ✨ 功能特性

- 🔄 **多格式支持**: SRT → ASS, VTT → ASS, ASS → ASS
- 🎨 **自定义样式**: 支持字体、颜色、大小等样式设置
- 🌏 **繁体转换**: 内置繁体中文转换功能
- 📁 **批量处理**: 支持同时处理多个文件
- 🖥️ **现代界面**: 基于PyQt5和QFluentWidgets的现代化UI
- 🎯 **拖拽支持**: 直接拖拽文件到程序窗口
- ⚙️ **灵活配置**: 可保存和管理多个字幕样式配置
- 🔧 **ASS语句**: 支持插入自定义ASS特效语句

## 📸 界面预览

![主界面](docs/images/main-interface.png)
![设置界面](docs/images/settings-interface.png)

## 🚀 快速开始

### 下载预编译版本

从 [Releases](https://github.com/senvenluckys/toAss/releases) 页面下载适合你操作系统的版本：

- **Windows**: `SRT转ASS字幕转换器-windows.exe`
- **macOS**: `SRT转ASS字幕转换器-macos`
- **Linux**: `SRT转ASS字幕转换器-linux`

### 从源码运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/senvenluckys/toAss.git
   cd toAss
   ```

2. **快速设置**
   ```bash
   python setup.py
   ```

3. **或手动安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python toAss.py
   ```

### 开发者工具

```bash
# 检查项目状态
python check.py

# 本地构建
python build.py

# 版本管理
python version.py current

# 部署到GitHub
python deploy.py
```

## 📋 系统要求

- **Python**: 3.9 或更高版本
- **操作系统**: Windows 10+, macOS 10.13+, Ubuntu 18.04+
- **内存**: 至少 512MB RAM
- **存储**: 至少 100MB 可用空间

## 🛠️ 开发环境设置

### 安装开发依赖

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果有开发依赖
```

### 构建可执行文件

```bash
# 使用PyInstaller构建
pyinstaller build.spec

# 或者使用简单命令
pyinstaller --onefile --windowed --name "SRT转ASS字幕转换器" toAss.py
```

## 📖 使用说明

### 基本使用

1. **添加文件**: 点击"添加文件"按钮或直接拖拽字幕文件到程序窗口
2. **配置选项**: 在设置页面配置字体、颜色等样式选项
3. **开始转换**: 点击"开始转换"按钮开始处理文件

### 高级功能

#### 自定义字幕样式
- 在主界面的"字幕配置"区域可以添加、编辑、删除字幕样式配置
- 支持设置字体、大小、颜色、边框等属性

#### 繁体中文转换
- 勾选"繁体中国化"选项可以将繁体中文转换为简体中文
- 使用在线API进行转换，需要网络连接

#### ASS特效语句
- 可以插入自定义的ASS特效语句
- 支持设置显示时间和特效内容

## 🔧 配置文件

程序会在运行目录下创建以下配置文件：

- `sub.json`: 字幕样式配置
- `settings.json`: 程序设置（输出目录、字体等）

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 使用 Python PEP 8 代码风格
- 添加适当的注释和文档字符串
- 确保所有测试通过

## 🐛 问题报告

如果遇到问题，请在 [Issues](https://github.com/senvenluckys/toAss/issues) 页面报告，包含以下信息：

- 操作系统和版本
- Python版本
- 错误信息和堆栈跟踪
- 重现步骤

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI框架
- [QFluentWidgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) - 现代化UI组件
- [pysubs2](https://github.com/tkarabela/pysubs2) - 字幕文件处理
- [PyInstaller](https://www.pyinstaller.org/) - 打包工具

## 📞 联系方式

- 项目主页: [https://github.com/senvenluckys/toAss](https://github.com/senvenluckys/toAss)
- 问题反馈: [Issues](https://github.com/senvenluckys/toAss/issues)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
