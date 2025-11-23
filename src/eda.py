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

    def news_description(self):
        """Visualize headline length and frequent publishers."""
        if self.df is None:
            print("No data loaded. Call `load_data()` first.")
            return

        if 'headline' in self.df.columns:
            self.df['headline_length'] = self.df['headline'].str.len()
            print('Headline Length Status:\n')
            print(self.df['headline_length'].describe())
        else:
            print("No 'headline' column found in dataframe.")

        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.title('Headlines Length Distribution')
        if 'headline_length' in self.df.columns:
            self.df['headline_length'].hist(bins=50)
        else:
            plt.text(0.5, 0.5, 'No headline data', ha='center')

        plt.subplot(1, 2, 2)
        plt.title('Top 10 Article Publishers')
        if 'publisher' in self.df.columns:
            self.df['publisher'].value_counts().head(7).plot(kind='bar', color='c', edgecolor='black')
            plt.xticks(rotation=45)
        else:
            plt.text(0.5, 0.5, 'No publisher data', ha='center')

        plt.tight_layout()
        # Avoid attempting to open a GUI window in headless/non-interactive environments.
        # Use backend check: if running with a non-interactive backend (e.g., Agg), close the
        # figure instead of calling `plt.show()` which emits a warning.
        try:
            import matplotlib
            backend = matplotlib.get_backend().lower()
        except Exception:
            backend = ''

        if backend.startswith('agg'):
            plt.close('all')
        else:
            plt.show()

    
    def time_series_analysis(self):
        """Helps us to visualize the times where many articles are published"""
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['day'] = self.df['date'].dt.day_name()
        self.df['hour'] = self.df['date'].dt.hour
        self.df['month'] = self.df['date'].dt.month
        self.df['year'] = self.df['date'].dt.year

        daily_count = self.df.groupby('day').size()
        monthly_count = self.df.groupby('month').size()

        plt.figure(figsize=(8,4))
        plt.subplot(1, 2, 1)
        daily_count.plot
        plt.title("Articles Published per Day")
        plt.xticks(rotation=45)

        plt.subplot(1, 2, 2)
        monthly_count.plot
        plt.title("Articles Published per Month")
        plt.xticks(rotation=45)

        plt.subplot(2, 2, 1)
        self.df['hour'].value_counts().sort_index().plot(kind='bar', color='purple')
        plt.title("Hourly News Article Publication")
        plt.xticks(rotation=45)

        plt.subplot(2, 2, 2)
        plt.title("Yearly Publication Trends")
        self.df['year'].plot(kind='bar', color='grey')
        plt.xticks(rotation=45)


        

