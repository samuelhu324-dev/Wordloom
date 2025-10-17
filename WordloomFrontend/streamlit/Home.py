# -*- coding: utf-8 -*-
"""
Home.py — API 版主页（检索 / 就地编辑 / 删除）
依赖：
  - from app import API_BASE         # 轻量配置，提供后端地址
  - from repo import client          # 前端 HTTP 客户端（ApiClient）
后端：
  - /entries/search                  # GET  检索
  - /entries                         # POST 新增（此页未用）
  - /entries/{entry_id}              # PUT  更新；DELETE 删除
"""
from __future__ import annotations
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

from app import API_BASE
from repo import client, ApiError

st.set_page_config(
    page_title="Wordloom · Home (API)",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 小工具
# -----------------------------
def _normalize_rows(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    """把后端返回字段规范到统一列名，便于渲染/编辑。"""
    if not rows:
        return pd.DataFrame(columns=["id", "src", "tgt", "ls", "lt", "source_name", "created_at"])
    normed = []
    for r in rows:
        normed.append({
            "id": r.get("id") or r.get("entry_id"),
            "src": r.get("src") or r.get("src_text") or r.get("source_text"),
            "tgt": r.get("tgt") or r.get("tgt_text") or r.get("target_text"),
            "ls": r.get("ls") or r.get("lang_src") or r.get("src_lang") or "zh",
            "lt": r.get("lt") or r.get("lang_tgt") or r.get("tgt_lang") or "en",
            "source_name": r.get("source_name") or r.get("source") or "",
            "created_at": r.get("created_at") or r.get("ts") or "",
        })
    df = pd.DataFrame(normed)
    # 统一排序：最新在前（若无时间字段不会报错）
    if "created_at" in df.columns and df["created_at"].notna().any():
        try:
            df["__dt"] = pd.to_datetime(df["created_at"], errors="coerce")
            df = df.sort_values("__dt", ascending=False).drop(columns=["__dt"])
        except Exception:
            pass
    return df

def _diff_updates(original: pd.DataFrame, edited: pd.DataFrame) -> List[Dict[str, Any]]:
    """找出被修改的行，用于批量调用 update_entry。"""
    updates = []
    orig = original.set_index("id")
    edt = edited.set_index("id")
    common_ids = orig.index.intersection(edt.index)
    for rid in common_ids:
        row_o = orig.loc[rid]
        row_e = edt.loc[rid]
        changed = {}
        for k in ["src", "tgt", "ls", "lt", "source_name"]:
            if k in row_o and k in row_e:
                vo = ("" if pd.isna(row_o[k]) else row_o[k])
                ve = ("" if pd.isna(row_e[k]) else row_e[k])
                if vo != ve:
                    changed[k] = ve
        if changed:
            updates.append({"id": int(rid), **changed})
    return updates

# -----------------------------
# 侧边栏：检索条件
# -----------------------------
with st.sidebar:
    st.markdown("### 🔧 连接")
    st.code(f"API_BASE = {API_BASE}", language="bash")
    st.divider()
    st.markdown("### 🔎 检索条件")
    q = st.text_input("关键词 / 短语（必填）", value="协议")
    limit = st.slider("返回条数", 10, 200, 50)
    col_a, col_b = st.columns(2)
    with col_a:
        ls = st.selectbox("源语言(ls)", ["", "zh", "en"], index=1)
    with col_b:
        lt = st.selectbox("目标语言(lt)", ["", "en", "zh"], index=1)
    source_name = st.text_input("出处（可留空/多词请到 Bulk 页）", value="")
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input("起始日期", value=None)
    with col2:
        date_to = st.date_input("结束日期", value=None)
    btn_search = st.button("开始检索", use_container_width=True, type="primary")

# -----------------------------
# 主区：结果表 / 编辑 / 删除
# -----------------------------
st.title("🔍 翻译语料检索（API 模式）")

if "search_df" not in st.session_state:
    st.session_state.search_df = pd.DataFrame()

if btn_search:
    try:
        rows = client.search(
            q=q.strip(),
            ls=(ls or None) or None,
            lt=(lt or None) or None,
            source_names=[source_name] if source_name.strip() else None,
            limit=int(limit),
            date_from=str(date_from) if date_from else None,
            date_to=str(date_to) if date_to else None,
        )
        st.session_state.search_df = _normalize_rows(rows)
        if st.session_state.search_df.empty:
            st.info("没有命中结果。你可以放宽条件或更换关键词。")
    except ApiError as e:
        st.error(f"检索失败：{e}")

df = st.session_state.search_df.copy()

if not df.empty:
    st.caption("提示：双击单元格即可编辑；选中要删除的 ID 后点击下方按钮。")
    # 用 data_editor 支持就地编辑（仅允许可改列）
    editable_cols = ["src", "tgt", "ls", "lt", "source_name"]
    # 保证列顺序
    show_cols = ["id", "src", "tgt", "ls", "lt", "source_name", "created_at"]
    for c in show_cols:
        if c not in df.columns:
            df[c] = ""
    df = df[show_cols]

    edited = st.data_editor(
        df,
        column_config={
            "id": st.column_config.NumberColumn("id", disabled=True),
            "src": st.column_config.TextColumn("源文本"),
            "tgt": st.column_config.TextColumn("译文"),
            "ls": st.column_config.TextColumn("ls"),
            "lt": st.column_config.TextColumn("lt"),
            "source_name": st.column_config.TextColumn("出处"),
            "created_at": st.column_config.TextColumn("创建时间", disabled=True),
        },
        disabled=["id", "created_at"],
        use_container_width=True,
        key="editor",
        num_rows="fixed",
        height=min(600, 120 + 38 * min(len(df), 12)),
    )

    st.divider()
    colL, colR = st.columns([2, 1])
    with colL:
        if st.button("💾 保存编辑变更", type="primary"):
            updates = _diff_updates(df, edited)
            if not updates:
                st.success("没有检测到修改。")
            else:
                ok, fail = 0, 0
                for u in updates:
                    try:
                        rid = u.pop("id")
                        client.update_entry(rid, **u)
                        ok += 1
                    except ApiError as e:
                        fail += 1
                        st.error(f"更新失败（id={rid}）：{e}")
                st.success(f"更新完成：成功 {ok} 条，失败 {fail} 条。")
                # 刷新表格
                st.session_state.search_df = edited
    with colR:
        del_ids_str = st.text_input("🗑️ 需删除的 ID（逗号分隔）", "")
        if st.button("删除所填 ID"):
            ids = []
            for x in del_ids_str.split(","):
                x = x.strip()
                if x.isdigit():
                    ids.append(int(x))
            if not ids:
                st.warning("请填入要删除的数字 ID（支持多个，逗号分隔）。")
            else:
                ok, fail = 0, 0
                for rid in ids:
                    try:
                        client.delete_entry(rid)
                        ok += 1
                    except ApiError as e:
                        fail += 1
                        st.error(f"删除失败（id={rid}）：{e}")
                # 从当前表中移除
                if ok:
                    st.session_state.search_df = st.session_state.search_df[~st.session_state.search_df["id"].isin(ids)]
                st.success(f"删除完成：成功 {ok} 条，失败 {fail} 条。")

else:
    st.info("左侧设置条件后点击“开始检索”。")

# 页脚
st.caption(f"现在是 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · 已连接 API: {API_BASE}")
