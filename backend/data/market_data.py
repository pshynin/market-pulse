import requests
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from config import settings
from db.models import MarketData
from db.session import SessionLocal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketDataCollector:
    """Collects market data from various financial APIs"""

    def __init__(self):
        self.alpha_vantage_key = settings.ALPHA_VANTAGE_API_KEY
        self.finnhub_key = settings.FINNHUB_API_KEY

    def collect_all_data(self) -> Optional[MarketData]:
        """Collect all market data and save to database"""
        try:
            # Collect stock price data
            spy_price = self.get_stock_price("SPY")
            rsp_price = self.get_stock_price("RSP")
            vix_value = self.get_vix_value()
            pe_ratio, eps_value = self.get_pe_ratio_and_eps()
            m2_supply, fed_balance = self.get_liquidity_metrics()
            gdp_value, ism_value = self.get_economic_indicators()

            # Create raw data object
            raw_data = {
                "spy": spy_price,
                "rsp": rsp_price,
                "vix": vix_value,
                "pe_ratio": pe_ratio,
                "eps": eps_value,
                "m2_supply": m2_supply,
                "fed_balance": fed_balance,
                "gdp": gdp_value,
                "ism": ism_value,
                "collected_at": datetime.utcnow().isoformat()
            }

            # Create market data record
            market_data = MarketData(
                spy_price=spy_price,
                rsp_price=rsp_price,
                vix_value=vix_value,
                pe_ratio=pe_ratio,
                eps_value=eps_value,
                m2_supply=m2_supply,
                fed_balance=fed_balance,
                gdp_value=gdp_value,
                ism_value=ism_value,
                raw_data=raw_data
            )

            # Save to database
            with SessionLocal() as db:
                db.add(market_data)
                db.commit()
                db.refresh(market_data)

            logger.info(
                f"Market data collected and saved (ID: {
                    market_data.id})")
            return market_data

        except Exception as e:
            logger.error(f"Error collecting market data: {str(e)}")
            return None

    def get_stock_price(self, symbol: str) -> float:
        """Get current price for a stock symbol"""
        if not self.alpha_vantage_key:
            logger.warning(
                f"Alpha Vantage API key not set. Using sample data for {symbol}.")
            # Sample data for testing
            sample_prices = {"SPY": 475.23, "RSP": 152.87}
            return sample_prices.get(symbol, 100.0)

        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={
                self.alpha_vantage_key}"
            response = requests.get(url)
            data = response.json()

            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                logger.warning(
                    f"Could not fetch price for {symbol}. Using sample data.")
                sample_prices = {"SPY": 475.23, "RSP": 152.87}
                return sample_prices.get(symbol, 100.0)

        except Exception as e:
            logger.error(f"Error fetching {symbol} price: {str(e)}")
            sample_prices = {"SPY": 475.23, "RSP": 152.87}
            return sample_prices.get(symbol, 100.0)

    def get_vix_value(self) -> float:
        """Get current VIX (volatility index) value"""
        # In a real implementation, you'd fetch this from a market data provider
        # For this example, using sample data
        try:
            if self.alpha_vantage_key:
                # Could use Alpha Vantage to get VIX data, but using sample for
                # now
                return 18.5  # Sample VIX value
            else:
                return 18.5  # Sample VIX value
        except Exception as e:
            logger.error(f"Error fetching VIX: {str(e)}")
            return 18.5  # Default sample value

    def get_pe_ratio_and_eps(self) -> Tuple[float, float]:
        """Get current P/E ratio and EPS for S&P 500"""
        # In a real implementation, you'd fetch this from a financial data provider
        # For this example, using sample data
        try:
            return 22.5, 215.43  # Sample P/E ratio and EPS
        except Exception as e:
            logger.error(f"Error fetching P/E and EPS: {str(e)}")
            return 22.5, 215.43  # Default sample values

    def get_liquidity_metrics(self) -> Tuple[float, float]:
        """Get current M2 money supply and Fed balance sheet"""
        # In a real implementation, you'd fetch this from FRED or similar
        # For this example, using sample data
        try:
            # Sample M2 supply (billions) and Fed balance sheet (billions)
            return 21500.0, 7500.0
        except Exception as e:
            logger.error(f"Error fetching liquidity metrics: {str(e)}")
            return 21500.0, 7500.0  # Default sample values

    def get_economic_indicators(self) -> Tuple[float, float]:
        """Get current GDP growth rate and ISM manufacturing index"""
        # In a real implementation, you'd fetch this from economic data providers
        # For this example, using sample data
        try:
            return 2.1, 48.5  # Sample GDP growth (%) and ISM index
        except Exception as e:
            logger.error(f"Error fetching economic indicators: {str(e)}")
            return 2.1, 48.5  # Default sample values

# Function to run data collection as a scheduled job


def collect_market_data() -> Optional[MarketData]:
    """Run market data collection as a scheduled job"""
    collector = MarketDataCollector()
    return collector.collect_all_data()


# For testing/debugging
if __name__ == "__main__":
    collect_market_data()
