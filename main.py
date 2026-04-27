import numpy as np
import pandas as pd
from datetime import datetime

# Import modular components created in previous steps
from 06_data_preprocessing import DataPreprocessor
from 01_monte_carlo_langevin import run_monte_carlo_simulation, compute_E_total
from 02_global_sensitivity import SensitivityAnalyzer
from 03_critical_slowing_down import calculate_recovery_time, check_resilience_status
from 04_policy_simulation import PolicySimulator
from 07_department_aggregation import SectorAggregator

def execute_full_tripolar_pipeline(country_name, raw_macro_data, raw_sector_data):
    """
    Full Orchestration Pipeline for Tripolar Capital Dynamics.
    Reference: Four-stage research path (Section 1.3).
    """
    print(f"\n{'='*20} ANALYZING: {country_name} {'='*20}")
    
    # --- STAGE 1: Data Preprocessing & Aggregation (06 & 07) ---
    preprocessor = DataPreprocessor()
    aggregator = SectorAggregator()
    
    # Calculate Macro Params [cite: 289]
    M, C, Phi, eta = preprocessor.calculate_basic_params(
        raw_macro_data['gdp'], raw_macro_data['m2'], 
        raw_macro_data['investment'], raw_macro_data['trust_score'],
        raw_macro_data['public_exp']
    )
    
    # Aggregate 42-sector data into 12-sector E_total [cite: 390]
    sector_results = aggregator.aggregate_data(raw_sector_data)
    avg_sector_e = sector_results.mean()
    
    # --- STAGE 2: Core Dynamics & Simulation (01) ---
    sim_params = {
        'M': M, 'C': C, 'Phi': Phi, 'eta': eta,
        'R': raw_macro_data['R_friction'], 
        'sigma_C': 0.15, 'sigma_L': 0.05, 'M0': 1.0
    }
    
    # Run Langevin SDE Simulation [cite: 110, 462]
    trajectory = run_monte_carlo_simulation(sim_params)
    e_total_macro = compute_E_total(M, C, sim_params['R'], 1.0, 1.0)
    
    # --- STAGE 3: Stability & Sensitivity Analysis (02 & 03) ---
    # Critical Slowing Down (CSD) check [cite: 509]
    tau = calculate_recovery_time(sim_params['R'], Phi, M, C)
    resilience_status = check_resilience_status(tau)
    
    # Global Sensitivity Analysis (LHS + Spearman) [cite: 480]
    analyzer = SensitivityAnalyzer(sim_params)
    sensitivity_rank = analyzer.run_analysis()
    
    # --- STAGE 4: Policy Simulation (04) ---
    simulator = PolicySimulator()
    # Scenario D: Optimal Policy Mix [cite: 781]
    e_optimum = simulator.simulate_policy_mix(e_total_macro)
    welfare_gain = simulator.calculate_welfare_loss(e_total_macro, e_optimum)

    # --- FINAL REPORTING (P4 Output) ---
    print(f"1. MACRO RISK (E_total): {e_total_macro:.4f}")
    print(f"2. SECTORAL RISK (Avg 12-Sectors): {avg_sector_e:.4f}")
    print(f"3. SYSTEM RESILIENCE (tau): {tau:.2f} | Status: {resilience_status}")
    print(f"4. TOP SENSITIVE PARAMETER: {sensitivity_rank.iloc[0]['Parameter']}")
    print(f"5. COORDINATION BENEFIT: +{welfare_gain*100:.2f}% Risk Reduction")
    print(f"{'='*60}")

if __name__ == "__main__":
    # Mock Macro Data based on 2025 Trend Extrapolation [cite: 434]
    mock_macro = {
        "Germany": {"gdp": 4.5e12, "m2": 3.8e12, "investment": 0.9e12, "trust_score": 46, "public_exp": 1.2e12, "R_friction": 1.45},
        "Japan": {"gdp": 4.2e12, "m2": 9.1e12, "investment": 1.1e12, "trust_score": 38, "public_exp": 0.8e12, "R_friction": 1.20},
        "USA": {"gdp": 28.0e12, "m2": 21.0e12, "investment": 6.2e12, "trust_score": 42, "public_exp": 6.5e12, "R_friction": 1.65}
    }
    
    # Mock 42-sector data based on Appendix A tables [cite: 1016, 1018, 1020]
    for country in ["Germany", "Japan", "USA"]:
        mock_sector_df = pd.DataFrame({
            'Number': range(1, 43),
            'E_total': np.random.uniform(0.5, 7.0, 42) # Placeholder for Table A1-A3 values
        })
        execute_full_tripolar_pipeline(country, mock_macro[country], mock_sector_df)
