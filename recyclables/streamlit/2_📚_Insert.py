
# --- imports: add/update these ---
from app import API_BASE
import re
from datetime import datetime, timedelta, date
from typing import List, Tuple
import streamlit as st

from sqlalchemy import select, update, and_
from models import SessionLocal, Source, Entry, Article, EntrySource
from repo import upsert_entry

st.set_page_config(page_title="Batch Insert (Flexible)", layout="wide", page_icon="📦")
st.title("📚 Insert — Insert / Detection / Rename / Recent")

# ===== CSS (improved sticky that survives scrolling) + widen inputs =====
st.markdown("""
<style>
/* Sticky toolbar that stays visible even when scrolling inside tabs */
.sticky-toolbar {
  position: sticky;
  top: 0;
  z-index: 9999;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
}

/* Avoid extra vertical gaps so toolbar hugging content */
.stRadio > div { gap: 14px !important; }

/* Make Insert button compact but visible */
.sticky-toolbar .stButton>button {
    background:#ff4b4b !important;
    color:#fff !important;
    border:0 !important;
    border-radius:12px !important;
    padding:8px 14px !important;
    font-weight:600 !important;
    box-shadow:0 6px 18px rgba(0,0,0,.12), 0 2px 6px rgba(0,0,0,.08) !important;
}
.sticky-toolbar .stButton>button:disabled { opacity:.55 !important; cursor:not-allowed !important; }

/* Widen main container & textareas */
.block-container { max-width: 1180px; }
.stTextArea textarea {
    min-height: 180px;
    line-height: 1.45;
    font-size: 0.96rem;
}
</style>
""", unsafe_allow_html=True)

def _list_sources() -> List[str]:
    with SessionLocal() as s:
        rows = s.execute(select(Source.name).where(Source.name != None)).all()
    return sorted({r[0] for r in rows if r[0]})

