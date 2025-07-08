from db.models import MarketData, SignalResult

def process_signals(market_data: MarketData) -> SignalResult:
    """Process market data into signal indicators (Green/Yellow/Red)
    
    This function implements the core business logic for signal processing.
    Each of the 5 key signals is calculated based on thresholds and market data.
    """
    # Create new signal result
    signal_result = SignalResult(
        market_data_id=market_data.id,
        market_breadth_signal=calculate_market_breadth_signal(market_data),
        valuation_signal=calculate_valuation_signal(market_data),
        volatility_signal=calculate_volatility_signal(market_data),
        liquidity_signal=calculate_liquidity_signal(market_data),
        macro_signal=calculate_macro_signal(market_data),
        overall_signal="Green"  # Default, will be updated
    )
    
    # Calculate overall signal based on individual signals
    signal_result.overall_signal = calculate_overall_signal(signal_result)
    
    return signal_result

def calculate_market_breadth_signal(market_data: MarketData) -> str:
    """Calculate market breadth signal based on SPY vs RSP
    
    Green: RSP outperforming SPY (broader market participation)
    Yellow: RSP and SPY similar performance
    Red: SPY outperforming RSP (narrow market)
    """
    # Calculate relative performance ratio
    # Higher values indicate broader market participation
    if not market_data.spy_price or not market_data.rsp_price:
        return "Yellow"  # Default if data missing
    
    rsp_spy_ratio = market_data.rsp_price / market_data.spy_price
    
    # These thresholds would need to be calibrated based on historical data
    if rsp_spy_ratio > 1.05:  # RSP outperforming by 5%+
        return "Green"
    elif rsp_spy_ratio < 0.95:  # RSP underperforming by 5%+
        return "Red"
    else:
        return "Yellow"

def calculate_valuation_signal(market_data: MarketData) -> str:
    """Calculate valuation signal based on P/E ratio vs historical norms
    
    Green: P/E below historical average
    Yellow: P/E near historical average
    Red: P/E significantly above historical average
    """
    # Historical S&P 500 average P/E is around 15-16
    if not market_data.pe_ratio:
        return "Yellow"  # Default if data missing
    
    if market_data.pe_ratio < 18:
        return "Green"  # Undervalued
    elif market_data.pe_ratio > 25:
        return "Red"    # Overvalued
    else:
        return "Yellow"  # Fair value

def calculate_volatility_signal(market_data: MarketData) -> str:
    """Calculate volatility signal based on VIX levels
    
    Green: Low volatility (VIX < 15)
    Yellow: Normal volatility (VIX 15-25)
    Red: High volatility (VIX > 25)
    """
    if not market_data.vix_value:
        return "Yellow"  # Default if data missing
    
    if market_data.vix_value < 15:
        return "Green"   # Low volatility, complacent market
    elif market_data.vix_value > 25:
        return "Red"     # High volatility, fearful market
    else:
        return "Yellow"  # Normal volatility

def calculate_liquidity_signal(market_data: MarketData) -> str:
    """Calculate liquidity signal based on M2 money supply and Fed balance sheet
    
    Green: Expanding liquidity
    Yellow: Stable liquidity
    Red: Contracting liquidity
    """
    # This would ideally compare current values to 3-month or 6-month trend
    # For now, using simplified placeholder logic
    if not market_data.m2_supply or not market_data.fed_balance:
        return "Yellow"  # Default if data missing
    
    # This is placeholder logic - in reality you'd compare to previous periods
    # to determine if liquidity is expanding, contracting, or stable
    if market_data.fed_balance > 8000:  # Placeholder value in billions
        return "Green"
    elif market_data.fed_balance < 7000:  # Placeholder value in billions
        return "Red"
    else:
        return "Yellow"

def calculate_macro_signal(market_data: MarketData) -> str:
    """Calculate macro signal based on GDP growth and ISM manufacturing
    
    Green: Strong GDP growth and ISM > 50
    Yellow: Moderate GDP growth or ISM near 50
    Red: GDP contraction or ISM < 45
    """
    if not market_data.gdp_value or not market_data.ism_value:
        return "Yellow"  # Default if data missing
    
    # GDP annual growth rate
    gdp_signal = "Yellow"
    if market_data.gdp_value > 2.5:
        gdp_signal = "Green"
    elif market_data.gdp_value < 1.0:
        gdp_signal = "Red"
    
    # ISM manufacturing index (above 50 = expansion, below 50 = contraction)
    ism_signal = "Yellow"
    if market_data.ism_value > 53:
        ism_signal = "Green"
    elif market_data.ism_value < 47:
        ism_signal = "Red"
    
    # Combine GDP and ISM signals
    if gdp_signal == "Red" or ism_signal == "Red":
        return "Red"
    elif gdp_signal == "Green" and ism_signal == "Green":
        return "Green"
    else:
        return "Yellow"

def calculate_overall_signal(signal_result: SignalResult) -> str:
    """Calculate overall market signal based on individual signals
    
    Rules:
    - If 3+ signals are Red: Overall is Red
    - If 3+ signals are Green AND no more than 1 is Red: Overall is Green
    - Otherwise: Yellow
    """
    signals = [
        signal_result.market_breadth_signal,
        signal_result.valuation_signal,
        signal_result.volatility_signal,
        signal_result.liquidity_signal,
        signal_result.macro_signal
    ]
    
    red_count = signals.count("Red")
    green_count = signals.count("Green")
    
    if red_count >= 3:
        return "Red"
    elif green_count >= 3 and red_count <= 1:
        return "Green"
    else:
        return "Yellow"
