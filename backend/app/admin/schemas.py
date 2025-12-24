from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OilReadingBase(BaseModel):
    id: Optional[str] = Field(None, description="ID")
    oil_Model: Optional[str] = Field(None, description="오일 모델명")
    viscosity: Optional[float] = Field(None, description="점도")
    tbn: Optional[float] = Field(None, description="TBN")
    acid_number: Optional[float] = Field(None, description="산가 (AN)")
    wear_fe: Optional[float] = Field(None, description="Fe (철)")
    wear_cu: Optional[float] = Field(None, description="Cu (구리)")
    wear_al: Optional[float] = Field(None, description="Al (알루미늄)")
    fuel_dilution: Optional[float] = Field(None, description="연료 희석 (%)")
    soot: Optional[float] = Field(None, description="그을음 (ppm)")
    mileage: Optional[int] = Field(None, description="마일수")
    notes: Optional[str] = Field(None, description="비고")

class OilReadingCreate(OilReadingBase):
    pass

class OilReadingOut(OilReadingBase):
    id: str
    timestamp: datetime 
    has_analysis: bool = False

    class Config:
        orm_mode = True

class AnalysisResultOut(BaseModel):
    id: int
    reading_id: str
    scores: dict
    reference_scores: dict
    explanation: str
    created_at: datetime

    class Config:
        orm_mode = True