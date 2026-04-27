import numpy as np
from scipy.linalg import eigvals

def calculate_recovery_time(R, Phi, M, C):
    """
    Calculates the system recovery time (tau).
    As parameters approach the critical surface $R\Phi/M = 1 - 0.5/C$, 
    tau diverges, signaling a loss of structural resilience.
    Reference: Section 4.3, Equation 4.3 of the paper.
    """
    # Calculate the distance to the theoretical critical threshold
    # Formula: 1 - 0.5/C
    critical_threshold = 1 - 0.5 / C
    current_ratio = (R * Phi) / M
    
    # Distance to criticality (the 'stability margin')
    distance = critical_threshold - current_ratio
    
    # Re(lambda_slow) characterizes the dominant decay rate.
    # As distance approaches zero, lambda_slow approaches zero from the negative side.
    epsilon = 1e-6
    re_lambda_slow = -max(distance, epsilon)
    
    # Recovery time tau is defined as the inverse of the absolute decay rate.
    tau = -1 / re_lambda_slow
    return tau

def compute_spectral_gap(matrix_size=100):
    """
    Analyzes the eigenvalue spectrum of the Fokker-Planck operator.
    Captures the 'Spectral Gap' narrowing as a leading indicator of phase transition.
    Reference: Section 4.3.2.
    """
    # Construct a representative Jacobian for the linearized system dynamics
    # In empirical applications, this matrix is derived from sector-level covariance.
    base_matrix = np.diag(np.linspace(-1.0, -0.05, matrix_size))
    stochastic_noise = np.random.normal(0, 0.01, (matrix_size, matrix_size))
    jacobian = base_matrix + stochastic_noise
    
    # Compute eigenvalues and sort by real part (descending order)
    ev = sorted(eigvals(jacobian).real, reverse=True)
    
    # The ratio between the two largest eigenvalues indicates the dominance of the slow manifold.
    lambda_1 = ev[0]
    lambda_2 = ev[1]
    
    return lambda_1 / lambda_2

def check_resilience_status(tau, threshold=33.3):
    """
    Evaluates the current system resilience status based on the recovery time.
    Threshold of 33.3 steps is derived from the empirical validation in Section 4.3.3.
    """
    if tau > threshold:
        return "CRITICAL WARNING: Significant Slowing Down (Resilience Loss)"
    elif tau > threshold * 0.7:
        return "CAUTION: Early Warning Signal Detected (Increasing Fragility)"
    else:
        return "STABLE: System Resilience Within Normal Range"
