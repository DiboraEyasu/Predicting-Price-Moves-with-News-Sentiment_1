# tests/test_news_analyzer.py
import unittest
import pandas as pd
import sys
import os
sys.path.append('../src')

from src.news_analyzer import NewsAnalyzer
from src.technical_analyzer import TechnicalAnalyzer
from src.sentiment_analyzer import SentimentAnalyzer

class TestNewsAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Create mock data for testing."""
        self.mock_data = pd.DataFrame({
            'headline': ['Great earnings report!', 'Market crash expected', 'Neutral news'],
            'date': pd.date_range('2024-01-01', periods=3),
            'publisher': ['Reuters', 'Bloomberg', 'CNBC']
        })
        self.mock_data.to_csv('test_data.csv', index=False)
        self.analyzer = NewsAnalyzer('test_data.csv')
    
    def test_data_loading(self):
        """Test that data loads successfully."""
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 3)
    
    def test_eda_returns_dict(self):
        """Test EDA returns proper structure."""
        results = self.analyzer.perform_eda()
        self.assertIsInstance(results, dict)
        self.assertIn('headline_stats', results)

class TestTechnicalAnalyzer(unittest.TestCase):
    
    def test_rsi_calculation(self):
        """Test RSI returns values between 0-100."""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106])
        rsi = TechnicalAnalyzer.calculate_rsi(prices, window=3)
        self.assertTrue(all((rsi.dropna() >= 0) & (rsi.dropna() <= 100)))

class TestSentimentAnalyzer(unittest.TestCase):
    
    def test_sentiment_range(self):
        """Test sentiment scores are between -1 and 1."""
        analyzer = SentimentAnalyzer()
        score = analyzer.get_sentiment_score("This is great news!")
        self.assertTrue(-1 <= score <= 1)

if __name__ == '__main__':
    unittest.main()