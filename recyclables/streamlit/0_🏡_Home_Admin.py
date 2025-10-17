# 0_🏡_Home_Admin.py — Search + Bulk Replace (Sticky) + Inline Edit/Delete + Source Filter
from app import API_BASE
import re, base64, pathlib
from datetime import datetime, timedelta, date
from typing import List, Tuple, Optional, Any
import streamlit as st
import pandas as pd

from sqlalchemy import select, update
from models import SessionLocal, Entry, EntrySource, Source
from repo import search, find_matches, bulk_replace, insert_sentence, get_article_by_title, create_article, get_article_sentences

st.set_page_config(page_title='Home Admin (Merged Sticky)', page_icon='🏡', layout='wide')
st.title('🏡 Home Admin — Search + Bulk Replace (Sticky Toolbars)')

# ========== Unified Typography (embed → CDN → plain) ==========
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None, is_variable: bool = False, use_cdn: bool = False):
    if embed_ok and font_b64:
        st.markdown(f"""
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
        .row {{ display:grid; grid-template-columns: var(--num-col-width) 1fr; column-gap: var(--num-gap); align-items:start; }}
        .num {{ color:#9ca3af; font-weight:400; font-size:1.25rem; font-family:"Palatino Linotype","Palatino","Georgia",serif; justify-self:end; }}
        .num.ghost {{ visibility:hidden; }}
        .source {{ margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; display:block; }}
        .ts     {{ margin-left: calc(var(--num-col-width) + var(--num-gap)); color:#6b7280; font-size:0.9rem; display:block; }}
        .src {{ font-size:1.1rem; line-height:1.6;  font-family:var(--font-en-serif); font-weight:500; margin-bottom:14px; display:block; }}
        .tgt {{ font-size:1.05rem; line-height:1.65; font-family:var(--font-zh-serif); font-weight:400; margin-bottom:18px; display:block; {'font-variation-settings: "wght" 400;' if is_variable else ''} }}
        .block-container hr {{ margin:18px 0 22px 0; border:0; border-top:1px solid #e5e7eb; }}
        .sticky {{ position: sticky; top: 0; z-index: 999; background: white; padding: 12px 12px 6px 12px; border-bottom: 1px solid #eee; box-shadow: 0 1px 0 rgba(0,0,0,0.02); }}
        .toolbar button{{ padding:0.15rem 0.35rem; margin-left:.2rem; border-radius:.4rem; }}
        .toolbar{{ text-align:right; margin-top:2px; }}
        </style>
        """, unsafe_allow_html=True)
    elif use_cdn:
        st.markdown("""
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
        .toolbar button{ padding:0.15rem 0.35rem; margin-left:.2rem; border-radius:.4rem; }
        .toolbar{ text-align:right; margin-top:2px; }
        .sticky { position: sticky; top: 0; z-index: 999; background: white; padding: 12px 12px 6px 12px; border-bottom: 1px solid #eee; box-shadow: 0 1px 0 rgba(0,0,0,0.02); }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
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
        .toolbar button{ padding:0.15rem 0.35rem; margin-left:.2rem; border-radius:.4rem; }
        .toolbar{ text-align:right; margin-top:2px; }
        .sticky { position: sticky; top: 0; z-index: 999; background: white; padding: 12px 12px 6px 12px; border-bottom: 1px solid #eee; box-shadow: 0 1px 0 rgba(0,0,0,0.02); }
        </style>
        """, unsafe_allow_html=True)

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

# ===== Helpers =====
def _fmt_ts(ts):
    if ts is None: return ""
    if hasattr(ts, "strftime"): return ts.strftime("%Y-%m-%d %H:%M:%S")
    return str(ts)


