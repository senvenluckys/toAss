#!/bin/bash

# macOS安全问题修复脚本
# 用于解决"应用程序已损坏"的问题

echo "🔧 SRT转ASS字幕转换器 - macOS安全修复脚本"
echo "================================================"

# 检查是否提供了文件路径
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <可执行文件路径>"
    echo "示例: $0 ~/Downloads/SRT-to-ASS-Converter"
    exit 1
fi

FILE_PATH="$1"

# 检查文件是否存在
if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 错误: 文件不存在: $FILE_PATH"
    exit 1
fi

echo "📁 处理文件: $FILE_PATH"

# 移除隔离属性
echo "🔓 移除隔离属性..."
xattr -d com.apple.quarantine "$FILE_PATH" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 隔离属性已移除"
else
    echo "⚠️  隔离属性可能不存在或已移除"
fi

# 移除所有扩展属性
echo "🧹 清理扩展属性..."
xattr -c "$FILE_PATH" 2>/dev/null
echo "✅ 扩展属性已清理"

# 添加执行权限
echo "🔑 添加执行权限..."
chmod +x "$FILE_PATH"
if [ $? -eq 0 ]; then
    echo "✅ 执行权限已添加"
else
    echo "❌ 添加执行权限失败"
    exit 1
fi

# 检查文件信息
echo ""
echo "📊 文件信息:"
ls -la "$FILE_PATH"
echo ""
echo "🔍 扩展属性:"
xattr -l "$FILE_PATH"

echo ""
echo "🎉 修复完成！"
echo ""
echo "现在你可以运行应用程序了:"
echo "   双击文件运行，或在终端中执行:"
echo "   $FILE_PATH"
echo ""
echo "如果仍然遇到问题，请尝试:"
echo "1. 系统设置 > 隐私与安全性 > 点击'仍要打开'"
echo "2. 或者从源码运行: python toAss.py"
