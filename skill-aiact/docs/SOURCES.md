# Sources Registry - EU AI Act Regulatory Knowledge Base

## 📜 Purpose

This document registers all primary and secondary sources used by `skill-aiact` for regulatory compliance assessment. Each source is categorized by legal effect, status, and includes stable identifiers (CELEX/ELI) for verification.

---

## 🔴 TIER 1: BINDING LEGAL ACTS (EUR-Lex)

### SRC-001: EU AI Act Regulation

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-001` |
| **Title** | Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence |
| **CELEX** | `32024R1689` |
| **ELI** | `http://data.europa.eu/eli/reg/2024/1689/oj` |
| **Consolidated Version ELI** | `http://data.europa.eu/eli/reg/2024/1689/2026-07-27/eng` |
| **Type** | REGULATION |
| **Status** | `BINDING` |
| **Legal Effect** | Directly applicable in all EU Member States |
| **Entry into Force** | 1 August 2024 |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |
| **Official URL** | https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng |
| **Consolidated URL** | https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng |

**Key Articles Covered:**
- Art. 3: Definitions (AI System, Provider, Deployer, etc.)
- Art. 4: AI Literacy
- Art. 5: Prohibited AI Practices
- Art. 6: High-Risk AI Systems Classification
- Art. 9: Risk Management System
- Art. 10: Data Governance
- Art. 11: Technical Documentation
- Art. 12: Record-Keeping / Logging
- Art. 13: Transparency & Information Provision
- Art. 14: Human Oversight
- Art. 15: Accuracy, Robustness, Cybersecurity
- Art. 26: Obligations of Deployers
- Art. 50: Transparency Obligations for Certain AI Systems
- Art. 73: Incident Reporting
- Annex I, III, IV: Classification & Requirements

---

### SRC-002: Digital Omnibus Amendment

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-002` |
| **Title** | Regulation (EU) 2026/1744 (Digital Omnibus) amending certain Union acts in the field of digitalisation |
| **CELEX** | `32026R1744` |
| **ELI** | `http://data.europa.eu/eli/reg/2026/1744/oj/eng` |
| **Type** | REGULATION (AMENDING) |
| **Status** | `BINDING` |
| **Legal Effect** | Amends timelines and provisions of Regulation 2024/1689 |
| **Entry into Force** | 27 July 2026 |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |
| **Official URL** | https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng |

**Key Modifications:**
- Simplified AI Literacy obligations (Art. 4)
- Adjusted high-risk system application dates (Annex III: 2 Dec 2027)
- Product integration timelines (Annex I: 2 Aug 2028)

---

## 🟠 TIER 2: OFFICIAL GUIDANCE (European Commission / AI Office)

### OFF-001: AI Act Regulatory Framework Overview

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-001` |
| **Title** | Artificial Intelligence Act - Regulatory Framework |
| **Publisher** | European Commission - DG CONNECT |
| **Type** | OFFICIAL_PORTAL |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Interpretative guidance, not binding |
| **URL** | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 14 |

---

### OFF-002: AI Literacy Q&A

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-002` |
| **Title** | AI Literacy Questions & Answers |
| **Publisher** | European Commission |
| **Type** | OFFICIAL_GUIDANCE |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Clarifies Art. 4 implementation expectations |
| **URL** | https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

**Key Points:**
- No uniform competency level imposed on individuals
- Context-dependent measures based on role, experience, use case
- Replicating repository practices ≠ automatic presumption of conformity

---

### OFF-003: AI System Definition Guidelines

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-003` |
| **Title** | Guidelines on the definition of an AI system |
| **Publisher** | European Commission |
| **Type** | OFFICIAL_GUIDANCE |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Interpretative guidance for Art. 3(1) |
| **URL** | https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-ai-system-definition-facilitate-first-ai-acts-rules-application |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### OFF-004: Prohibited AI Practices Guidelines

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-004` |
| **Title** | Guidelines on prohibited AI practices under Article 5 |
| **Publisher** | European Commission |
| **Type** | OFFICIAL_GUIDANCE |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Interpretative guidance for Art. 5 enforcement |
| **URL** | https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-prohibited-artificial-intelligence-ai-practices-defined-ai-act |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### OFF-005: High-Risk Classification Guidelines

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-005` |
| **Title** | Guidelines on high-risk AI systems classification |
| **Publisher** | European Commission |
| **Type** | OFFICIAL_GUIDANCE |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Interpretative guidance for Art. 6 + Annex III |
| **URL** | https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### OFF-006: General-Purpose AI Code of Practice

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-006` |
| **Title** | General-Purpose AI Code of Practice |
| **Publisher** | European Commission / AI Board |
| **Type** | CODE_OF_PRACTICE |
| **Status** | `VOLUNTARY_BEST_PRACTICE` |
| **Legal Effect** | Voluntary but may demonstrate adequacy for GPAI obligations |
| **Applicable From** | 2 August 2025 |
| **URL** | https://digital-strategy.ec.europa.eu/en/library/general-purpose-ai-code-practice |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### OFF-007: AI-Generated Content Transparency Code of Practice

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-007` |
| **Title** | Code of Practice on Transparency of AI-Generated Content |
| **Publisher** | European Commission / AI Board |
| **Type** | CODE_OF_PRACTICE |
| **Status** | `VOLUNTARY_BEST_PRACTICE` |
| **Legal Effect** | Voluntary but confirmed as adequate for Art. 50 transparency |
| **Applicable From** | 2 August 2026 |
| **URL** | https://digital-strategy.ec.europa.eu/en/policies/code-practice-transparency-ai-generated-content |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### OFF-008: AI Literacy Repository

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-008` |
| **Title** | Living Repository of AI Literacy Practices |
| **Publisher** | European Commission |
| **Type** | REPOSITORY |
| **Status** | `ONGOING` |
| **Legal Effect** | Examples only; replication ≠ automatic conformity |
| **URL** | https://digital-strategy.ec.europa.eu/en/library/living-repository-foster-learning-and-exchange-ai-literacy |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 14 |

