# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi

from .database import engine
from .models import Base
from .routers import auth, entries, sources

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wordloom API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(sources.router)

@app.get("/healthz")
def healthz():
    return {"ok": True}


# === 👇 新增这一段 ===
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Wordloom API",
        version="0.2.0",
        description="Wordloom 后端接口文档",
        routes=app.routes,
    )
    # 定义一个 Bearer Token 认证
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
# === 👆 新增结束 ===

from pathlib import Path
from fastapi import FastAPI

def read_version():
    # 优先读后端自己的 VERSION，读不到就回退到仓库根
    here = Path(__file__).resolve()
    backend_ver = here.parents[1] / "VERSION"              # WordloomBackend/api/VERSION
    root_ver    = here.parents[4] / "VERSION"              # Wordloom/VERSION
    vf = backend_ver if backend_ver.exists() else root_ver
    try:
        return vf.read_text(encoding="utf-8").strip()
    except Exception:
        return "unknown"

app = FastAPI(
    title="Wordloom API",
    version=read_version(),   # Swagger 右上角显示
)

@app.get("/version")
def get_version():
    return {
        "backend": read_version()
    }
