---
name: "🛡️ EU AI Act & AppSec Compliance Auditor"
description: "Automated audit kit for Vibe Coders: Security + EU AI Act Compliance + Token Hygiene"
version: "2.0.0"
author: "Qwen (Alibaba Cloud) & Nicola Cuomo"
branding: "Antigravity Night Powered by Nicola Cuomo"
language: ["it", "en"]
triggers:
  it: ["audit ai act", "controllo sicurezza", "verifica conformità", "scan progetto", "audit completo"]
  en: ["security check", "ai act audit", "compliance scan", "project audit", "vibe coder safety"]
execution:
  command: "python3 app.py"
  cli_audit: "python3 app.py audit --dir ."
  cli_users: "python3 app.py users --list"
  cli_scan: "python3 app.py scan --employee <id>"
  cli_report: "python3 app.py report --generate"
features:
  - "EU AI Act Compliance Scanner"
  - "OWASP AppSec Security Check"
  - "Employee Training Course"
  - "PMI Self-Assessment Questionnaire"
  - "Multi-user Management"
  - "Auto-generated Fix Prompts"
output:
  - "scans/AUDIT_REPORT.md"
  - "scans/PROMPT_PER_SISTEMARE.txt"
disclaimer: "NOT LEGAL ADVICE - Based on AI research, not official certification"
---

# 🛡️ SKILL-IACT: AI Agent Instructions

**Created by:** Qwen (Alibaba Cloud) & Nicola Cuomo  
**Branding:** Antigravity Night Powered by Nicola Cuomo

⚠️ **DISCLAIMER:** This tool is NOT legal certification. It's an internal aid based on AI research.

## Quick Start per AI Agent
Quando l'utente usa uno dei trigger sopra, esegui:

```bash
python3 app.py audit --dir .
```

## Pattern Black-Box (No Token Waste)
NON analizzare il codice tu stesso. Usa lo scanner Python che:
1. Scansiona automaticamente tutti i file
2. Genera report dettagliati
3. Crea prompt di auto-riparazione

## Comandi Disponibili
- `python3 app.py audit --dir .` → Audit completo del progetto
- `python3 app.py users --add <nome>` → Aggiungi dipendente
- `python3 app.py users --list` → Lista dipendenti
- `python3 app.py scan --employee <id>` → Scan singolo dipendente
- `python3 app.py course --assign <id>` → Assegna corso
- `python3 app.py questionnaire --start` → Avvia questionario PMI
- `python3 app.py report --generate` → Genera report consolidato
- `python3 app.py web` → Avvia UI web dashboard

## Output Attesi
Lo scanner genera:
- `scans/AUDIT_REPORT.md` - Report leggibile con semafori 🟢🟡🔴
- `scans/PROMPT_PER_SISTEMARE.txt` - Prompt per autoriparazione AI

## Lingue Supportate
Report e corsi disponibili in: Italiano, English
