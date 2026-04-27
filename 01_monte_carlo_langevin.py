import numpy as np

def compute_E_total(M, C_eff, R_geom, F_thermal, G_redundancy):
    """
    Tripolar Capital Dynamics Tensor Coupling Formula (Paper Formula 3).
    Calculates the systemic destructive energy E_total as the core risk parameter.
    Reference: Section 2.5, Equation 2.13.
    """
    return M * (C_eff**2) * (1 / R_geom) * F_thermal * G_redundancy

def run_monte_carlo_simulation(params, N=5000, T=200, dt=0.01, n_paths=10000):
    """
    Monte Carlo Path Simulation using Euler-Maruyama discretization.
    Simulates individual wealth evolution paths (Langevin SDE).
    Reference: Section 2.1 (Formula 2.1) and Section 4.1.
    """
    # Initialize wealth/capital matrix (paths, time steps)
    # Using large-N mean-field approximation as per Section 2.3
    M_traj = np.zeros((n_paths, T))
    M_traj[:, 0] = params.get('M0', 1.0) 
    
    # Extract tripolar parameters
    C = params['C']
    R = params['R']
    Phi = params['Phi']
    M_target = params['M']
    eta = params['eta']
    sigma_C = params['sigma_C']
    sigma_L = params['sigma_L']

    for t in range(1, T):
        # Generate two independent standard Wiener processes dW_C and dW_L
        # Reference: Section 2.1, Equation 2.1
        dW = np.random.normal(0, np.sqrt(dt), (n_paths, 2))
        
        # Calculate the Drift Term
        # Characterizes net growth constrained by the Information Structure Pole
        drift = (C * M_traj[:, t-1] * (1 - R * Phi / M_target) + eta * M_target / N)
        
        # Calculate the Diffusion Term
        # Reflects dual uncertainty: capital return noise and labor income noise
        diffusion = (sigma_C * M_traj[:, t-1] * dW[:, 0] + sigma_L * dW[:, 1])
        
        # Update capital evolution
        M_traj[:, t] = M_traj[:, t-1] + drift * dt + diffusion
        
    # Return the mean evolution trajectory across all simulation paths
    return M_traj.mean(axis=0)

def calculate_effective_circulation(C, lambda_ratio, kappa=0.8):
    """
    Calculates Effective Circulation Velocity (C_eff).
    Incorporates the Critical Slowing Down (CSD) effect.
    Reference: Section 2.4.1, Equation 2.9.
    """
    return C * (1 + kappa * (lambda_ratio - 1))
