import QuantLib as ql
import numpy as np

class CurveBootstrapper:
    
    def __init__(self, calculation_date: str):
        y, m, d = map(int, calculation_date.split('-'))
        self.calc_date = ql.Date(d, m, y)
        ql.Settings.instance().evaluationDate = self.calc_date
        
        self.calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
        self.day_count = ql.ActualActual(ql.ActualActual.ISDA)

    def build_curve(self, maturities_in_years: np.ndarray, yields: np.ndarray) -> ql.YieldTermStructure:
        helpers = []
        for m, y in zip(maturities_in_years, yields):
            months = int(round(m * 12))
            period = ql.Period(months, ql.Months)
            rate_quote = ql.QuoteHandle(ql.SimpleQuote(y))
            
            if m <= 1.0:
                helper = ql.DepositRateHelper(
                    rate_quote, period, 2, self.calendar, 
                    ql.ModifiedFollowing, False, self.day_count
                )
            else:
                helper = ql.SwapRateHelper(
                    rate_quote, period, self.calendar, ql.Annual,
                    ql.Unadjusted, self.day_count, ql.Euribor6M() 
                )
            helpers.append(helper)

        curve = ql.PiecewiseLogLinearDiscount(2, self.calendar, helpers, self.day_count)
        return curve

    def get_zero_rates(self, curve: ql.YieldTermStructure, target_maturities: np.ndarray) -> np.ndarray:
        rates = []
        for m in target_maturities:
            d = self.calendar.advance(self.calc_date, ql.Period(int(round(m * 365)), ql.Days))
            zero_rate = curve.zeroRate(d, self.day_count, ql.Continuous, ql.Annual).rate()
            rates.append(zero_rate)
        return np.array(rates)