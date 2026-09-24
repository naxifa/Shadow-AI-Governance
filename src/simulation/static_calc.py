import math
import pandas as pd

def run_static_baseline(
    csv_path="data/parameters/archetype_distributions.csv",
    recall_trust_layer=0.98,        # The filter catches 98% of patient identifiers
    p_breach_given_phi=0.008,       # 0.8% chance a leaked prompt causes a real audit/breach
    filter_latency_sec=0.080,       # 80 milliseconds of delay added by the filter
    hourly_clinical_wage=95.0       # Average doctor/nurse pay per hour ($95/hr)
):
    # Step 1: Load hospital size and cost numbers from the CSV file
    df = pd.read_csv(csv_path)
    
    print("\n" + "=" * 90)
    print("BASELINE HOSPITAL FINANCIAL RISK CALCULATOR")
    print(f"Filter Accuracy: {recall_trust_layer * 100:.1f}% | Prompt Delay: {filter_latency_sec * 1000:.0f} ms")
    print("=" * 90)
    
    # Run the exact same calculations for each hospital type
    for archetype in ["Community", "Regional", "Academic"]:
        arch = df[df["archetype"] == archetype].set_index("variable")
        
        # --- Grab baseline numbers for this hospital ---
        n_staff = float(arch.loc["N_staff", "mode_val"])           # Total hospital workers
        u_direct = float(arch.loc["U_direct", "mode_val"])         # % of staff secretly using AI (17%)
        q_prompt = float(arch.loc["Q_prompt", "mode_val"])         # AI questions asked per doctor per day
        p_phi = float(arch.loc["P_phi", "mode_val"])               # % of prompts that accidentally include patient data (~3%)
        
        c_base = float(arch.loc["C_base", "mode_val"])             # Standard breach cleanup cost ($7.42M)
        delta_c = float(arch.loc["Delta_C_shadow", "mode_val"])    # Extra cleanup cost for unapproved AI ($670k)
        ocr_cap = float(arch.loc["Cap_OCR", "mode_val"])           # Max government fine cap ($2.19M)
        cost_lic = float(arch.loc["Cost_license", "mode_val"])     # Software subscription price per year
        cost_dep = float(arch.loc["Cost_deploy", "mode_val"])      # One-time IT installation cost
        
        # --- Step 2: How many prompts are staff typing each year? ---
        # 250 standard working days in a hospital year
        active_clinicians = n_staff * u_direct
        annual_total_prompts = active_clinicians * (q_prompt * 250)
        annual_phi_prompts = annual_total_prompts * p_phi          # Prompts that leak private patient info
        
        # --- Step 3: What does ONE single breach cost the hospital? ---
        # Base cleanup + Shadow AI penalty + government fine
        incident_severity = c_base + delta_c + ocr_cap
        
        # --- Step 4: What happens if the hospital does NOTHING? (Unmitigated) ---
        # Calculate expected leaks per year (Lambda)
        lambda_unmitigated = annual_phi_prompts * p_breach_given_phi
        
        # Poisson probability formula: keeps the chance cleanly between 0% and 100%
        p_breach_unmitigated = 1.0 - math.exp(-lambda_unmitigated)
        
        # Expected Annual Loss = Probability of breach * Total cost of breach
        ale_unmitigated = p_breach_unmitigated * incident_severity
        
        # --- Step 5: What happens when we turn on the safety filter? (Mitigated) ---
        # The filter catches 98%, so only 2% slip past
        lambda_mitigated = lambda_unmitigated * (1.0 - recall_trust_layer)
        p_breach_mitigated = 1.0 - math.exp(-lambda_mitigated)
        ale_mitigated = p_breach_mitigated * incident_severity
        
        # --- Step 6: What is the Total Cost of Ownership (TCO)? ---
        # Account for doctor time lost waiting for the 80ms filter to scan text
        lost_hours = (annual_total_prompts * filter_latency_sec) / 3600.0
        cost_latency = lost_hours * hourly_clinical_wage
        
        # Total cost = Software license + IT setup + lost clinician time
        tco = cost_lic + cost_dep + cost_latency
        
        # --- Step 7: Does the safety filter pay for itself? (ROSI) ---
        risk_reduction = ale_unmitigated - ale_mitigated            # Money saved by stopping breaches
        net_savings = risk_reduction - tco                          # Savings minus what the software cost
        rosi = (net_savings / tco) * 100.0                          # Return on Security Investment (%)
        
        # Print out the results in clean dollar amounts
        print(f"\n[{archetype.upper()} HOSPITAL]")
        print(f"  • Staffing: {n_staff:,.0f} total staff -> {active_clinicians:,.0f} using AI tools")
        print(f"  • AI Prompts Sent: {annual_total_prompts:,.0f}/yr ({annual_phi_prompts:,.0f} contain private patient info)")
        print(f"  • Cost If Breached Once: ${incident_severity:,.2f}")
        print(f"  • Annual Breach Risk: {p_breach_unmitigated * 100:.1f}% chance without safety filter -> {p_breach_mitigated * 100:.2f}% chance with filter")
        print(f"  • Expected Annual Loss: \({ale_unmitigated:,.2f}/yr without filter ->\){ale_mitigated:,.2f}/yr with filter")
        print(f"  • Cost of Latency (Doctor Time Lost): ${cost_latency:,.2f}/yr ({filter_latency_sec * 1000:.0f} ms per prompt)")
        print(f"  • Total Cost to Run Filter: ${tco:,.2f}/yr")
        print(f"  • Net Financial Savings: ${net_savings:,.2f}/yr")
        print(f"  • Return on Investment (ROSI): {rosi:,.1f}%")

    print("\n" + "=" * 90 + "\n")

if __name__ == "__main__":
    run_static_baseline()