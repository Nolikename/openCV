#! /bin/bash

# 执行 build for testing

# 删除旧的 export 文件
app_export_dir="output/"

if [[ -d "$app_export_dir" ]]; then
	rm -rf $app_export_dir
	echo "## 删除旧的文件夹: $app_export_dir"
fi

xcodebuild build-for-testing \
	-scheme UIOperaterUITests \
	-workspace "UIOperater.xcworkspace" \
    -destination 'generic/platform=iOS' \
    -derivedDataPath 'output/'

if [[ $? -eq 0 ]]; then
	echo "## 成功生成 xctest run 文件"
	else
	echo "## 生成 xctest run 文件失败"
	exit 1
fi

exit 0