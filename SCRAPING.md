# Data Collection — PS 26108

## Approach
There is no bulk BIS API. Data is collected manually from:

1. **bis.gov.in "Know Your Standard"** — search by IS number to get:
   - Title, year, revision, reaffirmation status
   - Division council, sectional committee
   - Current status (Active/Withdrawn/Superseded)

2. **Standard PDF front matter (Clause 2)** — for normative reference lists:
   - Each standard lists its normative references in Clause 2
   - Extract IS numbers, titles, and relationship types

3. **DPIIT Gazette Notifications** — for QCO status:
   - Which products have mandatory BIS certification
   - Scheme type (Scheme-I ISI Mark vs Scheme-II CRS)
   - Notifying ministry

## Data Entry Format
Add entries to `/data/indian_standards_master_catalog.json` following the existing schema:
```json
{
  "is_number": "IS 694",
  "year": 2010,
  "revision": "Fourth Revision",
  "reaffirmed_year": 2020,
  "status": "ACTIVE",
  "latest_amendments": ["Amendment No. 1 (2014)", ...],
  "title": "Full standard title",
  "division_council": "ETD",
  "sectional_committee": "ETD 14",
  "keywords": ["pvc wire", "copper cable", ...],
  "normative_references": [
    { "is_number": "IS 8130:2013", "relationship": "RAW_MATERIAL", "title": "..." }
  ],
  "allied_standards": [
    { "is_number": "IS 732:2019", "relationship": "INSTALLATION_CODE", "title": "..." }
  ],
  "qco_details": {
    "is_mandatory": true,
    "qco_name": "...",
    "notifying_ministry": "DPIIT",
    "scheme": "Scheme-I (ISI Mark)"
  }
}
```

## Verification
Every `IS ####:YYYY` value must be checked against bis.gov.in at the time it's entered.
Mark anything not yet verified as `PLACEHOLDER — verify` rather than guessing a number.

## V1 Target
50–100 standards in the electrical/cable domain. Current: 11 verified entries.
