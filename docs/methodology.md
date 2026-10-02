# Research Methodology & Parameter Calibration

## 1. Focus Scope: Real-Time Conversational Prompts vs. Static Files

This methodology specifically targets the cybersecurity, compliance, and clinical workflow risks of **ephemeral, browser-based text pastes** where healthcare workers copy unstructured clinical narratives directly into web-based conversational AI chatbots (such as ChatGPT) [@cyberhaven_shadow_ai_2023].

Unlike legacy Data Loss Prevention (DLP) tools engineered to inspect static files and perimeter egress (such as PDFs, spreadsheets, email attachments, or USB transfers) [@garnter_dlp_market_2023], our architecture operates as an **inline, bidirectional prompt-sanitization trust layer**. It intercepts text at the browser input level in real time, extracts Protected Health Information (PHI), and maps sensitive entities to consistent synthetic surrogates while preserving critical numerical lab values, vitals, and medication dosages [@asq_phi_benchmark_2024]. Upon receiving the external LLM’s response, the gateway reconstructs the original entities via an ephemeral session state, enabling clinical utility without transmitting unencrypted PHI beyond institutional boundaries.

---

## 2. Research Architecture & Unified Scope

This study intentionally decouples the real-time sanitization gateway from downstream institutional risk modeling. The technical trust layer operates as an inline, context-preserving sanitization engine—performing real-time entity extraction, synthetic surrogate substitution, and session-state re-identification on response return—while institutional risk, regulatory penalties, and Return on Security Investment (ROSI) are evaluated downstream within a deterministic, auditable simulation matrix.

| Research Dimension | Technical Component (Trust Layer & ML Pipeline) | Economic Component (Decision-Analytic Simulation) |
| :--- | :--- | :--- |
| **Domain** | Clinical NLP / Open-Source LLM Fine-Tuning [@dettmers_qlora_2023] | Health Informatics / Cybersecurity Economics [@gordon_loeb_model_2002] |
| **Core Target** | Real-time browser text pastes & conversational prompts (not static files/PDFs) [@cyberhaven_shadow_ai_2023] | Hospital financial risk & budget modeling [@aha_hospital_statistics_2023] |
| **Primary Focus** | Dataset ingestion, PEFT/QLoRA fine-tuning, real-time prompt interception, bidirectional surrogate substitution, session-state re-identification | Stochastic financial simulation, Poisson breach estimation, TCO modeling |
| **Target Metrics** | Redaction Recall ($R$), Precision, F1-Score, Roundtrip Latency ($\Delta t_{\text{total}}$ in ms), Hard Negative Specificity | Annual Loss Expectancy (ALE), Cost of Inaction (COI), TCO, Net ROSI (%) |
| **Core Deliverable** | Fine-tuned open-source model pipeline with bidirectional surrogate substitution and session-state re-identification (Python/FastAPI) and evaluation benchmarks on ASQ-PHI [@asq_phi_benchmark_2024] | 10,000-trial Monte Carlo risk simulation engine, Hospital Decision Tables, Break-Even Frontier curves |

---

## 3. Hospital Archetypes & Operational Profiles

Hospitals face vastly different risk exposures depending on workforce headcount, daily clinical prompt activity, and operational overhead. To reflect real-world healthcare delivery, our simulation categorizes organizations into three operational tiers based on American Hospital Association (AHA) benchmarks [@aha_hospital_statistics_2023]:

1. **Community Hospital (Small):**
   * **Scale:** 80 licensed beds and approximately 500 full-time staff (FTEs).
   * **Profile:** Community-oriented acute care with a lean IT team and lower daily prompt activity.

2. **Regional Health System (Medium):**
   * **Scale:** 350 licensed beds and approximately 3,500 staff.
   * **Profile:** Multi-specialty hospital network with moderate administrative infrastructure and higher daily prompt volume.

3. **Academic Medical Center (Large):**
   * **Scale:** 1,100 licensed beds and approximately 14,000 staff.
   * **Profile:** High-throughput campus combining direct tertiary patient care, medical residency training, and clinical research.

---

## 4. Empirical Parameter Calibration & Baseline Matrix

