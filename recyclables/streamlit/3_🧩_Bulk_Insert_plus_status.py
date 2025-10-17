from app import API_BASE
import os, time
import streamlit as st
from pathlib import Path

from text_utils import segment_text  # 统一分句接口
from repo import insert_sentence, get_article_by_title, create_article, get_article_sentences

st.set_page_config(page_title="Bulk Insert • Segment + Import", page_icon="🧩", layout="wide")
st.title("🧩 Bulk Insert — Segment Text → Sentences → DB")

with st.expander("How it works / 说明", expanded=False):
    st.markdown("""
    - 把一段文本粘贴到下面；
    - 选择分句引擎：**rule**（默认，无需模型）、**stanza**（适合中文）、**spacy**（适合英文）；
    - 预览结果，确认无误后批量入库；
    - `.jpg / 3.14 / Dr.` 等点号场景会自动保护，避免误分。
    """)

# ------------------ Local Model Status Panel ------------------
st.subheader("📦 本地模型路径状态显示")
colM1, colM2 = st.columns(2)

with colM1:
    stanza_dir = Path("stanza_resources")
    stanza_exists = stanza_dir.exists() and stanza_dir.is_dir()
    try:
        import stanza  # noqa
        stanza_installed = True
    except Exception:
        stanza_installed = False

    st.markdown(f"- **Stanza 安装**：{'✅ 已安装' if stanza_installed else '❌ 未安装'}")
    st.markdown(f"- **本地目录**：`{stanza_dir.as_posix()}` → {'✅ 存在' if stanza_exists else '⚠️ 不存在'}")
    if stanza_exists:
        langs = [p.name for p in stanza_dir.iterdir() if p.is_dir() and len(p.name)==2]
        st.caption(f"已检测到的语言包：{', '.join(langs) if langs else '（未发现标准语言目录）'}")

with colM2:
    spacy_path = Path("models/en_core_web_sm")
    spacy_dir_exists = spacy_path.exists() and spacy_path.is_dir()
    try:
        import spacy  # noqa
        spacy_installed = True
    except Exception:
        spacy_installed = False

    st.markdown(f"- **spaCy 安装**：{'✅ 已安装' if spacy_installed else '❌ 未安装'}")
    st.markdown(f"- **本地模型路径**：`{spacy_path.as_posix()}` → {'✅ 存在' if spacy_dir_exists else '⚠️ 不存在'}")
    st.caption("若存在则优先从本地加载；否则使用系统已安装模型；两者都缺失时自动退回规则分句。")

st.divider()

# ------------------ Controls ------------------
colA, colB, colC, colD = st.columns([1,1,1,1])
with colA:
    engine = st.selectbox("Engine", ["rule", "stanza", "spacy"], help="rule 无依赖最快；stanza 中文更稳；spacy 英文强")
with colB:
    lang = st.selectbox("Lang", ["auto", "zh", "en"], index=0, help="stanza 用到；rule/spacy 忽略该选项")
with colC:
    article_title = st.text_input("Article Title（入库的文章名）", value="")
with colD:
    start_pos = st.number_input("Insert after position (1-based)", min_value=0, value=0, step=1, help="在该位置之后插入；0 表示插入开头")

text = st.text_area("Paste text here（粘贴待分句文本）", height=220, placeholder="在此粘贴文本…")

# ------------------ Preview ------------------
segmented = st.session_state.get("segmented_preview", [])
if st.button("🔍 Segment Preview"):
    t0 = time.time()
    segmented = segment_text(text or "", engine=engine, lang=lang)
    dt = time.time() - t0
    st.session_state["segmented_preview"] = segmented
    st.success(f"Preview {len(segmented)} sentence(s). ⏱ {dt:.3f}s")
    for i, s in enumerate(segmented, 1):
        st.markdown(f"**{i}.** {s}")

st.divider()

# ------------------ Insert ------------------
disabled_insert = not ((text or "").strip() and (article_title or "").strip())
if st.button("⚡ Bulk Insert To DB", type="primary", disabled=disabled_insert):
    # 保证有分句结果
    sents = st.session_state.get("segmented_preview")
    if not sents:
        t0 = time.time()
        sents = segment_text(text or "", engine=engine, lang=lang)
        dt = time.time() - t0
        st.info(f"自动完成分句，共 {len(sents)} 条。 ⏱ {dt:.3f}s")

    # 解析或创建文章
    art = get_article_by_title(article_title.strip())
    if not art:
        art = create_article(article_title.strip())
    aid = art.id if hasattr(art, "id") else art[0]

    # 决定插入位置
    try:
        seq = get_article_sentences(aid)
        ids = [ (r.id if hasattr(r, 'id') else r[0]) for r in seq ]
        pos = len(ids) if start_pos == 0 else start_pos
    except Exception:
        pos = start_pos

    # 批量插入
    inserted = 0
    t0 = time.time()
    for s in sents:
        s = s.strip()
        if not s:
            continue
        try:
            new_id = insert_sentence(aid, pos, s, "", ls="zh", lt="en", source_name=None)
            inserted += 1
            pos += 1
        except Exception as e:
            st.error(f"Insert failed at pos {pos}: {e}")
            break
    dt_all = time.time() - t0

    st.success(f"✅ Done. Inserted {inserted} sentence(s) into '{article_title}'. ⏱ {dt_all:.3f}s")
    st.balloons()
