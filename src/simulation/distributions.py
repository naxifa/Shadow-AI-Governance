import os
import json
from datetime import datetime
import numpy as np
import pandas as pd

# ==============================================================================
# 1. PARAMETRIC PROBABILITY DISTRIBUTIONS
# ==============================================================================

def sample_pert(low, mode, high, size=10000, lambd=4.0):
    """Beta-PERT distribution for bounded human behavioral rates."""
    alpha = 1.0 + lambd * (mode - low) / (high - low)
    beta = 1.0 + lambd * (high - mode) / (high - low)
    return low + np.random.beta(alpha, beta, size=size) * (high - low)

def sample_triangular(low, mode, high, size=10000):
    """Triangular distribution for bounded operational parameters."""
    return np.random.triangular(left=low, mode=mode, right=high, size=size)

def sample_lognormal(min_val, mode_val, max_val, size=10000):
    """Log-Normal distribution for heavy-tailed cybersecurity losses."""
    mu = np.log(mode_val)
    sigma = (np.log(max_val) - np.log(min_val)) / 3.29
    return np.random.lognormal(mean=mu, sigma=sigma, size=size)

# ==============================================================================
# 2. MONTE CARLO SIMULATION & PERSISTENCE
# ==============================================================================

RESULTS_DIR = "data/results"
RESULTS_CSV_PATH = os.path.join(RESULTS_DIR, "monte_carlo_summary.csv")
RESULTS_JSON_PATH = os.path.join(RESULTS_DIR, "monte_carlo_summary.json")

