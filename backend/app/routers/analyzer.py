from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.analyzer.schema import AnalysisRequest, AnalysisResult as LLMResult
from app.analyzer.llm_client import call_gpt4_1
from app.admin.database import get_db
from app.admin import crud as admin_crud

router = APIRouter()

@router.post("/api/analyze")
async def analyze(
    payload: AnalysisRequest,
    reading_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        llm_resp = call_gpt4_1(payload.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    result = LLMResult(**llm_resp)

    analysis = await admin_crud.create_analysis_result(
        db,
        reading_id=reading_id,
        result=result.dict()
    )

    return {
        "analysis_id": analysis.id,
        "reading_id": reading_id
    }

@router.get("/api/analysis/{reading_id}")
async def get_analysis_result(
    reading_id: str,
    db: AsyncSession = Depends(get_db)
):
    analysis = await admin_crud.get_analysis_result_by_reading_id(
        db, reading_id
    )

    if not analysis:
        raise HTTPException(status_code=404, detail="분석 결과 없음")

    return {
        "reading_id": analysis.reading_id,
        "scores": analysis.scores,
        "reference_scores": analysis.reference_scores,
        "explanation": analysis.explanation,
        "created_at": analysis.created_at,
    }