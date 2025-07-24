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

# 检查文件或应用程序包是否存在
if [ ! -e "$FILE_PATH" ]; then
    echo "❌ 错误: 文件或应用程序不存在: $FILE_PATH"
    echo ""
    echo "💡 提示: 请检查文件路径，常见位置："
    echo "   ~/Downloads/SRT-to-ASS-Converter"
    echo "   ~/Downloads/SRT-to-ASS-Converter.app"
    echo "   /Applications/SRT-to-ASS-Converter.app"
    exit 1
fi

# 检查是否是.app包
if [[ "$FILE_PATH" == *.app ]]; then
    echo "📱 检测到.app应用程序包"
    APP_BUNDLE=true
    # 找到.app包内的可执行文件
    APP_NAME=$(basename "$FILE_PATH" .app)
    EXECUTABLE_PATH="$FILE_PATH/Contents/MacOS/$APP_NAME"

    if [ ! -f "$EXECUTABLE_PATH" ]; then
        # 尝试其他可能的可执行文件名
        EXECUTABLE_PATH=$(find "$FILE_PATH/Contents/MacOS" -type f -perm +111 2>/dev/null | head -1)
        if [ -z "$EXECUTABLE_PATH" ]; then
            echo "❌ 错误: 在.app包中找不到可执行文件"
            exit 1
        fi
    fi

    echo "🎯 可执行文件: $EXECUTABLE_PATH"
else
    echo "📄 检测到普通可执行文件"
    APP_BUNDLE=false
    EXECUTABLE_PATH="$FILE_PATH"
fi

echo "📁 处理文件: $FILE_PATH"

# 移除隔离属性
echo "🔓 移除隔离属性..."
if [ "$APP_BUNDLE" = true ]; then
    # 对整个.app包递归移除隔离属性
    xattr -dr com.apple.quarantine "$FILE_PATH" 2>/dev/null
    xattr -dr com.apple.quarantine "$EXECUTABLE_PATH" 2>/dev/null
else
    xattr -d com.apple.quarantine "$FILE_PATH" 2>/dev/null
fi

if [ $? -eq 0 ]; then
    echo "✅ 隔离属性已移除"
else
    echo "⚠️  隔离属性可能不存在或已移除"
fi

# 移除所有扩展属性
echo "🧹 清理扩展属性..."
if [ "$APP_BUNDLE" = true ]; then
    # 清理整个.app包的扩展属性
    xattr -cr "$FILE_PATH" 2>/dev/null
else
    xattr -c "$FILE_PATH" 2>/dev/null
fi
echo "✅ 扩展属性已清理"

# 添加执行权限
echo "🔑 添加执行权限..."
if [ "$APP_BUNDLE" = true ]; then
    chmod +x "$EXECUTABLE_PATH"
    chmod +x "$FILE_PATH"
else
    chmod +x "$FILE_PATH"
fi

if [ $? -eq 0 ]; then
    echo "✅ 执行权限已添加"
else
    echo "❌ 添加执行权限失败"
    exit 1
fi

# 检查文件信息
echo ""
echo "📊 文件信息:"
if [ "$APP_BUNDLE" = true ]; then
    echo "应用程序包: $FILE_PATH"
    ls -la "$FILE_PATH"
    echo ""
    echo "可执行文件: $EXECUTABLE_PATH"
    ls -la "$EXECUTABLE_PATH"
else
    ls -la "$FILE_PATH"
fi

echo ""
echo "🔍 扩展属性:"
xattr -l "$FILE_PATH" 2>/dev/null || echo "无扩展属性"

echo ""
echo "🎉 修复完成！"
echo ""
if [ "$APP_BUNDLE" = true ]; then
    echo "现在你可以运行应用程序了:"
    echo "   方法1: 双击 $FILE_PATH"
    echo "   方法2: 在终端中执行: open '$FILE_PATH'"
    echo "   方法3: 直接运行可执行文件: '$EXECUTABLE_PATH'"
else
    echo "现在你可以运行应用程序了:"
    echo "   双击文件运行，或在终端中执行:"
    echo "   $FILE_PATH"
fi
echo ""
echo "如果仍然遇到问题，请尝试:"
echo "1. 系统设置 > 隐私与安全性 > 点击'仍要打开'"
echo "2. 或者从源码运行: python toAss.py"
