import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter

class DataPreprocessor:
    """
    数据预处理模块：执行 HP 滤波、Min-Max 标准化及趋势外推
    对应论文第 3.2 节及 3.4.2 节逻辑
    """
    def __init__(self, base_year=2008):
        self.base_year = base_year

    def standardize_param(self, series):
        """执行 Min-Max 标准化，确保跨国数据可比性 [cite: 345]"""
        return (series - series.min()) / (series.max() - series.min())

    def apply_hp_filter(self, series, lamb=1600):
        """执行统一的 HP 滤波处理协议 [cite: 1674]"""
        cycle, trend = hpfilter(series, lamb=lamb)
        return trend

    def calculate_basic_params(self, gdp, m2, investment, trust_score, public_exp):
        """
        计算论文定义的基础参数：
        M: 物质资本极 (Fixed Asset Investment / GDP) [cite: 314]
        C: 能量流动极 (GDP / M2) [cite: 320]
        Phi: 信息结构极宏观分量 (标准化社会信赖得分) [cite: 330]
        eta: 劳动收入转换率 (公共支出 / GDP) [cite: 335]
        """
        M = investment / gdp
        C = gdp / m2
        Phi = self.standardize_param(trust_score)
        eta = public_exp / gdp
        return M, C, Phi, eta

    def trend_extrapolation_2025(self, historical_data, target_gdp_2025):
        """
        实现 3.4.2 节所述的 2025 趋势外推法
        基于产业结构系数相对稳定假设进行比例估算 [cite: 439, 441]
        """
        structural_coeff = historical_data.iloc[-1] / historical_data.iloc[-1].sum()
        estimated_2025 = structural_coeff * target_gdp_2025
        return estimated_2025
