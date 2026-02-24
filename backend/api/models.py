from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SignalResponse(BaseModel):
    id: int
    timestamp: datetime
    market_breadth_signal: str
    valuation_signal: str
    volatility_signal: str
    liquidity_signal: str
    macro_signal: str
    overall_signal: str
    market_data_id: int

    class Config:
        orm_mode = True


class InsightResponse(BaseModel):
    id: int
    timestamp: datetime
    content: str
    signal_result_id: int

    class Config:
        orm_mode = True


class MarketDataResponse(BaseModel):
    id: int
    timestamp: datetime
    spy_price: float
    rsp_price: float
    vix_value: float
    pe_ratio: float
    eps_value: float
    m2_supply: Optional[float] = None
    fed_balance: Optional[float] = None
    gdp_value: Optional[float] = None
    ism_value: Optional[float] = None

    class Config:
        orm_mode = True
