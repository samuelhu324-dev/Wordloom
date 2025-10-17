# -*- coding: utf-8 -*-
"""
wordloom_api/app/routers/entries.py
相对导入版（非破坏式微调）：
- 仅使用包内相对导入（..repo / ..database / ..schemas / ..models）
- 路由前缀保持不变：/entries
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import select, desc

from ..schemas import EntryCreate, EntryOut
from ..database import get_db
from .auth import get_current_token
from ..repo import upsert_entry
from ..models import Entry, Source  # ORM 模型

router = APIRouter(prefix="/entries", tags=["entries"])


@router.post("", response_model=EntryOut, dependencies=[Depends(get_current_token)])
def create_entry(body: EntryCreate, db: Session = Depends(get_db)):
    """
    新建/写入一条记录，然后立即查询并返回规范化的输出模型。
    """
    try:
        new_id = upsert_entry(
            entry_id=None,
            src=body.src,
            tgt=body.tgt or "",
            ls=body.ls,
            lt=body.lt,
            source_name=body.source_name,
            source_url=body.source_url,
            created_at=body.created_at,
        )
    except Exception as e:
        # 把底层异常透传为 400，便于前端显示
        raise HTTPException(status_code=400, detail=str(e))

    row = db.execute(
        select(Entry, Source.name).join(Source, isouter=True).where(Entry.id == new_id)
    ).first()

    if not row:
        raise HTTPException(status_code=404, detail="entry not found after insert")

    e, sname = row[0], row[1]
    return EntryOut(
        id=e.id,
        src_text=e.src_text,
        tgt_text=e.tgt_text,
        lang_src=e.lang_src,
        lang_tgt=e.lang_tgt,
        created_at=e.created_at,
        source_name=sname,
    )


@router.get("/recent", response_model=List[EntryOut], dependencies=[Depends(get_current_token)])
def recent(limit: int = 20, db: Session = Depends(get_db)):
    """
    按创建时间倒序返回最近的若干条记录（1~100 之间）。
    """
    limit = max(1, min(100, limit))

    rows = db.execute(
        select(Entry, Source.name)
        .join(Source, isouter=True)
        .order_by(desc(Entry.created_at))
        .limit(limit)
    ).all()

    out: List[EntryOut] = []
    for row in rows:
        e, sname = row[0], row[1]
        out.append(
            EntryOut(
                id=e.id,
                src_text=e.src_text,
                tgt_text=e.tgt_text,
                lang_src=e.lang_src,
                lang_tgt=e.lang_tgt,
                created_at=e.created_at,
                source_name=sname,
            )
        )
    return out
