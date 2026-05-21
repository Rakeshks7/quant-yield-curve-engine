# Fixed Income Quant: Yield Curve Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![QuantLib](https://img.shields.io/badge/QuantLib-1.33-orange?style=for-the-badge)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-lightgrey?style=for-the-badge&logo=scipy)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An institutional-grade Fixed Income pricing engine that retrieves historical US Treasury data, bootstraps zero rates using piecewise log-linear interpolation, and implements the **Nelson-Siegel-Svensson (NSS)** parametric model to fit continuous yield curves. 

This project specifically models the dynamic yield curve shifts (Normal -> Inverted -> Steep) observed during the **2006–2008 Great Financial Crisis**.

## Key Features

- **Automated Data Pipeline:** Fetches constant maturity US Treasury yields (1M to 30Y) directly from the Federal Reserve Economic Data (FRED) API.
- **Advanced Bootstrapping:** Utilizes `QuantLib` to handle day-count conventions (Actual/Actual ISDA), holiday calendars, and zero-rate extraction.
- **NSS Optimization:** Implements the 6-parameter Nelson-Siegel-Svensson mathematical model via `scipy.optimize` to smooth noisy market data into a continuous curve.
- **Crisis Visualization:** Pro-quant terminal aesthetic plotting using `matplotlib` to visualize curve inversion.

## The Math: Nelson-Siegel-Svensson Model

The engine estimates the zero rate $y(t)$ for any maturity $t$ using the following optimization:

$$y(t) = \beta_0 + \beta_1 \left( \frac{1 - e^{-t/\tau_1}}{t/\tau_1} \right) + \beta_2 \left( \frac{1 - e^{-t/\tau_1}}{t/\tau_1} - e^{-t/\tau_1} \right) + \beta_3 \left( \frac{1 - e^{-t/\tau_2}}{t/\tau_2} - e^{-t/\tau_2} \right)$$

## Expected Output:
1 Terminal logs detailing the FRED data fetch and NSS calibration parameters ($\beta_0, \beta_1, \beta_2, \beta_3, \tau_1, \tau_2$).
2 A plot showing the historical evolution of the US Treasury curve from 2005 to 2008.
3 A plot showing the deeply inverted market data (Nov 2006) overlaid with the continuous, smooth NSS bootstrapped curve.

## Architecture
- src/data_loader.py: FRED API integration and data cleaning.
- src/bootstrapper.py: QuantLib environment setup and piecewise log-linear discounting.
- src/nss_model.py: SciPy curve fitting and mathematical parametric formulation.
- src/visualizer.py: Matplotlib plotting logic.
- main.py: The central pipeline orchestrating the above modules.

## Disclaimer
For Educational and Research Purposes Only. The code and models provided in this repository do not constitute financial advice, investment recommendations, or trading signals. Yield curve bootstrapping in a live production environment requires highly granular tick data, bid/ask spread handling, and proprietary instrument modeling not included in this academic demonstration.