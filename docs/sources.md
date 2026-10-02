 Where We Got Our Numbers & Why They Matter

This document details the empirical data sources, regulatory standards, and clinical benchmarks that parameterize our research model. It explains where each parameter originates, why healthcare cyber incidents carry disproportionate financial risk, how "Shadow AI" exacerbates containment lifecycles, and which statutory frameworks govern hospital liability.

---

## Week 1: Cyber Breach Severity, "Shadow AI" Surcharges & Statutory Ceilings

### 1. IBM Security & Ponemon Institute — *Cost of a Data Breach Report*
* **URL:** https://www.ibm.com/reports/threat-intelligence/cost-of-a-data-breach
* **Exact Evidence & Parameters Provided:**
  * **$7.42M Baseline Incident Cost ($C_{\text{base}}$):** Global average cost of a healthcare data breach.
  * **279-Day Lifecycle:** Average duration required to identify and contain a healthcare cyber breach (longest across surveyed industries).
* **Methodological Modeling Choice:**
  * The financial impact is modeled as a **Log-Normal distribution** (Min: $6.64M, Mode: $7.42M, Max: $10.93M) to account for long-tail financial exposure and high-impact catastrophe risks rather than assuming a symmetrical normal distribution.

### 2. IBM Think / Security Intelligence — *Shadow AI Has Reached the SOC: Security Teams' Blind Spots*
* **URL:** https://www.ibm.com/think/insights/shadow-ai-has-reached-soc-security-teams-blind-spots
* **Exact Evidence & Parameters Provided:**
  * **+$670,000 "Shadow AI" Surcharge ($\Delta C_{\text{shadow}}$):** Mean remediation and investigation penalty when breaches involve unvetted AI/SaaS tools.
  * **8.3% to 9.1% Financial Footprint:** Direct share of total enterprise breach cost attributable specifically to unsanctioned generative AI usage.
  * **20% to 43% Incident Involvement:** Proportion of modern enterprise cyber incidents that actively involve unapproved AI tools.
  * **97% Lack Governance:** Rate of organizations impacted by AI breaches that had zero inline safeguards or automated egress controls deployed.
* **Methodological Modeling Choice:**
  * The incremental surcharge is implemented as a **Triangular distribution** (Min: $400k, Mode: $670k, Max: $1.10M) to represent bounded escalation costs where empirical dispersion is constrained.

### 3. HHS Office for Civil Rights / Federal Register — *Civil Monetary Penalty Inflation Adjustments (45 CFR Part 102)*
* **URL:** https://www.federalregister.gov/documents/current/title-45/subtitle-A/subchapter-A/part-102
* **Exact Evidence & Parameters Provided:**
  * **$2,192,204 Statutory Penalty Ceiling ($\text{Cap}_{\text{OCR}}$):** Maximum annual civil monetary penalty under 45 CFR § 102.3 for Tier 4 "Willful Neglect" HIPAA violations per violation category.

### 4. Electronic Code of Federal Regulations — *HIPAA Privacy Rule: Business Associate Contracts (45 CFR § 164.502(e))*
* **URL:** https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502
* **Exact Evidence & Parameters Provided:**
  * **Statutory BAA Requirement:** Legal mandate establishing that transmitting unredacted Protected Health Information (PHI) to third-party commercial LLM vendors without an executed Business Associate Agreement constitutes a direct violation of federal privacy law.

---

## Week 2: Facility Stratification & Baseline Breach Frequencies

### 5. American Hospital Association (AHA) — *AHA Hospital Statistics Database*
* **URL:** https://www.aha.org/statistics
* **Exact Evidence & Parameters Provided:**
  * **Staffing Archetypes ($N_{\text{staff}}$):** Empirical clinical headcount distributions by facility tier:
    * *Community Hospital:* 80 to 180 clinicians (Mode: 120).
    * *Regional Hospital:* 800 to 2,000 clinicians (Mode: 1,200).
    * *Academic Medical Center:* 3,500 to 7,500 clinicians (Mode: 5,000).

### 6. HHS Office for Civil Rights (OCR) — *Breach Reporting Portal*
* **URL:** https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf
* **Exact Evidence & Parameters Provided:**
  * **700 to 750 Major Annual Breaches:** Federal historical baseline tracking data breaches affecting 500 or more patient records across all U.S. covered entities (~2 major incidents per calendar day).

### 7. HIPAA Journal — *Healthcare Data Breach Statistics (2009–2024)*
* **URL:** https://www.hipaajournal.com/healthcare-data-breach-statistics/
* **Exact Evidence & Methodological Clarification:**
  * **Covered Entity Aggregation:** OCR historical reporting aggregates breaches across acute care hospitals, outpatient clinics, health plans, and third-party Business Associates. Direct acute inpatient hospital incidents account for ~30% to 40% of federal filings.
  * **10% to 15% Annual Exposure Rate:** In our simulation, this range is defined as an **aggregate exposure event probability** (direct facility compromise plus third-party vendor/shadow SaaS exposure vectors associated with clinical workflows) rather than a direct, single-facility acute breach rate.
  * **90%+ Multi-Year Exposure:** Multi-year cumulative probability of a healthcare delivery system experiencing at least one security incident across its operational ecosystem.

### 8. Cyentia Institute — *Information Risk Insights Study (IRIS)*
* **URL:** https://www.cyentia.com/iris/
* **Exact Evidence & Parameters Provided:**
  * **Poisson Arrival Rate ($p_{\text{incident}} = 7.5 \times 10^{-6}$):** Calibration value for low-probability, high-frequency prompt egress risk, modeling annual unmitigated breach probability as $P(\text{Breach}) = 1 - e^{-\lambda}$.

---

## Week 3: Workforce Behavioral Adoption & Labor Opportunity Drag

