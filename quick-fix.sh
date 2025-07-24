#!/bin/bash

echo "🔧 SRT转ASS字幕转换器 - 快速修复脚本"
echo "======================================="

# 检查并安装Homebrew（如果需要）
if ! command -v brew &> /dev/null; then
    echo "📦 安装Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 检查并安装Python3
if ! command -v python3 &> /dev/null; then
    echo "🐍 安装Python3..."
    brew install python3
fi

# 检查并安装pip3
if ! command -v pip3 &> /dev/null; then
    echo "📦 安装pip3..."
    python3 -m ensurepip --upgrade
fi

echo ""
echo "🚀 从源码运行程序（推荐方法）"
echo "================================"

# 创建临时目录
TEMP_DIR="/tmp/srt-to-ass-converter"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "📥 下载源码..."
if command -v git &> /dev/null; then
    git clone https://github.com/senvenluckys/toAss.git .
else
    echo "Git未安装，使用curl下载..."
    curl -L https://github.com/senvenluckys/toAss/archive/main.zip -o main.zip
    unzip main.zip
    mv toAss-main/* .
    rm -rf toAss-main main.zip
fi

echo "📦 安装依赖..."
pip3 install -r requirements.txt

echo ""
echo "✅ 准备完成！"
echo ""
echo "现在运行程序:"
echo "python3 toAss.py"
echo ""
echo "或者创建桌面快捷方式:"
echo "echo '#!/bin/bash' > ~/Desktop/SRT转ASS转换器.command"
echo "echo 'cd $TEMP_DIR && python3 toAss.py' >> ~/Desktop/SRT转ASS转换器.command"
echo "chmod +x ~/Desktop/SRT转ASS转换器.command"
echo ""

# 询问是否立即运行
read -p "是否立即运行程序? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动程序..."
    python3 toAss.py
fi
