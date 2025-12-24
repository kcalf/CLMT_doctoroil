from sqlalchemy.future import select
from app.admin.models import OilReading, AnalysisResult
from app.admin.schemas import OilReadingCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, delete
from typing import List, Optional
from datetime import date, datetime, timedelta
from sqlalchemy import desc

async def create_reading(db: AsyncSession, reading: OilReadingCreate) -> OilReading:
    obj = OilReading(**reading.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_reading_by_id(
    db: AsyncSession,
    reading_id: str
) -> OilReading | None:

    q = (
        select(
            OilReading,
            exists().where(
                AnalysisResult.reading_id == OilReading.id
            ).label("has_analysis")
        )
        .where(OilReading.id == reading_id)
    )

    result = await db.execute(q)
    row = result.first()

    if not row:
        return None

    reading, has_analysis = row
    reading.has_analysis = has_analysis
    return reading

async def get_readings_by_date(db: AsyncSession, target_date: date) -> List[OilReading]:
    start = datetime.combine(target_date, datetime.min.time())
    end = start + timedelta(days=1)

    q = (
        select(
            OilReading,
            exists().where(
                AnalysisResult.reading_id == OilReading.id
            ).label("has_analysis")
        )
        .where(
            OilReading.timestamp >= start,
            OilReading.timestamp < end
        )
        .order_by(OilReading.timestamp.desc())
    )

    result = await db.execute(q)
    rows = result.all()

    items = []
    for reading, has_analysis in rows:
        reading.has_analysis = has_analysis  
        items.append(reading)

    return items

async def get_all_readings(db: AsyncSession, limit: Optional[int] = None) -> List[OilReading]:
    q = (
        select(
            OilReading,
            exists().where(
                AnalysisResult.reading_id == OilReading.id
            ).label("has_analysis")
        )
        .order_by(OilReading.timestamp.desc())
    )

    if limit:
        q = q.limit(limit)

    result = await db.execute(q)
    rows = result.all()

    items = []
    for reading, has_analysis in rows:
        reading.has_analysis = has_analysis  # 🔥 핵심
        items.append(reading)

    return items

async def create_analysis_result(
    db: AsyncSession,
    reading_id: str,
    result: dict
) -> AnalysisResult:
    obj = AnalysisResult(
        reading_id=reading_id,
        scores=result["scores"],
        reference_scores=result["reference_scores"],
        explanation=result["explanation"]
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_analysis_result_by_reading_id(
    db: AsyncSession,
    reading_id: str
) -> AnalysisResult | None:
    q = (
        select(AnalysisResult)
        .where(AnalysisResult.reading_id == reading_id)
        .order_by(desc(AnalysisResult.created_at))  
        .limit(1)
    )
    result = await db.execute(q)
    return result.scalars().first()

async def update_reading(
    db: AsyncSession,
    reading_id: str,
    reading: OilReadingCreate
) -> OilReading | None:

    result = await db.execute(
        select(OilReading).where(OilReading.id == reading_id)
    )
    obj = result.scalars().first()

    if not obj:
        return None

    for field, value in reading.dict(exclude={"id"}, exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)

    return obj