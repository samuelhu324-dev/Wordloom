from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QHBoxLayout,
    QLineEdit, QLabel, QCheckBox, QSpinBox
)
from PySide6.QtGui import QIcon
from pathlib import Path
import subprocess, os

from core.config import load_config
from core.tree_runner import write_tree_cmd, write_tree_py
from core.fix_runner import run_fix_script

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Wordloom Toolkit')
        try:
            self.setWindowIcon(QIcon('tools/WordloomToolkit/icons/app.ico'))
        except Exception:
            pass

        self.cfg = load_config()
        self.project_root = Path(self.cfg['project_root']).resolve()

        layout = QVBoxLayout(self)

        # 项目根
        row = QHBoxLayout()
        self.root_edit = QLineEdit(str(self.project_root))
        btn_browse = QPushButton('选择根目录')
        btn_browse.clicked.connect(self.choose_root)
        row.addWidget(QLabel('项目根：'))
        row.addWidget(self.root_edit, 1)
        row.addWidget(btn_browse)
        layout.addLayout(row)

        # Tree 控件
        row2 = QHBoxLayout()
        self.btn_tree = QPushButton('生成 Tree')
        self.btn_tree.clicked.connect(self.generate_tree)
        self.tree_out = QLineEdit(self.cfg.get('tree',{}).get('out_file','TREE.txt'))
        row2.addWidget(self.btn_tree)
        row2.addWidget(QLabel('输出文件名：'))
        row2.addWidget(self.tree_out, 1)
        layout.addLayout(row2)

        # Tree 打开动作
        row2b = QHBoxLayout()
        self.btn_open_tree = QPushButton('打开 Tree 文件')
        self.btn_open_dir  = QPushButton('打开所在文件夹')
        self.btn_open_tree.clicked.connect(self.open_tree_file)
        self.btn_open_dir.clicked.connect(self.open_tree_dir)
        row2b.addWidget(self.btn_open_tree)
        row2b.addWidget(self.btn_open_dir)
        layout.addLayout(row2b)
        self._last_tree_path = None

        # Fix Path 控件
        row3 = QHBoxLayout()
        self.btn_fix_dir = QPushButton('修复路径（选目录）')
        self.btn_fix_dir.clicked.connect(self.fix_choose_dir)
        self.btn_fix_files = QPushButton('修复路径（选文件们）')
        self.btn_fix_files.clicked.connect(self.fix_choose_files)
        self.chk_nohtml = QCheckBox('只规范路径（不转<img>）')
        self.spin_width = QSpinBox()
        self.spin_width.setRange(100, 2000)
        self.spin_width.setValue(480)
        row3.addWidget(self.btn_fix_dir)
        row3.addWidget(self.btn_fix_files)
        row3.addWidget(self.chk_nohtml)
        row3.addWidget(QLabel('宽度：'))
        row3.addWidget(self.spin_width)
        layout.addLayout(row3)

        # GIF 工坊按钮
        row4 = QHBoxLayout()
        self.btn_gif = QPushButton('打开 GIF 工坊（现有 Streamlit）')
        self.btn_gif.clicked.connect(self.open_gif_streamlit)
        row4.addWidget(self.btn_gif)
        layout.addLayout(row4)

        # 日志
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log, 1)

        self.append(f'配置已载入：{self.cfg}')

    def append(self, text):
        self.log.append(text)

    def choose_root(self):
        d = QFileDialog.getExistingDirectory(self, '选择项目根目录', str(self.project_root))
        if d:
            self.project_root = Path(d)
            self.root_edit.setText(str(self.project_root))
            self.append(f'项目根已设为：{self.project_root}')

    def generate_tree(self):
        root = Path(self.root_edit.text()).resolve()
        out_file = root / self.tree_out.text()
        self.append(f'开始生成 Tree：root={root} -> {out_file}')
        ok = write_tree_cmd(root, out_file)
        if not ok:
            ignore = self.cfg.get('tree', {}).get('ignore', [])
            write_tree_py(root, out_file, ignore=ignore)
        # 无论系统/兜底都统一显示成功
        self._last_tree_path = out_file
        self.append(f'✅ Tree 已生成：{out_file}')

    # —— 打开 Tree 文件 / 所在目录 ——
    def open_tree_file(self):
        p = self._last_tree_path
        if p and p.exists():
            os.startfile(str(p))
        else:
            self.append('未找到 Tree 文件；请先生成一次。')

    def open_tree_dir(self):
        p = self._last_tree_path
        if p and p.exists():
            subprocess.Popen(['explorer', '/select,', str(p)])
        else:
            self.append('未找到 Tree 文件；请先生成一次。')

    # —— 修复路径 ——
    def fix_choose_dir(self):
        d = QFileDialog.getExistingDirectory(self, '选择要修复的目录', str(self.project_root / 'assets' / 'docs'))
        if d:
            self.run_fix(Path(d))

    def fix_choose_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, '选择要修复的 Markdown 文件', str(self.project_root), 'Markdown (*.md)')
        if files:
            for f in files:
                self.run_fix(Path(f))

    def run_fix(self, target: Path):
        nohtml = self.chk_nohtml.isChecked()
        width = self.spin_width.value()
        try:
            res = run_fix_script(self.project_root, target, no_html=nohtml, width=width)
            out = (res.stdout or '').strip()
            err = (res.stderr or '').strip()
            if out:
                self.append(out)
            if err:
                self.append('[stderr]\n' + err)
            if res.returncode == 0:
                self.append('✅ 修复完成。')
            else:
                self.append(f'⚠️ 脚本退出码：{res.returncode}')
        except Exception as e:
            self.append(f'❌ 运行失败：{e}')

    # —— GIF 工坊 ——
    
def open_gif_streamlit(self):
        rel = self.cfg.get('gif',{}).get('streamlit_path','WordloomFrontend/streamlit/gif_maker.py')
        target = (self.project_root / rel).resolve()
        if not target.exists():
            self.append(f'未找到 {target} ，请在配置里调整 gif.streamlit_path')
            return
        # 注入项目根与输出目录到子进程环境，确保前端脚本落盘到正确的 assets 目录
        env = os.environ.copy()
        env['WL_PROJECT_ROOT'] = str(self.project_root)
        # 兼容：既支持 cfg['gif']['gif_dir'] 也支持顶层 gif_dir
        gcfg = self.cfg.get('gif', {})
        env['WL_GIF_DIR']   = str(gcfg.get('gif_dir', self.cfg.get('gif_dir', 'assets/static/media/gif')))
        env['WL_THUMB_DIR'] = str(gcfg.get('thumb_dir', self.cfg.get('thumb_dir', 'assets/static/media/thumb')))
        cmd = ['streamlit', 'run', str(target)]
        try:
            subprocess.Popen(cmd, env=env)
            self.append('已启动 Streamlit：' + ' '.join(cmd))
            self.append(f"已注入环境变量 WL_PROJECT_ROOT={env['WL_PROJECT_ROOT']}, WL_GIF_DIR={env['WL_GIF_DIR']}, WL_THUMB_DIR={env['WL_THUMB_DIR']}")
        except Exception as e:
            self.append(f'无法启动 Streamlit：{e}')
