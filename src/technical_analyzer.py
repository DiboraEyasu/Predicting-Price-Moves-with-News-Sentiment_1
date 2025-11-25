# src/technical_analyzer.py
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    """Handles technical indicator calculations."""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
        """Calculate Relative Strength Index.
        
        Args:
            prices: Series of closing prices
            window: Lookback period (default 14)
            
        Returns:
            Series of RSI values
        """
        deltas = prices.diff()
        gains = deltas.where(deltas > 0, 0)
        losses = -deltas.where(deltas < 0, 0)
        
        avg_gains = gains.rolling(window=window).mean()
        avg_losses = losses.rolling(window=window).mean()
        
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_sma(prices: pd.Series, window: int = 20) -> pd.Series:
        """Calculate Simple Moving Average."""
        return prices.rolling(window=window).mean()