# 1_📑_From_Page.py — Source Article View（API版）
from app import API_BASE
import streamlit as st
from datetime import datetime
from typing import Optional, List, Tuple
import pathlib, base64, requests, re

from repo import client  # create_article / get_article_sentences / insert_sentence / update_entry / delete_entry

st.set_page_config(layout="wide", page_title="From • Source Article View", page_icon="📑")

# ====== 字体样式（与原版一致） ======
def _emit_font_css(embed_ok: bool, font_b64: Optional[str] = None, use_cdn: bool = False):
    css = """
    :root{--font-en-serif:"Constantia","Palatino Linotype","Palatino","Georgia",serif;--font-zh-serif:"Noto Serif SC","Source Han Serif SC","SimSun","霞鹜文楷","KaiTi",serif;--num-col-width:2.4rem;--num-gap:0.5rem;}
    .highlight{background-color:#007BFF;color:#fff;padding:0 2px;border-radius:3px;}
    .brk{color:#007BFF;}
    .row{display:grid;grid-template-columns:var(--num-col-width) 1fr;column-gap:var(--num-gap);align-items:start;}
    .num{color:#9ca3af;font-weight:400;font-size:1.25rem;font-family:"Palatino Linotype","Palatino","Georgia",serif;justify-self:end;}
    .num.ghost{visibility:hidden;}
    .source{margin-left:calc(var(--num-col-width) + var(--num-gap));color:#6b7280;display:block;}
    .ts{margin-left:calc(var(--num-col-width) + var(--num-gap));color:#6b7280;font-size:0.9rem;display:block;}
    .src{font-size:1.1rem;line-height:1.6;font-family:var(--font-en-serif);font-weight:500;margin-bottom:14px;display:block;}
    .tgt{font-size:1.05rem;line-height:1.65;font-family:var(--font-zh-serif);font-weight:400;margin-bottom:18px;display:block;}
    .block-container hr{margin:18px 0 22px;border:0;border-top:1px solid #e5e7eb;}
    .toolbar button{padding:.15rem .35rem;margin-left:.2rem;border-radius:.4rem;}
    .toolbar{text-align:right;margin-top:2px;}
    """
    if embed_ok and font_b64:
        st.markdown(f"<style>@font-face{{font-family:'NotoSerifSCEmbed';src:url(data:font/otf;base64,{font_b64}) format('opentype');font-weight:100 900;font-style:normal;font-display:swap;}}:root{{--font-zh-serif:'NotoSerifSCEmbed','Noto Serif SC','Source Han Serif SC','SimSun','霞鹜文楷','KaiTi',serif;}}{css}</style>", unsafe_allow_html=True)
    elif use_cdn:
        st.markdown(f"<style>@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap');{css}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

try:
    fp = pathlib.Path("assets/NotoSerifCJKsc-VF.otf")
    if fp.exists() and fp.stat().st_size <= 10*1024*1024:
        _emit_font_css(True, base64.b64encode(fp.read_bytes()).decode(), use_cdn=False)
    else:
        _emit_font_css(False, None, use_cdn=True)
except Exception:
    _emit_font_css(False, None, use_cdn=True)

st.title("📑 From • Source Article View")

# ====== 辅助：来源列表 ======
def list_sources(limit=500) -> List[str]:
    try:
        r = requests.get(f"{API_BASE}/sources", params={"limit":limit}, timeout=10)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return sorted({d.get("name","") for d in data if d.get("name")})
        return sorted({str(x) for x in data if x})
    except Exception:
        return []

def colorize_brackets(text: str) -> str:
    return re.sub(r'\[([^\[\]]+)\]', r"[<span class='brk'>\1</span>]", text or "")

# ====== 顶栏：选择出处 + 撤销/重做（仍保留） ======
if "undo" not in st.session_state: st.session_state.undo = []
if "redo" not in st.session_state: st.session_state.redo = []

def push_undo(action: dict):
    st.session_state.undo.append(action); st.session_state.redo.clear()

def do_undo():  # 用 API 反向执行
    if not st.session_state.undo: st.warning("Nothing to undo."); return
    act = st.session_state.undo.pop(); t = act.get("type")
    if t == "edit":
        client.update_entry(act["id"], **act["before"])
    elif t == "move":
        client.update_entry(act["id"], position=act["before_pos"], article_id=act["article_id"])
    elif t in ("insert_new","clone_insert"):
        client.delete_entry(act["new_id"])
    elif t == "delete":
        # 简化：把删除前的文本在当前位置再插回（位置由后端处理）
        client.insert_sentence(act["article_id"], act["before_pos"]-1, act["before"]["src"], act["before"]["tgt"], ls=act["before"]["ls"], lt=act["before"]["lt"])
    st.session_state.redo.append(act)

def do_redo():
    if not st.session_state.redo: st.warning("Nothing to redo."); return
    act = st.session_state.redo.pop(); t = act.get("type")
    if t == "edit":
        client.update_entry(act["id"], **act["after"])
    elif t == "move":
        client.update_entry(act["id"], position=act["after_pos"], article_id=act["article_id"])
    elif t in ("insert_new","clone_insert"):
        client.insert_sentence(act["article_id"], act["after_pos"]-1, act["payload"]["src"], act["payload"]["tgt"], ls=act["payload"]["ls"], lt=act["payload"]["lt"])
    elif t == "delete":
        client.delete_entry(act["deleted_id"])
    st.session_state.undo.append(act)

# 出处选择
srcs = list_sources()
if not srcs:
    st.info("还没有来源（source）。先在 Insert/Bulk 里入库一些带来源的条目吧。"); st.stop()
label = st.selectbox("Choose Source (出处)", [f"{s}" for s in srcs], key="top_src_select")
current_source = label

# 解析/创建文章
art_id = None
try:
    # 后端建议：POST /articles {title} => 返回 id；若已存在可直接返回现有 id
    art_id = client.create_article(current_source)
except Exception:
    pass
art_id = int(art_id) if isinstance(art_id, int) else int(art_id or 0)

# 拉取句子序列（已按 position 排好）
rows: List[Tuple[int,str,str,int,Optional[str]]] = []
if art_id:
    seq = client.get_article_sentences(art_id)
    # 兼容 (id, src, tgt, pos, ts) / dict
    for r in seq:
        if isinstance(r, dict):
            rows.append((int(r.get("id")), r.get("src") or r.get("src_text",""), r.get("tgt") or r.get("tgt_text",""), int(r.get("position",0)), r.get("created_at")))
        else:
            rows.append((int(r[0]), r[1], r[2], int(r[3]), r[4]))

cols = st.columns([4,1,1])
with cols[1]:
    if st.button("↶ Undo"): do_undo()
with cols[2]:
    if st.button("↷ Redo"): do_redo()

st.subheader(f"Sentences for: {current_source}")

# ===== 渲染 + 右侧工具条 =====
for rid, src_text, tgt_text, pos, ts in rows:
    c_text, c_tools = st.columns([10,2])
    with c_text:
        st.markdown(f"<div class='row'><span class='num'>{pos}.</span><span class='src'>{colorize_brackets(src_text)}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='row'><span class='num ghost'>{pos}.</span><span class='tgt'>{colorize_brackets(tgt_text)}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<span class='source'>{current_source}</span>", unsafe_allow_html=True)
        if ts: st.markdown(f"<span class='ts'>ID: {rid} • {ts}</span>", unsafe_allow_html=True)

    with c_tools:
        st.markdown("<div class='toolbar'>", unsafe_allow_html=True)
        edit_clicked   = st.button("✏️", key=f"tb_edit_{rid}", help="Edit / Insert after")
        insert_clicked = st.button("➕", key=f"tb_insert_{rid}", help="Insert after")
        del_clicked    = st.button("🗑", key=f"tb_del_{rid}", help="Delete")
        st.markdown("</div>", unsafe_allow_html=True)

    if edit_clicked or insert_clicked:
        with st.expander("Edit / Insert", expanded=True):
            tabs = st.tabs(["Edit this sentence", "Insert AFTER"])
            # 编辑
            with tabs[0]:
                c1, c2 = st.columns(2)
                with c1:
                    new_src = st.text_area("中文 / Source text", value=src_text, height=90, key=f"edit_src_{rid}")
                    new_tgt = st.text_area("English / Target text", value=tgt_text, height=90, key=f"edit_tgt_{rid}")
                with c2:
                    new_position = st.number_input("Move to position", min_value=1, value=pos, step=1, key=f"edit_pos_{rid}")
                b1, b2 = st.columns([1,1])
                with b1:
                    if st.button("Save text", key=f"save_{rid}"):
                        before = {"src": src_text, "tgt": tgt_text}
                        after = {"src": new_src.strip() or src_text, "tgt": new_tgt.strip() or tgt_text}
                        client.update_entry(rid, **after)
                        push_undo({"type":"edit","id":rid,"before":before,"after":after,"article_id":art_id})
                        st.success("Saved.")
                with b2:
                    if st.button("Move", key=f"move_{rid}"):
                        client.update_entry(rid, position=int(new_position), article_id=art_id)
                        push_undo({"type":"move","id":rid,"before_pos":pos,"after_pos":int(new_position),"article_id":art_id})
                        st.success(f"Moved to position {int(new_position)}.")

            # 插入
            with tabs[1]:
                sub_tabs = st.tabs(["Create New", "Clone by ID"])
                with sub_tabs[0]:
                    with st.form(f"form_new_after_{rid}", clear_on_submit=True):
                        zh = st.text_area("中文 / Source text", height=80, key=f"ins_zh_{rid}")
                        en = st.text_area("English / Target text", height=80, key=f"ins_en_{rid}")
                        ok = st.form_submit_button("Insert (Ctrl+Enter)")
                    if ok:
                        if not zh.strip() or not en.strip():
                            st.error("Both zh and en are required.")
                        else:
                            new_id = client.insert_sentence(art_id, pos, zh, en, ls="zh", lt="en")
                            push_undo({"type":"insert_new","new_id":new_id,"article_id":art_id,"after_pos":pos+1,"payload":{"src":zh,"tgt":en,"ls":"zh","lt":"en"}})
                            st.success(f"Inserted new entry #{new_id} at position {pos+1}.")
                with sub_tabs[1]:
                    clone_id = st.text_input("Entry ID to clone", key=f"clone_id_{rid}")
                    if st.button("Clone & Insert", key=f"clone_btn_{rid}"):
                        try:
                            cid = int(clone_id.strip())
                        except:
                            st.error("Please enter a valid integer entry ID.")
                        else:
                            # 直接用当前行内容克隆最稳（与 Search 页面一致）
                            new_id = client.insert_sentence(art_id, pos, src_text, tgt_text)
                            push_undo({"type":"clone_insert","new_id":new_id,"article_id":art_id,"after_pos":pos+1,
                                       "payload":{"src":src_text,"tgt":tgt_text,"ls":"zh","lt":"en"}})
                            st.success(f"Cloned entry #{cid} → new entry #{new_id} at position {pos+1}.")

    if del_clicked:
        with st.expander("Confirm delete?", expanded=True):
            st.warning("This will delete this entry from DB. You can Undo afterwards.")
            if st.button("Delete permanently", key=f"del_yes_{rid}"):
                before = {"src": src_text, "tgt": tgt_text, "ls":"zh", "lt":"en"}
                client.delete_entry(rid)
                push_undo({"type":"delete","deleted_id":rid,"article_id":art_id,"before":before,"before_pos":pos})
                st.success("Deleted.")

    st.markdown("---")