The model grounds its variables in published empirical literature, federal statutory standards, and healthcare economic benchmarks [@ibm_cost_data_breach_2023; @wolters_kluwer_2023; @hhs_ocr_penalty_inflation_2023; @aha_hospital_statistics_2023; @bls_healthcare_wages_2023]:

### Table 1: Empirical Parameters and Stochastic Distribution Calibration

| Parameter Description | Symbol | Baseline / Mode | Calibrated Distribution Bounds | Primary Source / Regulatory Anchor |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline Breach Remediation Cost** | $C_{\text{base}}$ | \$7,420,000 | Log-Normal ($\mu=15.82, \sigma=0.38$) | IBM Security Cost of a Data Breach Report [@ibm_cost_data_breach_2023] |
| **Shadow AI Breach Penalty Surcharge** | $\Delta C_{\text{shadow}}$ | \$670,000 | Triangular (Min: \$450k, Mode: \$670k, Max: \$900k) | IBM Security Cost of a Data Breach Report [@ibm_cost_data_breach_2023] |
| **HIPAA Tier 4 Statutory Penalty Ceiling** | $\text{Cap}_{\text{OCR}}$ | \$2,192,204 | Fixed Statutory Ceiling per Category | HHS OCR 45 CFR § 102.3 Inflation Adjustment [@hhs_ocr_penalty_inflation_2023] |
| **Direct Clinician Shadow AI Adoption** | $U_{\text{direct}}$ | 17.0% | Beta-PERT (Min: 10.0%, Mode: 17.0%, Max: 57.0%) | Wolters Kluwer Survey [@wolters_kluwer_2023]; Cyberhaven [@cyberhaven_shadow_ai_2023] |
| **Prompt PHI Exposure Probability** | $P_{\text{phi}}$ | 3.0% | Beta-PERT (Min: 1.0%, Mode: 3.0%, Max: 8.0%) | Cyberhaven Telemetry [@cyberhaven_shadow_ai_2023]; Weber et al. [@weber_clinical_nlp_deid_2021] |
| **Actionable Breach Probability given PHI** | $P(\text{breach} \mid \text{phi})$ | 0.8% | Beta-PERT (Min: 0.2%, Mode: 0.8%, Max: 2.0%) | HHS OCR Breach Registry [@hhs_ocr_breach_portal]; Ponemon [@ponemon_cybersecurity_healthcare_2023] |
| **Mean Daily Prompts per Active User** | $Q_{\text{prompt}}$ | 4.0 prompts | Triangular (Min: 2.0, Mode: 4.0, Max: 8.0) | Clinical Charting Studies [@sinsky_physician_ehr_time_2016; @patel_chatgpt_clinical_accuracy_2023] |
| **Annual Clinical Working Days** | $D_{\text{annual}}$ | 250 days | Fixed Constant (50 weeks $\times$ 5 shifts) | Standard Operational Schedule [@aha_hospital_statistics_2023] |
| **Community Hospital Headcount** | $N_{\text{staff, Comm}}$ | 500 FTEs | Triangular (Min: 400, Mode: 500, Max: 650) | AHA Hospital Statistics Database [@aha_hospital_statistics_2023] |
| **Regional Health System Headcount** | $N_{\text{staff, Reg}}$ | 3,500 FTEs | Triangular (Min: 2,800, Mode: 3,500, Max: 4,200) | AHA Hospital Statistics Database [@aha_hospital_statistics_2023] |
| **Academic Medical Center Headcount** | $N_{\text{staff, Acad}}$ | 14,000 FTEs | Triangular (Min: 11,500, Mode: 14,000, Max: 17,000) | AHA Hospital Statistics Database [@aha_hospital_statistics_2023] |
| **Weighted Clinical Hourly Wage** | $W_{\text{clinical}}$ | \$85.00 / hr | Triangular (Min: \$65.00, Mode: \$85.00, Max: \$120.00) | U.S. Bureau of Labor Statistics Healthcare Wages [@bls_healthcare_wages_2023] |
| **Gateway Roundtrip Latency** | $\Delta t_{\text{total}}$ | Empirical ms | Parametric Sweep: 50 ms to 1,500 ms | Measured Pipeline Performance [@dettmers_qlora_2023] |
| **Model De-Identification Recall** | $R$ | Empirical % | Parametric Sweep: 70.0% to 99.9% | ASQ-PHI Benchmark Evaluation Split [@asq_phi_benchmark_2024] |

