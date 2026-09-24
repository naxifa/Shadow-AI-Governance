# Where We Got Our Numbers & Why They Matter

This document details the empirical data sources, regulatory standards, and clinical benchmarks that parameterize our research model. It explains where each parameter originates, why healthcare cyber incidents carry disproportionate financial risk, how "Shadow AI" exacerbates containment lifecycles, and which statutory frameworks govern hospital liability.

---

## 1. Healthcare Data Breaches & The "Shadow AI" Surcharge

**Primary Source:** IBM Security & Ponemon Institute — *Cost of a Data Breach Report*
URL: https://www.ibm.com/reports/threat-intelligence/cost-of-a-data-breach

**Supplemental Reference:** IBM Think — *Shadow AI Has Reached the SOC: Security Teams' Blind Spots*
URL: https://www.ibm.com/think/insights/shadow-ai-has-reached-soc-security-teams-blind-spots

### Empirical Parameter Derivations

* **$7.42 Million Baseline Incident Cost (Cbase):**
  The global average cost of a healthcare data breach is $7.42 million. Healthcare has remained the costliest industry for data breaches for over a decade, driven by extensive forensic analysis, patient notification requirements, business disruption, and legal fallout.

* **+$670,000 "Shadow AI Penalty" (ΔCshadow):**
  Breaches involving unmonitored or unapproved generative AI tools incur an additional $670,000 surcharge above standard baseline recovery costs. This surcharge stems from unindexed cloud caching, lack of audit trails, and delayed discovery.

* **8.3% to 9.1% Financial Burden:**
  The direct financial footprint of Shadow AI accounts for roughly 8.3% to 9.1% of the total cost of an enterprise security incident.

* **279-Day Lifecycle:**
  The mean time to identify and contain a healthcare data breach is 279 days, or over 9 months. The absence of centralized logging in third-party browser chats significantly contributes to this discovery lag.

* **20% to 43% Incident Involvement:**
  Between 20% and 43% of enterprise cybersecurity incidents now directly involve unsanctioned artificial intelligence software.

* **97% Lack Governance Controls:**
  Approximately 97% of organizations that experienced an AI-related security incident reported having zero automated controls or real-time inline safeguards in place.

---

## 2. Regulatory Fines & Statutory Ceilings (HIPAA Enforcement)

**Primary Source:** U.S. Department of Health and Human Services (HHS) & Federal Register
Agency Portal URL: https://www.federalregister.gov/agencies/health-and-human-services-department

**Statutory Reference:** 45 CFR § 102.3 — Civil Monetary Penalty Inflation Adjustments
Annual Enforcement Schedules: https://www.federalregister.gov/documents/current/title-45/subtitle-A/subchapter-A/part-102

### Statutory Rules & Limits

* **$2,192,204 Annual Statutory Cap (CapOCR):**
  Under 45 CFR § 102.3, the HHS Office for Civil Rights (OCR) enforces annual statutory penalty limits for HIPAA non-compliance. For Tier 4 "Willful Neglect" involving unmonitored, systemic transmissions of unencrypted patient data without corrective controls, the maximum annual fine cap is adjusted to **$2,192,204 per violation category**.

* **The Business Associate Agreement (BAA) Mandate:**
  Under 45 CFR § 164.502(e), covered entities may not disclose Protected Health Information (PHI) to third-party software vendors without an executed BAA. Pasting patient narratives, lab values, or treatment plans into consumer-facing LLM browser interfaces lacks a BAA and constitutes an automatic violation of federal privacy law.

---

## 3. Hospital Incident Frequency & Industry Baselines

**Primary Source:** HHS Office for Civil Rights (OCR) Public Breach Reporting Portal
Portal URL: https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf

**Industry Benchmark & Longitudinal Tracker:** HIPAA Journal Healthcare Data Breach Statistics
Tracker URL: https://www.hipaajournal.com/healthcare-data-breach-statistics/

### Operational Frequency Derivations

