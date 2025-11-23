# Financial News and Stock Price Integration Dataset Project

## 📌 Overview

This project focuses on analyzing news broadcasts and the stock price of a company 
simultaneoously to provide a proper and an actionable insight for different 
stock forecasting companies and specifically Nova Solutions at its present status.

## Business Objective

The primary goal of this project is to enhance the predictive analytics capabilities of **Nova Financial Solutions**
as it aims to enhance its predictive analytics capabilities to significantly boost its financial forecasting accuracy and operational efficiency through advanced data analysis. As a Data Analyst at Nova Financial Solutions,  I have tried to conduct a rigorous analysis of the financial news dataset and provide a meaningful summary and insight.

## Situational Overview

As a Data Analyst at Nova Financial Solutions, a consultancy firm in data driven insights for stock market, the analysis aims to
 * Perform **Sentiment Analysis** on the ‘headline’ text to quantify the tone and sentiment expressed in financial news.
 * Establish statistical **Correlation Analysis** between the sentiment derived from news articles and the corresponding stock price movements.

## 📂Datasets

From the bulky data, we are going to perform the analysis on the data collected and published between
January 1, 2025 and November 18, 2025. The structure of the data is:
 * **headline**: Article release headline, the title of the news article, includes key actions like stocks hitting highs, price target changes, or company earnings.
 * **url**: The direct link to the full news article.
 * **publisher**: Author/creator of article.
 * **date**: The publication date and time, including timezone information(UTC-4 timezone).
 * **stock**: Stock ticker symbol (unique series of letters assigned to a publicly traded company). For example (AAPL: Apple)

## Learning Objectives

 * **Skills** 
    Not yet encountered but expect to 
    * compute technical indicators for finance (MA, RSI, MACD) using TA-Lib and PyNance
    * become familiar to running sentiment analysis using NLP tools on News headlines and translate it to other sectors as well.
 * **Knowledge**
    * Sentiment analysis and getting actionable insight from crude documents and providing a correlation between it and a data of any sector we want to derive insight for, daily stock returns in our context.
    * Time series analysis by integrating quantitative and qualitative data.

## Project Tasks

### 📌 Task 1: Git and GitHub

##### ✅ Steps to be performed

* Setting up a proper working environment
    * Virtual Python environment
    * Git version control 
    * CI/CD 

##### ✅ Steps to be performed

* Perform Exploratory Data Analysis (EDA) analysis on:
    * Descriptive Statistics
    * Text Analysis(Topic Modeling)
    * Time Series Analysis
    * Publisher A1nalysis

### 📌 Task 2: Quantitative analysis using pynance and TaLib

##### ✅ Steps to be performed
 * **Date Alignment**:
 * **Sentiment Analysis**: to quantify the tone of each article of the news headlines (positive, negative, neutral).
  Tools to be used are Python libraries like **nltk and TextBlob**.

 * **Analysis**
    * **Calculate Daily Stock Returns**:
    * **Correlation Analysis**:
        * Aggregate Sentiments
        * Calculate Correlation
### 📌 Task 3: Correlation between news and stock movement
##### ✅ Steps to be performed


## 🛠️ Environment Setup

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Git

### Installation Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DiboraEyasuE/stock-challenge-week1.git
   cd TEST
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On Mac/Linux
python -m venv .venv
source .venv/bin/activate

    ``` pip install -r requirements.txt
    ``` python --version
    ``` pip list