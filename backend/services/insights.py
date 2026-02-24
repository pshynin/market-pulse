import os
import openai
import logging
from typing import Dict, Any, Optional

from db.models import SignalResult, AIInsight
from config import settings

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_market_insight(signal_result: SignalResult) -> AIInsight:
    """Generate market insights based on signal results using GPT-4

    Args:
        signal_result: The latest signal result with all indicators

    Returns:
        AIInsight object with generated content
    """
    if not settings.OPENAI_API_KEY:
        logger.warning(
            "OpenAI API key not configured. Using default insight message.")
        return AIInsight(
            content="AI insights not available. Please configure OpenAI API key.",
            signal_result_id=signal_result.id
        )

    try:
        # Create a context for GPT with the current signals
        prompt = create_insight_prompt(signal_result)

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a financial market analyst specializing in macro trends and market signals. "
                 "Your job is to provide concise, actionable insights about the current market conditions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )

        # Extract content from response
        insight_text = response.choices[0].message.content.strip()

        # Create and return AIInsight object
        return AIInsight(
            content=insight_text,
            signal_result_id=signal_result.id
        )

    except Exception as e:
        logger.error(f"Error generating insight with GPT: {str(e)}")
        return AIInsight(
            content=f"Error generating AI insight: {str(e)}",
            signal_result_id=signal_result.id
        )


def create_insight_prompt(signal_result: SignalResult) -> str:
    """Create a detailed prompt for the GPT model based on signal results"""
    signal_descriptions = {
        "market_breadth": {
            "Green": "Market breadth is healthy with broad participation across stocks.",
            "Yellow": "Market breadth is neutral, showing average participation across stocks.",
            "Red": "Market breadth is poor, indicating a narrow market with few stocks driving gains."
        },
        "valuation": {
            "Green": "Valuations are attractive relative to historical averages.",
            "Yellow": "Valuations are near historical averages.",
            "Red": "Valuations are significantly above historical averages, suggesting potential overvaluation."
        },
        "volatility": {
            "Green": "Volatility is low, indicating market complacency.",
            "Yellow": "Volatility is at normal levels.",
            "Red": "Volatility is elevated, suggesting market fear or uncertainty."
        },
        "liquidity": {
            "Green": "Liquidity conditions are supportive with expanding money supply.",
            "Yellow": "Liquidity conditions are neutral.",
            "Red": "Liquidity conditions are tightening with contracting money supply."
        },
        "macro": {
            "Green": "Economic indicators show strong growth.",
            "Yellow": "Economic indicators show moderate growth.",
            "Red": "Economic indicators show slowing growth or contraction."
        },
        "overall": {
            "Green": "Overall market conditions appear favorable for continued growth.",
            "Yellow": "Overall market conditions suggest caution with mixed signals.",
            "Red": "Overall market conditions suggest defensive positioning due to multiple warning signs."
        }
    }

    # Get the description for each signal
    market_breadth_desc = signal_descriptions["market_breadth"][signal_result.market_breadth_signal]
    valuation_desc = signal_descriptions["valuation"][signal_result.valuation_signal]
    volatility_desc = signal_descriptions["volatility"][signal_result.volatility_signal]
    liquidity_desc = signal_descriptions["liquidity"][signal_result.liquidity_signal]
    macro_desc = signal_descriptions["macro"][signal_result.macro_signal]
    overall_desc = signal_descriptions["overall"][signal_result.overall_signal]

    # Build the prompt
    prompt = f"""Based on the following market signals, provide a concise 1-paragraph analysis of current market conditions:

1. Market Breadth: {signal_result.market_breadth_signal} - {market_breadth_desc}
2. Valuations: {signal_result.valuation_signal} - {valuation_desc}
3. Volatility: {signal_result.volatility_signal} - {volatility_desc}
4. Liquidity: {signal_result.liquidity_signal} - {liquidity_desc}
5. Economic Indicators: {signal_result.macro_signal} - {macro_desc}

Overall Market Signal: {signal_result.overall_signal} - {overall_desc}

In your response:
1. Explain what these signals suggest about current market conditions
2. Identify key risks or opportunities
3. Suggest one potential action for investors to consider
4. Keep your response concise (around 100-150 words)"""

    return prompt
