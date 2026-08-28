from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.app.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    asset_id = Column(String(50), unique=True, index=True, nullable=False)
    asset_name = Column(String(200), nullable=False)
    asset_type = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    business_criticality = Column(String(50), nullable=False)
    asset_value_inr = Column(Float, nullable=False)
    is_internet_exposed = Column(Boolean, default=False)
    downtime_cost_per_hour_inr = Column(Float, default=20000.0)
    mfa_enabled = Column(Boolean, default=False)
    edr_installed = Column(Boolean, default=False)
