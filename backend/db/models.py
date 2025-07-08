from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    spy_price = Column(Float)
    rsp_price = Column(Float)
    vix_value = Column(Float)
    pe_ratio = Column(Float)
    eps_value = Column(Float)
    m2_supply = Column(Float, nullable=True)
    fed_balance = Column(Float, nullable=True)
    gdp_value = Column(Float, nullable=True)
    ism_value = Column(Float, nullable=True)
    raw_data = Column(JSON, nullable=True)  # Store raw API response

class SignalResult(Base):
    __tablename__ = "signal_results"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    market_breadth_signal = Column(String(10))  # Green, Yellow, Red
    valuation_signal = Column(String(10))
    volatility_signal = Column(String(10))
    liquidity_signal = Column(String(10))
    macro_signal = Column(String(10))
    overall_signal = Column(String(10))
    market_data_id = Column(Integer, ForeignKey("market_data.id"))
    
    market_data = relationship("MarketData")

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    content = Column(Text)
    signal_result_id = Column(Integer, ForeignKey("signal_results.id"))
    
    signal_result = relationship("SignalResult")
