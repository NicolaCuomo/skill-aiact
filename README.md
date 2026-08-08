# 🛡️ SKILL-IACT

**EU AI Act Compliance & Governance Skill for AI Agents and LLMs**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![EU AI Act Regulation](https://img.shields.io/badge/EU%20AI%20Act-2024%2F1689-blue)](https://artificialintelligenceact.eu/)
[![Agent Plugins 1.0.0](https://img.shields.io/badge/Agent%20Plugins-1.0.0-green)](https://agent-plugins.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 Overview & Mission

**SKILL-IACT** is a specialized instruction set and compliance auditor package for AI Agents (such as Cursor, Claude Code, and custom LLM workflows). It provides agents with the exact legal context, risk classification schemas, and compliance timelines of the **EU AI Act (Regulation EU 2024/1689)**.

By loading this skill, you turn any AI agent into an expert capable of auditing codebases, analyzing system architectures, classifying risk levels, and drafting actionable compliance checklists for European SMEs and developers.

---

## 🚀 Core Capabilities

* **🚦 Risk Classification Decision Tree**: Step-by-step guidance through prohibited practices (Art. 5), high-risk systems (Art. 6 & Annex III), and transparency rules (Art. 50).
* **📚 GPAI Governance Audits**: Structured checks for general-purpose AI models, data supply documentation, and copyright alignment.
* **📅 Timeline Reference**: Detailed compliance deadlines (6, 12, 24, and 36-month enforcement intervals).
* **⚖️ Legal Citations**: Answers are grounded and directly linked to Articles of the official published Regulation.

---

## ⚡ Quick Start & Installation

### Option A: Install via Agent Plugins CLI (Standard)
Since the repository is compliant with the **Agent Plugins 1.0.0** specification, you can install it into any compatible tool (Cursor, Claude Code, VS Code, etc.) with a single command:

```bash
npx plugins add NicolaCuomo/skill-aiact
```

### Option B: Manual Integration into Prompts
Simply copy the contents of [`SKILL.md`](SKILL.md) and append it as a System Prompt or developer instruction block in your agent configurations.

---

## 📝 Example Query & Output

### User Query
> "We are building an AI-powered recruitment application that screens CVs for job openings in Italy. What are our obligations under the EU AI Act?"

### Agent Response with SKILL-IACT
```
### 🚦 EU AI Act Compliance Verdict: HIGH-RISK

Based on Regulation (EU) 2024/1689, your application falls under the High-Risk category.

| Category | Riferimento Normativo | Stato / Obbligo |
|---|---|---|
| Domain | Annex III, Item 4(a) | Recruitment & CV screening is classified as High-Risk. |
| Quality & Logging | Article 12 | Implement automated logging to trace decisions. |
| Human Oversight | Article 14 | Design system with a human-in-the-loop interface. |

### 🛠️ Action Plan:
1. Ensure human oversight interfaces (e.g., CV screening scores must be approved/rejected by a HR staff member before final decision).
2. Set up detailed logging of CV parsing inputs and scores.
```

---

## ⚠️ Legal Disclaimer

*This tool provides information and guidance based on Regulation (EU) 2024/1689. It is designed to assist in compliance reviews but does not constitute official legal advice or certification. Always consult with a qualified legal professional for binding regulatory assessments.*

---

## 🗺️ Roadmap & Contributing

We welcome contributions! Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) to learn how to propose updates to the decision paths, add compliance checklists, or improve translation files.

© 2026 Nicola Cuomo | Antigravity Night Powered by Nicola Cuomo
