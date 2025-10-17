# 0_🏡_Home_Admin.py — Search + Bulk Replace (Sticky) + Inline Edit/Delete + Source Filter  [API版]
from app import API_BASE
import re, base64, pathlib, requests
from datetime import datetime, timedelta, date
from typing import List, Optional
import streamlit as st
import pandas as pd

from repo import client  # ApiClient：search / update_entry / delete_entry / insert_sentence / create_article / get_article_sentences / find_matches / bulk_replace

st.set_page_config(page_title='Home Admin (Merged Sticky)', page_icon='🏡', layout='wide')
st.title('🏡 Home Admin — Search + Bulk Replace（API）')

# ========== Typography（与原版一致） ==========
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None, is_variable: bool = False, use_cdn: bool = False):
    css_common = """
    :root { --font-en-serif:"Constantia","Palatino Linotype","Palatino","Georgia",serif; --font-zh-serif:"Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif; --num-col-width:2.4rem; --num-gap:0.5rem; }
    .highlight{background-color:#007BFF;color:#fff;padding:0 2px;border-radius:3px;}
    .brk{color:#007BFF;}
    .row{display:grid;grid-template-columns:var(--num-col-width) 1fr;column-gap:var(--num-gap);align-items:start;}
    .num{color:#9ca3af;font-weight:400;font-size:1.25rem;font-family:"Palatino Linotype","Palatino","Georgia",serif;justify-self:end;}
    .num.ghost{visibility:hidden;}
    .source{margin-left:calc(var(--num-col-width) + var(--num-gap));color:#6b7280;display:block;}
    .ts{margin-left:calc(var(--num-col-width) + var(--num-gap));color:#6b7280;font-size:0.9rem;display:block;}
    .src{font-size:1.1rem;line-height:1.6;font-family:var(--font-en-serif);font-weight:500;margin-bottom:14px;display:block;}
    .tgt{font-size:1.05rem;line-height:1.65;font-family:var(--font-zh-serif);font-weight:400;margin-bottom:18px;display:block;}
    .block-container hr{margin:18px 0 22px 0;border:0;border-top:1px solid #e5e7eb;}
    .toolbar button{padding:.15rem .35rem;margin-left:.2rem;border-radius:.4rem;}
    .toolbar{text-align:right;margin-top:2px;}
    .sticky{position:sticky;top:0;z-index:999;background:#fff;padding:12px 12px 6px;border-bottom:1px solid #eee;box-shadow:0 1px 0 rgba(0,0,0,.02);}
    """
    if embed_ok and font_b64:
        st.markdown(f"<style>@font-face{{font-family:'NotoSerifSCEmbed';src:url(data:font/otf;base64,{font_b64}) format('opentype');font-weight:100 900;font-style:normal;font-display:swap;}}"
                    f":root{{--font-zh-serif:'NotoSerifSCEmbed','Noto Serif SC','Source Han Serif SC','SimSun','霞鹜文楷','KaiTi',serif;}}{css_common}</style>", unsafe_allow_html=True)
    elif use_cdn:
        st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap');"
                    f"{css_common}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{css_common}</style>", unsafe_allow_html=True)

_font_b64 = None
try:
    font_path = pathlib.Path("assets/NotoSerifCJKsc-VF.otf")
    if font_path.exists() and font_path.stat().st_size <= 10*1024*1024:
        _font_b64 = base64.b64encode(font_path.read_bytes()).decode()
        _emit_font_css(True, _font_b64, is_variable=True, use_cdn=False)
    else:
        _emit_font_css(False, None, is_variable=False, use_cdn=True)
except Exception:
    _emit_font_css(False, None, is_variable=False, use_cdn=True)

# ===== 工具函数 =====
def _fmt_ts(ts):
    if ts is None: return ""
    if hasattr(ts, "strftime"): return ts.strftime("%Y-%m-%d %H:%M:%S")
    return str(ts)