### 9. Wolters Kluwer Health — *Clinicians Embrace Generative AI*
* **URL:** https://www.wolterskluwer.com/en/expert-insights/survey-finds-clinicians-embrace-generative-ai
* **Exact Evidence & Parameters Provided:**
  * **17% Direct Clinical Adoption ($U_{\text{direct}}$):** Baseline mode for clinicians routinely using unapproved generative AI tools for primary clinical charting, referral summarization, and diagnostic support.
  * **40% Peer Observation Rate:** Clinicians reporting observing peers utilizing unvetted AI in their workflows.

### 10. American Medical Association (AMA) — *Physician Sentiments on AI*
* **URL:** https://www.ama-assn.org/practice-management/digital/ama-physicians-sentiments-ai-report
* **Exact Evidence & Parameters Provided:**
  * **15% Routine Adoption Baseline:** Validated the lower boundary and mode of physician generative AI adoption across clinical specialties.
* **Methodological Modeling Choice:**
  * Clinician adoption is parameterized using a **Beta-PERT distribution** (Min: 10%, Mode: 17%, Max: 45%). Beta-PERT is used over a triangular distribution to avoid artificial kurtosis and smooth uncertainty around the empirically supported mode.

### 11. Microsoft & LinkedIn — *Work Trend Index Annual Report*
* **URL:** https://www.microsoft.com/en-us/worklab/work-trend-index/
* **Exact Evidence & Parameters Provided:**
  * **78% "Bring Your Own AI" (BYOAI):** Proportion of workforce using personal AI accounts on enterprise workstations.
  * **82% Clipboard Pasting Vector:** Proportion of employees copy-pasting internal text directly into browser AI interfaces, validating the client-side clipboard intercept architecture.

### 12. U.S. Bureau of Labor Statistics (BLS) — *OEWS & Employer Costs for Employee Compensation (ECEC)*
* **URL (OEWS):** https://www.bls.gov/oes/
* **URL (ECEC):** https://www.bls.gov/ecec/
* **Blended Clinical Compensation Formulation:**
  * Clinician opportunity wage is parameterized by blending physician and nursing mean hourly compensation from the BLS Occupational Employment and Wage Statistics (OEWS), loaded with the BLS ECEC benefits factor:
    * *Physician Mean Base Wage (BLS OEWS 29-1210/1228):* ~$125.00/hr
    * *Registered Nurse Mean Base Wage (BLS OEWS 29-1141):* ~$45.00/hr
    * *Assumed Clinical Query Mix:* 40% Physician / 60% Nurse & Advanced Practice Provider (APP)
    * *Raw Blended Wage:* $(0.40 \times \$125) + (0.60 \times \$45) = \$77.00/\text{hr}$
    * *ECEC Benefits Loading Factor:* ~1.43x (reflecting civilian/healthcare private industry benefit allocations of ~30%)
  * **Fully Loaded Clinician Opportunity Rate:** $\$77.00 \times 1.43 \approx \mathbf{\$110.11/\text{hr}}$
  * **Latency Formula:**
    $$C_{\text{latency}} = \left(\frac{\text{Annual Prompts} \times 0.080\text{ s}}{3,600\text{ s/hr}}\right) \times \$110.11/\text{hr}$$

---

## Week 4: Stochastic Risk Engine & Clinical NLP Benchmark Ingestion

### 13. Weatherhead, Golovko & McCaffrey (2026) — *Data in Brief*
* **Journal Citation:** *ASQ-PHI: An Adversarial Synthetic Data Benchmark for Clinical De-Identification and Search Utility*, *Data in Brief*, 65, 112586.
* **DOI URL:** https://doi.org/10.1016/j.dib.2026.112586
* **Repositories:** [GitHub](https://github.com/JamesWeatherhead/asq-phi) | [Mendeley Data](https://data.mendeley.com/datasets/csz5dzp7nx/1)
* **Exact Evidence & Parameters Provided:**
  * **1,051 Clinical Benchmark Prompts:** 832 PHI-positive queries and 219 adversarial hard negatives.
  * **2,973 Tagged HIPAA Entities:** Labeled across Safe Harbor categories, consolidated into `Name`, `Location`, `Date`, `Contact`, and `ID`.
  * **Dataset Splits:** Stratified into 70% train (735 prompts), 15% validation (158 prompts), and 15% test (158 prompts), preserving the 219 non-PHI hard negatives for utility testing.

### 14. Simulated Parameter Assumption: Daily Clinician Prompt Volume
* **Classification:** Explicit Modeler Assumption (Exploratory Bounds).
* **Rationale:** Because Shadow AI operates unmonitored across consumer browser interfaces without EHR integration, empirical daily prompt counts across health system staff remain unmeasured in published literature.
* **Simulation Parameter:** Modeled as a uniform exploratory range of **2 to 12 prompts per active clinician per shift**.
* **Methodological Control:** Subjected to one-way sensitivity analysis across $1\text{ to }15\text{ prompts/day}$ to evaluate model sensitivity and ensure positive return on security investment (ROSI) under low query volumes.

### 15. Simulated Parameter Assumption: Incidental PHI Prompt Density
* **Classification:** Explicit Modeler Assumption (Calibrated against Enterprise DLP Industry Benchmarks).
* **Rationale:** Replaced preliminary literature placeholders with synthetic exploratory bounds informed by enterprise Data Loss Prevention (DLP) telemetry tracking unstructured text egress.
* **Simulation Parameter:** Modeled as a bounded stochastic parameter between **15% and 40% of unsanctioned clinical queries containing incidental Safe Harbor PHI**.
* **Methodological Control:** Evaluated across a sensitivity range of $5\%\text{ to }50\%$ to confirm trust layer net savings across varying levels of clinician documentation discipline.
