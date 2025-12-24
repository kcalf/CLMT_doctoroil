from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Float
from sqlalchemy.sql import func
from app.admin.database import Base

class OilReading(Base):
    __tablename__ = "oil_readings"

    id = Column(String, primary_key=True, index=True)
    oil_Model = Column(String, nullable=True)

    # 측정/입력한 날짜/시각 (서버측 자동 저장)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # 측정 항목
    viscosity = Column(Float, nullable=True)        # 점도 (Viscosity)
    tbn = Column(Float, nullable=True)              # TBN (Total Base Number)
    acid_number = Column(Float, nullable=True)      # 산가 (AN, Acid Number)

    # 마모 금속 입자 (Fe, Cu, Al)
    wear_fe = Column(Float, nullable=True)          # Fe (철)
    wear_cu = Column(Float, nullable=True)          # Cu (구리)
    wear_al = Column(Float, nullable=True)          # Al (알루미늄)

    # 불순물
    fuel_dilution = Column(Float, nullable=True)    # 연료 희석 (Fuel Dilution) - % 등
    soot = Column(Float, nullable=True)             # 그을음 (Soot) - ppm 등

    mileage = Column(Integer, nullable=True)        # 마일수 (주행거리)
    
    notes = Column(String(512), nullable=True)      # 비고(선택)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    reading_id = Column(String, ForeignKey("oil_readings.id"), index=True)

    scores = Column(JSON, nullable=False)
    reference_scores = Column(JSON, nullable=False)
    explanation = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())