from pydantic import BaseModel, Field
from typing import Dict

class AnalysisRequest(BaseModel):
    oil_Model: str = Field(..., description="oil Model")
    viscosity: float = Field(..., description="점도 (예: cSt 등)")
    tbn: float = Field(..., description="TBN 값")
    an: float = Field(..., description="산가(AN)")
    fe: float = Field(..., description="금속 마모 입자 Fe (ppm)")
    cu: float = Field(..., description="금속 마모 입자 Cu (ppm)")
    al: float = Field(..., description="금속 마모 입자 Al (ppm)")
    fuel_dilution: float = Field(..., description="Fuel Dilution (%)")
    soot: float = Field(..., description="Soot (%)")
    mileage: int = Field(..., description="주행거리 (km)")

class AnalysisResult(BaseModel):
    scores: Dict[str, float]  # keys: viscosity, contamination, wear, an, tbn  (0-100)
    reference_scores: Dict[str,float]
    explanation: str          # 한국어 상세 해설