import numpy as np

def compute_E_total(M, C_eff, R_geom, F_thermal, G_redundancy):
    """
    三极资本动力学张量耦合公式 (对应论文 Formula 3)
    计算系统总破坏能 E_total，作为核心风险序参数
    """
    return M * (C_eff**2) * (1 / R_geom) * F_thermal * G_redundancy

def run_monte_carlo_simulation(params, N=5000, T=200, dt=0.01, n_paths=10000):
    """
    基于 Euler-Maruyama 离散化方案的 Monte Carlo 路径模拟
    对应论文第 4.1 节及附录 D.1 逻辑
    """
    # 初始化财富/资本矩阵 (路径数, 时间步)
    M_traj = np.zeros((n_paths, T))
    M_traj[:, 0] = params.get('M0', 1.0) # 初始资本
    
    # 提取三极参数
    C = params['C']
    R = params['R']
    Phi = params['Phi']
    M_target = params['M']
    eta = params['eta']
    sigma_C = params['sigma_C']
    sigma_L = params['sigma_L']

    for t in range(1, T):
        # 产生两个独立的维纳过程增量 dW_C 和 dW_L
        dW = np.random.normal(0, np.sqrt(dt), (n_paths, 2))
        
        # 计算漂移项 (Drift term): 资本增长受信息结构极约束
        # 对应论文公式 (2.1)
        drift = (C * M_traj[:, t-1] * (1 - R * Phi / M_target) + eta * M_target / N)
        
        # 计算扩散项 (Diffusion term): 包含乘性资本噪声和加性劳动噪声
        diffusion = (sigma_C * M_traj[:, t-1] * dW[:, 0] + sigma_L * dW[:, 1])
        
        # 财富演化更新
        M_traj[:, t] = M_traj[:, t-1] + drift * dt + diffusion
        
    # 返回大样本下的平均演化轨迹
    return M_traj.mean(axis=0)

def calculate_effective_params(C, lambda_ratio, kappa=0.8):
    """
    计算有效循环速度 C_eff (引入临界减慢效应 CSD)
    对应论文第 2.4.1 节逻辑
    """
    return C * (1 + kappa * (lambda_ratio - 1))