def _highlight_keywords(text, keywords, case_sensitive=False, regex_mode=False):
    """Highlight keywords but skip HTML tags (prevent <span> corruption)."""
    if not keywords or not text:
        return text or ""
    try:
        if regex_mode:
            pat = re.compile(keywords, 0 if case_sensitive else re.IGNORECASE)
        else:
            words = [re.escape(k) for k in keywords.split() if k]
            if not words:
                return text
            pat = re.compile("(" + "|".join(words) + ")", 0 if case_sensitive else re.IGNORECASE)
    except re.error:
        return text

    # --- Fix: skip HTML tags during highlight ---
    parts = re.split(r'(<[^>]+>)', text)
    for i, p in enumerate(parts):
        if not p or p.startswith("<"):
            continue
        parts[i] = pat.sub(lambda m: f"<span class='highlight'>{m.group(0)}</span>", p)
    return "".join(parts)


def _colorize_brackets(text):
    return re.sub(r'\[([^\[\]]+)\]', r"[<span class='brk'>\1</span>]", text or "")

def _render_text(text, keywords, case_sensitive=False, regex_mode=False):
    return _highlight_keywords(_colorize_brackets(text), keywords, case_sensitive, regex_mode)

def _get_source_name_for_entry(eid: int) -> str:
    with SessionLocal() as s:
        q = (select(Source.name)
             .select_from(EntrySource)
             .join(Source, Source.id == EntrySource.source_id)
             .where(EntrySource.entry_id == eid))
        return s.execute(q).scalar_one_or_none() or ""

def _relink_source(entry_id: int, source_name: str):
    with SessionLocal() as s:
        s.execute(EntrySource.__table__.delete().where(EntrySource.entry_id == entry_id))
        if source_name.strip():
            src_obj = s.execute(select(Source).where(Source.name == source_name.strip())).scalar_one_or_none()
            if not src_obj:
                src_obj = Source(name=source_name.strip())
                s.add(src_obj); s.flush()
            s.add(EntrySource(entry_id=entry_id, source_id=src_obj.id))
        s.commit()

def _all_source_names(limit: int = 500) -> list[str]:
    """Fetch up to `limit` distinct source names, sorted alphabetically."""
    with SessionLocal() as s:
        rows = s.execute(select(Source.name).order_by(Source.name).limit(limit)).all()
        return [r[0] for r in rows if r and r[0]]

# ===== Tabs =====
tab_search, tab_bulk = st.tabs(["🔎 Search", "🛠️ Bulk Replace"])

