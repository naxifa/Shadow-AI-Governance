import numpy as np
import pandas as pd

def sample_pert(low, mode, high, size=10000, lambd=4):
    """
    Beta-PERT distribution:
    Used for human habits (like clinician AI adoption rates).
    Values naturally peak near the mode (17%) while staying strictly inside min/max bounds.
    """
    alpha = 1 + lambd * (mode - low) / (high - low)
    beta = 1 + lambd * (high - mode) / (high - low)
    return low + np.random.beta(alpha, beta, size=size) * (high - low)

def sample_triangular(low, mode, high, size=10000):
    """
    Triangular distribution:
    Used for hospital sizes and operational budgets bounded by clear low, typical, and high numbers.
    """
    return np.random.triangular(left=low, mode=mode, right=high, size=size)

def sample_lognormal(min_val, mode_val, max_val, size=10000):
    """
    Log-Normal distribution:
    Used for catastrophic data breach costs where most incidents cost an average amount,
    but rare disasters create a heavy multi-million dollar tail.
    """
    mu = np.log(mode_val)
    # 3.29 covers roughly a 90% confidence span across the min-max bounds
    sigma = (np.log(max_val) - np.log(min_val)) / 3.29
    return np.random.lognormal(mean=mu, sigma=sigma, size=size)

def load_and_verify_parameters(csv_path="data/parameters/archetype_distributions.csv"):
    """
    Week 3 Sanity Check:
    Loads the parameter CSV table and verifies that all sampling curves run cleanly.
    """
    df = pd.read_csv(csv_path)
    print(f" Loaded parameter table successfully! Total parameters: {len(df)}\n")
    
    for archetype in ["Community", "Regional", "Academic"]:
        arch_df = df[df["archetype"] == archetype].set_index("variable")
        
        # 1. Staff Headcount (Triangular)
        n_staff = sample_triangular(
            float(arch_df.loc["N_staff", "min_val"]),
            float(arch_df.loc["N_staff", "mode_val"]),
            float(arch_df.loc["N_staff", "max_val"])
        )
        
        # 2. Clinician AI Adoption Rate (Beta-PERT)
        u_direct = sample_pert(
            float(arch_df.loc["U_direct", "min_val"]),
            float(arch_df.loc["U_direct", "mode_val"]),
            float(arch_df.loc["U_direct", "max_val"])
        )
        
        # 3. Base Breach Remediation Cost (Log-Normal)
        c_base = sample_lognormal(
            float(arch_df.loc["C_base", "min_val"]),
            float(arch_df.loc["C_base", "mode_val"]),
            float(arch_df.loc["C_base", "max_val"])
        )
        
        active_clinicians = n_staff * u_direct
        
        print(f"--- {archetype.upper()} HOSPITAL SANITY CHECK (10,000 Draws) ---")
        print(f"  * Mean Active AI Clinicians : {np.mean(active_clinicians):,.1f} staff")
        print(f"  * 90% Range Active Clinicians : [{np.percentile(active_clinicians, 5):,.0f} - {np.percentile(active_clinicians, 95):,.0f}]")
        print(f"  * Mean Base Breach Cost       : ${np.mean(c_base):,.2f}")
        print(f"  * Median Base Breach Cost     : ${np.median(c_base):,.2f}\n")

if __name__ == "__main__":
    load_and_verify_parameters()