---

### OFF-009: Standardisation Guidance

| Field | Value |
|-------|-------|
| **Source ID** | `OFF-009` |
| **Title** | AI Act Standardisation Guidance |
| **Publisher** | European Commission |
| **Type** | GUIDANCE |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Explains relationship between harmonised standards and AI Act |
| **URL** | https://digital-strategy.ec.europa.eu/en/policies/ai-act-standardisation |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

## 🟡 TIER 3: DATA PROTECTION (GDPR / EDPB)

### GDPR-001: General Data Protection Regulation

| Field | Value |
|-------|-------|
| **Source ID** | `GDPR-001` |
| **Title** | Regulation (EU) 2016/679 (GDPR) |
| **CELEX** | `32016R0679` |
| **Type** | REGULATION |
| **Status** | `BINDING` |
| **Legal Effect** | Directly applicable data protection law |
| **URL** | https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 90 |

**Note:** AI Act does NOT replace GDPR. Both apply concurrently where personal data is processed.

---

### EDPB-001: EDPB Opinion 28/2024 on AI & Personal Data

| Field | Value |
|-------|-------|
| **Source ID** | `EDPB-001` |
| **Title** | Opinion 28/2024 on processing of personal data in the context of AI models |
| **Publisher** | European Data Protection Board (EDPB) |
| **Type** | OPINION |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Interpretative guidance on GDPR in AI context |
| **URL** | https://www.edpb.europa.eu/our-work-tools/our-documents/opinions/opinion-282024-processing-personal-data-context-ai-models_en |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 60 |

---

### EDPB-002: AI Privacy Risks & Mitigations Report

| Field | Value |
|-------|-------|
| **Source ID** | `EDPB-002` |
| **Title** | AI Privacy Risks & Mitigations - Large Language Models |
| **Publisher** | European Data Protection Board (EDPB) |
| **Type** | REPORT |
| **Status** | `OFFICIAL_FINAL` |
| **Legal Effect** | Best practice guidance for GDPR compliance in LLM contexts |
| **URL** | https://www.edpb.europa.eu/our-work-tools/our-documents/reports/ai-privacy-risks-mitigations-large-language-models_en |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 60 |

---

## 🟢 TIER 4: STANDARDS & FRAMEWORKS (VOLUNTARY)

### STD-001: ISO/IEC 42001 AI Management System

| Field | Value |
|-------|-------|
| **Source ID** | `STD-001` |
| **Title** | ISO/IEC 42001:2023 - Artificial Intelligence Management System |
| **Publisher** | ISO/IEC |
| **Type** | INTERNATIONAL_STANDARD |
| **Status** | `VOLUNTARY_STANDARD` |
| **Legal Effect** | Not legally binding; may support AI Act compliance evidence |
| **URL** | https://www.iso.org/standard/81230.html |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 90 |

**Mapping Note:** ISO 42001 provides management system framework but does NOT automatically ensure AI Act compliance.

---

### STD-002: ISO/IEC 27001 Information Security

| Field | Value |
|-------|-------|
| **Source ID** | `STD-002` |
| **Title** | ISO/IEC 27001:2022 - Information Security Management |
| **Publisher** | ISO/IEC |
| **Type** | INTERNATIONAL_STANDARD |
| **Status** | `VOLUNTARY_STANDARD` |
| **Legal Effect** | Not legally binding; supports cybersecurity requirements |
| **URL** | https://www.iso.org/standard/27001 |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 90 |

---

### STD-003: ISO/IEC 27701 Privacy Information Management

