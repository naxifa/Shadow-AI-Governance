# Research Methodology & Parameter Calibration

## 1. Focus Scope: Real-Time Conversational Prompts vs. Static Files

This methodology specifically targets the cybersecurity, compliance, and clinical workflow risks of **ephemeral, browser-based text pastes** where healthcare workers copy unstructured clinical narratives directly into web-based conversational AI chatbots (such as ChatGPT).

Unlike legacy Data Loss Prevention (DLP) tools engineered to inspect static files and perimeter egress (such as PDFs, spreadsheets, email attachments, or USB transfers), our architecture operates as an outbound, inline prompt-interception trust layer. It intercepts text at the browser input level in real time, detects and redacts Protected Health Information (PHI), and maps sensitive entities to synthetic surrogates while preserving critical numerical lab values, vitals, and medication dosages.

---

## 2. Research Architecture & Unified Scope

This study intentionally decouples the real-time redaction filter from the institutional risk calculation. The fine-tuned language model operates strictly as an entity detection and redaction filter, while institutional risk, regulatory penalties, and Return on Security Investment (ROSI) are evaluated downstream within a deterministic, auditable simulation matrix.

| Research Dimension | Technical Component (Trust Layer & ML Pipeline) | Economic Component (Decision-Analytic Simulation) |
| :--- | :--- | :--- |
| **Domain** | Clinical NLP / Open-Source LLM Fine-Tuning | Health Informatics / Cybersecurity Economics |
| **Core Target** | Real-time browser text pastes & conversational prompts (not static files/PDFs) | Hospital financial risk & budget modeling |
| **Primary Focus** | Dataset ingestion, PEFT/LoRA fine-tuning, real-time prompt interception, context-preserving substitution | Stochastic financial simulation, Poisson breach estimation, TCO modeling |
| **Target Metrics** | Redaction Recall ($R$), Precision, F1-Score, Inference Latency ($\Delta t$ in ms), Hard Negative Specificity | Annual Loss Expectancy (ALE), Cost of Inaction (COI), TCO, Net ROSI (%) |
| **Core Deliverable** | Fine-tuned open-source model pipeline (Python/FastAPI) and evaluation benchmarks | 10,000-trial Monte Carlo risk simulation engine, Hospital Decision Tables, Break-Even Frontier curves |

---

## 3. Hospital Archetypes & Operational Profiles

Hospitals face vastly different risk levels depending on their staff size, daily workflow, and security overhead. To reflect real-world healthcare delivery, our simulation categorizes organizations into three operational tiers based on American Hospital Association (AHA) benchmarks:

1. **Community Hospital (Small):**
   * **Scale:** 80 licensed beds and approximately 500 full-time staff (FTEs).
   * **Profile:** Community-oriented acute care with a lean IT team and lower daily prompt activity.

2. **Regional Health System (Medium):**
   * **Scale:** 350 licensed beds and approximately 3,500 staff.
   * **Profile:** Multi-specialty hospital network with moderate administrative infrastructure and higher daily prompt volume.

3. **Academic Medical Center (Large):**
   * **Scale:** 1,100 licensed beds and approximately 14,000 staff.
   * **Profile:** High-throughput campus combining direct patient care, medical residency training, and clinical research.

---

## 4. Empirical Data & Parameter Anchors

Rather than relying on arbitrary assumptions, the model grounds its variables in published empirical studies and federal statutory standards:

* **Clinician AI Adoption Rates ($U_{\text{direct}}$):**  
  Measures the percentage of clinical staff who directly use unapproved, external generative AI tools for work tasks. Based on findings from the Wolters Kluwer survey, the baseline direct clinical adoption mode is set to **17%** (with 40% observing colleagues doing so, and broader industry studies reporting 57% to 80% adoption across enterprise staff). In our model, this rate ranges from a 10% minimum in Community hospitals to an upper bound of 57% in high-volume settings. Furthermore, 82% of enterprise knowledge workers admit to copying and pasting work text directly into web AI tools.

