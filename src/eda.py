import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt
from nltk.corpus import stopwords
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

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
        plt.tight_layout()
        plt.show()


        # function to remove punctuation, number and convert to lower case
    def clean_text(text):
        text=str(text).lower() # lowercase
        text = re.sub(r'\d+', '', text)  # remove numbers
        text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
        return text
    

    def text_analysis(self):
        self.df["clean_headline"] = self.df.headline.apply()
        stop_words = set(stopwords.words('english'))

        # Single word analysis
        words = self.df['clean_headline'].str.split().explode()
        top_words = words[~words.isin(stop_words)].value_counts().head(15)

        # Multi-word phrases analysis
        phrases = {
            'bigrams': (2,2),
            'trigrams': (3,3), 
            'mixed': (2,3)
        }

        for name, ngram_range in phrases.items():
            vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words='english')
            X = vectorizer.fit_transform(self.df['clean_headline'])
            frequencies = X.sum(axis=0).A1
            features = vectorizer.get_feature_names_out()
            top_phrases = sorted(zip(features, frequencies), key=lambda x: x[1], reverse=True)[:10]
            
            print(f"\n🔤 Top {name.upper()}:")
            for phrase, freq in top_phrases:
                print(f"  {phrase:<30} {freq:>6,}")

        # Financial zoom expressions
        financial_terms = ['earnings', 'fda', 'dividend', 'merger', 'target price', 'stock split']
        print(f"\n🎯 FINANCIAL TERM COUNTS:")
        for term in financial_terms:
            count = self.df['clean_headline'].str.contains(term, case=False).sum()
            print(f"  {term:<15} {count:>6,}")


    def publisher_analysis(self):
        # Analyze top 3 publishers' content differences
        top_3_publishers = self.df['publisher'].value_counts().head(3).index

        print("Content Specialization by Top Publishers:")
        for publisher in top_3_publishers:
            publisher_df = self.df[self.df['publisher'] == publisher]
            
            # Get unique keywords for this publisher
            publisher_keywords = publisher_df['headline'], top_n=8
            
            print(f"\n{publisher}:")
            print(f"  • Articles: {len(publisher_df):,}")
            print(f"  • Unique keywords: {[word for word, count in publisher_keywords]}")
            print(f"  • Avg headline length: {publisher_df['headline_length'].mean():.1f} chars")

        # Check for email domains in publisher names
        email_publishers = df[df['publisher'].str.contains('@', na=False)]
        if len(email_publishers) > 0:
            print(f"\n📧 Email Publishers Found: {len(email_publishers)}")
            email_publishers['domain'] = email_publishers['publisher'].str.split('@').str[1]
            print("Top email domains:")
            print(email_publishers['domain'].value_counts().head(5))
        else:
            print("\n📧 No email addresses found in publisher names")


if __name__ == "__main__":
    df = pd.read_csv('./data/raw_analyst_ratings.csv')

    df.load_data()
    df.basic_info()
    df.clean_text()

    df.time_series_analysis()
    df.text_analysis()