def split_text(text: str, mode: str, delim_regex: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    if mode == "no_split":
        return [text]
    if mode == "by_line":
        return [ln.strip() for ln in text.splitlines() if ln.strip()]
    parts = re.split(delim_regex, text)
    return [p.strip() for p in parts if p and p.strip()]

def lang_score(text: str):
    zh = len(re.findall(r'[\u4e00-\u9fff]', text))
    en = len(re.findall(r'[A-Za-z]', text))
    return zh, en

def check_lang_direction(text: str, expect: str, min_len: int, dominance: float) -> bool:
    if not text or len(text) < min_len:
        return True
    zh, en = lang_score(text)
    if expect == "zh":
        return zh >= dominance * max(1, en)
    else:
        return en >= dominance * max(1, zh)

# -------- Tabs --------
tab_insert, tab_preview, tab_detect, tab_rename, tab_recent = st.tabs(
    ["📥 Insert", "👀 Preview", "🧪 Detection", "🛠️ Rename", "🧾 Recent"]
)

# -------- Insert tab --------
with tab_insert:
    # ===== Sticky Row: Direction + Insert (right-side buttons removed) =====
    st.markdown('<div class="sticky-toolbar">', unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1], gap="small")
    with c1:
        direction = st.radio("本批次翻译方向 / Direction", ["zh→en", "en→zh"], index=1, horizontal=True, key="ins_dir")
    with c2:
        # compute can_insert from current state
        mode_display = st.session_state.get("ins_mode", "不要拆分（整段入库）")
        mode_key_top = {"不要拆分（整段入库）": "no_split",
                        "按行对齐（每行是一条）": "by_line",
                        "按分隔符（正则）": "by_regex"}.get(mode_display, "no_split")
        default_regex = r"[。！？；;.!?:]+"
        delim_regex_top = st.session_state.get("ins_regex", default_regex)

        src_text_top = st.session_state.get("src_input","")
        tgt_text_top = st.session_state.get("tgt_input","")
        src_items_top = split_text(src_text_top, mode_key_top, delim_regex_top)
        tgt_items_top = split_text(tgt_text_top, mode_key_top, delim_regex_top) if tgt_text_top.strip() else []
        pairs_top: List[Tuple[str, str]] = (
            list(zip(src_items_top[:min(len(src_items_top), len(tgt_items_top))], tgt_items_top))
            if tgt_items_top else [(s, "") for s in src_items_top]
        )
        pick_top = st.session_state.get("ins_srcpick", "➕ New…")
        src_name_top = st.session_state.get("ins_srcname", "MyBatch") if pick_top == "➕ New…" else pick_top
        can_insert_top = len(pairs_top) > 0 and str(src_name_top).strip() != ""

        top_clicked = st.button("📥 入库 / Insert", type="primary", disabled=not can_insert_top, key="ins_btn_top")
    st.markdown('</div>', unsafe_allow_html=True)

    ls, lt = ("zh", "en") if st.session_state.get("ins_dir", "en→zh") == "zh→en" else ("en", "zh")

    # ===== Original controls remain below =====
    mode = st.selectbox(
        "拆分方式 / Split Mode",
        ["不要拆分（整段入库）", "按行对齐（每行是一条）", "按分隔符（正则）"],
        index=0, key="ins_mode"
    )
    mode_key = {"不要拆分（整段入库）": "no_split",
                "按行对齐（每行是一条）": "by_line",
                "按分隔符（正则）": "by_regex"}[mode]

    default_regex = r"[。！？；;.!?:]+"
    delim_regex = st.text_input(
        "分隔符正则（仅在“按分隔符”模式下生效） / Delimiter Regex",
        value=default_regex,
        disabled=(mode_key != "by_regex"),
        key="ins_regex"
    )

    col1, col2 = st.columns(2)
    with col1:
        src_label = "中文段落（来源）" if ls == "zh" else "English paragraph (Source)"
        src_text = st.text_area(src_label, height=200, key="src_input")
    with col2:
        tgt_label = "English paragraph（译文，可选）" if lt == "en" else "中文段落（译文，可选）"
        tgt_text = st.text_area(tgt_label, height=200, key="tgt_input")

    existing_sources = _list_sources()
    options = ["➕ New…"] + existing_sources
    pick = st.selectbox(
        "统一出处 / Source Name (type to search existing)",
        options=options,
        index=0 if "MyBatch" not in existing_sources else options.index("MyBatch"),
        help="Choose an existing source (search by typing) or pick 'New…' to enter a fresh name.",
        key="ins_srcpick"
    )

    if pick == "➕ New…":
        src_name = st.text_input("New source name", value="MyBatch", key="ins_srcname")
    else:
        src_name = pick

    timestamp = st.text_input(
        "统一时间 / Timestamp (ISO)",
        value=datetime.now().isoformat(timespec="seconds"),
        key="ins_ts"
    )

    # recompute pairs for actual insert
    src_items = split_text(st.session_state.get("src_input",""), mode_key, delim_regex)
    tgt_raw = st.session_state.get("tgt_input","").strip()
    tgt_items = split_text(tgt_raw, mode_key, delim_regex) if tgt_raw else []
    pairs: List[Tuple[str, str]] = (
        list(zip(src_items[:min(len(src_items), len(tgt_items))], tgt_items))
        if tgt_items else [(s, "") for s in src_items]
    )

    def _direction_ok() -> bool:
        if not st.session_state.get("detect_enable", True):
            return True
        ok_src = check_lang_direction(st.session_state.get("src_input",""), ls, int(st.session_state.get("detect_minlen", 10)),
                                      float(st.session_state.get("detect_dom", 2.0)))
        if not ok_src:
            st.error("🔎 检测到源文与当前方向不符，请检查是否导错（中英对调）。")
            return False
        tgt_text_val = st.session_state.get("tgt_input","").strip()
        if tgt_text_val:
            ok_tgt = check_lang_direction(tgt_text_val, lt, int(st.session_state.get("detect_minlen", 10)),
                                          float(st.session_state.get("detect_dom", 2.0)))
            if not ok_tgt:
                st.error("🔎 检测到译文与当前方向不符，请检查是否导错（中英对调）。")
                return False
        return True

    if top_clicked:
        if _direction_ok():
            ok, fail = 0, 0
            for sline, tline in pairs:
                try:
                    upsert_entry(
                        entry_id=None,
                        src=sline,
                        tgt=tline,
                        ls=ls,
                        lt=lt,
                        source_name=src_name.strip(),
                        created_at=timestamp.strip() or None
                    )
                    ok += 1
                except Exception:
                    fail += 1
            if ok and not fail:
                st.success(f"✅ 已入库 {ok} 条，方向 {ls}→{lt}，来源：{src_name}")
            elif ok and fail:
                st.warning(f"⚠️ 部分成功：成功 {ok} 条，失败 {fail} 条。")
            else:
                st.error("❌ 入库失败，未写入任何条目。")

