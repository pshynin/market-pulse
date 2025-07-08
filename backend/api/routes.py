from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import datetime

from db.session import get_db
from db.models import MarketData, SignalResult, AIInsight
from services.signals import process_signals
from services.insights import generate_market_insight
from api.models import SignalResponse, InsightResponse

router = APIRouter()

@router.get("/signals/current", response_model=SignalResponse)
async def get_current_signals(db: Session = Depends(get_db)):
    """Get the most recent market signals"""
    latest_signals = db.query(SignalResult).order_by(SignalResult.timestamp.desc()).first()
    
    if not latest_signals:
        raise HTTPException(status_code=404, detail="No signals available")
        
    return latest_signals

@router.get("/signals/history")
async def get_signal_history(
    days: int = Query(30, description="Number of days of history"),
    db: Session = Depends(get_db)
):
    """Get historical signals for the specified number of days"""
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    
    signal_history = (
        db.query(SignalResult)
        .filter(SignalResult.timestamp >= cutoff_date)
        .order_by(SignalResult.timestamp.asc())
        .all()
    )
    
    return signal_history

@router.get("/insights/current", response_model=InsightResponse)
async def get_current_insight(db: Session = Depends(get_db)):
    """Get the most recent AI market insight"""
    latest_insight = db.query(AIInsight).order_by(AIInsight.timestamp.desc()).first()
    
    if not latest_insight:
        raise HTTPException(status_code=404, detail="No insights available")
        
    return latest_insight

@router.post("/signals/refresh")
async def refresh_signals(db: Session = Depends(get_db)):
    """Manually trigger a refresh of market signals"""
    # Get latest market data
    latest_market_data = db.query(MarketData).order_by(MarketData.timestamp.desc()).first()
    
    if not latest_market_data:
        raise HTTPException(status_code=404, detail="No market data available")
    
    # Process signals based on latest data
    signal_result = process_signals(latest_market_data)
    db.add(signal_result)
    db.commit()
    db.refresh(signal_result)
    
    # Generate insight
    insight = generate_market_insight(signal_result)
    db.add(insight)
    db.commit()
    
    return {"message": "Signals refreshed successfully", "signal_id": signal_result.id}