* **Healthcare Sector Baseline Breach Cost ($C_{\text{base}}$):**  
  According to the IBM Security *Cost of a Data Breach Report*, healthcare breaches average **$7.42 million per incident**, remaining the highest across all sectors for over a decade, with an average identification and containment lifecycle of **279 days**. Historical data from the HHS OCR breach portal confirms between **700 and 750 large-scale breaches annually** (affecting 500+ patient records), representing an estimated **10% to 15% annual baseline breach probability** for an individual hospital, with over **90% of healthcare organizations experiencing at least one breach within a three-year window**.

* **Shadow AI Breach Surcharge ($\Delta C_{\text{shadow}}$):**  
  Incidents involving unapproved "Shadow AI" incur an average **$670,000 penalty surcharge** above baseline costs due to extended forensic triage, discovery bottlenecks, and untracked cloud caching. Shadow AI directly accounts for **8.3% to 9.1% of the entire incident bill** and appears in **20% to 43% of enterprise security incidents**. Moreover, unsanctioned tools exhibit a **65% higher rate of direct PHI/PII leakage** compared to standard network breaches.

* **Statutory Enforcement Penalty Ceiling ($\text{Cap}_{\text{OCR}}$):**  
  Calibrated using the HHS Office for Civil Rights (OCR) annual enforcement maximum under 45 CFR § 102.3. For Tier 4 "Willful Neglect" violations, the federal statutory penalty cap is set to **$2,192,204 per violation category annually**. Transmitting PHI to non-BAA-covered endpoints constitutes an automatic violation of HIPAA Privacy and Security Rules.

---

## 5. Clinical Data Curation & LLM Fine-Tuning Pipeline

### 5.1 Training & Evaluation Corpora
* **ASQ-PHI Benchmark Anchor:** The primary evaluation benchmark is anchored on the foundational **1,051-query ASQ-PHI dataset** (comprising 2,973 tagged HIPAA Safe Harbor entities across 13 core categories).
* **Adversarial Hard Negatives:** Crucially includes **219 clinical hard negatives**—prompts with complex medical numbers, vitals, and dosages (e.g., potassium levels, 50 mg dosing) but zero PHI. This ensures the model learns not to over-redact critical physiological values.
* **Extensibility:** The ingestion pipeline is structured modularly, allowing seamless incorporation of additional clinical corpora (such as the i2b2/n2c2 clinical de-identification challenge sets and MIMIC-IV-Note subsets) into the instruction-tuning schema.

### 5.2 Model Fine-Tuning
* **Base Architectures:** Fine-tuning open-source foundation models (e.g., Llama 3 8B or Mistral 7B).
* **Adaptation Method:** Utilizing Parameter-Efficient Fine-Tuning (PEFT) via QLoRA (Quantized Low-Rank Adaptation). This yields high contextual entity identification on unstructured conversational clinical prompts while maintaining a compact memory footprint for local hospital inference.

### 5.3 Context-Preserving Redaction
The model intercepts real-time text input, identifies sensitive entities, and maps them to consistent synthetic surrogates (e.g., replacing *John Doe* with `[PATIENT_A]` and *St. Jude* with `[HOSPITAL_B]`) so downstream commercial LLMs can still perform medical reasoning before re-identification on response return.

---

## 6. Probability Distributions

A static single-point average fails to capture real-world operational variance and cybersecurity tail risk. We assign three specific probability curves to model different behaviors:

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

## 7. Mathematical Formulation

### 7.1 Bounded Stochastic Hazard Function
In basic risk models, multiplying risk factors linearly distorts results—in large academic centers, high prompt volumes can produce mathematically invalid probabilities exceeding 100%.

To prevent this scale distortion, annual breach probability is modeled using a standard Poisson hazard formulation:

$$P(\text{Breach} \ge 1) = 1 - e^{-\lambda}$$

Where:

$$\lambda = N_{\text{staff}} \times U_{\text{direct}} \times Q_{\text{prompt}} \times 250 \times P_{\text{phi}} \times P(\text{breach} \mid \text{phi})$$

