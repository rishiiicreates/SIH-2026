# Smart India Hackathon (SIH 2026) — Master Solution Blueprints & Dual Roadmap
**Directory Location:** `/Users/rishii/SIH-2026/`  
**Focus:** Problem Statement 26045 (Ayush IPR) & Problem Statement 26108 (BIS Standards Procurement)  
**Team Leadership:** Rishii (Frontend Lead + ML Escalation Mentor) & Sahaj (ML / RAG / Graph RAG Lead)  

---

## 📑 Core Documentation Index

1. [**`Dual_Roadmap_PS26045_and_PS26108.md`**](file:///Users/rishii/SIH-2026/Dual_Roadmap_PS26045_and_PS26108.md) ⭐⭐⭐
   * **Target Focus:** Step-by-step roadmap specifically built for **PS 26045** and **PS 26108**.
   * **ML Escalation Protocol:** Sahaj leads all ML/RAG/Graph development; Rishii acts as Frontend Lead + On-Demand ML Escalation Guide when Sahaj gets stuck.
   * **36-Hour Hackathon Hour-by-Hour Sprint:** Exact timelines from setup to final jury pitch.

2. [**`PS_26045_IP_SAKTI_Ayurveda_IPR_Master_Blueprint.md`**](file:///Users/rishii/SIH-2026/PS_26045_IP_SAKTI_Ayurveda_IPR_Master_Blueprint.md)
   * **Ministry of Ayush / AIIA** technical blueprint.
   * Formulation Classification Wizard, Dual-Jurisdiction Switch (National vs WIPO GRATK), Biological Diversity Act 2023/24 ABS Form Router, and Bhashini Voice.

3. [**`PS_26108_BIS_Standards_Procurement_Master_Blueprint.md`**](file:///Users/rishii/SIH-2026/PS_26108_BIS_Standards_Procurement_Master_Blueprint.md)
   * **Department of Consumer Affairs (DoCA) / Bureau of Indian Standards (BIS)** technical blueprint.
   * Hybrid RRF Search, Neo4j Normative Reference Dependency Trees, Mandatory QCO Compliance Engine, and GeM Chrome Extension.

4. [**`Platform_Strategy_Web_vs_Mobile_Analysis.md`**](file:///Users/rishii/SIH-2026/Platform_Strategy_Web_vs_Mobile_Analysis.md)
   * Platform comparison (PWA + Voice for Ayush; Desktop Web + Chrome Extension for GeM Procurement).

5. [**`Team_Roles_and_Sprint_Delegation_Matrix.md`**](file:///Users/rishii/SIH-2026/Team_Roles_and_Sprint_Delegation_Matrix.md)
   * Granular 6-member task breakdown (Rishii, Sahaj, Tanishka, Prerak, Diksha, Member 6).

6. [**`SIH_Top_6_PS_Master_Analysis_and_Team_Execution_Plan.md`**](file:///Users/rishii/SIH-2026/SIH_Top_6_PS_Master_Analysis_and_Team_Execution_Plan.md)
   * Broad reference comparing PS 26045, 26107, 26108, 26130, 26100, and 26101.

---

## 📦 Official Datasets & Graph Data (`/Users/rishii/SIH-2026/data/`)

| Dataset File | Format | Records | Description |
| :--- | :--- | :--- | :--- |
| [**`bis_mandatory_qco_scheme1.json`**](file:///Users/rishii/SIH-2026/data/bis_mandatory_qco_scheme1.json) | JSON / CSV | 752 Records | Official BIS Scheme-I (ISI Mark) products under mandatory Central Quality Control Orders (QCOs). |
| [**`bis_mandatory_crs_scheme2.json`**](file:///Users/rishii/SIH-2026/data/bis_mandatory_crs_scheme2.json) | JSON / CSV | 30 Records | Official BIS Scheme-II (CRS) products for MeitY electronics, IT hardware, and LED lighting. |
| [**`indian_standards_master_catalog.json`**](file:///Users/rishii/SIH-2026/data/indian_standards_master_catalog.json) | JSON / CSV | Multi-Domain | Structured taxonomy mapping Primary Standards to Normative References, Raw Materials, Test Methods, and Safety Codes. |
| [**`bis_normative_graph_triples.json`**](file:///Users/rishii/SIH-2026/data/bis_normative_graph_triples.json) | JSON | 53 Triples | Neo4j / NetworkX graph expansion triples (`HAS_NORMATIVE_REF`, `TEST_METHOD`, `MANDATED_BY_QCO`). |
| [**`sample_procurement_tenders_eval.json`**](file:///Users/rishii/SIH-2026/data/sample_procurement_tenders_eval.json) | JSON | 4 Tenders | Real-world benchmark public tenders from GeM, CPWD, Railways (IREPS), and State WRD. |
