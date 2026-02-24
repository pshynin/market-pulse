from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
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
    latest_signals = db.query(SignalResult).order_by(
        SignalResult.timestamp.desc()).first()

    if not latest_signals:
        raise HTTPException(status_code=404, detail="No signals available")

    return latest_signals


@router.get("/signals/history")
async def get_signal_history(
    days: int = Query(7, description="Number of days of history"),
    include_raw_data: bool = Query(
        False, description="Include raw market data for each signal"),
    db: Session = Depends(get_db)
):
    """Get historical signals with trend analysis for the specified number of days"""
    cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    # Get signal history with related market data
    query = (
        db.query(SignalResult)
        .options(joinedload(SignalResult.market_data))
        .filter(SignalResult.timestamp >= cutoff_date)
        .order_by(SignalResult.timestamp.asc())
    )

    signal_history = query.all()

    if not signal_history:
        return {"signals": [], "trends": {}, "raw_data": {}}

    # Calculate trends for each signal type
    trends = calculate_signal_trends(signal_history)

    # Build response structure
    result = {
        "signals": signal_history,
        "trends": trends,
    }

    # Include raw data if requested
    if include_raw_data:
        raw_data = {}
        for day in signal_history:
            date_str = day.timestamp.strftime("%Y-%m-%d")
            raw_data[date_str] = {
                "spy_price": day.market_data.spy_price,
                "rsp_price": day.market_data.rsp_price,
                "spy_rsp_ratio": day.market_data.spy_price / day.market_data.rsp_price if day.market_data.rsp_price else None,
                "vix_value": day.market_data.vix_value,
                "pe_ratio": day.market_data.pe_ratio,
                "eps_value": day.market_data.eps_value,
                "m2_supply": day.market_data.m2_supply,
                "fed_balance": day.market_data.fed_balance,
                "gdp_value": day.market_data.gdp_value,
                "ism_value": day.market_data.ism_value,
            }
        result["raw_data"] = raw_data

    return result


def calculate_signal_trends(signal_history):
    """Calculate trends for each signal type.

    Converts Green/Yellow/Red to numeric values for trend calculation.
    Returns a dict with slope values for each signal type.
    """
    if not signal_history or len(signal_history) < 2:
        return {}

    # Signal types to analyze
    signal_types = [
        "market_breadth_signal",
        "valuation_signal",
        "volatility_signal",
        "liquidity_signal",
        "macro_signal",
        "overall_signal"
    ]

    trends = {}

    # Calculate trend for each signal type
    for signal_type in signal_types:
        values = []
        for day in signal_history:
            signal_value = getattr(day, signal_type)
            # Convert signal to numeric value
            if signal_value == "Green":
                values.append(1.0)
            elif signal_value == "Yellow":
                values.append(0.0)
            else:  # Red
                values.append(-1.0)

        # Calculate slope using simple linear regression
        if len(values) > 1:
            x = list(range(len(values)))
            # Use numpy for linear regression
            try:
                import numpy as np
                from scipy import stats
                slope, _, _, _, _ = stats.linregress(x, values)
                trends[signal_type] = round(slope, 2)
            except ImportError:
                # Fallback if scipy not available
                n = len(x)
                x_mean = sum(x) / n
                y_mean = sum(values) / n
                numerator = sum((x[i] - x_mean) * (values[i] - y_mean)
                                for i in range(n))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
                slope = numerator / denominator if denominator else 0
                trends[signal_type] = round(slope, 2)

    return trends


@router.get("/insights/current", response_model=InsightResponse)
async def get_current_insight(db: Session = Depends(get_db)):
    """Get the most recent AI market insight"""
    latest_insight = db.query(AIInsight).order_by(
        AIInsight.timestamp.desc()).first()

    if not latest_insight:
        raise HTTPException(status_code=404, detail="No insights available")

    return latest_insight


@router.post("/signals/refresh")
async def refresh_signals(db: Session = Depends(get_db)):
    """Manually trigger a refresh of market signals"""
    # Get latest market data
    latest_market_data = db.query(MarketData).order_by(
        MarketData.timestamp.desc()).first()

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

    return {"message": "Signals refreshed successfully",
            "signal_id": signal_result.id}