| Field | Value |
|-------|-------|
| **Source ID** | `STD-003` |
| **Title** | ISO/IEC 27701:2019 - Privacy Information Management |
| **Publisher** | ISO/IEC |
| **Type** | INTERNATIONAL_STANDARD |
| **Status** | `VOLUNTARY_STANDARD` |
| **Legal Effect** | Not legally binding; supports GDPR evidence |
| **URL** | https://www.iso.org/standard/27701 |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 90 |

---

### STD-004: NIST AI Risk Management Framework

| Field | Value |
|-------|-------|
| **Source ID** | `STD-004` |
| **Title** | NIST AI RMF 1.0 - Artificial Intelligence Risk Management Framework |
| **Publisher** | NIST (US National Institute of Standards and Technology) |
| **Type** | FRAMEWORK |
| **Status** | `VOLUNTARY_FRAMEWORK` |
| **Legal Effect** | US framework; informative only for EU AI Act |
| **URL** | https://www.nist.gov/itl/ai-risk-management-framework |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 90 |

---

## 🛡️ TIER 5: TECHNICAL SECURITY STANDARDS

### SEC-001: OWASP Top 10 for LLM Applications

| Field | Value |
|-------|-------|
| **Source ID** | `SEC-001` |
| **Title** | OWASP Top 10 for Large Language Model Applications |
| **Publisher** | OWASP Foundation |
| **Type** | SECURITY_GUIDANCE |
| **Status** | `COMMUNITY_STANDARD` |
| **Legal Effect** | Best practice; not legally binding |
| **URL** | https://owasp.org/www-project-top-10-for-large-language-model-applications/ |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 60 |

---

### SEC-002: OWASP Agentic AI Security

| Field | Value |
|-------|-------|
| **Source ID** | `SEC-002` |
| **Title** | OWASP Agentic AI Security Guidance |
| **Publisher** | OWASP Foundation |
| **Type** | SECURITY_GUIDANCE |
| **Status** | `DRAFT` |
| **Legal Effect** | Emerging best practice; not legally binding |
| **URL** | https://owasp.org/projects/agentic-ai-security/ |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

## 🇮🇹 TIER 6: ITALIAN NATIONAL IMPLEMENTATION

### ITA-001: Garante Privacy - AI Section

| Field | Value |
|-------|-------|
| **Source ID** | `ITA-001` |
| **Title** | Intelligenza Artificiale - Garante per la Protezione dei Dati Personali |
| **Publisher** | Italian Data Protection Authority (Garante Privacy) |
| **Type** | NATIONAL_AUTHORITY |
| **Status** | `ONGOING` |
| **Legal Effect** | National enforcement guidance; supplementary to GDPR/AI Act |
| **URL** | https://www.garanteprivacy.it/intelligenza-artificiale |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 30 |

---

### ITA-002: Italian AI Act Implementation Law

| Field | Value |
|-------|-------|
| **Source ID** | `ITA-002` |
| **Title** | Decreto Legislativo di attuazione del Regolamento UE 2024/1689 |
| **Publisher** | Italian Parliament / Government |
| **Type** | NATIONAL_LEGISLATION |
| **Status** | `PENDING` |
| **Legal Effect** | Will specify national enforcement authorities and sanctions procedures |
| **URL** | TBD |
| **Last Verified** | 2026-08-08 |
| **TTL (Days)** | 14 |

**Note:** Italy must designate competent authorities and establish sanction procedures per AI Act Chapter X.

---

## 📋 Source Status Legend

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `BINDING` | Directly applicable EU law | Mandatory compliance |
| `OFFICIAL_FINAL` | Official guidance published | Strongly recommended to follow |
| `OFFICIAL_DRAFT` | Draft guidance from official body | Monitor for changes |
| `VOLUNTARY_STANDARD` | Non-binding standard | May support evidence |
| `VOLUNTARY_FRAMEWORK` | Non-binding framework | Informative reference |
| `COMMUNITY_STANDARD` | Industry best practice | Recommended for security |
| `ONGOING` | Actively updated resource | Regular review needed |
| `PENDING` | Awaiting publication | Monitor for release |

---

## 🔄 Source Monitoring Protocol

All sources must be re-verified before their TTL expires:

- **Binding Legal Acts (TTL: 30 days):** Check EUR-Lex for amendments
- **Official Guidance (TTL: 14-30 days):** Check Commission portals for updates
- **Standards/Frameworks (TTL: 90 days):** Check for new versions
- **National Implementation (TTL: 14 days):** Critical during transposition period

The `src/sources/monitor.py` module automates this tracking and flags controls as `STALE` when sources exceed TTL.

---

**Last Document Review:** 2026-08-08  
**Next Scheduled Review:** 2026-09-08  
**Document Owner:** skill-aiact Compliance Team
