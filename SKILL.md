---
name: "🛡️ EU AI Act & AppSec Compliance Auditor"
description: "Automated audit kit for Vibe Coders: Security + EU AI Act Compliance + Token Hygiene"
version: "2.0.0"
author: "System Integrator Italia"
language: ["it", "en", "de", "fr", "es"]
triggers:
  it: ["audit ai act", "controllo sicurezza", "verifica conformità", "scan progetto", "audit completo"]
  en: ["security check", "ai act audit", "compliance scan", "project audit", "vibe coder safety"]
  de: ["sicherheitscheck", "ai act prüfung", "konformitäts-scan"]
  fr: ["vérification sécurité", "audit ai act", "scan conformité"]
  es: ["verificación seguridad", "auditoría ai act", "escaneo conformidad"]
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
  - "Massive Employee Results Dashboard"
  - "Auto-generated Fix Prompts"
  - "Multilingual Support (IT/EN/DE/FR/ES)"
output:
  - "AUDIT_REPORT.md"
  - "PROMPT_PER_SISTEMARE.txt"
  - "EMPLOYEE_RESULTS.json"
  - "PMI_ASSESSMENT.pdf"
---

# 🛡️ SKILL-IACT: AI Agent Instructions

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
- `python3 app.py dashboard` → Avvia UI web

## Output Attesi
Lo scanner genera:
- `scans/AUDIT_REPORT.md` - Report leggibile con semafori 🟢🟡🔴
- `scans/PROMPT_PER_SISTEMARE.txt` - Prompt per autoriparazione AI
- `data/EMPLOYEE_RESULTS.json` - Risultati dipendenti
- `data/PMI_ASSESSMENT.json` - Autovalutazione PMI

## Lingue Supportate
Tutti i report e corsi sono disponibili in: Italiano, English, Deutsch, Français, Español