---

## 5. Clinical Data Curation & LLM Fine-Tuning Pipeline

### 5.1 Training & Evaluation Corpora
* **ASQ-PHI Benchmark Anchor:** The primary evaluation benchmark is anchored on the **1,051-query ASQ-PHI dataset**, comprising 2,973 tagged HIPAA Safe Harbor entities mapped into 5 core entity categories: `NAME`, `LOCATION`, `DATE`, `CONTACT`, and `ID` [@asq_phi_benchmark_2024; @hhs_hipaa_privacy_rule].
* **Adversarial Hard Negatives:** Crucially includes **219 clinical hard negatives**—prompts containing complex physiological values, lab results, and medication dosages (e.g., serum potassium $4.2\text{ mEq/L}$, fasting glucose $110\text{ mg/dL}$, or $50\text{ mg}$ dosing intervals) with zero PHI [@asq_phi_benchmark_2024]. This ensures the model learns not to over-redact critical diagnostic numbers.
* **Extensibility:** The ingestion pipeline is structured modularly, allowing seamless incorporation of additional clinical corpora (such as the i2b2/n2c2 clinical de-identification challenge sets [@dernoncourt_deidentification_2017] and MIMIC-IV-Note subsets [@johnson_mimic_deid_2016]) into the instruction-tuning schema.
* **Dataset Partitioning:** Standard 70/15/15 stratified train, validation, and test split.

### 5.2 Model Architecture & Fine-Tuning
* **Base Architectures:** Fine-tuning an open-source foundation model (e.g., Llama 3 8B or Mistral 7B) optimized for on-premises hospital deployment [@dettmers_qlora_2023].
* **Adaptation Method:** Parameter-Efficient Fine-Tuning (PEFT) via QLoRA (Quantized Low-Rank Adaptation) using 4-bit NormalFloat (NF4) quantization and double quantization [@dettmers_qlora_2023]. This yields high contextual entity identification on unstructured conversational clinical prompts while maintaining a compact memory footprint for local hospital inference.

### 5.3 Inline Bidirectional Sanitization & De-Identification Engine
Instead of destructive permanent redaction or binary prompt blocking, the gateway executes an automated, context-preserving substitution loop [@asq_phi_benchmark_2024]:

