from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.admin.database import engine, Base
from app.routers import admin, analyzer


app = FastAPI(
    title="DoctorOil Admin + Analyzer",
    version="1.0"
)

# 정적 파일 (관리자 웹)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# 라우터 등록
app.include_router(
    admin.router,
    prefix="",
    tags=["Admin"]
)

app.include_router(
    analyzer.router,
    prefix="/analyze",
    tags=["Analyzer"]
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
