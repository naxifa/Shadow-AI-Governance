# Research Methodology & Parameter Calibration

## Hospital Archetypes & Operational Profiles
Hospitals face vastly different risk levels depending on their staff size, daily workflow, and security overhead. To reflect real-world healthcare delivery, our simulation categorizes organizations into three operational tiers based on American Hospital Association (AHA) benchmarks[cite: 1]:

1. **Community Hospital (Small):** 
   * **Scale:** 80 licensed beds and approximately 500 full-time staff (FTEs)[cite: 1].
   * **Profile:** Community-oriented acute care with a lean IT team and low daily query volume[cite: 1].
2. **Regional Health System (Medium):** 
   * **Scale:** 350 licensed beds and approximately 3,500 staff[cite: 1].
   * **Profile:** Multi-specialty hospital network with moderate administrative infrastructure and higher daily prompt activity[cite: 1].
3. **Academic Medical Center (Large):** 
   * **Scale:** 1,100 licensed beds and approximately 14,000 staff[cite: 1].
   * **Profile:** High-throughput campus combining direct patient care, medical residency training, and clinical research[cite: 1].

---

## Real-World Data & Parameter Anchors
Rather than relying on arbitrary assumptions, the model grounds its variables in published empirical studies and federal statutory standards[cite: 1]:

* **Clinician Direct AI Adoption Rate ($U_{\text{direct}}$):** 
  Measures the percentage of clinical staff who directly use unapproved, external generative AI tools for work tasks[cite: 1]. Based on findings from the Wolters Kluwer survey, the baseline adoption mode is set to **17%** direct user adoption (with 40% of staff reporting that they observe unapproved AI tools in use across their organization)[cite: 1]. In our model, this rate ranges from a 10% minimum in Community hospitals to a 35% upper limit in research-heavy Academic centers.
* **Shadow AI Breach Surcharge ($\Delta C_{\text{shadow}}$):** 
  Based on IBM Security's *Cost of a Data Breach Report*, incidents involving unapproved "Shadow AI" incur an average **$670,000 penalty surcharge**[cite: 1]. This extra cost reflects extended detection windows and prolonged forensic triage[cite: 1].
* **Statutory Enforcement Penalty Ceiling ($\text{Cap}_{\text{OCR}}$):** 
  Calibrated using the HHS Office for Civil Rights (OCR) annual enforcement maximum under 45 CFR § 102.3. For Tier 4 "Willful Neglect" violations, the federal statutory penalty cap is **$2,190,294 per violation category**[cite: 1].

---

## Probability Distributions
A static single-point average fails to capture real-world operational variance and cybersecurity uncertainty. We assign three specific probability curves to model different behaviors:

1. **Beta-PERT Distributions (Human Behavior & Rates):**
   * *Variables:* Clinician AI adoption rates ($U_{\text{direct}}$) and prompt exposure probability ($P_{\text{phi}}$).
   * *Why:* Human habits naturally cluster around a central, most likely value (the mode) but have firm lower and upper limits. Beta-PERT places realistic weight on the mode while respecting boundaries.
2. **Triangular Distributions (Operational Sizing & Fixed Costs):**
   * *Variables:* Staff headcounts, daily prompt frequencies, and software licensing/deployment expenses.
   * *Why:* Vendor pricing and operational staffing are best bounded by known minimum, likely, and maximum estimates.
3. **Log-Normal Distributions (Catastrophic Breach Severity):**
   * *Variables:* Base data breach remediation expenses ($C_{\text{base}}$).
   * *Why:* Most cyber incidents incur moderate cleanup costs, but rare incidents result in multi-million dollar catastrophic liabilities. The Log-Normal curve accurately models this long, heavy tail of risk.

---

## Bounded Stochastic Hazard Function
In basic risk models, multiplying risk factors linearly can distort results—in large academic centers, high prompt counts can create mathematically invalid probabilities exceeding 100%[cite: 1].

To prevent this scale distortion, annual breach probability is modeled using a standard Poisson hazard formulation[cite: 1]:

$$P(\text{Breach} \ge 1) = 1 - e^{-\lambda}$$

Where:
* **$\lambda$ (Lambda)** is the expected number of leak events per year, calculated as:
  $$\lambda = (\text{Active Clinicians} \times \text{Annual Prompts per Clinician} \times P_{\text{phi}}) \times \lambda_{\text{leak}}$$
* **$\text{Active Clinicians}$** is defined as $\text{Staff Headcount} \times U_{\text{direct}}$.
* **$\text{Annual Prompts per Clinician}$** is calculated across a standard baseline of 250 clinical working days per year.
* **$P_{\text{phi}}$** is the probability that a submitted clinical prompt contains sensitive Protected Health Information.
* **$\lambda_{\text{leak}}$** is the empirical discovery factor that an exposed prompt triggers an external leak, audit, or reportable incident.

Under this formulation, if a small hospital has an expected leak rate of $\lambda = 0.1$, the annual breach probability is $1 - e^{-0.1} \approx 9.5\%$. If an Academic Medical Center processes high prompt volumes yielding $\lambda = 5.0$, the breach probability cleanly converges to $1 - e^{-5.0} \approx 99.3\%$. This keeps all calculated probabilities bounded between 0% and 100% regardless of institutional scale.