import streamlit as st
import re
from datetime import datetime, timedelta, date
from io import BytesIO
from typing import List, Tuple, Optional, Any

import pandas as pd
from repo import search

# ⬇️ 本地字体嵌入 import（保留）
import base64, pathlib
# ⬆️

st.set_page_config(layout="wide", page_title="Translation Retrieval", page_icon="🔎")

# =========================
# 样式：悬挂缩进用 Grid；编号列/间距统一使用 rem
# =========================
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None, is_variable: bool = False, use_cdn: bool = False):
    if embed_ok and font_b64:
        st.markdown(
            f"""
            <style>
            @font-face {{
                font-family: 'NotoSerifSCEmbed';
                src: url(data:font/otf;base64,{font_b64}) format('opentype');
                font-weight: 100 900;
                font-style: normal;
                font-display: swap;
            }}
            :root {{
              --font-en-serif: "Constantia","Palatino Linotype","Palatino","Georgia",serif;
              --font-zh-serif: "NotoSerifSCEmbed","Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif;

              --num-col-width: 2.4rem;
              --num-gap: 0.5rem;
            }}

            .highlight {{ background-color:#007BFF; color:#fff; padding:0 2px; border-radius:3px; }}
            .brk {{ color:#007BFF; }}

            .row {{
              display:grid;
              grid-template-columns: var(--num-col-width) 1fr;
              column-gap: var(--num-gap);
              align-items:start;
            }}
            .num {{
              color:#9ca3af;
              font-weight:400; 
              font-size:1.25rem; 
              font-family:"Palatino Linotype","Palatino","Georgia",serif;
              justify-self:end;
            }}
            .num.ghost {{ visibility:hidden; }}

            .source {{ margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; display:block; }}
            .ts     {{ margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; font-size:0.9rem; display:block; }}

            .src {{ font-size:1.1rem; line-height:1.6;  font-family:var(--font-en-serif); font-weight:500; margin-bottom:14px; display:block; }}
            .tgt {{ font-size:1.05rem; line-height:1.65; font-family:var(--font-zh-serif); font-weight:400; margin-bottom:18px; display:block; { 'font-variation-settings: "wght" 400;' if is_variable else '' } }}
            .block-container hr {{ margin:18px 0 22px 0; border:0; border-top:1px solid #e5e7eb; }}
            </style>
            """ ,
            unsafe_allow_html=True
        )
    elif use_cdn:
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap');
            :root {
              --font-en-serif: "Constantia","Palatino Linotype","Palatino","Georgia",serif;
              --font-zh-serif: "Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif;

              --num-col-width: 2.4rem;
              --num-gap: 0.5rem;
            }

            .highlight { background-color:#007BFF; color:#fff; padding:0 2px; border-radius:3px; }
            .brk { color:#007BFF; }

            .row { display:grid; grid-template-columns: var(--num-col-width) 1fr; column-gap: var(--num-gap); align-items:start; }
            .num { color:#9ca3af; font-weight:400; font-size:1.25rem; font-family:"Palatino Linotype","Palatino","Georgia",serif; justify-self:end; }
            .num.ghost { visibility:hidden; }

            .source { margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; display:block; }
            .ts     { margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; font-size:0.9rem; display:block; }

            .src { font-size:1.1rem; line-height:1.6; font-family:var(--font-en-serif); font-weight:500; margin-bottom:14px; display:block; }
            .tgt { font-size:1.05rem; line-height:1.65; font-family:var(--font-zh-serif); font-weight:400; margin-bottom:18px; display:block; }
            .block-container hr { margin:18px 0 22px 0; border:0; border-top:1px solid #e5e7eb; }
            </style>
            """ ,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            :root {
              --font-en-serif: "Constantia","Palatino Linotype","Palatino","Georgia",serif;
              --font-zh-serif: "Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif;

              --num-col-width: 2.4rem;
              --num-gap: 0.5rem;
            }

            .highlight { background-color:#007BFF; color:#fff; padding:0 2px; border-radius:3px; }
            .brk { color:#007BFF; }

            .row { display:grid; grid-template-columns: var(--num-col-width) 1fr; column-gap: var(--num-gap); align-items:start; }
            .num { color:#9ca3af; font-weight:400; font-size:1.25rem; font-family:"Palatino Linotype","Palatino","Georgia",serif; justify-self:end; }
            .num.ghost { visibility:hidden; }

            .source { margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; display:block; }
            .ts     { margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; font-size:0.9rem; display:block; }

            .src { font-size:1.1rem; line-height:1.6; font-family:var(--font-en-serif); font-weight:500; margin-bottom:14px; display:block; }
            .tgt { font-size:1.05rem; line-height:1.65; font-family:var(--font-zh-serif); font-weight:400; margin-bottom:18px; display:block; }
            .block-container hr { margin:18px 0 22px 0; border:0; border-top:1px solid #e5e7eb; }
            </style>
            """ ,
            unsafe_allow_html=True
        )

# 读取本地字体并尝试内嵌（大文件自动放弃，转为 CDN）
_font_b64 = None
try:
    font_path = pathlib.Path("assets/NotoSerifCJKsc-VF.otf")
    if font_path.exists():
        size_mb = font_path.stat().st_size / (1024*1024)
        if size_mb <= 10:
            _font_b64 = base64.b64encode(font_path.read_bytes()).decode()
            _emit_font_css(True, _font_b64, is_variable=True, use_cdn=False)
        else:
            _emit_font_css(False, None, is_variable=False, use_cdn=True)
    else:
        _emit_font_css(False, None, is_variable=False, use_cdn=True)
except Exception:
    _emit_font_css(False, None, is_variable=False, use_cdn=True)

# ========== 兼容旧函数（不改变样式，只防报错） ==========
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None):
    if embed_ok and font_b64:
        st.markdown(
            f"""
            <style>
            @font-face {{
                font-family: 'NotoSerifSCEmbed';
                src: url(data:font/otf;base64,{font_b64}) format('opentype');
                font-weight: normal;
                font-style: normal;
            }}
            </style>
            """ ,
            unsafe_allow_html=True
        )
    else:
        st.markdown("<style></style>", unsafe_allow_html=True)

try:
    font_path = pathlib.Path("assets/NotoSerifCJKsc-VF.otf")
    if font_path.exists():
        _font_b64 = base64.b64encode(font_path.read_bytes()).decode()
        _emit_font_css(True, _font_b64)
    else:
        _emit_font_css(False, None)
except Exception:
    _emit_font_css(False, None)

# =========================

st.title("🔎 搜索 / Search")

q  = st.text_input("关键词 / Keyword")
ls = st.selectbox("源语言 / Source Lang", ["","en","zh"], index=1)
lt = st.selectbox("目标语言 / Target Lang", ["","zh","en"], index=1)

opt = st.selectbox(
    "时间筛选 / Time Filter",
    ["全部 / All", "最近7天 / Last 7 days", "最近30天 / Last 30 days", "自定义范围 / Custom Range"]
)
date_from = None
date_to   = None
if opt == "最近7天 / Last 7 days":
    date_from = (datetime.now() - timedelta(days=7)).date().isoformat()
elif opt == "最近30天 / Last 30 days":
    date_from = (datetime.now() - timedelta(days=30)).date().isoformat()
elif opt == "自定义范围 / Custom Range":
    c1, c2 = st.columns(2)
    with c1:
        df = st.date_input("开始日期 / From", value=date.today())
    with c2:
        dt = st.date_input("结束日期 / To", value=date.today())
    date_from = df.isoformat() if df else None
    date_to   = dt.isoformat() if dt else None

limit = st.number_input("每页数量 / Page Size", 10, 200, 50)

def highlight(text: str, keywords: Optional[str]) -> str:
    if not keywords:
        return text
    words = [re.escape(k) for k in keywords.split() if k]
    if not words:
        return text
    pattern = re.compile("(" + "|".join(words) + ")", re.IGNORECASE)
    return pattern.sub(lambda m: f"<span class='highlight'>{m.group(0)}</span>", text)

def colorize_brackets(text: str) -> str:
    return re.sub(r'\[([^\[\]]+)\]', r"[<span class='brk'>\1</span>]", text)

def render_text(text: str, keywords: Optional[str]) -> str:
    s = colorize_brackets(text)
    s = highlight(s, keywords)
    return s

def safe_search(q, ls, lt, limit, date_from=None, date_to=None):
    try:
        return search(q, ls, lt, limit=limit, date_from=date_from, date_to=date_to)
    except TypeError:
        return search(q, ls, lt, limit=limit)

def fmt_ts(ts: Any) -> Optional[str]:
    if ts is None:
        return None
    if hasattr(ts, "strftime"):
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    return str(ts)

go = st.button("搜索 / Go")

export_rows: List[Tuple] = []

if go:
    rows = safe_search(q, ls or None, lt or None, limit=limit, date_from=date_from, date_to=date_to)
    export_rows = rows
    for i, row in enumerate(rows, start=1):
        _id, src, tgt = row[0], row[1], row[2]
        source_name = row[3] if len(row) >= 4 else None
        ts = row[4] if len(row) >= 5 else None
        src_h = render_text(src, q)
        tgt_h = render_text(tgt, q)

        st.markdown(f"<div class='row'><span class='num'>{i}.</span><span class='src'>{src_h}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='row'><span class='num ghost'>{i}.</span><span class='tgt'>{tgt_h}</span></div>", unsafe_allow_html=True)

        if source_name:
            st.markdown(f"<span class='source'>{source_name}</span>", unsafe_allow_html=True)
        ts_s = fmt_ts(ts)
        if ts_s:
            st.markdown(f"<span class='ts'>时间 / Time: {ts_s}</span>", unsafe_allow_html=True)
        st.markdown("---")

if export_rows:
    records = []
    for row in export_rows:
        rec = {
            "id": row[0],
            "src_text": row[1],
            "tgt_text": row[2],
            "source_name": row[3] if len(row) >= 4 else None,
            "created_at": fmt_ts(row[4]) if len(row) >= 5 else None,
        }
        records.append(rec)
    df = pd.DataFrame.from_records(records, columns=["id","src_text","tgt_text","source_name","created_at"])

    c1, c2 = st.columns(2)
    with c1:
        csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ 导出 CSV（含 created_at） / Export CSV",
            data=csv_bytes,
            file_name="search_results.csv",
            mime="text/csv"
        )
    with c2:
        output = BytesIO()
        try:
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="results")
            st.download_button(
                "⬇️ 导出 Excel（含 created_at） / Export Excel",
                data=output.getvalue(),
                file_name="search_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception:
            st.info("未安装 openpyxl，暂时无法导出 Excel，仅提供 CSV 导出。")
