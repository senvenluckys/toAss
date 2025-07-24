#!/bin/bash

echo "🔍 SRT转ASS字幕转换器 - 闪退诊断脚本"
echo "=============================================="

# 检查是否提供了应用程序路径
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <应用程序路径>"
    echo "示例: $0 /Applications/SRT-to-ASS-Converter.app"
    exit 1
fi

APP_PATH="$1"

# 检查应用程序是否存在
if [ ! -e "$APP_PATH" ]; then
    echo "❌ 错误: 应用程序不存在: $APP_PATH"
    exit 1
fi

echo "📱 应用程序: $APP_PATH"

# 找到可执行文件
if [[ "$APP_PATH" == *.app ]]; then
    APP_NAME=$(basename "$APP_PATH" .app)
    EXECUTABLE="$APP_PATH/Contents/MacOS/$APP_NAME"
    
    if [ ! -f "$EXECUTABLE" ]; then
        EXECUTABLE=$(find "$APP_PATH/Contents/MacOS" -type f -perm +111 2>/dev/null | head -1)
    fi
else
    EXECUTABLE="$APP_PATH"
fi

if [ ! -f "$EXECUTABLE" ]; then
    echo "❌ 找不到可执行文件"
    exit 1
fi

echo "🎯 可执行文件: $EXECUTABLE"

# 检查文件权限
echo ""
echo "📋 文件权限检查:"
ls -la "$EXECUTABLE"

# 检查扩展属性
echo ""
echo "🔍 扩展属性检查:"
xattr -l "$EXECUTABLE" 2>/dev/null || echo "无扩展属性"

# 检查文件类型
echo ""
echo "📄 文件类型:"
file "$EXECUTABLE"

# 检查依赖库
echo ""
echo "📚 依赖库检查:"
otool -L "$EXECUTABLE" 2>/dev/null | head -10

# 尝试运行并捕获错误
echo ""
echo "🚀 尝试运行应用程序..."
echo "如果程序正常启动，请关闭它然后按Ctrl+C停止此脚本"
echo "如果程序闪退，错误信息将显示在下方:"
echo "----------------------------------------"

# 设置超时运行
timeout 10s "$EXECUTABLE" 2>&1 || {
    exit_code=$?
    echo ""
    echo "----------------------------------------"
    if [ $exit_code -eq 124 ]; then
        echo "✅ 程序运行超过10秒，可能正常启动了"
        echo "如果程序界面没有出现，可能是界面问题"
    else
        echo "❌ 程序退出，退出代码: $exit_code"
    fi
}

echo ""
echo "🔧 建议的解决方案:"
echo "1. 从源码运行以查看详细错误:"
echo "   git clone https://github.com/senvenluckys/toAss.git"
echo "   cd toAss"
echo "   pip3 install -r requirements.txt"
echo "   python3 toAss.py"
echo ""
echo "2. 检查系统日志:"
echo "   log show --predicate 'process == \"SRT-to-ASS-Converter\"' --last 5m"
echo ""
echo "3. 查看控制台崩溃报告:"
echo "   open /Applications/Utilities/Console.app"
echo ""
echo "4. 如果问题持续，请在GitHub上报告问题:"
echo "   https://github.com/senvenluckys/toAss/issues"
