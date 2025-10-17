from app import API_BASE
import streamlit as st
from datetime import datetime
from typing import Optional
import pathlib, base64

# Ensure full model imports (fix NameError: Article)
from sqlalchemy import select, func, update
from models import SessionLocal, Entry, EntrySource, Source, Article, init_db
from repo import insert_sentence, get_article_by_title, create_article, get_article_sentences, delete_entry

st.set_page_config(layout="wide", page_title="From • Source Article View", page_icon="📑")
init_db()

# =========================
# Unified typography injection WITHOUT f-strings
# =========================
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None, use_cdn: bool = False):
    if embed_ok and font_b64:
        css = """
<style>
@font-face {
  font-family: 'NotoSerifSCEmbed';
  src: url(data:font/otf;base64,{B64}) format('opentype');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
:root {
  --font-en-serif: "Constantia","Palatino Linotype","Palatino","Georgia",serif;
  --font-zh-serif: "NotoSerifSCEmbed","Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif;
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
.src { font-size:1.1rem; line-height:1.6;  font-family:var(--font-en-serif); font-weight:500; margin-bottom:14px; display:block; }
.tgt { font-size:1.05rem; line-height:1.65; font-family:var(--font-zh-serif); font-weight:400; margin-bottom:18px; display:block; }
.block-container hr { margin:18px 0 22px 0; border:0; border-top:1px solid #e5e7eb; }
.toolbar button{ padding:0.15rem 0.35rem; margin-left:.2rem; border-radius:.4rem; }
.toolbar{ text-align:right; margin-top:2px; }
</style>
"""
        st.markdown(css.replace("{B64}", font_b64), unsafe_allow_html=True)
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
</style>
""", unsafe_allow_html=True)

# Try font embedding and gracefully fall back
_font_b64 = None
try:
    font_path = pathlib.Path("assets/NotoSerifCJKsc-VF.otf")
    if font_path.exists() and font_path.stat().st_size <= 10*1024*1024:
        _font_b64 = base64.b64encode(font_path.read_bytes()).decode()
        _emit_font_css(True, _font_b64, use_cdn=False)
    else:
        _emit_font_css(False, None, use_cdn=True)
except Exception:
    _emit_font_css(False, None, use_cdn=True)

st.title("📑 From • Source Article View")


# ===== Helpers =====
def ensure_article_for_source(source: Source) -> Article:
    art = get_article_by_title(source.name)
    if art:
        return art
    create_article(source.name, source_name=source.name)
    return get_article_by_title(source.name)

def list_sources(alpha: bool = True):
    with SessionLocal() as s:
        stmt = select(Source).order_by(Source.name.asc() if alpha else Source.id.desc())
        return s.execute(stmt).scalars().all()

def sync_positions_for_source(source_id: int, article_id: int) -> int:
    """Attach source-linked entries that don't yet belong to the article, then assign positions by created_at."""
    with SessionLocal() as s:
        max_pos = s.execute(select(func.max(Entry.position)).where(Entry.article_id == article_id)).scalar()
        next_pos = 1 if max_pos is None else max_pos + 1
        stmt = (select(Entry.id, Entry.created_at)
                .join(EntrySource, EntrySource.entry_id == Entry.id)
                .where(EntrySource.source_id == source_id, Entry.article_id.is_(None))
                .order_by(Entry.created_at.asc()))
        rows = s.execute(stmt).all()
        c = 0
        for eid, _ in rows:
            s.execute(update(Entry).where(Entry.id == eid).values(article_id=article_id, position=next_pos))
            next_pos += 1; c += 1
        s.commit()
        return c

def get_article_id_for_source(source: Source) -> int:
    return ensure_article_for_source(source).id

def get_sentences_for_source(source: Source):
    aid = get_article_id_for_source(source)
    synced = sync_positions_for_source(source.id, aid)
    return get_article_sentences(aid), synced, aid

def _ensure_source(session, source_name: str):
    if not source_name:
        return None
    obj = session.execute(select(Source).where(Source.name == source_name)).scalar_one_or_none()
    if not obj:
        obj = Source(name=source_name)
        session.add(obj); session.flush()
    return obj

def relink_source(entry_id: int, source_name: str):
    with SessionLocal() as s:
        s.execute(EntrySource.__table__.delete().where(EntrySource.entry_id == entry_id))
        if source_name.strip():
            src_obj = _ensure_source(s, source_name.strip())
            s.add(EntrySource(entry_id=entry_id, source_id=src_obj.id))
        s.commit()