def _highlight_keywords(text, keywords, case_sensitive=False, regex_mode=False):
    if not keywords or not text: return text or ""
    try:
        pat = re.compile(keywords if regex_mode else "(" + "|".join([re.escape(k) for k in keywords.split() if k]) + ")",
                         0 if case_sensitive else re.IGNORECASE)
    except re.error:
        return text
    parts = re.split(r'(<[^>]+>)', text)
    for i, p in enumerate(parts):
        if not p or p.startswith("<"): continue
        parts[i] = pat.sub(lambda m: f"<span class='highlight'>{m.group(0)}</span>", p)
    return "".join(parts)

def _colorize_brackets(text): return re.sub(r'\[([^\[\]]+)\]', r"[<span class='brk'>\1</span>]", text or "")
def _render_text(text, keywords, case_sensitive=False, regex_mode=False):
    return _highlight_keywords(_colorize_brackets(text), keywords, case_sensitive, regex_mode)

def _all_source_names(limit: int = 500) -> list[str]:
    # 通过后端 /sources 获取（若你的路由不同，请改成实际路径）
    try:
        r = requests.get(f"{API_BASE}/sources", params={"limit":limit}, timeout=10)
        r.raise_for_status()
        data = r.json()
        # 兼容返回 [{'name':...}] 或 ['name', ...]
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return sorted({d.get("name","") for d in data if d.get("name")})
        return sorted({str(x) for x in data if x})
    except Exception:
        return []

# ===== 选项卡 =====
tab_search, tab_bulk = st.tabs(["🔎 Search", "🛠️ Bulk Replace"])

