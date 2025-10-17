import streamlit as st
from datetime import datetime, date
from repo import add_entry
from models import init_db
import re

init_db()
st.title("📝 快速录入 / Quick Add")

def _safe_add_entry(src, tgt, ls, lt, source_name, source_url, created_at_iso):
    try:
        return add_entry(src, tgt, ls, lt, source_name, source_url, created_at=created_at_iso)
    except TypeError:
        # 向后兼容旧版本 repo.add_entry
        return add_entry(src, tgt, ls, lt, source_name, source_url)

# 时间格式正则：HH:MM 或 HH:MM:SS
TIME_RE = re.compile(r"^\d{2}:\d{2}(:\d{2})?$")

with st.form("add"):
    src = st.text_area("原文 / Source", height=140)
    tgt = st.text_area("译文 / Target", height=140)

    c1, c2, c3 = st.columns(3)
    with c1:
        ls = st.selectbox("源语言", ["en", "zh"], index=0)   # 默认 en
    with c2:
        lt = st.selectbox("目标语言", ["zh", "en"], index=0) # 默认 zh
    with c3:
        source_name = st.text_input("来源名称")

    source_url = st.text_input("来源链接（可选）")

    # —— 时间属性 —— #
    with st.expander("时间属性 / Time Attributes"):
        use_now = st.checkbox("使用当前时间 / Use now", value=True)
        d = st.date_input("日期 / Date", value=date.today(), disabled=use_now)
        time_text = st.text_input(
            "时间 / Time (HH:MM 或 HH:MM:SS)",
            value=datetime.now().strftime("%H:%M:%S"),
            disabled=use_now
        )

    submitted = st.form_submit_button("保存 / Save")

    if submitted:
        if not src.strip() or not tgt.strip():
            st.error("原文和译文都需要填写 / Source and Target required.")
        else:
            if use_now:
                created_iso = datetime.now().replace(microsecond=0).isoformat(sep=" ")
            else:
                if not TIME_RE.match(time_text.strip()):
                    st.error("时间格式应为 HH:MM 或 HH:MM:SS")
                    st.stop()
                created_iso = f"{d.isoformat()} {time_text.strip()}"

            try:
                eid = _safe_add_entry(
                    src, tgt, ls, lt,
                    source_name or None, source_url or None,
                    created_iso
                )
                st.success(f"Saved entry #{eid}")
            except Exception as e:
                st.error(str(e))