# ---------------- SEARCH ----------------
with tab_search:
    st.markdown('<div class="sticky">', unsafe_allow_html=True)
    q = st.text_input("Keyword(s)", key="search_q")
    colA, colB, colC = st.columns([1, 1, 2])
    with colA:
        ls = st.selectbox("Source Lang", ["", "en", "zh"], index=1, key="search_ls")
    with colB:
        lt = st.selectbox("Target Lang", ["", "zh", "en"], index=1, key="search_lt")
    with colC:
        colx1, colx2, colx3 = st.columns([1, 1, 1])
        with colx1:
            case_sensitive = st.checkbox("Case", value=False, key="search_case")
        with colx2:
            regex_mode = st.checkbox("Regex", value=False, key="search_regex")
        with colx3:
            limit = st.number_input("Page Size", 10, 500, 80, step=10, key="search_limit")

    # === New: Source filter (select or type) ===
    src_list = ["(Any)"] + _all_source_names(500)
    colS1, colS2, colS3 = st.columns([1.2, 1.2, 0.8])
    with colS1:
        src_sel = st.selectbox("Source filter (select)", options=src_list, index=0, key="search_source_sel")
    with colS2:
        src_typed = st.text_input("or type (partial ok)", key="search_source_typed")
    with colS3:
        src_exact = st.checkbox("Exact", value=False, key="search_source_exact")

    opt = st.selectbox("Time", ["All", "Last 7 days", "Last 30 days", "Custom Range"], key="search_time")
    go = st.button("Run Search", key="search_go")
    st.markdown("</div>", unsafe_allow_html=True)

    date_from = date_to = None
    if opt == "Last 7 days":
        date_from = (datetime.now() - timedelta(days=7)).date().isoformat()
    elif opt == "Last 30 days":
        date_from = (datetime.now() - timedelta(days=30)).date().isoformat()
    elif opt == "Custom Range":
        c1, c2 = st.columns(2)
        with c1: df = st.date_input("From", value=date.today(), key="search_df")
        with c2: dt = st.date_input("To", value=date.today(), key="search_dt")
        date_from, date_to = df.isoformat(), dt.isoformat()

    # Decide effective source filter
    effective_source = (src_typed.strip() if src_typed and src_typed.strip() else None)
    if not effective_source and src_sel and src_sel != "(Any)":
        effective_source = src_sel

    if go:
        rows = search(q, ls or None, lt or None, limit=int(limit), date_from=date_from, date_to=date_to)
        shown = 0
        for i, row in enumerate(rows, start=1):
            _id, src, tgt = row[0], row[1], row[2]
            sname = _get_source_name_for_entry(_id)

            # Apply source filter client-side if provided
            if effective_source:
                if src_exact:
                    if sname != effective_source:
                        continue
                else:
                    if effective_source.lower() not in (sname or "").lower():
                        continue

            src_h = _render_text(src, q, case_sensitive, regex_mode)
            tgt_h = _render_text(tgt, q, case_sensitive, regex_mode)

            c_text, c_tools = st.columns([10,2])
            with c_text:
                shown += 1
                st.markdown(f"<div class='row'><span class='num'>{shown}.</span><span class='src'>{src_h}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='row'><span class='num ghost'>{shown}.</span><span class='tgt'>{tgt_h}</span></div>", unsafe_allow_html=True)
                st.markdown(f"<span class='source'>{sname}</span>", unsafe_allow_html=True)
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
                    with SessionLocal() as s:
                        e = s.get(Entry, _id)
                    c1, c2 = st.columns(2)
                    with c1:
                        new_src = st.text_area("中文 / Source text", value=e.src_text if e else src, height=90, key=f"edit_src_{_id}")
                        new_tgt = st.text_area("English / Target text", value=e.tgt_text if e else tgt, height=90, key=f"edit_tgt_{_id}")
                    with c2:
                        new_source_name = st.text_input("Source name", value=sname, key=f"edit_sourcename_{_id}")
                    b1, b2 = st.columns([1,1])
                    with b1:
                        if st.button("Save", key=f"save_{_id}"):
                            with SessionLocal() as s:
                                ent = s.get(Entry, _id)
                                if ent:
                                    ent.src_text = new_src.strip() or ent.src_text
                                    ent.tgt_text = new_tgt.strip() or ent.tgt_text
                                    s.commit()
                            _relink_source(_id, new_source_name)
                            st.success("Saved.")
                    with b2:
                        st.caption("Use Bulk Replace for mass edits.")

            if ins_clicked:
                with st.expander("Insert AFTER", expanded=True):
                    s_guess = sname
                    art_title = st.text_input("Article title", value=s_guess, key=f"ins_art_title_{_id}")
                    art = get_article_by_title(art_title.strip()) if art_title.strip() else None
                    if not art and art_title.strip():
                        if st.checkbox("Create article if not exists", value=True, key=f"ins_create_{_id}"):
                            art = create_article(art_title.strip())
                    if art:
                        aid = art.id if hasattr(art, "id") else art[0]
                        pos_default = 0
                        try:
                            seq = get_article_sentences(aid)
                            ids = [ (r.id if hasattr(r,'id') else r[0]) for r in seq ]
                            if _id in ids:
                                pos_default = ids.index(_id) + 1
                        except Exception:
                            pos_default = 0
                        ins_pos = st.number_input("Insert after position (1-based)", min_value=0, value=pos_default, step=1, key=f"ins_pos_{_id}")
                        with st.form(f"ins_form_{_id}", clear_on_submit=True):
                            zh_new = st.text_area("中文 / Source text", height=80, key=f"ins_zh_{_id}")
                            en_new = st.text_area("English / Target text", height=80, key=f"ins_en_{_id}")
                            do_ins = st.form_submit_button("Insert AFTER")
                        if do_ins:
                            if not zh_new.strip() or not en_new.strip():
                                st.error("Both zh and en are required.")
                            else:
                                try:
                                    new_id = insert_sentence(aid, ins_pos, zh_new, en_new, ls="zh", lt="en", source_name=None)
                                    st.success(f"Inserted new entry #{new_id} at position {ins_pos+1}.")
                                except Exception as e:
                                    st.error(f"Insert failed: {e}")
                    else:
                        st.info("Provide a valid article title to insert into.")

            if clone_clicked:
                with st.expander("Clone & Insert AFTER", expanded=True):
                    s_guess = sname
                    art_title2 = st.text_input("Article title", value=s_guess, key=f"clone_art_title_{_id}")
                    art2 = get_article_by_title(art_title2.strip()) if art_title2.strip() else None
                    if not art2 and art_title2.strip():
                        if st.checkbox("Create article if not exists", value=True, key=f"clone_create_{_id}"):
                            art2 = create_article(art_title2.strip())
                    if art2:
                        aid2 = art2.id if hasattr(art2, "id") else art2[0]
                        pos_default2 = 0
                        try:
                            seq2 = get_article_sentences(aid2)
                            ids2 = [ (r.id if hasattr(r,'id') else r[0]) for r in seq2 ]
                            if _id in ids2:
                                pos_default2 = ids2.index(_id) + 1
                        except Exception:
                            pos_default2 = 0
                        ins_pos2 = st.number_input("Insert after position (1-based)", min_value=0, value=pos_default2, step=1, key=f"clone_pos_{_id}")
                        clone_id = st.text_input("Entry ID to clone", key=f"clone_id_{_id}")
                        if st.button("Clone & Insert", key=f"clone_go_{_id}"):
                            try:
                                eid = int(clone_id.strip())
                            except Exception:
                                st.error("Please enter a valid integer entry ID.")
                            else:
                                with SessionLocal() as s2:
                                    e2 = s2.get(Entry, eid)
                                if not e2:
                                    st.error(f"Entry #{eid} not found.")
                                else:
                                    try:
                                        new_id = insert_sentence(aid2, ins_pos2, e2.src_text, e2.tgt_text, ls=e2.lang_src, lt=e2.lang_tgt, source_name=None)
                                        st.success(f"Cloned entry #{eid} → new entry #{new_id} at position {ins_pos2+1}.")
                                    except Exception as e:
                                        st.error(f"Clone-insert failed: {e}")
                    else:
                        st.info("Provide a valid article title to insert into.")

            if del_clicked:
                with st.expander("Confirm delete?", expanded=True):
                    st.warning("This will delete the entry permanently.")
                    c1, c2 = st.columns(2)
                    if c1.button("Delete", key=f"del_yes_{_id}"):
                        with SessionLocal() as s:
                            ent = s.get(Entry, _id)
                            if ent:
                                s.delete(ent); s.commit()
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
    if opt2 == "Last 7 days":
        date_from2 = (datetime.now() - timedelta(days=7)).date().isoformat()
    elif opt2 == "Last 30 days":
        date_from2 = (datetime.now() - timedelta(days=30)).date().isoformat()
    elif opt2 == "Custom range":
        c1, c2 = st.columns(2)
        with c1: df2 = st.date_input("From", value=date.today(), key="bulk_df")
        with c2: dt2 = st.date_input("To", value=date.today(), key="bulk_dt")
        date_from2, date_to2 = df2.isoformat(), dt2.isoformat()

    if prev_btn:
        preview_rows = find_matches(keyword=kw, scope=scope, source_name=src_name_filter or None,
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
        changed = bulk_replace(keyword=kw, replacement=repl, scope=scope,
                               source_name=src_name_filter or None,
                               date_from=date_from2, date_to=date_to2,
                               regex_mode=regex_mode2, case_sensitive=case_sensitive2,
                               strict_word=strict_word, first_only=first_only)
        st.success(f"✅ Done! Updated {changed} rows.")
