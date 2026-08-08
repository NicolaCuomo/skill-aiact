# skill-aiact

**"The Vibe-Coder's Safety Net: Automated AppSec & EU AI Act Audit Kit for AI Agents 🛡️⚖️"**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-ready-green.svg)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

---

## 🚀 Quick Start

```bash
# Clone and run
git clone https://github.com/your-org/skill-aiact.git
cd skill-aiact
python3 audit.py /path/to/your/project
```

## 📋 Cosa Fa

SKILL-IACT è un toolkit di audit automatico per sviluppatori "vibe-coder" che usano AI per programmare. Controlla:

### 🔒 Sicurezza Applicativa (OWASP)
- **Secret Leak**: API key, password, token hardcoded
- **SQL Injection**: Query dinamiche non parametrize
- **Path Traversal**: Accesso file con input utente
- **XSS**: Rendering non sicuro di dati utente

### ⚖️ Compliance EU AI Act
- **Audit Log**: Tracciabilità delle decisioni AI
- **PII Handling**: Gestione dati personali
- **Human-in-the-Loop**: Revisione umana per decisioni critiche
- **Risk Assessment**: Valutazione impatto AI

### 💰 Token Hygiene
- **Prompt Bloat**: Prompt >500 token
- **File Optimization**: File >1k token da splittare
- **Repetitive Content**: Contenuti ridondanti

## 📖 Documentazione

| File | Descrizione |
|------|-------------|
| `SKILL.md` | Istruzioni ultra-sline per AI Agent (<40 righe) |
| `audit.py` | Motore CLI principale |
| `checks/` | Moduli di controllo (AppSec, AI Act, Token) |
| `templates/` | Template per auto-riparazione |

## 💡 Esempi d'Uso

```bash
# Scan completo
python3 audit.py /path/to/project

# Solo controlli sicurezza
python3 audit.py --checks appsec

# Output JSON
python3 audit.py --format json

# Combinato
python3 audit.py /app --checks appsec aiact --format json
```

## 🔧 Auto-Riparazione

Dopo l'audit, usa il template generato per ottenere patch automatiche:

1. Esegui `python3 audit.py` sul tuo progetto
2. Copia le vulnerabilità Critical/High
3. Incolla nel template `templates/FIX_PROMPT_TEMPLATE.md`
4. Invia all'AI Developer per la patch
5. Verifica con un nuovo scan

## 📊 Exit Codes

- `0`: Nessuna vulnerabilità Critical/High trovata
- `1`: Trovate vulnerabilità Critical o High

## 🤝 Contributing

Contributi benvenuti! Apri una issue o una PR.

## 📄 License

MIT License - vedi [LICENSE](LICENSE)
