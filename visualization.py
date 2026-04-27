import matplotlib.pyplot as plt
import numpy as np

class ModelVisualizer:
    """
    Visualization Module: Generates charts for systemic risk analysis.
    Corresponds to Figures 4.1, 4.4, and 6.3 in the paper.
    """
    def __init__(self, style='seaborn-v0_8-whitegrid'):
        try:
            plt.style.use(style)
        except:
            plt.style.use('ggplot')

    def plot_systemic_energy_trend(self, time_axis, e_total_series, country_name):
        """
        Plots the evolution of Systemic Destructive Energy (E_total).
        Reference: Figure 4.1.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(time_axis, e_total_series, label=f'E_total ({country_name})', color='darkblue', linewidth=2)
        plt.axhline(y=np.mean(e_total_series), color='red', linestyle='--', label='Historical Mean')
        plt.title(f"Systemic Destructive Energy Evolution: {country_name}")
        plt.xlabel("Time Steps (Quarterly)")
        plt.ylabel("E_total (Risk Order Parameter)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_critical_slowing_down(self, distance_to_criticality, recovery_time):
        """
        Plots the Recovery Time (tau) divergence as the system approaches the critical surface.
        Reference: Figure 4.4 (CSD Signal).
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(distance_to_criticality, recovery_time, alpha=0.6, color='darkorange')
        plt.plot(distance_to_criticality, recovery_time, color='darkred', linestyle='-', alpha=0.3)
        plt.title("Critical Slowing Down: Recovery Time vs. Distance to Criticality")
        plt.xlabel("Distance to Critical Surface (1 - 0.5/C - R*Phi/M)")
        plt.ylabel("Recovery Time (tau)")
        plt.yscale('log') # Recovery time exhibits exponential growth near criticality
        plt.tight_layout()
        plt.show()

    def plot_policy_comparison(self, countries, nash_results, optimal_results):
        """
        Generates a bar chart comparing Nash Equilibrium (Baseline) vs. Social Optimum.
        Reference: Figure 6.3 (Policy Impact).
        """
        x = np.arange(len(countries))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        rects1 = ax.bar(x - width/2, nash_results, width, label='Nash Equilibrium (No Coordination)', color='gray')
        rects2 = ax.bar(x + width/2, optimal_results, width, label='Social Optimum (Full Coordination)', color='green')

        ax.set_ylabel('E_total (Systemic Risk)')
        ax.set_title('Risk Reduction: Nash Equilibrium vs. Social Optimum')
        ax.set_xticks(x)
        ax.set_xticklabels(countries)
        ax.legend()
        plt.tight_layout()
        plt.show()
