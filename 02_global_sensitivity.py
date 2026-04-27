import numpy as np
import pandas as pd
from scipy.stats import spearmanr, qmc
from 01_monte_carlo_langevin import compute_E_total

class SensitivityAnalyzer:
    """
    Implements Global Sensitivity Analysis using LHS and Spearman Rank Correlation.
    Reference: Section 4.2 of the paper.
    """
    def __init__(self, baseline_params, n_samples=2000, variation=0.25):
        self.baseline = baseline_params
        self.n_samples = n_samples
        self.variation = variation
        # Parameters to test based on Section 4.2 [cite: 484-489]
        self.param_names = ['M', 'C', 'R', 'Phi', 'lambda_ratio', 'eta']

    def run_analysis(self):
        # 1. Latin Hypercube Sampling [cite: 480]
        sampler = qmc.LatinHypercube(d=len(self.param_names))
        sample = sampler.random(n=self.n_samples)
        
        # 2. Scale samples to +/- 25% of baseline 
        lower_bounds = [self.baseline[p] * (1 - self.variation) for p in self.param_names]
        upper_bounds = [self.baseline[p] * (1 + self.variation) for p in self.param_names]
        scaled_samples = qmc.scale(sample, lower_bounds, upper_bounds)
        
        e_results = []
        for s in scaled_samples:
            p_dict = dict(zip(self.param_names, s))
            # Placeholder for effective parameters defined in Section 2.4 [cite: 167, 173, 180, 186]
            # Assuming baseline F_thermal and G_redundancy for sensitivity focus
            e_val = compute_E_total(p_dict['M'], p_dict['C'], p_dict['R'], 1.0, 1.0)
            e_results.append(e_val)
            
        # 3. Calculate Spearman Rank Correlation [cite: 482]
        sensitivity_df = []
        for i, name in enumerate(self.param_names):
            rho, p_val = spearmanr(scaled_samples[:, i], e_results)
            sensitivity_df.append({'Parameter': name, 'Spearman_rho': rho})
            
        df = pd.DataFrame(sensitivity_df).sort_values(by='Spearman_rho', ascending=False)
        return df

if __name__ == "__main__":
    # Example baseline based on Germany's data [cite: 434, 459]
    baseline = {'M': 2.0, 'C': 0.7, 'R': 1.45, 'Phi': 0.46, 'lambda_ratio': 1.1, 'eta': 0.25}
    analyzer = SensitivityAnalyzer(baseline)
    print(analyzer.run_analysis())
