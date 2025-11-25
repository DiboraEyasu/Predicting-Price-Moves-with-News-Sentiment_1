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