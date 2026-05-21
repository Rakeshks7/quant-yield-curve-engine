import numpy as np
from scipy.optimize import curve_fit
import logging

class NelsonSiegelSvensson:
    
    def __init__(self):
        self.params = None

    @staticmethod
    def nss_formula(t: np.ndarray, beta0: float, beta1: float, beta2: float, beta3: float, tau1: float, tau2: float) -> np.ndarray:
        t = np.maximum(t, 1e-6)
        
        term1 = (1 - np.exp(-t / tau1)) / (t / tau1)
        term2 = term1 - np.exp(-t / tau1)
        term3 = ((1 - np.exp(-t / tau2)) / (t / tau2)) - np.exp(-t / tau2)
        
        return beta0 + beta1 * term1 + beta2 * term2 + beta3 * term3

    def fit(self, maturities: np.ndarray, yields: np.ndarray):
        p0 = [np.mean(yields), -0.01, 0.01, 0.01, 1.0, 1.0]
        
        bounds = (
            [-np.inf, -np.inf, -np.inf, -np.inf, 0.01, 0.01],
            [np.inf, np.inf, np.inf, np.inf, 100.0, 100.0]
        )
        
        try:
            popt, _ = curve_fit(self.nss_formula, maturities, yields, p0=p0, bounds=bounds, maxfev=10000)
            self.params = popt
            logging.info(f"NSS Calibration Successful. Parameters: {np.round(self.params, 4)}")
            return popt
        except Exception as e:
            logging.error(f"NSS Fitting failed: {e}")
            raise RuntimeError("Optimization failed to converge.")

    def predict(self, maturities: np.ndarray) -> np.ndarray:
        if self.params is None:
            raise ValueError("Model has not been calibrated.")
        return self.nss_formula(maturities, *self.params)