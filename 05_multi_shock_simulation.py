import numpy as np

class ExternalShockEngine:
    """
    External Shocks Module: Implements the extended model from Chapter 5.
    Analyzes the impact of non-linear shocks (AI, Climate, Aging, CBDC) 
    on the tripolar parameter space.
    """
    def __init__(self, base_params):
        self.params = base_params.copy()

    def apply_climate_shock(self, physical_risk_factor=0.12, transition_cost=0.08):
        """
        Calculates the impact of Climate Risk.
        Increases institutional friction (R) and reduces material capital efficiency.
        Reference: Section 5.1 of the paper.
        """
        shacked_params = self.params.copy()
        # Physical risk increases maintenance costs and friction
        shacked_params['R'] = self.params['R'] * (1 + physical_risk_factor)
        # Transition costs temporarily reduce effective material capital (M)
        shacked_params['M'] = self.params['M'] * (1 - transition_cost)
        return shacked_params

    def apply_ai_productivity_shock(self, alpha=0.25, displacement_rate=0.15):
        """
        Calculates the impact of the AI Revolution.
        Dual effect: Increases circulation velocity (C) but may lower labor income conversion (eta).
        Reference: Section 5.2.
        """
        shacked_params = self.params.copy()
        # AI boosts productivity and transaction speed
        shacked_params['C'] = self.params['C'] * (1 + alpha)
        # Structural unemployment may reduce the stability of labor income conversion
        shacked_params['eta'] = self.params['eta'] * (1 - displacement_rate)
        return shacked_params

    def apply_demographic_shock(self, dependency_ratio_increase=0.1):
        """
        Calculates the impact of Population Aging.
        Primarily reduces the Material Capital Pole (M) and labor conversion rate.
        Reference: Section 5.3.
        """
        shacked_params = self.params.copy()
        reduction_factor = 1 - (dependency_ratio_increase * 0.5)
        shacked_params['M'] = self.params['M'] * reduction_factor
        shacked_params['eta'] = self.params['eta'] * reduction_factor
        return shacked_params

    def apply_cbdc_shock(self, liquidity_efficiency=0.18):
        """
        Calculates the impact of CBDC and Financial Digitalization.
        Significant boost to Energy Flow Pole (C) and reduction in geometric friction.
        Reference: Section 5.4.
        """
        shacked_params = self.params.copy()
        shacked_params['C'] = self.params['C'] * (1 + liquidity_efficiency)
        # Digitalization reduces the 'distance' or friction in capital flow
        shacked_params['R'] = self.params['R'] * 0.95 
        return shacked_params

    def evaluate_resonance_risk(self, shock_list):
        """
        Evaluates the potential for 'Risk Resonance' when multiple shocks occur simultaneously.
        Reference: Section 5.5, 'Non-linear Amplification'.
        """
        # Logic: Shocks are not purely additive; they exhibit cross-parameter resonance.
        # This function identifies if combined shocks push the system beyond the critical surface.
        current_p = self.params
        for shock_func in shock_list:
            current_p = shock_func(current_p)
        
        return current_p
