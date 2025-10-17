WordloomToolkit GUI (first runnable shell)
==========================================

快速开始（建议放置路径）：
D:\PROJECT\WORDLOOM\tools\WordloomToolkit\

1) 安装依赖（推荐在虚拟环境或 pipx-run）
   pip install -r requirements.txt

2) 运行
   python app.py

3) 功能说明
   - Tree：优先调用 Windows 自带 `tree /f /a` 输出到配置中的 out_file；若系统无 tree，则使用 Python 版遍历生成。
   - Fix Path：调用你仓库里的 fix_md_paths.py（需要你把它放到 `assets/docs/fix_md_paths.py`）；支持选择目录、只规范路径（--no-html）或设置宽度。
   - GIF 工坊：当前按钮会尝试启动你的 streamlit 版本（路径可在设置里修改）；下一版再内嵌。

4) 配置文件（就近原则）
   - tools/WordloomToolkit/config/user.yaml
   - tools/WordloomToolkit/config/default.yaml
   都不存在时，使用内置默认：project_root=[上级或当前]，tree.out_file=TREE.md，gif.streamlit_path=WordloomFrontend/streamlit/gif_maker.py

5) 打包（Windows）
   pip install pyinstaller
   pyinstaller -w -F app.py -n WordloomToolkit.exe --icon=tools/WordloomToolkit/icons/app.ico --add-data "tools/WordloomToolkit/config;tools/WordloomToolkit/config"
   将 dist/WordloomToolkit.exe 放到 tools/WordloomToolkit/ 下。