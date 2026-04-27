import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter

class DataPreprocessor:
    """
    Data Preprocessing Module: Implements HP Filtering, Min-Max Normalization, 
    and Trend Extrapolation based on Section 3.2 and 3.4.2 of the paper.
    """
    def __init__(self, base_year=2008):
        self.base_year = base_year

    def standardize_param(self, series):
        """
        Applies Min-Max Normalization to ensure cross-national comparability.
        """
        return (series - series.min()) / (series.max() - series.min())

    def apply_hp_filter(self, series, lamb=1600):
        """
        Applies the Hodrick-Prescott (HP) filter for trend decomposition.
        """
        cycle, trend = hpfilter(series, lamb=lamb)
        return trend

    def calculate_basic_params(self, gdp, m2, investment, trust_score, public_exp):
        """
        Calculates basic parameters:
        M: Material Capital Pole (Fixed Asset Investment / GDP)
        C: Energy Flow Pole (GDP / M2)
        Phi: Information Structure Pole - Macro (Normalized Trust Score)
        eta: Labor Income Conversion Rate (Public Expenditure / GDP)
        """
        M = investment / gdp
        C = gdp / m2
        Phi = self.standardize_param(trust_score)
        eta = public_exp / gdp
        return M, C, Phi, eta

    def trend_extrapolation_2025(self, historical_data, target_gdp_2025):
        """
        Implements the 2025 Trend Extrapolation Method (Section 3.4.2).
        Estimated based on the assumption of stable structural coefficients.
        """
        structural_coeff = historical_data.iloc[-1] / historical_data.iloc[-1].sum()
        estimated_2025 = structural_coeff * target_gdp_2025
        return estimated_2025