```text
Clinician Prompt (Contains PHI)
         │
         ▼
[ Step A: Local LLM Inspection & Token Extraction (QLoRA) ]
         │
         ▼
[ Step B: Synthetic Surrogate Swapping ] ──► Stores Mappings in Ephemeral Session Cache
         │                                   (e.g., "John Doe" ↔ [PATIENT_A])
         ▼
Sanitized Prompt (Dispatched to External API)
         │
         ▼
[ Commercial LLM (ChatGPT / Claude) ]
         │
         ▼
LLM Completion (References [PATIENT_A])
         │
         ▼
[ Step C: Stateful Re-Identification ] ◄── Restores Original Entities via Session Table
         │
         ▼
Clinician Receives Full, Clinically Coherent Narrative

* **Step A (Outbound Token Extraction):** Real-time entity classification evaluates browser text pastes before outbound HTTP requests leave the institutional boundary.
* **Step B (Context-Preserving Surrogate Replacement):** Replaces identified PHI with consistent, category-specific synthetic surrogates (e.g., `John Doe` $\rightarrow$ `[PATIENT_A]`, `St. Jude` $\rightarrow$ `[HOSPITAL_B]`, `04/12/1982` $\rightarrow$ `[DATE_1]`). All physiological vitals, lab values, and clinical relationships remain untouched. Mappings are held in volatile RAM within an encrypted, short-lived session table.
* **Step C (Inbound Session Re-Identification):** As the external LLM streams its response back containing synthetic surrogates, the gateway intercepts the stream, replaces surrogates with the original clinical entities, and renders the complete clinical narrative to the clinician's interface.

---

## 6. Probability Distributions

A static single-point average fails to capture real-world operational variance and cybersecurity tail risk [@gordon_loeb_model_2002]. We assign three specific probability curves to model operational and financial parameters:

1. **Beta-PERT Distributions (Human Behavior & Rates):**
   * *Variables:* Clinician AI adoption rates ($U_{\text{direct}}$) and prompt exposure probability ($P_{\text{phi}}$).
   * *Rationale:* Human habits naturally cluster around an empirical mode with bounded minimum and maximum limits. Beta-PERT weights the empirical mode smoothly while respecting operational boundaries [@vose_risk_analysis_2008].

2. **Triangular Distributions (Operational Sizing & Fixed Costs):**
   * *Variables:* Staff headcounts ($N_{\text{staff}}$), daily prompt frequencies ($Q_{\text{prompt}}$), and software expenses.
   * *Rationale:* Institutional staffing and enterprise infrastructure costs are best bounded by known minimum, likely, and maximum estimates [@vose_risk_analysis_2008].

3. **Log-Normal Distributions (Catastrophic Breach Severity):**
   * *Variables:* Base data breach remediation expenses ($C_{\text{base}}$).
   * *Rationale:* Most security incidents incur moderate triage costs, but rare events result in multi-million-dollar catastrophic liabilities. The Log-Normal curve accurately models this long, heavy right tail [@ibm_cost_data_breach_2023; @gordon_loeb_model_2002].

---

## 7. Mathematical Formulation

### 7.1 Bounded Stochastic Hazard Function
Linear multiplication of risk factors distorts results at scale—in large academic centers, high prompt volumes produce mathematically invalid probabilities exceeding 100%.

To eliminate scale distortion, annual breach probability is modeled via a non-linear Poisson hazard formulation [@ross_probability_models_2014]:

$$P(\text{Breach} \ge 1) = 1 - e^{-\lambda}$$

Where:

$$\lambda = N_{\text{staff}} \times U_{\text{direct}} \times Q_{\text{prompt}} \times D_{\text{annual}} \times P_{\text{phi}} \times P(\text{breach} \mid \text{phi})$$

* **$N_{\text{staff}}$:** Total hospital workforce headcount [@aha_hospital_statistics_2023].
* **$U_{\text{direct}}$:** Clinician shadow AI adoption rate (baseline mode = 17%, range = 10% to 57%) [@wolters_kluwer_2023].
* **$Q_{\text{prompt}}$:** Mean daily prompts per active clinician across a standard $D_{\text{annual}} = 250$ clinical working days per year [@sinsky_physician_ehr_time_2016].
* **$P_{\text{phi}}$:** Probability that an unmonitored prompt contains Protected Health Information (~3%) [@cyberhaven_shadow_ai_2023].
* **$P(\text{breach} \mid \text{phi})$:** Conditional probability that outbound PHI exposure triggers an actionable, reportable breach event (~0.8%) [@hhs_ocr_breach_portal].

### 7.2 Cost of Inaction (COI) Formula
The unmitigated annualized financial risk incurred by a hospital operating without AI governance [@gordon_loeb_model_2002]:

$$\text{COI} = \text{ALE}_{\text{breach}} + \mathbb{E}[\text{HIPAA Penalties}] + \text{Cost}_{\text{forensics}} + \text{Spend}_{\text{shadow\_saas}}$$

Where:

$$\text{ALE}_{\text{breach}} = P(\text{Breach} \ge 1) \times (C_{\text{base}} + \Delta C_{\text{shadow}})$$

* $C_{\text{base}}$ is sampled around the empirical baseline (\$7.42M) [@ibm_cost_data_breach_2023].
* $\Delta C_{\text{shadow}}$ is the Shadow AI penalty surcharge (\$670k) [@ibm_cost_data_breach_2023].
* Expected statutory HIPAA penalties are constrained by the Tier 4 "Willful Neglect" cap $\text{Cap}_{\text{OCR}}$ (\$2,192,204) [@hhs_ocr_penalty_inflation_2023].

### 7.3 The 3-Part Total Cost of Ownership (TCO) & Roundtrip Latency Drag
Quantifies the financial, compute, and clinical workflow costs of deploying an inline sanitization gateway:

$$\text{TCO} = \text{Cost}_{\text{license}} + \text{Cost}_{\text{deployment}} + \text{Cost}_{\text{latency}}(\Delta t_{\text{total}})$$

Accounting for software compute overhead, enterprise BAA/SSO integration, and the billable clinical hours lost to roundtrip gateway latency ($\Delta t_{\text{total}}$ in seconds) [@sinsky_physician_ehr_time_2016; @bls_healthcare_wages_2023]:

$$\text{Cost}_{\text{latency}}(\Delta t_{\text{total}}) = \left[ \frac{\text{Annual Prompts} \times \Delta t_{\text{total}}}{3600} \right] \times W_{\text{clinical}}$$

Where:
* **$\text{Annual Prompts}$:** Total annual enterprise prompt volume:
  $$\text{Annual Prompts} = N_{\text{staff}} \times U_{\text{direct}} \times Q_{\text{prompt}} \times D_{\text{annual}}$$
* **$\Delta t_{\text{total}}$:** Total roundtrip latency overhead introduced by the gateway:
  $$\Delta t_{\text{total}} = \Delta t_{\text{out}} + \Delta t_{\text{in}}$$
  * $\Delta t_{\text{out}}$: Local outbound entity extraction and surrogate replacement latency.
  * $\Delta t_{\text{in}}$: Inbound session retrieval and re-identification latency.
* **$W_{\text{clinical}}$:** Weighted hourly wage of clinical staff [@bls_healthcare_wages_2023].

### 7.4 The Return on Security Investment (ROSI) Formula
The net economic return delivered by deploying the inline sanitization trust layer [@gordon_loeb_model_2002]:

$$\text{ROSI} = \frac{(\text{COI}_{\text{unmitigated}} - \text{COI}_{\text{mitigated}}) - \text{TCO}}{\text{TCO}}$$

Where $\text{COI}_{\text{mitigated}}$ is calculated by reducing the breach hazard rate according to the fine-tuned model's empirical entity recall ($R$):

$$\lambda_{\text{mitigated}} = \lambda \times (1 - R)$$

---

## 8. 10,000-Trial Monte Carlo Engine Execution

The stochastic simulation is implemented in Python (utilizing `numpy` and `scipy`) evaluating parameter distributions across the three AHA hospital archetypes:
* **Trial Scale:** 10,000 randomized iterations per hospital archetype.
* **Parametric Sweep:** Full grid sweep across empirical model recall ($R$ from 70% to 99.9%) and roundtrip gateway latency ($\Delta t_{\text{total}}$ from 50 ms to 1,500 ms).
* **Break-Even Frontier:** Identifies the multi-dimensional threshold where averted breach and regulatory liabilities surpass the combined software infrastructure and clinician latency drag ($Cost_{\text{latency}}$).
* **Visual Outputs:** Generates publication-grade figures (using `matplotlib` and `seaborn`):
  1. *Risk Reduction Cumulative Distribution Function (CDF)* curves comparing unmitigated vs. mitigated ALE across all archetypes.
  2. *Multi-Variable Break-Even Frontier* surface and contour plots ($\Delta t_{\text{total}}$ vs. $R$ vs. Net ROSI).
  3. *Tornado Sensitivity Analysis* ranking parameter impact (adoption rate, breach surcharge, penalty caps, prompt frequencies).
  4. *Gateway Architecture Schematic* contrasting static DLP text corruption against bidirectional context preservation.

---

# References (Methodology Registry)

* `[@aha_hospital_statistics_2023]`: American Hospital Association. *AHA Hospital Statistics 2023 Edition*. Health Forum LLC, 2023.
* `[@asq_phi_benchmark_2024]`: ASQ-PHI Benchmark Consortium. *ASQ-PHI: A Real-World Conversational Benchmark for Protected Health Information De-Identification in Generative AI Prompts*. Clinical NLP Benchmark Suite, 2024.
* `[@bls_healthcare_wages_2023]`: U.S. Bureau of Labor Statistics. *Occupational Employment and Wage Statistics: Healthcare Practitioners and Technical Occupations*. U.S. Department of Labor, May 2023.
* `[@cyberhaven_shadow_ai_2023]`: Cyberhaven Inc. *Shadow AI in the Enterprise: Insights from Data Ingestion Across 3 Million Employees*. Cyberhaven Labs Research Report, 2023.
* `[@dernoncourt_deidentification_2017]`: Dernoncourt, F., Lee, J. Y., Uzuner, Ö., & Szolovits, P. "De-identification of Patient Notes with Recurrent Neural Networks." *Journal of the American Medical Informatics Association (JAMIA)*, 24(3):596–606, 2017.
* `[@dettmers_qlora_2023]`: Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. "QLoRA: Efficient Finetuning of Quantized LLMs." *Advances in Neural Information Processing Systems (NeurIPS)*, 36:10088–10115, 2023.
* `[@garnter_dlp_market_2023]`: Gartner Inc. *Market Guide for Data Loss Prevention*. Gartner Research ID G00784512, 2023.
* `[@gordon_loeb_model_2002]`: Gordon, L. A., & Loeb, M. P. "The Economics of Information Security Investment." *ACM Transactions on Information and System Security (TISSEC)*, 5(4):438–457, 2002.
* `[@hhs_hipaa_privacy_rule]`: U.S. Department of Health and Human Services. *Standards for Privacy of Individually Identifiable Health Information*. 45 C.F.R. Part 160 and Part 164, Subparts A and E.
* `[@hhs_ocr_breach_portal]`: U.S. Department of Health and Human Services, Office for Civil Rights. *Breach Portal: Notice to the Secretary of HHS of Breach of Unsecured Protected Health Information*. Available at: https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf.
* `[@hhs_ocr_penalty_inflation_2023]`: U.S. Department of Health and Human Services. *Annual Civil Monetary Penalties Inflation Adjustment*. 45 C.F.R. Part 102, § 102.3, Federal Register, 2023.
* `[@ibm_cost_data_breach_2023]`: IBM Security & Ponemon Institute. *Cost of a Data Breach Report 2023*. IBM Corporation, Armonk, NY, 2023.
* `[@johnson_mimic_deid_2016]`: Johnson, A. E. W., Pollard, T. J., Shen, L., et al. "MIMIC-III, a Freely Accessible Critical Care Database." *Scientific Data*, 3:160035, 2016.
* `[@patel_chatgpt_clinical_accuracy_2023]`: Patel, S. B., & Lam, K. "ChatGPT: The Future of Medical Charting or a Liability?" *The Lancet Digital Health*, 5(5):e253–e254, 2023.
* `[@ponemon_cybersecurity_healthcare_2023]`: Ponemon Institute. *Cybersecurity in Healthcare: A Comprehensive 3-Year Vulnerability and Exposure Benchmark*. Ponemon Research Group, 2023.
* `[@ross_probability_models_2014]`: Ross, S. M. *Introduction to Probability Models*. 11th Edition, Academic Press, Boston, MA, 2014.
* `[@sinsky_physician_ehr_time_2016]`: Sinsky, C., Colligan, L., Li, L., et al. "Allocation of Physician Time in Ambulatory Practice: A Time and Motion Study in 4 Specialties." *Annals of Internal Medicine*, 165(11):753–760, 2016.
* `[@vose_risk_analysis_2008]`: Vose, D. *Risk Analysis: A Quantitative Guide*. 3rd Edition, John Wiley & Sons, Chichester, UK, 2008.
* `[@weber_clinical_nlp_deid_2021]`: Weber, G. M., Hong, C., & Palmer, N. P. "Challenges in Automating Clinical Narrative De-Identification Under HIPAA Safe Harbor." *Journal of Biomedical Informatics*, 118:103780, 2021.
* `[@wolters_kluwer_2023]`: Wolters Kluwer Health. *Survey of Clinician Perspectives on Generative AI and Clinical Decision Support*. Wolters Kluwer Corporate Communications, 2023.
