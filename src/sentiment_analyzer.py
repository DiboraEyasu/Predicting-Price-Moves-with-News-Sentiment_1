# src/sentiment_analyzer.py
from textblob import TextBlob
import pandas as pd

class SentimentAnalyzer:
    """Handles text sentiment analysis."""
    
    @staticmethod
    def get_sentiment_score(text: str) -> float:
        """Calculate sentiment polarity.
        
        Args:
            text: Input text to analyze
            
        Returns:
            float: Sentiment score between -1 (negative) and 1 (positive)
        """
        if pd.isna(text) or not str(text).strip():
            return 0.0
        return TextBlob(str(text)).sentiment.polarity
    
    def analyze_news_sentiment(self, headlines: pd.Series) -> pd.Series:
        """Batch process sentiment for news headlines."""
        return headlines.apply(self.get_sentiment_score)