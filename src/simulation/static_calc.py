import pandas as pd

def run_static_baseline(csv_path="data/parameters/archetype_distributions.csv", recall_trust_layer=0.98):
    df = pd.read_csv(csv_path)
    
    print("\n" + "="*86)
    print("STATIC DETERMINISTIC BASELINE FINANCIAL ASSESSMENT (MODE VALUES)")
    print(f"Trust Layer Target Recall: {recall_trust_layer * 100:.1f}% | Discovery Hazard Factor: 0.00008")
    print("="*86)
    
    lambda_leak_factor = 0.00008
    
    for archetype in ["Community", "Regional", "Academic"]:
        arch = df[df["archetype"] == archetype].set_index("variable")
        
        n_staff = float(arch.loc["N_staff", "mode_val"])
        u_direct = float(arch.loc["U_direct", "mode_val"])
        q_prompt = float(arch.loc["Q_prompt", "mode_val"])
        p_phi = float(arch.loc["P_phi", "mode_val"])
        
        c_base = float(arch.loc["C_base", "mode_val"])
        delta_c = float(arch.loc["Delta_C_shadow", "mode_val"])
        ocr_cap = float(arch.loc["Cap_OCR", "mode_val"])
        cost_lic = float(arch.loc["Cost_license", "mode_val"])
        cost_dep = float(arch.loc["Cost_deploy", "mode_val"])
        
        # Clinical prompts containing PHI per year (250 work days)
        active_clinicians = n_staff * u_direct
        annual_phi_prompts = active_clinicians * (q_prompt * 250) * p_phi
        
        # Incident severity
        incident_severity = c_base + delta_c + ocr_cap
        
        # Unmitigated annual loss
        unmitigated_breach_rate = annual_phi_prompts * lambda_leak_factor
        ale_unmitigated = unmitigated_breach_rate * incident_severity
        
        # Mitigated annual loss
        escaped_phi_prompts = annual_phi_prompts * (1.0 - recall_trust_layer)
        mitigated_breach_rate = escaped_phi_prompts * lambda_leak_factor
        ale_mitigated = mitigated_breach_rate * incident_severity
        
        # Security Investment & ROSI
        defense_cost = cost_lic + cost_dep
        risk_reduction = ale_unmitigated - ale_mitigated
        net_savings = risk_reduction - defense_cost
        rosi = (risk_reduction - defense_cost) / defense_cost * 100
        
        print(f"\n[{archetype.upper()} HOSPITAL BASELINE]")
        print(f"  • Headcount & AI Users       : {n_staff:,.0f} staff -> {active_clinicians:,.0f} active AI users")
        print(f"  • Annual PHI Prompts Exposed : {annual_phi_prompts:,.0f} prompts/year")
        print(f"  • Single Incident Severity   : ${incident_severity:,.2f}")
        print(f"  • Expected Annual Loss (ALE) : ${ale_unmitigated:,.2f}/yr (Unmitigated) vs ${ale_mitigated:,.2f}/yr (Mitigated)")
        print(f"  • Trust Layer Deployment Cost: ${defense_cost:,.2f}/yr")
        print(f"  • Net Financial Savings      : ${net_savings:,.2f}/yr")
        print(f"  • Return on Security Invest. : {rosi:,.1f}%")

    print("\n" + "="*86 + "\n")

if __name__ == "__main__":
    run_static_baseline()