import numpy as np
from src.data_loader import YieldDataFetcher
from src.bootstrapper import CurveBootstrapper
from src.nss_model import NelsonSiegelSvensson
from src.visualizer import CurveVisualizer

def main():
    START_DATE = '2005-01-01'
    END_DATE = '2008-12-31'
    
    CRISIS_DATES = ['2005-06-01', '2006-11-01', '2007-06-01', '2008-06-01']
    
    TARGET_DATE = '2006-11-01' 

    fetcher = YieldDataFetcher(START_DATE, END_DATE)
    df = fetcher.fetch_data()
    maturities = fetcher.maturities

    print("\n--- Visualizing Historical Crisis Curves ---")
    CurveVisualizer.plot_historical_curves(df, CRISIS_DATES, maturities)

    target_idx = df.index.get_indexer([pd.to_datetime(TARGET_DATE)], method='nearest')[0]
    actual_date = df.index[target_idx]
    market_yields = df.loc[actual_date].values
    
    print(f"\n--- Bootstrapping and Fitting Curve for {actual_date.strftime('%Y-%m-%d')} ---")

    calc_date_str = actual_date.strftime('%Y-%m-%d')
    bootstrapper = CurveBootstrapper(calc_date_str)

    ql_curve = bootstrapper.build_curve(maturities, market_yields)
    zero_rates = bootstrapper.get_zero_rates(ql_curve, maturities)

    nss = NelsonSiegelSvensson()
    nss.fit(maturities, zero_rates)

    continuous_maturities = np.linspace(0.1, 30.0, 300)
    nss_smooth_curve = nss.predict(continuous_maturities)

    CurveVisualizer.plot_nss_fit(
        maturities, 
        zero_rates, 
        continuous_maturities, 
        nss_smooth_curve, 
        calc_date_str
    )

if __name__ == "__main__":
    main()