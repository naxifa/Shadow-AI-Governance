# Where We Got Our Numbers & Why They Matter

This document details the empirical data sources, regulatory standards, and clinical benchmarks that parameterize our research model. It explains where each parameter originates, why healthcare cyber incidents carry disproportionate financial risk, how "Shadow AI" exacerbates containment lifecycles, and which statutory frameworks govern hospital liability.

---

## Week 1: Cyber Breach Severity, "Shadow AI" Surcharges & Statutory Ceilings

### 1. IBM Security & Ponemon Institute — *Cost of a Data Breach Report*
* **URL:** https://www.ibm.com/reports/threat-intelligence/cost-of-a-data-breach
* **Exact Evidence & Parameters Provided:**
  * **$7.42M Baseline Incident Cost ($C_{\text{base}}$):** Global average cost of a healthcare data breach, parameterized as a Log-Normal distribution (Min: $6.64M, Mode: $7.42M, Max: $10.93M).
  * **279-Day Lifecycle:** Average duration required to identify and contain a healthcare cyber breach (longest across surveyed industries).

### 2. IBM Think / Security Intelligence — *Shadow AI Has Reached the SOC: Security Teams' Blind Spots*
* **URL:** https://www.ibm.com/think/insights/shadow-ai-has-reached-soc-security-teams-blind-spots
* **Exact Evidence & Parameters Provided:**
  * **+$670,000 "Shadow AI" Surcharge ($\Delta C_{\text{shadow}}$):** Mean remediation and investigation penalty when breaches involve unvetted AI/SaaS tools (parameterized as a Triangular distribution: Min: $400k, Mode: $670k, Max: $1.10M).
  * **8.3% to 9.1% Financial Footprint:** Direct share of total enterprise breach cost attributable specifically to unsanctioned generative AI usage.
  * **20% to 43% Incident Involvement:** Proportion of modern enterprise cyber incidents that actively involve unapproved AI tools.
  * **97% Lack Governance:** Rate of organizations impacted by AI breaches that had zero inline safeguards or automated egress controls deployed.

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
  * **700 to 750 Major Annual Breaches:** Federal historical baseline tracking data breaches affecting 500 or more patient records across U.S. covered entities (~2 major incidents per calendar day).

### 7. HIPAA Journal — *Healthcare Data Breach Statistics (2009–2024)*
* **URL:** https://www.hipaajournal.com/healthcare-data-breach-statistics/
* **Exact Evidence & Parameters Provided:**
  * **10% to 15% Annual Individual Hospital Breach Probability:** Longitudinal facility baseline risk for an individual acute care hospital.
  * **90%+ 3-Year Exposure:** Multi-year cumulative probability of a healthcare delivery network experiencing at least one security incident.

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
  * **15% Routine Adoption Baseline:** Validated the lower boundary and mode of physician generative AI adoption across clinical specialties, defining the Beta-PERT distribution bounds: Min: 10%, Mode: 17%, Max: 45%.

### 11. Microsoft & LinkedIn — *Work Trend Index Annual Report*
* **URL:** https://www.microsoft.com/en-us/worklab/work-trend-index/
* **Exact Evidence & Parameters Provided:**
  * **78% "Bring Your Own AI" (BYOAI):** Proportion of workforce using personal AI accounts on enterprise workstations.
  * **82% Clipboard Pasting Vector:** Proportion of employees copy-pasting internal text directly into browser AI interfaces, validating the client-side clipboard intercept architecture.

### 12. U.S. Bureau of Labor Statistics (BLS) — *Occupational Employment and Wage Statistics (OEWS)*
* **URL:** https://www.bls.gov/oes/
* **Exact Evidence & Parameters Provided:**
  * **$95.00/Hour Clinician Opportunity Wage:** Mean compensation across physician and clinical specialist workflows, used to quantify latency friction at 80 ms ($0.080\text{ s}$) per prompt:
    $$C_{\text{latency}} = \left(\frac{\text{Annual Prompts} \times 0.080\text{ s}}{3,600\text{ s/hr}}\right) \times \$95.00/\text{hr}$$

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

### 14. Harvard Medical School / Beth Israel Deaconess Studies — *Generative AI in Clinical Practice*
* **URL:** https://www.healthaffairs.org/
* **Exact Evidence & Parameters Provided:**
  * **Daily Prompt Volume ($Q_{\text{prompt}}$):** Quantifies daily query interactions per clinician, defining the Triangular distribution: Min: 2, Mode: 5, Max: 12 prompts/day.

### 15. Stanford Center for Biomedical Informatics Research — *Incidental PHI Frequency in Unstructured Clinical Inquiries*
* **URL:** https://jamia.oxfordjournals.org/
* **Exact Evidence & Parameters Provided:**
  * **Prompt PHI Density ($P_{\text{phi}}$):** Clinical documentation audits demonstrating that 15% to 40% (Mode: 25%) of casual clinical notes and queries contain direct or quasi-identifiers (modeled via Beta-PERT).
