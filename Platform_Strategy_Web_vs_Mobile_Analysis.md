# Platform Strategy & Architectural Decision: Web App vs. Mobile App
**Document Purpose:** Comparative analysis of target user environments, delivery channels, and implementation recommendations for SIH-2026 Problem Statements **26045** and **26108**.

---

## 1. Comparative Platform Matrix

| Problem Statement | Recommended Primary Platform | Secondary Platform / Key USP | Rationale & User Persona Alignment |
| :--- | :--- | :--- | :--- |
| **PS 26045**<br>*(IP-SAKTI Sahayak — Ministry of Ayush)* | **Responsive Web App / PWA**<br>*(Next.js / React + Tailwind)* | **Voice-First Mobile Layout / WhatsApp Bot** | **Dual Persona:** Biotech startups & researchers use desktop for complex IPR filings, while grassroots *Vaidyas* & herb growers use smartphones with vernacular voice (Bhashini). |
| **PS 26108**<br>*(Indian Standards in Procurement — DoCA / BIS)* | **Desktop Web Application**<br>*(Next.js / React + FastAPI)* | **Chrome / Edge Browser Extension (for GeM Portal)** | **Desk-Bound Workflow:** 100% of public tenders (GeM, CPPP, IREPS) are authored on desktop PCs in office environments. A browser extension overlay on GeM provides high evaluation impact. |

---

## 2. Deep Dive: PS 26045 (Ayurveda IPR & Regulatory Assistant)

### Target User Personas
1. **The Ayush Startup Founder / Patent Attorney:**
   - *Device:* Laptop / Desktop (macOS / Windows / Linux).
   - *Workflow:* Deep statutory research, comparing national patent rules vs WIPO treaties, reviewing prior-art references, generating strategy PDFs.
   - *Needs:* Multi-pane dashboard, split-screen PDF preview, citation inspector, formulation wizard.
2. **The Grassroots Vaidya / Ayurvedic Practitioner / Cultivator:**
   - *Device:* Smartphone (Android / iOS).
   - *Workflow:* Asking if a local formulation or wild-harvested herb (*Ashwagandha*, *Sarpagandha*) requires NBA Form I approval or State Biodiversity Board intimation.
   - *Needs:* One-tap voice search (Hindi, Sanskrit, Tamil, Marathi), large audio playback button, minimal text clutter, WhatsApp integration.

### Architectural Solution for PS 26045:
- Build a **Progressive Web App (PWA)** using Next.js / React 19.
- **On Desktop:** Renders a 3-pane legal research workbench.
- **On Mobile:** Renders a clean chat interface with a prominent **Bhashini Voice Microphone** and high-contrast audio response cards.

---

## 3. Deep Dive: PS 26108 (Indian Standards Recommendation Engine for Procurement)

### Target User Personas
1. **Public Procurement Officers (GeM / CPPP Buyers, CPWD / Railways Engineers):**
   - *Device:* 100% Desktop Office PCs connected to government intranets/browsers.
   - *Workflow:* Drafting Technical Eligibility Criteria (TEC), uploading Excel Bill of Quantities (BoQs), creating tenders on the GeM portal.
   - *Key Realization:* **Nobody authors multi-crore public tenders on a mobile phone.** A standalone mobile app does not fit actual procurement workflows.

### Architectural Solution for PS 26108:
1. **Desktop Web Portal (Tender Analysis & Spec Studio):**
   - Drag-and-drop parsing of tender PDFs, Word docs, and BoQ Excel sheets.
   - Interactive Neo4j Normative Graph tree viewer (React Flow / D3.js).
   - Real-time QCO Compliance Checker and 1-click NIT Clause Generator.
2. **The Chrome / Edge Browser Extension (The Hackathon Winner USP):**
   - Floats directly over active **GeM (Government e-Marketplace)** and **CPPP** tender creation forms.
   - When the buyer types an item description (e.g. *"Submersible agricultural pump 5HP"*), the extension detects the input, performs a background API lookup, and displays:
     - Recommended Standard: `IS 14220 : 2018`
     - Mandatory QCO Alert: `ISI Mark Scheme-I Required`
     - Action: `[+ Insert Spec Clause into GeM]`

---

## 4. Implementation Recommendations for Hackathon Teams

| Sprint Phase | PS 26045 (Ayurveda IPR) Focus | PS 26108 (BIS Procurement) Focus |
| :--- | :--- | :--- |
| **Phase 1 (Core)** | Responsive Web App with Formulation Wizard & Dual-Jurisdiction Switch. | Desktop Web Portal with PDF/BoQ parsing and Hybrid Search. |
| **Phase 2 (Graph & Guardrails)** | Neo4j Legal Knowledge Graph + Citation Grounding. | Neo4j Normative Tree Graph + QCO Scheme Compliance Checker. |
| **Phase 3 (Vernacular & Integration)** | Bhashini Voice Input/Output for Mobile PWA view. | Chrome/Edge Browser Extension overlay on GeM Portal. |
