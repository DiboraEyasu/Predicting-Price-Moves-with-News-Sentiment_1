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


   