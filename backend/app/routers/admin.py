from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.admin import crud, schemas
from app.admin.database import get_db

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("app/static/index.html")

@router.post("/api/readings", response_model=schemas.OilReadingOut)
async def create_reading(
    reading: schemas.OilReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_reading(db, reading)

@router.get("/api/readings/by-date", response_model=list[schemas.OilReadingOut])
async def readings_by_date(
    date: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="YYYY-MM-DD 형식 필요")

    return await crud.get_readings_by_date(db, target_date)

@router.get("/api/readings/all", response_model=list[schemas.OilReadingOut])
async def get_all_readings(
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_readings(db, limit=None)

@router.get("/analysis/{reading_id}", response_class=HTMLResponse)
async def analysis_page(reading_id: str):
    return FileResponse("app/static/analysis_result.html")

@router.get("/api/analysis/{reading_id}", response_model=schemas.AnalysisResultOut)
async def get_analysis_result(
    reading_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await crud.get_analysis_result_by_reading_id(db, reading_id)
    if not result:
        raise HTTPException(status_code=404, detail="분석 결과 없음")
    return result

@router.put("/api/readings/{reading_id}", response_model=schemas.OilReadingOut)
async def update_reading(
    reading_id: str,
    reading: schemas.OilReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_reading(db, reading_id, reading)
    if not updated:
        raise HTTPException(status_code=404, detail="존재하지 않음")
    return updated

@router.get(
    "/api/readings/{reading_id}",
    response_model=schemas.OilReadingOut
)
async def get_reading(
    reading_id: str,
    db: AsyncSession = Depends(get_db)
):
    reading = await crud.get_reading_by_id(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="존재하지 않음")
    return reading