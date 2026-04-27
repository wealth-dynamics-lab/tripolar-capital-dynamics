import numpy as np
from scipy.linalg import eigvals

def calculate_recovery_time(R, Phi, M, C):
    """
    计算系统恢复时间 tau
    对应论文第 4.3 节：当参数接近临界表面 R*Phi/M = 1 - 0.5/C 时，tau 会发生发散
    """
    # 计算当前的参数位置与临界点的距离
    # 理论临界值计算：1 - 0.5/C
    critical_threshold = 1 - 0.5 / C
    current_ratio = (R * Phi) / M
    
    # 计算最慢非零特征值的实部 (简化映射模型)
    # 对应论文公式 (4.3) 逻辑：Re(lambda_slow) 趋近于 0
    distance = critical_threshold - current_ratio
    
    # 避免除以零，设定一个极小值
    epsilon = 1e-5
    re_lambda_slow = -max(distance, epsilon)
    
    # 恢复时间 tau = -1 / Re(lambda_slow)
    tau = -1 / re_lambda_slow
    return tau

def compute_eigenvalue_ratio(matrix_size=100):
    """
    数值计算 Fokker-Planck 算子的特征值谱
    对应论文第 4.3 节验证方法
    """
    # 构造一个模拟的 Jacobian 矩阵 (实际应用中需根据具体数据构造)
    # 此处演示特征值比率 lambda1/lambda2 的提取逻辑
    mock_jacobian = np.diag(np.linspace(-1.0, -0.1, matrix_size))
    # 引入微小扰动
    mock_jacobian += np.random.normal(0, 0.01, (matrix_size, matrix_size))
    
    ev = sorted(eigvals(mock_jacobian).real, reverse=True)
    
    # 提取前两个最大特征值 (靠近0的负值)
    lambda1 = ev[0]
    lambda2 = ev[1]
    
    return lambda1 / lambda2

def check_csd_signal(tau, threshold=30):
    """
    判断是否触发临界减慢预警信号
    根据论文 4.3 节：tau > 30 步时，系统显示出显著的减慢特征
    """
    if tau > threshold:
        return "WARNING: Critical Slowing Down Detected (Resilience Decaying)"
    else:
        return "SAFE: System Resilience Stable"