def move_entry_within_article(entry_id: int, new_position: int):
    with SessionLocal() as s:
        e = s.get(Entry, entry_id)
        if not e or e.article_id is None or e.position is None:
            return False
        old = e.position; aid = e.article_id
        if new_position == old: return True
        if new_position < 1: new_position = 1
        max_pos = s.execute(select(func.max(Entry.position)).where(Entry.article_id == aid)).scalar() or 1
        if new_position > max_pos: new_position = max_pos
        if new_position < old:
            s.execute(update(Entry).where(Entry.article_id==aid, Entry.position>=new_position, Entry.position<old).values(position=Entry.position+1))
        else:
            s.execute(update(Entry).where(Entry.article_id==aid, Entry.position<=new_position, Entry.position>old).values(position=Entry.position-1))
        e.position = new_position
        s.commit()
        return True

def reflow_positions(aid: int):
    with SessionLocal() as s:
        rows = s.execute(select(Entry).where(Entry.article_id==aid).order_by(Entry.position.asc(), Entry.id.asc())).scalars().all()
        for i, ent in enumerate(rows, start=1):
            ent.position = i
        s.commit()

# ===== Undo/Redo (session-level stacks) =====
if "undo" not in st.session_state: st.session_state.undo = []
if "redo" not in st.session_state: st.session_state.redo = []

def push_undo(action: dict):
    st.session_state.undo.append(action)
    st.session_state.redo.clear()

def do_undo():
    if not st.session_state.undo:
        st.warning("Nothing to undo.")
        return
    act = st.session_state.undo.pop()
    t = act.get("type")
    if t == "edit":
        with SessionLocal() as s:
            e = s.get(Entry, act["id"])
            if e:
                e.src_text = act["before"]["src_text"]
                e.tgt_text = act["before"]["tgt_text"]
                e.created_at = datetime.fromisoformat(act["before"]["created_at"]) if act["before"]["created_at"] else e.created_at
                s.commit()
        relink_source(act["id"], act["before"].get("source_name",""))
    elif t == "move":
        move_entry_within_article(act["id"], act["before_pos"])
    elif t in ("insert_new","clone_insert"):
        delete_entry(act["new_id"])
        reflow_positions(act["article_id"])
    elif t == "delete":
        with SessionLocal() as s:
            e = Entry(
                id=None,
                src_text=act["before"]["src_text"],
                tgt_text=act["before"]["tgt_text"],
                lang_src=act["before"]["lang_src"],
                lang_tgt=act["before"]["lang_tgt"],
                created_at=datetime.fromisoformat(act["before"]["created_at"]) if act["before"]["created_at"] else datetime.utcnow(),
                article_id=act["article_id"],
                position=act["before_pos"]
            )
            s.add(e); s.flush()
            relink_name = act["before"].get("source_name","")
            if relink_name:
                s.add(EntrySource(entry_id=e.id, source_id=_ensure_source(s, relink_name).id))
            s.commit()
        reflow_positions(act["article_id"])
    st.session_state.redo.append(act)

def do_redo():
    if not st.session_state.redo:
        st.warning("Nothing to redo.")
        return
    act = st.session_state.redo.pop()
    t = act.get("type")
    if t == "edit":
        with SessionLocal() as s:
            e = s.get(Entry, act["id"])
            if e:
                e.src_text = act["after"]["src_text"]
                e.tgt_text = act["after"]["tgt_text"]
                e.created_at = datetime.fromisoformat(act["after"]["created_at"]) if act["after"]["created_at"] else e.created_at
                s.commit()
        relink_source(act["id"], act["after"].get("source_name",""))
    elif t == "move":
        move_entry_within_article(act["id"], act["after_pos"])
    elif t in ("insert_new","clone_insert"):
        with SessionLocal() as s:
            e2 = Entry(
                src_text=act["payload"]["src_text"],
                tgt_text=act["payload"]["tgt_text"],
                lang_src=act["payload"]["ls"],
                lang_tgt=act["payload"]["lt"],
                created_at=datetime.utcnow(),
                article_id=act["article_id"],
                position=act["after_pos"]
            )
            s.add(e2); s.commit()
    elif t == "delete":
        delete_entry(act["deleted_id"])
        reflow_positions(act["article_id"])
    st.session_state.undo.append(act)