* **700 to 750 Major Breaches Annually:**
  An average of 700 to 750 large-scale healthcare data breaches affecting 500 or more patient records are reported to federal authorities annually, representing approximately two major incidents every day.

* **10% to 15% Annual Hospital Breach Probability:**
  Distributed across approximately 6,000 active acute care and specialty hospitals in the United States, an individual hospital operates with an estimated **10% to 15% baseline probability** of experiencing a reportable breach in a single calendar year.

* **90%+ 3-Year Cumulative Exposure:**
  Longitudinal data reveals that over 90% of healthcare delivery organizations experience at least one security incident or reportable breach within a rolling three-year operational window.

---

## 4. Clinician Behavioral Adoption & Workflow Realities

**Primary Clinical Survey:** Wolters Kluwer Health — *Clinicians Embrace Generative AI*
Survey URL: https://www.wolterskluwer.com/en/expert-insights/survey-finds-clinicians-embrace-generative-ai

**Cross-Industry Survey:** Microsoft & LinkedIn — *Work Trend Index*
Report URL: https://www.microsoft.com/en-us/worklab/work-trend-index/

### Behavioral Parameter Derivations

* **17% Direct Clinical Adoption Baseline (Udirect):**
  While 40% of clinicians report observing colleagues utilizing unapproved AI tools, **17% directly acknowledge using unauthorized AI applications for primary clinical charting, referral summarization, and diagnostic support**. This 17% establishes the mode of our Beta-PERT adoption distribution.

* **57% to 80% Broad Healthcare & Enterprise Adoption:**
  Across broader healthcare workforces and general business functions, between 57% and 80% of staff utilize AI applications to mitigate documentation fatigue.

* **78% "Bring Your Own AI" (BYOAI):**
  Nearly 4 out of 5 knowledge workers bring unvetted, personal AI accounts to workplace workstations to accelerate daily tasks.

* **82% Direct Browser Text Pasting:**
  Approximately 82% of workers interacting with web-based generative AI admit to copy-pasting internal organizational text directly into public browser interfaces—the exact egress vector intercepted by our inline trust layer.

---

## 5. Clinical NLP Evaluation & Benchmark Dataset

* **Primary Dataset Benchmark:** ASQ-PHI (*Adversarial Synthetic Queries for Protected Health Information de-identification*)  
  **Citation:** Weatherhead, Golovko & McCaffrey (2026), *Data in Brief* 65, 112586  
  **GitHub Repository:** https://github.com/JamesWeatherhead/asq-phi  
  **Mendeley Data Repository:** https://data.mendeley.com/datasets/csz5dzp7nx/1

### Dataset Composition:

* **1,051 Total Clinical Queries:**  
  A benchmark corpus of 1,051 fully synthetic single-turn clinical prompts reflecting conversational queries submitted to generative AI interfaces.
  * **832 PHI-Positive Prompts (79.2%):** Queries containing one or more direct patient identifiers.
  * **219 Adversarial Hard Negatives (20.8%):** Queries containing zero PHI but engineered with syntactically similar medical text (e.g., ages under 90, lab measurements like "potassium 3.2 mEq/L", and drug dosages like "50 mg").

* **2,973 Tagged HIPAA Entities:**  
  Labeled across 13 core textual HIPAA Safe Harbor identifier types represented as JSON objects with exact spans and values (e.g., `NAME`, `GEOGRAPHIC_LOCATION`, `DATE`, `MEDICAL_RECORD_NUMBER`, `PHONE_NUMBER`).

* **Clinical Purpose:**  
  Evaluates model specificity against over-redaction. It prevents the filter from stripping critical medical numbers and physiological indicators, which would otherwise erode the prompt's clinical utility for downstream language models.

* **Pipeline Extensibility:**  
  The ingestion schema supports expansion into established clinical research corpora, including the i2b2/n2c2 clinical NLP challenge datasets and MIMIC-IV-Note de-identification splits.