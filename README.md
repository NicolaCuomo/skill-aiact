# 🛡️ skill-aiact

**The Vibe-Coder's Safety Net: Automated AppSec & EU AI Act Audit Kit for AI Agents**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-ready-green.svg)](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/skill-aiact.git
cd skill-aiact

# Run a full audit on your project
python3 scripts/cli.py audit /path/to/your/project

# Save report to file
python3 scripts/cli.py audit . --output REPORT.md
```

---

## 📋 What It Does

SKILL-IACT is an automated audit toolkit designed for **"vibe-coders"** – developers who use AI assistants (Cursor, Claude Code, Antigravity) to write code. It performs two critical checks:

### 🔐 1. Application Security (OWASP Top 10)

Scans your codebase for common security vulnerabilities:

| Check | Description | Severity |
|-------|-------------|----------|
| **Secret Leak** | Hardcoded API keys, passwords, tokens | 🔴 CRITICAL |
| **SQL Injection** | Dynamic SQL queries without parameterization | 🔴 CRITICAL |
| **Path Traversal** | File access with unsanitized user input | 🟠 HIGH |
| **XSS** | Unsafe rendering of user data | 🟠 HIGH |
| **Eval Injection** | Dangerous eval/exec usage | 🔴 CRITICAL |
| **.env Exposure** | Exposed environment files | 🟠 HIGH |
| **Git Config** | Missing patterns in .gitignore | 🟡 MEDIUM |

### ⚖️ 2. EU AI Act Compliance

Verifies your AI system meets regulatory requirements:

| Requirement | Article | Description |
|-------------|---------|-------------|
| **Audit Logging** | Art. 12 | Traceability of AI decisions |
| **PII Handling** | Art. 10 + GDPR | Personal data protection |
| **Human-in-the-Loop** | Art. 14 | Human oversight mechanisms |
| **Risk Assessment** | Art. 9 | Risk management system |
| **Transparency** | Art. 50 | AI disclosure obligations |
| **Data Governance** | Art. 10 | Data quality and bias mitigation |

---

## 🎯 Why Vibe-Coders Need This

When you're coding with AI, it's easy to:

- ❌ Accidentally paste API keys into code
- ❌ Generate SQL queries without parameterization
- ❌ Forget audit logging for AI decisions
- ❌ Miss human review requirements for high-risk outputs

**SKILL-IACT catches these issues before they reach production.**

---

## 💻 Usage

### Basic Commands

```bash
# Full audit (AppSec + EU AI Act)
python3 scripts/cli.py audit /path/to/project

# Only security checks
python3 scripts/cli.py audit . --checks appsec

# Only AI Act compliance
python3 scripts/cli.py audit . --checks aiact

# Output as JSON
python3 scripts/cli.py audit . --format json

# Save Markdown report
python3 scripts/cli.py audit . --format markdown --output REPORT.md
```

### Generate Auto-Fix Prompts

After running an audit, generate a prompt for your AI developer:

```bash
# First, create a JSON report
python3 scripts/cli.py audit . --format json --output report.json

# Generate fix prompt
python3 scripts/cli.py generate-fix report.json --output FIX_PROMPT.md
```

Then copy `FIX_PROMPT.md` into your AI coding assistant!

---

## 📊 Example Output

### CLI Output

```
🔍 SKILL-IACT AUDIT REPORT - 5 issue(s) found
======================================================================

📁 AppSec
--------------------------------------------------

[1] 🔴 [CRITICAL]
    Type: Secret Leak
    File: src/config.py:15
    Issue: API Key hardcoded
    💡 Fix: Use environment variables or a secrets manager...

[2] 🟠 [HIGH]
    Type: SQL Injection
    File: src/database.py:42
    Issue: SQL with f-string interpolation
    💡 Fix: Use parameterized queries...

📁 EU AI Act
--------------------------------------------------

[3] 🟠 [HIGH]
    Type: Audit Logging
    File: project-wide:N/A
    Issue: ✗ Missing: System must maintain audit logs...
    💡 Fix: Implement comprehensive logging for all AI decisions...

======================================================================
```

### Compliance Score

```
⚖️ EU AI Act Compliance Score

- Score: 50.0%
- Status: PARTIAL
- Requirements Met: 3/6
```

---

## 📁 Project Structure

```
skill-aiact/
├── SKILL.md                     # AI Agent instructions (<40 righe)
├── README.md                    # This file
├── scripts/
│   ├── cli.py                   # Main CLI entry point
│   ├── audit_ai_act.py          # EU AI Act compliance checker
│   └── audit_appsec.py          # OWASP security checker
└── examples/
    └── sample-report.json       # Example audit report
```

---

## 🔧 Integration Examples

### GitHub Actions

```yaml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run SKILL-IACT
        run: |
          python3 scripts/cli.py audit . --format json --output audit-report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit-report.json
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running SKILL-IACT security audit..."
python3 scripts/cli.py audit . --checks appsec

if [ $? -eq 1 ]; then
    echo "❌ Security issues found. Please fix before committing."
    exit 1
fi

echo "✅ No security issues detected."
exit 0
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add new vulnerability patterns** – Submit regex patterns for new attack vectors
2. **Improve AI Act checks** – Add more compliance requirements
3. **Bug reports** – Open issues for false positives/negatives
4. **Documentation** – Improve guides and examples

### Development Setup

```bash
# Clone fork
git clone https://github.com/your-username/skill-aiact.git
cd skill-aiact

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies (none required - pure Python!)
pip install -e .

# Run tests
python3 -m pytest tests/
```

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **OWASP Foundation** – For the Top 10 vulnerability guidelines
- **European Commission** – For the EU AI Act framework
- **Vibe-Coders everywhere** – For pushing the boundaries of AI-assisted development

---

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/your-org/skill-aiact/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/skill-aiact/discussions)

---

<div align="center">

**Built with ❤️ for the AI-native developer community**

[⬆ Back to top](#-skill-aiact)

</div>
