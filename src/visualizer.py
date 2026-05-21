import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class CurveVisualizer:
    
    @staticmethod
    def plot_historical_curves(df: pd.DataFrame, dates_to_plot: list, maturities: np.ndarray):
        plt.style.use('dark_background') # Pro-quant terminal aesthetic
        plt.figure(figsize=(10, 6))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(dates_to_plot)))
        
        for idx, d in enumerate(dates_to_plot):
            closest_date = df.index[df.index.get_indexer([pd.to_datetime(d)], method='nearest')[0]]
            yields = df.loc[closest_date].values * 100  
            plt.plot(maturities, yields, marker='o', color=colors[idx], linewidth=2, label=closest_date.strftime('%Y-%m-%d'))

        plt.title("US Treasury Yield Curve Evolution (Great Financial Crisis)")
        plt.xlabel("Maturity (Years)")
        plt.ylabel("Yield (%)")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.4)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_nss_fit(maturities: np.ndarray, market_yields: np.ndarray, continuous_maturities: np.ndarray, nss_yields: np.ndarray, date_str: str):
        plt.style.use('dark_background')
        plt.figure(figsize=(10, 6))
        
        plt.scatter(maturities, market_yields * 100, color='cyan', s=60, label='Market Data (FRED)', zorder=5)
        plt.plot(continuous_maturities, nss_yields * 100, color='magenta', linewidth=2, label='NSS Smooth Fit')
        
        plt.title(f"Nelson-Siegel-Svensson Bootstrapped Zero Curve ({date_str})")
        plt.xlabel("Maturity (Years)")
        plt.ylabel("Zero Rate (%)")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.4)
        plt.tight_layout()
        plt.show()