# ---------------- SEARCH ----------------
with tab_search:
    st.markdown('<div class="sticky">', unsafe_allow_html=True)
    q = st.text_input("Keyword(s)", key="search_q")
    colA, colB, colC = st.columns([1, 1, 2])
    with colA: ls = st.selectbox("Source Lang", ["", "en", "zh"], index=1, key="search_ls")
    with colB: lt = st.selectbox("Target Lang", ["", "zh", "en"], index=1, key="search_lt")
    with colC:
        colx1, colx2, colx3 = st.columns([1, 1, 1])
        with colx1: case_sensitive = st.checkbox("Case", value=False, key="search_case")
        with colx2: regex_mode = st.checkbox("Regex", value=False, key="search_regex")
        with colx3: limit = st.number_input("Page Size", 10, 500, 80, step=10, key="search_limit")

    # Source filter（选择或输入）
    src_list = ["(Any)"] + _all_source_names(500)
    colS1, colS2, colS3 = st.columns([1.2, 1.2, 0.8])
    with colS1: src_sel = st.selectbox("Source filter (select)", options=src_list, index=0, key="search_source_sel")
    with colS2: src_typed = st.text_input("or type (partial ok)", key="search_source_typed")
    with colS3: src_exact = st.checkbox("Exact", value=False, key="search_source_exact")

    opt = st.selectbox("Time", ["All", "Last 7 days", "Last 30 days", "Custom Range"], key="search_time")
    go = st.button("Run Search", key="search_go")
    st.markdown("</div>", unsafe_allow_html=True)

    date_from = date_to = None
    if opt == "Last 7 days": date_from = (datetime.now() - timedelta(days=7)).date().isoformat()
    elif opt == "Last 30 days": date_from = (datetime.now() - timedelta(days=30)).date().isoformat()
    elif opt == "Custom Range":
        c1, c2 = st.columns(2)
        with c1: df = st.date_input("From", value=date.today(), key="search_df")
        with c2: dt = st.date_input("To", value=date.today(), key="search_dt")
        date_from, date_to = df.isoformat(), dt.isoformat()

    effective_source = (src_typed.strip() if src_typed and src_typed.strip() else None)
    if not effective_source and src_sel and src_sel != "(Any)": effective_source = src_sel

    if go:
        rows = client.search(q, ls or None, lt or None, limit=int(limit), date_from=date_from, date_to=date_to)
        shown = 0
        for i, row in enumerate(rows, start=1):
            _id, src, tgt = row[0], row[1], row[2]
            sname = row[3] if len(row) > 3 else ""

            # 源过滤（客户端侧）
            if effective_source:
                if src_exact:
                    if sname != effective_source: continue
                else:
                    if effective_source.lower() not in (sname or "").lower(): continue

            src_h = _render_text(src, q, case_sensitive, regex_mode)
            tgt_h = _render_text(tgt, q, case_sensitive, regex_mode)

            c_text, c_tools = st.columns([10,2])
            with c_text:
                shown += 1
                st.markdown(f"<div class='row'><span class='num'>{shown}.</span><span class='src'>{src_h}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='row'><span class='num ghost'>{shown}.</span><span class='tgt'>{tgt_h}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='source'>{sname or ''}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='ts'>ID: {_id}</span>", unsafe_allow_html=True)

            with c_tools:
                st.markdown("<div class='toolbar'>", unsafe_allow_html=True)
                edit_clicked = st.button("✏️", key=f"search_edit_{_id}", help="Edit this entry")
                ins_clicked  = st.button("➕", key=f"search_ins_{_id}", help="Insert AFTER")
                clone_clicked = st.button("🧬", key=f"search_clone_{_id}", help="Clone & Insert AFTER")
                del_clicked  = st.button("🗑", key=f"search_del_{_id}", help="Delete this entry")
                st.markdown("</div>", unsafe_allow_html=True)

            if edit_clicked:
                with st.expander("Edit", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        new_src = st.text_area("中文 / Source text", value=src, height=90, key=f"edit_src_{_id}")
                        new_tgt = st.text_area("English / Target text", value=tgt, height=90, key=f"edit_tgt_{_id}")
                    with c2:
                        new_source_name = st.text_input("Source name", value=sname or "", key=f"edit_sourcename_{_id}")
                    b1, _ = st.columns([1,1])
                    with b1:
                        if st.button("Save", key=f"save_{_id}"):
                            payload = {"src": new_src.strip() or src, "tgt": new_tgt.strip() or tgt, "source_name": (new_source_name or "").strip()}
                            client.update_entry(_id, **payload)
                            st.success("Saved.")

            if ins_clicked or clone_clicked:
                with st.expander(("Insert AFTER" if ins_clicked else "Clone & Insert AFTER"), expanded=True):
                    art_title = st.text_input("Article title", value=sname or "", key=f"art_title_{_id}")
                    aid = None
                    if art_title.strip():
                        # 若无则创建后返回 id
                        a = client.create_article(art_title.strip(), source_name=art_title.strip())
                        aid = int(a) if isinstance(a, int) else int(getattr(a, "id", a[0]))
                    if aid:
                        # 估计插入位置（取当前文章已有条目数）
                        try:
                            seq = client.get_article_sentences(aid)
                            ids = [(r["id"] if isinstance(r, dict) else r[0]) for r in seq]
                            pos_default = len(ids)
                        except Exception:
                            pos_default = 0
                        ins_pos = st.number_input("Insert after position (1-based)", min_value=0, value=pos_default, step=1, key=f"ins_pos_{_id}")
                        if ins_clicked:
                            with st.form(f"ins_form_{_id}", clear_on_submit=True):
                                zh_new = st.text_area("中文 / Source text", height=80, key=f"ins_zh_{_id}")
                                en_new = st.text_area("English / Target text", height=80, key=f"ins_en_{_id}")
                                do_ins = st.form_submit_button("Insert AFTER")
                            if do_ins:
                                if not zh_new.strip() or not en_new.strip():
                                    st.error("Both zh and en are required.")
                                else:
                                    new_id = client.insert_sentence(aid, ins_pos, zh_new, en_new, ls="zh", lt="en")
                                    st.success(f"Inserted new entry #{new_id} at position {ins_pos+1}.")
                        else:  # clone
                            clone_id = st.text_input("Entry ID to clone", key=f"clone_id_{_id}")
                            if st.button("Clone & Insert", key=f"clone_go_{_id}"):
                                try:
                                    cid = int(clone_id.strip())
                                except Exception:
                                    st.error("Please enter a valid integer entry ID.")
                                else:
                                    # 直接取当前行内容克隆最稳
                                    new_id = client.insert_sentence(aid, ins_pos, src, tgt)
                                    st.success(f"Cloned #{cid} → new #{new_id} at pos {ins_pos+1}.")
                    else:
                        st.info("Provide a valid article title to insert into.")

            if del_clicked:
                with st.expander("Confirm delete?", expanded=True):
                    st.warning("This will delete the entry permanently.")
                    c1, _ = st.columns(2)
                    if c1.button("Delete", key=f"del_yes_{_id}"):
                        client.delete_entry(_id)
                        st.success(f"Deleted #{_id}.")
            st.markdown("---")

# ---------------- BULK REPLACE ----------------
with tab_bulk:
    st.markdown('<div class="sticky">', unsafe_allow_html=True)
    colA, colB, colC = st.columns([2, 2, 1])
    with colA: kw = st.text_input("Find", key="bulk_find")
    with colB: repl = st.text_input("Replace with", key="bulk_repl")
    with colC: scope = st.radio("Scope", ["src", "tgt", "both"], index=2, horizontal=True, key="bulk_scope")
    row2c1, row2c2, row2c3, row2c4 = st.columns([1, 1, 1, 1])
    with row2c1: regex_mode2 = st.checkbox("Regex", value=False, key="bulk_regex")
    with row2c2: case_sensitive2 = st.checkbox("Case", value=False, key="bulk_case")
    with row2c3: strict_word = st.checkbox(r"Word boundary (ASCII \b)", value=False, key="bulk_word")
    with row2c4: first_only = st.checkbox("First only", value=False, key="bulk_first")
    src_name_filter = st.text_input("Source filter (optional)", key="bulk_srcfilter")
    opt2 = st.selectbox("Time", ["All", "Last 7 days", "Last 30 days", "Custom range"], key="bulk_time")
    limit2 = st.number_input("Preview size", 5, 2000, 80, key="bulk_limit")
    prev_btn = st.button("🔍 Preview matches", key="bulk_preview")
    st.markdown("</div>", unsafe_allow_html=True)

    date_from2 = date_to2 = None
    if opt2 == "Last 7 days": date_from2 = (datetime.now() - timedelta(days=7)).date().isoformat()
    elif opt2 == "Last 30 days": date_from2 = (datetime.now() - timedelta(days=30)).date().isoformat()
    elif opt2 == "Custom range":
        c1, c2 = st.columns(2)
        with c1: df2 = st.date_input("From", value=date.today(), key="bulk_df")
        with c2: dt2 = st.date_input("To", value=date.today(), key="bulk_dt")
        date_from2, date_to2 = df2.isoformat(), dt2.isoformat()

    if prev_btn:
        preview_rows = client.find_matches(keyword=kw, scope=scope, source_name=src_name_filter or None,
                                           date_from=date_from2, date_to=date_to2, limit=int(limit2),
                                           regex_mode=regex_mode2, case_sensitive=case_sensitive2, strict_word=strict_word)
        for _id, src, tgt, sname, ts in preview_rows:
            st.markdown(f"<div class='row'><span class='num'>#{_id}</span><span class='src'>{_render_text(src, kw, case_sensitive2, regex_mode2)}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='row'><span class='num ghost'>#{_id}</span><span class='tgt'>{_render_text(tgt, kw, case_sensitive2, regex_mode2)}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<span class='source'>{sname}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='ts'>{_fmt_ts(ts)}</span>", unsafe_allow_html=True)
            st.markdown("---")

    confirm = st.checkbox("I previewed and confirm this change", value=True, key="bulk_confirm")
    if st.button("⚡ Run replace", type="primary", disabled=not confirm, key="bulk_run"):
        changed = client.bulk_replace(keyword=kw, replacement=repl, scope=scope,
                                      source_name=src_name_filter or None,
                                      date_from=date_from2, date_to=date_to2,
                                      regex_mode=regex_mode2, case_sensitive=case_sensitive2,
                                      strict_word=strict_word, first_only=first_only)
        st.success(f"✅ Done! Updated {changed} rows.")
