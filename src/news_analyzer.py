# src/news_analyzer.py
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any

class NewsAnalyzer:
    """
    Analyzes financial news data for sentiment and correlations.
    
    Args:
        data_path (str): Path to the CSV file containing news data
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None  # Consistent scoping
        self._load_data()  # Auto-load on init
    
    def _load_data(self) -> bool:
        """Load and validate dataset.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.df = pd.read_csv(self.data_path, parse_dates=['date'])
            print(f"✅ Loaded {len(self.df)} records")
            return True
        except Exception as e:
            print(f"❌ Load failed: {e}")
            return False
    
    
    def perform_eda(self) -> Dict[str, Any]:
        """Perform exploratory data analysis.
        
        Returns:
            Dictionary containing EDA results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call _load_data() first.")
        
        results = {}
        
        # 1. Headline analysis
        if 'headline' in self.df.columns:
            self.df['headline_length'] = self.df['headline'].str.len().fillna(0)
            results['headline_stats'] = self.df['headline_length'].describe().to_dict()
        
        # 2. Time series analysis
        if 'date' in self.df.columns:
            daily_count = self.df.resample('D', on='date').size()
            results['daily_articles'] = len(daily_count)
            results['date_range'] = {
                'start': self.df['date'].min().strftime('%Y-%m-%d'),
                'end': self.df['date'].max().strftime('%Y-%m-%d')
            }
        
        # 3. Publisher analysis
        if 'publisher' in self.df.columns:
            results['top_publishers'] = self.df['publisher'].value_counts().head(5).to_dict()
        
        return results 
    # In NewsAnalyzer class
    def sentiment_correlation_pipeline(self, price_data: pd.Series) -> Dict[str, float]:
        """Run sentiment correlation analysis.
        
        Args:
            price_data: Series of stock prices/returns
            
        Returns:
            Dictionary with correlation results
        """
        # 1. Calculate sentiment
        sentiment_analyzer = SentimentAnalyzer()
        self.df['sentiment'] = sentiment_analyzer.analyze_news_sentiment(self.df['headline'])
        
        # 2. Align with price data (simplified)
        self.df['price_return'] = price_data.pct_change()  # Mock - replace with real data
        
        # 3. Calculate correlation
        correlation = self.df['sentiment'].corr(self.df['price_return'])
        
        return {
            'sentiment_correlation': correlation,
            'sentiment_mean': self.df['sentiment'].mean(),
            'valid_records': len(self.df.dropna())
        }