def run_monte_carlo(
    csv_path="data/parameters/archetype_distributions.csv",
    trials=10000,
    recall_trust_layer=0.98,
    p_incident_per_phi_prompt=7.5e-6,
    filter_latency_sec=0.080,
    hourly_clinical_wage=95.0,
    seed=42,
    save_results=True
):
    """
    Executes 10,000 stochastic trials and returns a summary DataFrame.
    Automatically persists results to disk to avoid re-running simulations.
    """
    np.random.seed(seed)
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Configuration file not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    print("\n" + "=" * 92)
    print("WEEK 4 MONTE CARLO RISK SIMULATION (10,000 TRIALS PER ARCHETYPE)")
    print(f"Calibration: Recall = {recall_trust_layer*100:.1f}% | Latency Drag = {filter_latency_sec*1000:.0f}ms | Wage = ${hourly_clinical_wage:.0f}/hr")
    print("=" * 92)

    results_table = []

    for archetype in ["Community", "Regional", "Academic"]:
        arch = df[df["archetype"] == archetype].set_index("variable")

        # Stochastic Variable Draws
        n_staff = sample_triangular(
            float(arch.loc["N_staff", "min_val"]),
            float(arch.loc["N_staff", "mode_val"]),
            float(arch.loc["N_staff", "max_val"]),
            size=trials
        )
        u_direct = sample_pert(
            float(arch.loc["U_direct", "min_val"]),
            float(arch.loc["U_direct", "mode_val"]),
            float(arch.loc["U_direct", "max_val"]),
            size=trials
        )
        q_prompt = sample_triangular(
            float(arch.loc["Q_prompt", "min_val"]),
            float(arch.loc["Q_prompt", "mode_val"]),
            float(arch.loc["Q_prompt", "max_val"]),
            size=trials
        )
        p_phi = sample_pert(
            float(arch.loc["P_phi", "min_val"]),
            float(arch.loc["P_phi", "mode_val"]),
            float(arch.loc["P_phi", "max_val"]),
            size=trials
        )
        c_base = sample_lognormal(
            float(arch.loc["C_base", "min_val"]),
            float(arch.loc["C_base", "mode_val"]),
            float(arch.loc["C_base", "max_val"]),
            size=trials
        )
        delta_c = sample_triangular(
            float(arch.loc["Delta_C_shadow", "min_val"]),
            float(arch.loc["Delta_C_shadow", "mode_val"]),
            float(arch.loc["Delta_C_shadow", "max_val"]),
            size=trials
        )
        ocr_cap = float(arch.loc["Cap_OCR", "mode_val"])
        cost_lic = sample_triangular(
            float(arch.loc["Cost_license", "min_val"]),
            float(arch.loc["Cost_license", "mode_val"]),
            float(arch.loc["Cost_license", "max_val"]),
            size=trials
        )
        cost_deploy = sample_triangular(
            float(arch.loc["Cost_deploy", "min_val"]),
            float(arch.loc["Cost_deploy", "mode_val"]),
            float(arch.loc["Cost_deploy", "max_val"]),
            size=trials
        )

        # Operational Calculations
        active_clinicians = n_staff * u_direct
        annual_prompts = active_clinicians * (q_prompt * 250)
        phi_prompts = annual_prompts * p_phi
        incident_severity = c_base + delta_c + ocr_cap

        # Poisson Arrival Modeling
        lambda_unmitigated = phi_prompts * p_incident_per_phi_prompt
        p_breach_unmitigated = 1.0 - np.exp(-lambda_unmitigated)
        ale_unmitigated = p_breach_unmitigated * incident_severity

        lambda_mitigated = lambda_unmitigated * (1.0 - recall_trust_layer)
        p_breach_mitigated = 1.0 - np.exp(-lambda_mitigated)
        ale_mitigated = p_breach_mitigated * incident_severity

        cost_latency = (annual_prompts * filter_latency_sec / 3600.0) * hourly_clinical_wage
        tco = cost_lic + cost_deploy + cost_latency

        risk_reduction = ale_unmitigated - ale_mitigated
        net_savings = risk_reduction - tco
        rosi = (net_savings / tco) * 100.0

        # Percentile Logging
        print(f"\n[{archetype.upper()} HOSPITAL ARCHETYPE]")
        print(f"  • Unmitigated Breach Prob : {np.median(p_breach_unmitigated)*100:5.2f}%  [5th: {np.percentile(p_breach_unmitigated, 5)*100:5.2f}% | 95th: {np.percentile(p_breach_unmitigated, 95)*100:5.2f}%]")
        print(f"  • Mitigated Breach Prob   : {np.median(p_breach_mitigated)*100:5.2f}%  [5th: {np.percentile(p_breach_mitigated, 5)*100:5.2f}% | 95th: {np.percentile(p_breach_mitigated, 95)*100:5.2f}%]")
        print(f"  • Annual ALE (Baseline)   : \({np.median(ale_unmitigated):>11,.2f}  [5th:\){np.percentile(ale_unmitigated, 5):>9,.2f} | 95th: ${np.percentile(ale_unmitigated, 95):>11,.2f}]")
        print(f"  • Annual ALE (Mitigated)  : \({np.median(ale_mitigated):>11,.2f}  [5th:\){np.percentile(ale_mitigated, 5):>9,.2f} | 95th: ${np.percentile(ale_mitigated, 95):>11,.2f}]")
        print(f"  • 3-Part Annual TCO       : ${np.median(tco):>11,.2f}")
        print(f"  • Net Financial Savings   : \({np.median(net_savings):>11,.2f}  [5th:\){np.percentile(net_savings, 5):>9,.2f} | 95th: ${np.percentile(net_savings, 95):>11,.2f}]")
        print(f"  • Empirical Net ROSI      : {np.median(rosi):>10.1f}%  [5th: {np.percentile(rosi, 5):>7.1f}% | 95th: {np.percentile(rosi, 95):>9.1f}%]")

        results_table.append({
            "archetype": archetype,
            "annual_prompts_median": int(np.median(annual_prompts)),
            "p_breach_unmit_median": float(np.median(p_breach_unmitigated)),
            "p_breach_mit_median": float(np.median(p_breach_mitigated)),
            "ale_unmit_median": float(np.median(ale_unmitigated)),
            "ale_mit_median": float(np.median(ale_mitigated)),
            "tco_median": float(np.median(tco)),
            "net_savings_p5": float(np.percentile(net_savings, 5)),
            "net_savings_median": float(np.median(net_savings)),
            "net_savings_p95": float(np.percentile(net_savings, 95)),
            "rosi_p5": float(np.percentile(rosi, 5)),
            "rosi_median": float(np.median(rosi)),
            "rosi_p95": float(np.percentile(rosi, 95))
        })

    summary_df = pd.DataFrame(results_table)

    # Automated Persistence Layer
    if save_results:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        summary_df.to_csv(RESULTS_CSV_PATH, index=False)
        
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "trials": trials,
            "recall": recall_trust_layer,
            "filter_latency_sec": filter_latency_sec,
            "results": results_table
        }
        with open(RESULTS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
            
        print(f"\n Results saved to:\n  • {RESULTS_CSV_PATH}\n  • {RESULTS_JSON_PATH}")

    print("\n" + "=" * 92)
    return summary_df

# ==============================================================================
# 3. CONVENIENT ACCESS HELPER FOR FUTURE WEEKS
# ==============================================================================

def get_latest_results(force_rerun=False):
    """
    Retrieves latest simulation figures without re-running the 10,000 trials.
    If results don't exist yet, it automatically runs the simulation once.
    """
    if not force_rerun and os.path.exists(RESULTS_CSV_PATH):
        return pd.read_csv(RESULTS_CSV_PATH)
    return run_monte_carlo(save_results=True)

if __name__ == "__main__":
    run_monte_carlo()