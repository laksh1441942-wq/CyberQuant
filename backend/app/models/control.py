from sqlalchemy import Column, Integer, String, Float
from backend.app.database import Base

class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    control_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    cost_inr = Column(Float, nullable=False)
    risk_reduction_inr = Column(Float, nullable=False)
    frameworks = Column(String(500), nullable=True)  # Comma-separated or JSON tags
