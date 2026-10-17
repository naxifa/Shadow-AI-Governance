import pandas as pd
import numpy as np

# Load the breach dataset
df = pd.read_excel("data/raw/breach_report.xls")

# Filter for healthcare providers
providers = df[df["Covered Entity Type"] == "Healthcare Provider"].copy()
records = pd.to_numeric(providers["Individuals Affected"], errors="coerce").dropna()

print("\n" + "=" * 60)
print("EMPIRICAL BREACH RECORDS DISTRIBUTION (HHS OCR 2026)")
print("=" * 60)
print(f"Total Healthcare Provider Incidents: {len(records)}")
print(f"25th Percentile: {int(np.percentile(records, 25)):,} records")
print(f"Median (50th):   {int(np.median(records)):,} records")
print(f"75th Percentile: {int(np.percentile(records, 75)):,} records")
print(f"90th Percentile: {int(np.percentile(records, 90)):,} records")
print(f"Mean Exposure:   {int(np.mean(records)):,} records")
print("=" * 60 + "\n")
