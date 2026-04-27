import numpy as np
import pandas as pd
from datetime import datetime
from 06_data_preprocessing import DataPreprocessor
from 01_monte_carlo_langevin import run_monte_carlo_simulation, compute_E_total
from 03_critical_slowing_down import calculate_recovery_time, check_resilience_status
from 04_policy_simulation import PolicySimulator

def run_tripolar_analysis(country_name, raw_data):
    """
    Main execution pipeline for the Tripolar Capital Dynamics Model.
    Follows the P0-P4 workflow described in the UCAS framework.
    """
    print(f"--- Executing Analysis for {country_name} [{datetime.now().strftime('%Y-%m-%d')}] ---")
    
    # 1. Data Preprocessing (Section 3.2)
    preprocessor = DataPreprocessor()
    M, C, Phi, eta = preprocessor.calculate_basic_params(
        raw_data['gdp'], 
        raw_data['m2'], 
        raw_data['investment'], 
        raw_data['trust_score'], 
        raw_data['public_exp']
    )
    
    # 2. Parameter Setup for Simulation (Section 4.1)
    # Using empirical constants for R_geom and sigma based on Appendix A
    sim_params = {
        'M': M, 'C': C, 'Phi': Phi, 'eta': eta,
        'R': raw_data['R_friction'], 
        'sigma_C': 0.15, 'sigma_L': 0.05,
        'M0': 1.0
    }
    
    # 3. Core Langevin Simulation (Monte Carlo)
    avg_trajectory = run_monte_carlo_simulation(sim_params)
    
    # 4. Critical Slowing Down (CSD) Analysis (Section 4.3)
    tau = calculate_recovery_time(sim_params['R'], Phi, M, C)
    resilience_report = check_resilience_status(tau)
    
    # 5. E_total Calculation (The Order Parameter)
    # E_total = M * C^2 * (1/R) * F_thermal * G_redundancy
    # (F and G are set to baseline 1.0 for this standard run)
    e_total = compute_E_total(M, C, sim_params['R'], 1.0, 1.0)
    
    # 6. Policy Simulation (Chapter 6)
    simulator = PolicySimulator()
    e_optimum = simulator.simulate_policy_mix(e_total)
    welfare_gain = simulator.calculate_welfare_loss(e_total, e_optimum)

    # Output Results
    print(f"Systemic Destructive Energy (E_total): {e_total:.4f}")
    print(f"Recovery Time (tau): {tau:.2f} steps")
    print(f"Status: {resilience_report}")
    print(f"Potential Risk Reduction via Coordination: {welfare_gain*100:.2f}%")
    print("-" * 50)

if __name__ == "__main__":
    # Mock data for demonstration based on 2025/2026 projections (Section 3.5)
    # In a real run, replace these with actual CSV imports
    countries_data = {
        "Germany": {
            "gdp": 4.5e12, "m2": 3.8e12, "investment": 0.9e12, 
            "trust_score": 46, "public_exp": 1.2e12, "R_friction": 1.45
        },
        "Japan": {
            "gdp": 4.2e12, "m2": 9.1e12, "investment": 1.1e12, 
            "trust_score": 38, "public_exp": 0.8e12, "R_friction": 1.20
        },
        "USA": {
            "gdp": 28.0e12, "m2": 21.0e12, "investment": 6.2e12, 
            "trust_score": 42, "public_exp": 6.5e12, "R_friction": 1.65
        }
    }

    for country, data in countries_data.items():
        run_tripolar_analysis(country, data)
