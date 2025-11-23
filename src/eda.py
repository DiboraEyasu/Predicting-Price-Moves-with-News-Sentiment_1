import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt
from nltk.corpus import stopwords

class NewsEDA:
    def __init__(self, filepath=None):
        self.df = None
        self.filepath = filepath


   
    def load_data(self, filepath=None):
        """Load the data from a csv file. If `filepath` is not provided,
        the instance `self.filepath` is used.
        """
        filepath = filepath or self.filepath
        if filepath is None:
            raise ValueError("No filepath provided to load_data()")

        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return None

        # try to parse date column if present
        self.df = pd.read_csv(filepath)
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            try:
                self.df.sort_values('date', inplace=True)
            except Exception:
                pass

        print("✅ Data Loaded Successfully")
        return self.df

    def basic_info(self):
        """Print general information about the dataframe."""
        if self.df is not None:
            print("Columns:", self.df.columns.to_list())
            self.df.dropna(inplace=True)
            if 'date' in self.df.columns:
                print("\nDate range:")
                print("Min date:", self.df['date'].min())
                print("Max date:", self.df['date'].max())
