import pandas_datareader as pdr
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class YieldDataFetcher:
    
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers = {
            '1 Mo': 'DGS1MO', '3 Mo': 'DGS3MO', '6 Mo': 'DGS6MO',
            '1 Yr': 'DGS1', '2 Yr': 'DGS2', '3 Yr': 'DGS3',
            '5 Yr': 'DGS5', '7 Yr': 'DGS7', '10 Yr': 'DGS10',
            '20 Yr': 'DGS20', '30 Yr': 'DGS30'
        }
        self.maturities = np.array([1/12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])

    def fetch_data(self) -> pd.DataFrame:
        logging.info(f"Fetching FRED data from {self.start_date} to {self.end_date}...")
        symbols = list(self.tickers.values())
        try:
            df = pdr.get_data_fred(symbols, self.start_date, self.end_date)
            df.columns = list(self.tickers.keys())
            df = df.dropna()
            logging.info(f"Successfully fetched {len(df)} trading days of yield data.")
            return df / 100.0  
        except Exception as e:
            logging.error(f"Data fetching failed: {e}")
            raise