# -------- Preview tab (unchanged features) --------
with tab_preview:
    st.markdown("## 👀 预览 / Preview")
    direction = st.session_state.get("ins_dir", "en→zh")
    ls, lt = ("zh", "en") if direction == "zh→en" else ("en", "zh")
    mode_display = st.session_state.get("ins_mode", "不要拆分（整段入库）")
    mode_key = {"不要拆分（整段入库）": "no_split",
                "按行对齐（每行是一条）": "by_line",
                "按分隔符（正则）": "by_regex"}.get(mode_display, "no_split")
    default_regex = r"[。！？；;.!?:]+"
    delim_regex = st.session_state.get("ins_regex", default_regex)
    src_text = st.session_state.get("src_input","")
    tgt_text = st.session_state.get("tgt_input","")
    src_items = split_text(src_text, mode_key, delim_regex)
    tgt_items = split_text(tgt_text, mode_key, delim_regex) if tgt_text.strip() else []
    pairs: List[Tuple[str, str]] = (
        list(zip(src_items[:min(len(src_items), len(tgt_items))], tgt_items))
        if tgt_items else [(s, "") for s in src_items]
    )
    st.write(f"将要插入的条目数 / Items to insert: **{len(pairs)}**")
    with st.expander("展开查看每条 / Show items", expanded=True):
        for i, (sline, tline) in enumerate(pairs, 1):
            st.markdown(f"**#{i}**")
            st.markdown(f"- 源文 / Source: {sline}")
            if tline:
                st.markdown(f"- 译文 / Target: {tline}")
            st.markdown("---")

    if st.button("⚡ Preview 快捷入库", key="preview_quick_insert", type="primary", help="不离开预览直接入库"):
        pick = st.session_state.get("ins_srcpick", "➕ New…")
        src_name = st.session_state.get("ins_srcname", "MyBatch") if pick == "➕ New…" else pick
        timestamp = st.session_state.get("ins_ts", datetime.now().isoformat(timespec="seconds"))

        def _direction_ok_preview() -> bool:
            if not st.session_state.get("detect_enable", True):
                return True
            ok_src = check_lang_direction(st.session_state.get("src_input",""), ls, int(st.session_state.get("detect_minlen", 10)),
                                          float(st.session_state.get("detect_dom", 2.0)))
            if not ok_src:
                st.error("🔎 检测到源文与当前方向不符，请检查是否导错（中英对调）。")
                return False
            tgt_text_val = st.session_state.get("tgt_input","").strip()
            if tgt_text_val:
                ok_tgt = check_lang_direction(tgt_text_val, lt, int(st.session_state.get("detect_minlen", 10)),
                                              float(st.session_state.get("detect_dom", 2.0)))
                if not ok_tgt:
                    st.error("🔎 检测到译文与当前方向不符，请检查是否导错（中英对调）。")
                    return False
            return True

        if _direction_ok_preview():
            ok, fail = 0, 0
            for sline, tline in pairs:
                try:
                    upsert_entry(
                        entry_id=None,
                        src=sline,
                        tgt=tline,
                        ls=ls,
                        lt=lt,
                        source_name=src_name.strip(),
                        created_at=str(timestamp).strip() or None
                    )
                    ok += 1
                except Exception:
                    fail += 1
            if ok and not fail:
                st.success(f"✅ 预览快捷入库完成：{ok} 条，方向 {ls}→{lt}，来源：{src_name}")
            elif ok and fail:
                st.warning(f"⚠️ 预览快捷入库部分成功：成功 {ok} 条，失败 {fail} 条。")
            else:
                st.error("❌ 预览快捷入库失败，未写入任何条目。")

