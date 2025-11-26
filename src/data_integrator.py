import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

class DataIntegrator:
    """Handles merging of news and price data with proper date alignment."""
    
    def __init__(self):
        self.merged_data = None
        
    def align_news_with_prices(self, 
                             news_df: pd.DataFrame, 
                             price_df: pd.DataFrame,
                             news_date_col: str = 'date',
                             price_date_col: str = 'Date') -> pd.DataFrame:
        """
        Align news data with trading days, handling non-trading days.
        
        Args:
            news_df: DataFrame with news articles and dates
            price_df: DataFrame with stock prices and dates
            news_date_col: Name of date column in news data
            price_date_col: Name of date column in price data
            
        Returns:
            Merged DataFrame with aligned dates
        """
        # Ensure datetime format
        news_df = news_df.copy()
        price_df = price_df.copy()
        
        news_df[news_date_col] = pd.to_datetime(news_df[news_date_col])
        price_df[price_date_col] = pd.to_datetime(price_df[price_date_col])
        
        # Extract date only (remove time)
        news_df['trade_date'] = news_df[news_date_col].dt.date
        price_df['trade_date'] = price_df[price_date_col].dt.date
        
        # Aggregate news sentiment by trading day
        daily_sentiment = (news_df.groupby('trade_date')['sentiment']
                          .agg(['mean', 'count'])
                          .rename(columns={'mean': 'avg_sentiment', 
                                         'count': 'news_count'}))
        
        # Calculate daily returns from prices
        price_df['daily_return'] = price_df['Close'].pct_change()
        
        # Merge on trading dates
        self.merged_data = (price_df.merge(daily_sentiment, 
                                         left_on='trade_date', 
                                         right_index=True, 
                                         how='inner')
                          .dropna(subset=['daily_return', 'avg_sentiment']))
        
        print(f"✅ Merged {len(self.merged_data)} trading days with news coverage")
        return self.merged_data
    
    def calculate_correlation_stats(self) -> Dict:
        """Calculate statistical correlation between sentiment and returns."""
        if self.merged_data is None:
            raise ValueError("No merged data available. Run align_news_with_prices first.")
        
        # Pearson correlation
        corr_coef, p_value = stats.pearsonr(self.merged_data['avg_sentiment'], 
                                          self.merged_data['daily_return'])
        
        # Spearman correlation (non-parametric)
        spearman_corr, spearman_p = stats.spearmanr(self.merged_data['avg_sentiment'],
                                                  self.merged_data['daily_return'])
        
        # Basic statistics
        stats_report = {
            'pearson_correlation': corr_coef,
            'pearson_p_value': p_value,
            'spearman_correlation': spearman_corr,
            'spearman_p_value': spearman_p,
            'significant_pearson': p_value < 0.05,
            'significant_spearman': spearman_p < 0.05,
            'days_analyzed': len(self.merged_data),
            'avg_news_per_day': self.merged_data['news_count'].mean(),
            'sentiment_range': (self.merged_data['avg_sentiment'].min(),
                              self.merged_data['avg_sentiment'].max())
        }
        
        return stats_report
    
    def create_correlation_plots(self, save_path: Optional[str] = None) -> None:
        """Create professional plots of sentiment vs returns."""
        if self.merged_data is None:
            raise ValueError("No merged data available.")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('News Sentiment vs Stock Returns Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Scatter plot with regression line
        self._plot_scatter_with_regression(axes[0, 0])
        
        # Plot 2: Time series of sentiment and returns
        self._plot_time_series(axes[0, 1])
        
        # Plot 3: Returns distribution by sentiment
        self._plot_returns_by_sentiment(axes[1, 0])
        
        # Plot 4: Correlation heatmap
        self._plot_correlation_heatmap(axes[1, 1])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"📊 Correlation plots saved to {save_path}")
        
        plt.show()
    
    def _plot_scatter_with_regression(self, ax) -> None:
        """Scatter plot with regression line and confidence interval."""
        x = self.merged_data['avg_sentiment']
        y = self.merged_data['daily_return']
        
        # Calculate regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        line = slope * x + intercept
        
        ax.scatter(x, y, alpha=0.6, s=50)
        ax.plot(x, line, 'r-', label=f'R² = {r_value**2:.3f}, p = {p_value:.3f}')
        ax.set_xlabel('Average Daily Sentiment')
        ax.set_ylabel('Daily Returns')
        ax.set_title('Sentiment vs Returns Correlation')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_time_series(self, ax) -> None:
        """Time series of sentiment and returns."""
        dates = self.merged_data['trade_date']
        
        # Plot sentiment
        color = 'tab:blue'
        ax.set_xlabel('Date')
        ax.set_ylabel('Sentiment', color=color)
        ax.plot(dates, self.merged_data['avg_sentiment'], color=color, alpha=0.7)
        ax.tick_params(axis='y', labelcolor=color)
        
        # Plot returns on secondary axis
        ax2 = ax.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Daily Returns', color=color)
        ax2.plot(dates, self.merged_data['daily_return'], color=color, alpha=0.7)
        ax2.tick_params(axis='y', labelcolor=color)
        
        ax.set_title('Sentiment and Returns Over Time')
        ax.grid(True, alpha=0.3)
    
    def _plot_returns_by_sentiment(self, ax) -> None:
        """Box plot of returns grouped by sentiment levels."""
        # Create sentiment categories
        conditions = [
            self.merged_data['avg_sentiment'] < -0.1,
            (self.merged_data['avg_sentiment'] >= -0.1) & (self.merged_data['avg_sentiment'] <= 0.1),
            self.merged_data['avg_sentiment'] > 0.1
        ]
        choices = ['Negative', 'Neutral', 'Positive']
        
        self.merged_data['sentiment_category'] = np.select(conditions, choices, default='Neutral')
        
        # Box plot
        sentiment_order = ['Negative', 'Neutral', 'Positive']
        box_data = [self.merged_data[self.merged_data['sentiment_category'] == cat]['daily_return'] 
                   for cat in sentiment_order]
        
        ax.boxplot(box_data, labels=sentiment_order)
        ax.set_ylabel('Daily Returns')
        ax.set_title('Returns Distribution by Sentiment Level')
        ax.grid(True, alpha=0.3)
    
    def _plot_correlation_heatmap(self, ax) -> None:
        """Correlation heatmap of key variables."""
        corr_cols = ['avg_sentiment', 'daily_return', 'news_count', 'Close', 'Volume']
        corr_data = self.merged_data[corr_cols].corr()
        
        im = ax.imshow(corr_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr_cols)))
        ax.set_yticks(range(len(corr_cols)))
        ax.set_xticklabels(corr_cols, rotation=45)
        ax.set_yticklabels(corr_cols)
        
        # Add correlation values as text
        for i in range(len(corr_cols)):
            for j in range(len(corr_cols)):
                ax.text(j, i, f'{corr_data.iloc[i, j]:.2f}', 
                       ha='center', va='center', fontweight='bold')
        
        ax.set_title('Variable Correlation Heatmap')
        plt.colorbar(im, ax=ax)