* **$N_{\text{staff}}$:** Total hospital workforce headcount.
* **$U_{\text{direct}}$:** Clinician shadow AI adoption rate (baseline mode = 17%, range = 10% to 57%).
* **$Q_{\text{prompt}}$:** Mean daily prompts per active clinician across a standard 250 clinical working days per year.
* **$P_{\text{phi}}$:** Probability that an unmonitored prompt contains Protected Health Information (~3%).
* **$P(\text{breach} \mid \text{phi})$:** Conditional probability that outbound PHI exposure triggers an actionable, reportable breach event (~0.8%).

Under this formulation, if a small hospital has an expected leak rate of $\lambda = 0.1$, the annual breach probability is:

$$1 - e^{-0.1} \approx 9.5\%$$

If an Academic Medical Center processes high prompt volumes yielding $\lambda = 5.0$, the breach probability cleanly converges to:

$$1 - e^{-5.0} \approx 99.3\%$$

This keeps all calculated probabilities bounded between 0% and 100% regardless of institutional scale.

### 7.2 Cost of Inaction (COI) Formula
The unmitigated financial risk incurred by a hospital operating without AI governance:

$$\text{COI} = \text{ALE}_{\text{breach}} + \mathbb{E}[\text{HIPAA Penalties}] + \text{Cost}_{\text{forensics}} + \text{Spend}_{\text{shadow\_saas}}$$

Where:

$$\text{ALE}_{\text{breach}} = P(\text{Breach} \ge 1) \times (C_{\text{base}} + \Delta C_{\text{shadow}})$$

* $C_{\text{base}}$ is sampled around the empirical baseline ($7.42M).
* $\Delta C_{\text{shadow}}$ is the Shadow AI penalty surcharge ($670k).
* Annual statutory HIPAA penalties are constrained by $\text{Cap}_{\text{OCR}}$ ($2,192,204).

### 7.3 The 3-Part Total Cost of Ownership (TCO) & Latency Drag
Quantifies the financial, compute, and clinical workflow costs of deploying an inline filter:

$$\text{TCO} = \text{Cost}_{\text{license}} + \text{Cost}_{\text{deployment}} + \text{Cost}_{\text{latency}}(\Delta t)$$

Accounting for software compute overhead, enterprise BAA/SSO integration, and the billable clinical hours lost to filter processing latency ($\Delta t$ in seconds):

$$\text{Cost}_{\text{latency}}(\Delta t) = \left[ \frac{\text{Annual Prompts} \times \Delta t}{3600} \right] \times W_{\text{clinical}}$$

Where:
* **$\text{Annual Prompts}$:** Total enterprise prompt volume ($N_{\text{staff}} \times U_{\text{direct}} \times Q_{\text{prompt}} \times 250$).
* **$\Delta t$:** Added latency in seconds introduced by the prompt interception filter.
* **$W_{\text{clinical}}$:** Weighted hourly wage of clinical staff.

### 7.4 The Return on Security Investment (ROSI) Formula
The net economic return delivered by deploying the real-time trust layer:

$$\text{ROSI} = \frac{(\text{COI}_{\text{unmitigated}} - \text{COI}_{\text{mitigated}}) - \text{TCO}}{\text{TCO}}$$

Where $\text{COI}_{\text{mitigated}}$ is calculated by reducing the hazard rate according to the fine-tuned model's recall ($R$):

$$\lambda_{\text{mitigated}} = \lambda \times (1 - R)$$

---

## 8. 10,000-Trial Monte Carlo Engine Execution

Stochastic simulation implemented in Python (using `numpy` and `scipy`) evaluating probability distributions across the three AHA hospital archetypes:
* **Trial Scale:** 10,000 randomized iterations per hospital archetype.
* **Parametric Sweep:** Full sweep across recall ($R$ from 70% to 99.9%) and filter latency ($\Delta t$ from 50 ms to 1,500 ms).
* **Visual Outputs:** Generates Cumulative Distribution Function (CDF) risk reduction curves, Multi-variable Break-Even Frontier charts, and Tornado parameter sensitivity plots (`matplotlib` and `seaborn`) to establish exact bed-level break-even thresholds for hospital leadership.