# -------- Detection / Rename / Recent tabs kept as-is --------
with tab_detect:
    st.markdown('<div class="sticky-toolbar">', unsafe_allow_html=True)
    enable_detect = st.checkbox("启用语言方向检测 / Enable direction check", value=True, key="detect_enable")
    cold1, cold2, cold3 = st.columns(3)
    with cold1:
        min_len = st.number_input("最小检测长度 / Min length", min_value=0, max_value=500,
                                  value=10, step=1, key="detect_minlen")
    with cold2:
        dominance = st.slider("主导比 / Dominance ratio", min_value=1.0, max_value=5.0,
                              value=2.0, step=0.1, key="detect_dom")
    with cold3:
        st.caption("当中文(或英文)数量 ≥ 主导比 × 另一方，即判定方向正确。")
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("检测参数会在“📥 Insert”页和“👀 Preview 快捷入库”前自动应用。")

with tab_rename:
    existing_sources = _list_sources()
    if not existing_sources:
        st.info("No existing sources found.")
    else:
        old = st.selectbox("Pick existing source", options=existing_sources, key="rename_old")
        new = st.text_input("New name", key="rename_new", placeholder="Type the new source name")
        col_a, col_b = st.columns([1, 3])
        with col_a:
            do = st.button("Rename", type="secondary", disabled=(not new.strip()), key="rename_do")
        if do:
            new_name = new.strip()
            if new_name in existing_sources and new_name != old:
                st.warning("That name already exists. Consider choosing a unique name.")
            else:
                try:
                    with SessionLocal() as s:
                        s.execute(update(Source).where(Source.name == old).values(name=new_name))
                        s.execute(update(Article).where(Article.title == old).values(title=new_name))
                        s.commit()
                    st.success(f"✅ Renamed '{old}' → '{new_name}' (Source + Article).")
                except Exception as e:
                    st.error(f"❌ Rename failed: {e}")

with tab_recent:
    cnt = st.selectbox("显示条数 / Show count", [5, 10, 20, 50], index=0, key="recent_cnt")
    today = date.today()
    start_7 = today - timedelta(days=6)
    date_range = st.date_input("筛选日期范围 / Date range (optional)",
                               [start_7, today], key="recent_range")
    with SessionLocal() as s:
        stmt = (
            select(Entry, Source.name)
            .join(EntrySource, Entry.id == EntrySource.entry_id, isouter=True)
            .join(Source, EntrySource.source_id == Source.id, isouter=True)
        )
        if date_range:
            if isinstance(date_range, list) and len(date_range) == 2 and date_range[0] and date_range[1]:
                start_dt = datetime.combine(date_range[0], datetime.min.time())
                end_dt = datetime.combine(date_range[1], datetime.max.time())
                stmt = stmt.where(and_(Entry.created_at >= start_dt, Entry.created_at <= end_dt))
        stmt = stmt.order_by(Entry.id.desc()).limit(int(cnt))
        rows = s.execute(stmt).all()

    for row in rows:
        e: Entry = row[0]
        src_display = row[1] if len(row) > 1 and row[1] else "(no source)"
        tag = f"[{e.lang_src}_to_{e.lang_tgt}]"
        time_disp = e.created_at.isoformat(sep=' ', timespec='seconds') if getattr(e, "created_at", None) else "-"
        st.markdown(f"**{tag}** 来源: {src_display}  时间: {time_disp}")
        st.markdown(f"- 源文：{e.src_text}")
        if getattr(e, "tgt_text", None):
            st.markdown(f"- 译文：{e.tgt_text}")
        st.markdown("---")