# ===== Top bar: choose + undo/redo =====
cols = st.columns([4,1,1])
with cols[0]:
    # Keep alphabetical for predictability
    with SessionLocal() as s:
        stmt = select(Source).order_by(Source.name.asc())
        srcs = s.execute(stmt).scalars().all()
    if not srcs:
        st.info("No sources yet. Add entries with a source first."); st.stop()
    options = {f"{s.name} (#{s.id})": s for s in srcs}
    label = st.selectbox("Choose Source (出处)", list(options.keys()), key="top_src_select")
    current_source = options[label]
with cols[1]:
    if st.button("↶ Undo"):
        do_undo()
with cols[2]:
    if st.button("↷ Redo"):
        do_redo()

rows, synced, article_id = get_sentences_for_source(current_source)
st.subheader(f"Sentences for: {current_source.name}")
if synced:
    st.success(f"Synchronized {synced} entries into ordered sequence.")

# ===== Helpers for rendering (color square brackets like Search) =====
import re as _re
def colorize_brackets(text: str) -> str:
    return _re.sub(r'\[([^\[\]]+)\]', r"[<span class='brk'>\1</span>]", text)

# ===== Render sentences with Search-like layout + right mini-toolbar =====
for rid, src_text, tgt_text, pos, ts in rows:
    # left content (numbers + text), right compact toolbar
    c_text, c_tools = st.columns([10,2])

    src_h = colorize_brackets(src_text or "")
    tgt_h = colorize_brackets(tgt_text or "")

    with c_text:
        st.markdown(f"<div class='row'><span class='num'>{pos}.</span><span class='src'>{src_h}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='row'><span class='num ghost'>{pos}.</span><span class='tgt'>{tgt_h}</span></div>", unsafe_allow_html=True)
        # meta lines (source name and timestamp)
        st.markdown(f"<span class='source'>{current_source.name}</span>", unsafe_allow_html=True)
        if ts:
            ts_s = ts.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ts, "strftime") else str(ts)
            st.markdown(f"<span class='ts'>ID: {rid} • {ts_s}</span>", unsafe_allow_html=True)

    with c_tools:
        st.markdown("<div class='toolbar'>", unsafe_allow_html=True)
        edit_clicked   = st.button("✏️", key=f"tb_edit_{rid}", help="Edit / Insert after")
        insert_clicked = st.button("➕", key=f"tb_insert_{rid}", help="Insert after")
        del_clicked    = st.button("🗑", key=f"tb_del_{rid}", help="Delete")
        st.markdown("</div>", unsafe_allow_html=True)

    # === Edit/Insert panels ===
    if edit_clicked or insert_clicked:
        with st.expander("Edit / Insert", expanded=True):
            tabs = st.tabs(["Edit this sentence", "Insert AFTER"])
            # ==== Edit this sentence ====
            with tabs[0]:
                with SessionLocal() as s:
                    e = s.get(Entry, rid)
                    q = select(Source.name).select_from(EntrySource).join(Source, Source.id==EntrySource.source_id).where(EntrySource.entry_id==rid)
                    current_src_name = s.execute(q).scalar_one_or_none() or current_source.name or ""
                c1, c2 = st.columns(2)
                with c1:
                    new_src = st.text_area("中文 / Source text", value=e.src_text if e else src_text, height=90, key=f"edit_src_{rid}")
                    new_tgt = st.text_area("English / Target text", value=e.tgt_text if e else tgt_text, height=90, key=f"edit_tgt_{rid}")
                with c2:
                    new_source_name = st.text_input("Source name", value=current_src_name, key=f"edit_sourcename_{rid}")
                    new_created = st.text_input("Created at (ISO, optional)", value=(e.created_at.isoformat(timespec='seconds') if e and e.created_at else ""), key=f"edit_created_{rid}")
                    new_position = st.number_input("Move to position", min_value=1, value=pos, step=1, key=f"edit_pos_{rid}")
                b1, b2 = st.columns([1,1])
                with b1:
                    if st.button("Save text / metadata", key=f"save_{rid}"):
                        before = {"src_text": src_text, "tgt_text": tgt_text, "created_at": ts.isoformat() if ts else "", "source_name": current_src_name}
                        after = {"src_text": new_src.strip() or src_text, "tgt_text": new_tgt.strip() or tgt_text, "created_at": new_created.strip(), "source_name": new_source_name.strip()}
                        with SessionLocal() as s:
                            ent = s.get(Entry, rid)
                            if ent:
                                ent.src_text = after["src_text"]
                                ent.tgt_text = after["tgt_text"]
                                if after["created_at"]:
                                    try:
                                        ent.created_at = datetime.fromisoformat(after["created_at"])
                                    except Exception:
                                        st.error("Invalid datetime format. Use ISO like 2025-10-10T12:34:56")
                                s.commit()
                        relink_source(rid, after["source_name"])
                        push_undo({"type":"edit","id":rid,"before":before,"after":after})
                        st.success("Saved.")
                with b2:
                    if st.button("Move", key=f"move_{rid}"):
                        if move_entry_within_article(rid, int(new_position)):
                            push_undo({"type":"move","id":rid,"before_pos":pos,"after_pos":int(new_position)})
                            st.success(f"Moved to position {int(new_position)}. Refresh to see update.")
                        else:
                            st.error("Move failed.")

            # ==== Insert AFTER ====
            with tabs[1]:
                sub_tabs = st.tabs(["Create New", "Clone by ID"])
                with sub_tabs[0]:
                    st.caption("Ctrl+Enter to submit.")
                    with st.form(f"form_new_after_{rid}", clear_on_submit=True):
                        zh = st.text_area("中文 / Source text", height=80, key=f"ins_zh_{rid}")
                        en = st.text_area("English / Target text", height=80, key=f"ins_en_{rid}")
                        ok = st.form_submit_button("Insert (Ctrl+Enter)")
                    st.components.v1.html(f"""
                    <script>
                      (function(){{
                        const root = window.parent.document;
                        function clickBtn(){{
                          const btns = Array.from(root.querySelectorAll('button'));
                          const btn = btns.find(b => b.innerText.includes('Insert (Ctrl+Enter)'));
                          if(btn) btn.click();
                        }}
                        root.addEventListener('keydown', function(e){{
                          if((e.ctrlKey||e.metaKey) && e.key==='Enter'){{ clickBtn(); }}
                        }}, {{capture:true}});
                      }})();
                    </script>
                    """, height=0)
                    if ok:
                        if not zh.strip() or not en.strip():
                            st.error("Both zh and en are required.")
                        else:
                            new_id = insert_sentence(article_id, pos, zh, en, ls="zh", lt="en", source_name=None)
                            push_undo({"type":"insert_new","new_id":new_id,"article_id":article_id,"after_pos":pos+1,"payload":{"src_text":zh,"tgt_text":en,"ls":"zh","lt":"en"}})
                            st.success(f"Inserted new entry #{new_id} at position {pos+1}.")
                with sub_tabs[1]:
                    clone_id = st.text_input("Entry ID to clone", key=f"clone_id_{rid}")
                    if st.button("Clone & Insert", key=f"clone_btn_{rid}"):
                        try:
                            eid = int(clone_id.strip())
                        except:
                            st.error("Please enter a valid integer entry ID.")
                        else:
                            with SessionLocal() as s:
                                e2 = s.get(Entry, eid)
                                if not e2:
                                    st.error(f"Entry #{eid} not found.")
                                else:
                                    new_id = insert_sentence(article_id, pos, e2.src_text, e2.tgt_text, ls=e2.lang_src, lt=e2.lang_tgt, source_name=None)
                                    push_undo({"type":"clone_insert","new_id":new_id,"article_id":article_id,"after_pos":pos+1,"payload":{"src_text":e2.src_text,"tgt_text":e2.tgt_text,"ls":e2.lang_src,"lt":e2.lang_tgt}})
                                    st.success(f"Cloned entry #{eid} → new entry #{new_id} at position {pos+1}.")

    # ==== Delete panel ====
    if del_clicked:
        with st.expander("Confirm delete?", expanded=True):
            st.warning("This will delete this entry from the article (and DB). You can Undo afterwards.")
            c1, c2 = st.columns(2)
            if c1.button("Delete permanently", key=f"del_yes_{rid}"):
                before = {"src_text": src_text, "tgt_text": tgt_text, "lang_src":"zh", "lang_tgt":"en", "created_at": ts.isoformat() if ts else "", "source_name":""}
                delete_entry(rid)
                reflow_positions(article_id)
                push_undo({"type":"delete","deleted_id":rid,"article_id":article_id,"before":before,"before_pos":pos})
                st.success("Deleted.")

    st.markdown("---")
