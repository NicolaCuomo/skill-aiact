#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SKILL-IACT: EU AI Act & AppSec Compliance Auditor
Application principale con Flask UI + CLI + Audit Engine

Author: System Integrator Italia
License: MIT
Version: 2.0.0
"""

import os
import sys
import json
import hashlib
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import argparse

# ============================================================================
# CONFIGURAZIONE E COSTANTI
# ============================================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SCANS_DIR = BASE_DIR / "scans"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Assicurati che le directory esistano
for directory in [DATA_DIR, SCANS_DIR, STATIC_DIR, TEMPLATES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "skill_iact.db"

# Pattern per sicurezza (AppSec)
SECRET_PATTERNS = {
    "openai_key": r"sk-[a-zA-Z0-9]{48}",
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret_key": r"[0-9A-Za-z/+]{40}",
    "github_token": r"ghp_[a-zA-Z0-9]{36}",
    "stripe_key": r"sk_live_[a-zA-Z0-9]{24}",
    "google_api": r"AIza[0-9A-Za-z_-]{35}",
    "jwt_token": r"eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
    "password_assignment": r"(?i)(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']",
    "db_connection": r"(?i)(mongodb|postgres|mysql|redis)://[^:\s]+:[^@\s]+@",
    "bearer_token": r"(?i)bearer\s+[a-zA-Z0-9_-]{20,}",
}

# Pattern per EU AI Act Compliance
AI_ACT_PATTERNS = {
    "audit_logging": r"(?i)(audit.?log|log.*event|track.*action|record.*decision)",
    "pii_handling": r"(?i)(codice.?fiscale|partita.?iva|iban|email|telefono|indirizzo)",
    "human_in_loop": r"(?i)(confirm|approve|verify|human.?check|manual.?review)",
    "transparency": r"(?i)(explain|rationale|decision.*reason|motivation)",
    "risk_assessment": r"(?i)(risk.*assess|impact.*analysis|threat.*model)",
}

# Pattern PII sensibili
PII_PATTERNS = {
    "codice_fiscale": r"[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]",
    "partita_iva": r"\b[0-9]{11}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "iban": r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{4}[0-9]{7}[A-Z0-9]{0,16}\b",
    "phone": r"\b(?:\+39)?[0-9]{10,15}\b",
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Employee:
    id: int
    name: str
    email: str
    department: str
    created_at: str
    course_completed: bool = False
    course_score: int = 0
    questionnaire_completed: bool = False
    last_scan_date: Optional[str] = None

@dataclass
class ScanResult:
    id: int
    employee_id: int
    scan_type: str  # 'appsec', 'ai_act', 'full'
    score: float
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    details: Dict
    scan_date: str

@dataclass
class QuestionnaireResponse:
    id: int
    employee_id: int
    answers: Dict[int, str]
    total_score: int
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH'
    submitted_at: str

# ============================================================================
# DATABASE MANAGER
# ============================================================================

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inizializza il database con tutte le tabelle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella Employees
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                department TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                course_completed BOOLEAN DEFAULT FALSE,
                course_score INTEGER DEFAULT 0,
                questionnaire_completed BOOLEAN DEFAULT FALSE,
                last_scan_date TEXT
            )
        """)
        
        # Tabella Scan Results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                scan_type TEXT NOT NULL,
                score REAL NOT NULL,
                critical_issues INTEGER DEFAULT 0,
                high_issues INTEGER DEFAULT 0,
                medium_issues INTEGER DEFAULT 0,
                low_issues INTEGER DEFAULT 0,
                details TEXT,
                scan_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        
        # Tabella Questionnaire Responses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questionnaire_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                answers TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        """)
        
        # Tabella Company Assessment
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_data TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                action_plan TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_employee(self, name: str, email: str, department: str = "Generale") -> Optional[int]:
        """Aggiunge un nuovo dipendente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO employees (name, email, department) VALUES (?, ?, ?)",
                (name, email, department)
            )
            conn.commit()
            employee_id = cursor.lastrowid
            return employee_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_employee(self, employee_id: int) -> Optional[Dict]:
        """Ottieni un dipendente per ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_employees(self) -> List[Dict]:
        """Ottieni tutti i dipendenti"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_course_completion(self, employee_id: int, completed: bool, score: int = 0):
        """Aggiorna completamento corso"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employees SET course_completed = ?, course_score = ? WHERE id = ?",
            (completed, score, employee_id)
        )
        conn.commit()
        conn.close()
    
    def save_scan_result(self, employee_id: int, scan_type: str, score: float, 
                         details: Dict, critical: int = 0, high: int = 0,
                         medium: int = 0, low: int = 0) -> int:
        """Salva risultato scan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO scan_results 
               (employee_id, scan_type, score, critical_issues, high_issues, 
                medium_issues, low_issues, details, scan_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (employee_id, scan_type, score, critical, high, medium, low,
             json.dumps(details), datetime.now().isoformat())
        )
        
        # Aggiorna last_scan_date del dipendente
        cursor.execute(
            "UPDATE employees SET last_scan_date = ? WHERE id = ?",
            (datetime.now().isoformat(), employee_id)
        )
        
        conn.commit()
        scan_id = cursor.lastrowid
        conn.close()
        return scan_id
    
    def get_employee_scans(self, employee_id: int) -> List[Dict]:
        """Ottieni tutti gli scan di un dipendente"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM scan_results WHERE employee_id = ? ORDER BY scan_date DESC",
            (employee_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def save_questionnaire_response(self, employee_id: int, answers: Dict, 
                                     total_score: int, risk_level: str) -> int:
        """Salva risposta questionario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO questionnaire_responses 
               (employee_id, answers, total_score, risk_level, submitted_at)
               VALUES (?, ?, ?, ?, ?)""",
            (employee_id, json.dumps(answers), total_score, risk_level,
             datetime.now().isoformat())
        )
        
        cursor.execute(
            "UPDATE employees SET questionnaire_completed = ? WHERE id = ?",
            (True, employee_id)
        )
        
        conn.commit()
        response_id = cursor.lastrowid
        conn.close()
        return response_id
    
    def get_dashboard_stats(self) -> Dict:
        """Ottieni statistiche dashboard"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        stats = {}
        
        # Totale dipendenti
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        stats['total_employees'] = cursor.fetchone()['count']
        
        # Corso completato
        cursor.execute("SELECT COUNT(*) as count FROM employees WHERE course_completed = 1")
        stats['course_completed'] = cursor.fetchone()['count']
        
        # Questionario completato
        cursor.execute("SELECT COUNT(*) as count FROM employees WHERE questionnaire_completed = 1")
        stats['questionnaire_completed'] = cursor.fetchone()['count']
        
        # Scan totali
        cursor.execute("SELECT COUNT(*) as count FROM scan_results")
        stats['total_scans'] = cursor.fetchone()['count']
        
        # Media punteggio ultimi scan
        cursor.execute("""
            SELECT AVG(score) as avg_score FROM scan_results 
            WHERE scan_date >= datetime('now', '-30 days')
        """)
        row = cursor.fetchone()
        stats['avg_score_30days'] = row['avg_score'] if row['avg_score'] else 0
        
        # Issue critiche totali
        cursor.execute("""
            SELECT SUM(critical_issues) as total_critical,
                   SUM(high_issues) as total_high
            FROM scan_results
        """)
        row = cursor.fetchone()
        stats['total_critical'] = row['total_critical'] or 0
        stats['total_high'] = row['total_high'] or 0
        
        conn.close()
        return stats

# ============================================================================
# AUDIT ENGINE
# ============================================================================

class AuditEngine:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.results = {
            'appsec': {'issues': [], 'score': 100},
            'ai_act': {'issues': [], 'score': 100},
            'token_hygiene': {'issues': [], 'score': 100}
        }
    
    def scan_files(self, extensions: List[str] = None) -> List[Path]:
        """Scansiona tutti i file nel progetto"""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.json', '.html', '.md', '.txt', '.env', '.yaml', '.yml']
        
        files = []
        for ext in extensions:
            files.extend(self.project_dir.rglob(f'*{ext}'))
        
        # Escludi directory comuni
        exclude_dirs = {'__pycache__', 'node_modules', '.git', 'venv', 'env', '.venv'}
        filtered_files = [f for f in files if not any(excl in str(f) for excl in exclude_dirs)]
        
        return filtered_files
    
    def check_appsec(self, file_path: Path, content: str) -> List[Dict]:
        """Controlli AppSec e OWASP"""
        issues = []
        
        for pattern_name, pattern in SECRET_PATTERNS.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'type': 'CRITICAL',
                    'category': 'Secret Leak',
                    'pattern': pattern_name,
                    'file': str(file_path),
                    'line': line_num,
                    'message': f"Possibile {pattern_name} rilevato",
                    'recommendation': "Rimuovi immediatamente il segreto e usa variabili d'ambiente"
                })
        
        # Controlla SQL injection
        sqli_patterns = [
            r'execute\s*\(\s*f["\'].*SELECT.*\{',
            r'cursor\.execute\s*\([^,]+%',
            r'\+\s*["\'].*SELECT.*["\']\s*\+',
        ]
        for pattern in sqli_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                line_num = content.count('\n', 0, content.find(re.search(pattern, content).group())) + 1
                issues.append({
                    'type': 'HIGH',
                    'category': 'SQL Injection',
                    'file': str(file_path),
                    'line': line_num,
                    'message': "Possibile SQL Injection - usa query parametrizzate",
                    'recommendation': "Usa prepared statements o ORM"
                })
        
        # Controlla Path Traversal
        if re.search(r'open\s*\([^)]*\+[^)]*\)', content) or \
           re.search(r'os\.path\.join\s*\([^)]*request', content, re.IGNORECASE):
            issues.append({
                'type': 'HIGH',
                'category': 'Path Traversal',
                'file': str(file_path),
                'message': "Possibile Path Traversal - valida gli input",
                'recommendation': "Sanitizza tutti i percorsi file"
            })
        
        return issues
    
    def check_ai_act_compliance(self, file_path: Path, content: str) -> List[Dict]:
        """Controlli conformità EU AI Act"""
        issues = []
        
        # Controlla presenza audit logging
        has_logging = any(re.search(p, content, re.IGNORECASE) for p in AI_ACT_PATTERNS['audit_logging'])
        if not has_logging and '.py' in str(file_path):
            issues.append({
                'type': 'MEDIUM',
                'category': 'Art. 12 - Audit Logging',
                'file': str(file_path),
                'message': "Nessun sistema di audit logging rilevato",
                'recommendation': "Implementa logging strutturato per tracciare decisioni AI"
            })
        
        # Controlla gestione PII
        for pii_type, pattern in PII_PATTERNS.items():
            if re.search(pattern, content):
                issues.append({
                    'type': 'HIGH',
                    'category': 'Art. 10 - PII Handling',
                    'file': str(file_path),
                    'message': f"Possibile {pii_type} non anonimizzato",
                    'recommendation': "Anonimizza o pseudonimizza i dati personali prima di inviarli all'AI"
                })
        
        # Controlla Human-in-the-Loop
        functions_to_check = ['send_email', 'delete_', 'payment', 'transfer', 'approve']
        for func in functions_to_check:
            if func in content.lower():
                has_hitl = re.search(AI_ACT_PATTERNS['human_in_loop'], content, re.IGNORECASE)
                if not has_hitl:
                    issues.append({
                        'type': 'MEDIUM',
                        'category': 'Art. 14 - Human-in-the-Loop',
                        'file': str(file_path),
                        'message': f"Funzione critica '{func}' senza supervisione umana evidente",
                        'recommendation': "Aggiungi conferma umana per operazioni critiche"
                    })
        
        return issues
    
    def check_token_hygiene(self, file_path: Path, content: str) -> List[Dict]:
        """Controlli igiene token e performance"""
        issues = []
        
        # Controlla prompt bloat
        if file_path.suffix in ['.md', '.txt']:
            word_count = len(content.split())
            token_estimate = word_count * 1.3  # Stima approssimativa
            if token_estimate > 1000:
                issues.append({
                    'type': 'LOW',
                    'category': 'Token Bloat',
                    'file': str(file_path),
                    'message': f"File grande (~{int(token_estimate)} token)",
                    'recommendation': "Considera di suddividere prompt lunghi per ridurre costi"
                })
        
        return issues
    
    def run_full_audit(self) -> Dict:
        """Esegue audit completo"""
        files = self.scan_files()
        
        all_issues = []
        
        for file_path in files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            
            # AppSec
            appsec_issues = self.check_appsec(file_path, content)
            all_issues.extend(appsec_issues)
            
            # AI Act
            ai_act_issues = self.check_ai_act_compliance(file_path, content)
            all_issues.extend(ai_act_issues)
            
            # Token Hygiene
            token_issues = self.check_token_hygiene(file_path, content)
            all_issues.extend(token_issues)
        
        # Calcola punteggi
        critical = len([i for i in all_issues if i['type'] == 'CRITICAL'])
        high = len([i for i in all_issues if i['type'] == 'HIGH'])
        medium = len([i for i in all_issues if i['type'] == 'MEDIUM'])
        low = len([i for i in all_issues if i['type'] == 'LOW'])
        
        # Score calculation
        appsec_score = max(0, 100 - (critical * 20) - (high * 10) - (medium * 5))
        ai_act_score = max(0, 100 - (high * 15) - (medium * 5))
        overall_score = (appsec_score + ai_act_score) / 2
        
        return {
            'timestamp': datetime.now().isoformat(),
            'project_dir': str(self.project_dir),
            'files_scanned': len(files),
            'overall_score': round(overall_score, 2),
            'appsec_score': appsec_score,
            'ai_act_score': ai_act_score,
            'summary': {
                'critical': critical,
                'high': high,
                'medium': medium,
                'low': low,
                'total': len(all_issues)
            },
            'issues': all_issues
        }
    
    def generate_fix_prompt(self, results: Dict) -> str:
        """Genera prompt per autoriparazione AI"""
        prompt = """# 🤖 PROMPT PER AUTORIZPARAZIONE AI

Ciao! Ho eseguito uno scan di sicurezza e conformità sul mio progetto.
Per favore, aiutami a risolvere i seguenti problemi:

## 📊 RIEPILOGO
- **Punteggio Generale:** {overall_score}/100
- **File Scansionati:** {files_scanned}
- **Issue Totali:** {total_issues}

## 🔴 CRITICI ({critical})
""".format(
            overall_score=results['overall_score'],
            files_scanned=results['files_scanned'],
            total_issues=results['summary']['total'],
            critical=results['summary']['critical']
        )
        
        critical_issues = [i for i in results['issues'] if i['type'] == 'CRITICAL']
        for issue in critical_issues[:5]:  # Max 5 critical
            prompt += f"- [{issue['category']}] {issue['file']}:{issue.get('line', '?')} - {issue['message']}\n"
        
        prompt += "\n## 🟠 ALTI ({high})\n".format(high=results['summary']['high'])
        high_issues = [i for i in results['issues'] if i['type'] == 'HIGH']
        for issue in high_issues[:5]:
            prompt += f"- [{issue['category']}] {issue['file']}:{issue.get('line', '?')} - {issue['message']}\n"
        
        prompt += """
## 🎯 ISTRUZIONI
Per ogni problema:
1. Spiega il rischio in modo semplice
2. Fornisci il codice corretto
3. Indica come testare la fix

Grazie!
"""
        
        return prompt

# ============================================================================
# FLASK APPLICATION
# ============================================================================

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = DatabaseManager(DB_PATH)

# ============================================================================
# ROUTES WEB UI
# ============================================================================

@app.route('/')
def index():
    """Dashboard principale"""
    stats = db.get_dashboard_stats()
    employees = db.get_all_employees()[:10]  # Ultimi 10
    return render_template('index.html', stats=stats, employees=employees)

@app.route('/employees')
def employees_list():
    """Lista tutti i dipendenti"""
    employees = db.get_all_employees()
    return render_template('employees.html', employees=employees)

@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    """Aggiungi nuovo dipendente"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        
        if not name or not email:
            flash('Nome ed email sono obbligatori', 'error')
            return redirect(url_for('add_employee'))
        
        employee_id = db.add_employee(name, email, department)
        if employee_id:
            flash(f'Dipendente {name} aggiunto con successo!', 'success')
            return redirect(url_for('employees_list'))
        else:
            flash('Email già registrata', 'error')
    
    return render_template('add_employee.html')

@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    """Dettaglio dipendente"""
    employee = db.get_employee(employee_id)
    if not employee:
        flash('Dipendente non trovato', 'error')
        return redirect(url_for('employees_list'))
    
    scans = db.get_employee_scans(employee_id)
    return render_template('employee_detail.html', employee=employee, scans=scans)

@app.route('/course')
def course():
    """Pagina corso formazione"""
    return render_template('course.html')

@app.route('/course/complete', methods=['POST'])
def complete_course():
    """Completa corso"""
    employee_id = request.form.get('employee_id', type=int)
    score = request.form.get('score', type=int, default=0)
    
    if employee_id:
        db.update_course_completion(employee_id, True, score)
        flash('Corso completato con successo!', 'success')
    
    return redirect(url_for('employee_detail', employee_id=employee_id))

@app.route('/questionnaire')
def questionnaire():
    """Questionario autovalutazione"""
    return render_template('questionnaire.html')

@app.route('/questionnaire/submit', methods=['POST'])
def submit_questionnaire():
    """Invia questionario"""
    employee_id = request.form.get('employee_id', type=int)
    answers = {}
    
    # Estrai risposte dal form
    for key, value in request.form.items():
        if key.startswith('q'):
            try:
                q_num = int(key[1:])
                answers[q_num] = value
            except ValueError:
                continue
    
    # Calcola punteggio
    score_map = {'yes': 2, 'partial': 1, 'no': 0, 'unknown': 0}
    total_score = sum(score_map.get(v.lower(), 0) for v in answers.values())
    
    # Determina livello rischio
    if total_score >= 24:
        risk_level = 'LOW'
    elif total_score >= 15:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'HIGH'
    
    if employee_id:
        db.save_questionnaire_response(employee_id, answers, total_score, risk_level)
        flash(f'Questionario compilato! Punteggio: {total_score}/30 - Rischio: {risk_level}', 'success')
    
    return redirect(url_for('employee_detail', employee_id=employee_id))

@app.route('/scan', methods=['GET', 'POST'])
def run_scan():
    """Esegui scan su progetto"""
    if request.method == 'POST':
        project_dir = request.form.get('project_dir', '.')
        employee_id = request.form.get('employee_id', type=int)
        
        engine = AuditEngine(Path(project_dir))
        results = engine.run_full_audit()
        
        # Salva risultato
        if employee_id:
            scan_id = db.save_scan_result(
                employee_id=employee_id,
                scan_type='full',
                score=results['overall_score'],
                details=results,
                critical=results['summary']['critical'],
                high=results['summary']['high'],
                medium=results['summary']['medium'],
                low=results['summary']['low']
            )
            results['scan_id'] = scan_id
        
        # Genera fix prompt
        fix_prompt = engine.generate_fix_prompt(results)
        
        # Salva report
        report_path = SCANS_DIR / f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        return render_template('scan_results.html', results=results, fix_prompt=fix_prompt)
    
    employees = db.get_all_employees()
    return render_template('scan.html', employees=employees)

@app.route('/reports')
def reports():
    """Lista report"""
    scan_files = sorted(SCANS_DIR.glob('*.json'), reverse=True)
    reports = []
    for sf in scan_files[:50]:  # Max 50 report
        try:
            with open(sf) as f:
                data = json.load(f)
                reports.append({
                    'filename': sf.name,
                    'timestamp': data.get('timestamp', ''),
                    'score': data.get('overall_score', 0),
                    'issues': data.get('summary', {}).get('total', 0)
                })
        except Exception:
            continue
    
    return render_template('reports.html', reports=reports)

@app.route('/api/stats')
def api_stats():
    """API per statistiche"""
    return jsonify(db.get_dashboard_stats())

@app.route('/api/employees')
def api_employees():
    """API per lista dipendenti"""
    return jsonify(db.get_all_employees())

# ============================================================================
# CLI COMMANDS
# ============================================================================

def cli_audit(args):
    """Comando CLI: audit"""
    print("🛡️  SKILL-IACT: EU AI Act & AppSec Compliance Auditor")
    print("=" * 60)
    
    project_dir = Path(args.dir) if args.dir else Path('.')
    print(f"📁 Progetto: {project_dir.absolute()}")
    print()
    
    engine = AuditEngine(project_dir)
    results = engine.run_full_audit()
    
    # Stampa risultati
    print("📊 RISULTATI AUDIT")
    print("-" * 60)
    print(f"File scansionati: {results['files_scanned']}")
    print(f"Punteggio generale: {results['overall_score']}/100")
    print()
    print("🔴 Critici:", results['summary']['critical'])
    print("🟠 Alti:", results['summary']['high'])
    print("🟡 Medi:", results['summary']['medium'])
    print("🔵 Bassi:", results['summary']['low'])
    print()
    
    # Salva report
    report_path = SCANS_DIR / "AUDIT_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 🛡️ SKILL-IACT Audit Report\n\n")
        f.write(f"**Data:** {results['timestamp']}\n")
        f.write(f"**Progetto:** {results['project_dir']}\n")
        f.write(f"**Punteggio:** {results['overall_score']}/100\n\n")
        f.write(f"## Riepilogo\n\n")
        f.write(f"- File scansionati: {results['files_scanned']}\n")
        f.write(f"- Issue totali: {results['summary']['total']}\n\n")
        f.write(f"## Issue Critiche\n\n")
        for issue in [i for i in results['issues'] if i['type'] == 'CRITICAL'][:10]:
            f.write(f"- 🔴 {issue['message']} ({issue['file']}:{issue.get('line', '?')})\n")
    
    print(f"✅ Report salvato: {report_path}")
    
    # Genera fix prompt
    fix_prompt = engine.generate_fix_prompt(results)
    fix_path = SCANS_DIR / "PROMPT_PER_SISTEMARE.txt"
    with open(fix_path, 'w', encoding='utf-8') as f:
        f.write(fix_prompt)
    
    print(f"✅ Fix prompt salvato: {fix_path}")
    print()
    
    # Exit code
    if results['summary']['critical'] > 0 or results['summary']['high'] > 0:
        print("⚠️  Trovate vulnerabilità critiche o alte!")
        return 1
    else:
        print("✅ Nessuna vulnerabilità critica o alta trovata")
        return 0

def cli_users(args):
    """Comando CLI: users"""
    if args.list:
        employees = db.get_all_employees()
        print("👥 DIPENDENTI REGISTRATI")
        print("-" * 60)
        for emp in employees:
            status = "✅" if emp['course_completed'] else "❌"
            print(f"{emp['id']}. {emp['name']} ({emp['email']}) - Corso: {status}")
    elif args.add:
        name, email = args.add.split(':')
        emp_id = db.add_employee(name.strip(), email.strip())
        if emp_id:
            print(f"✅ Dipendente aggiunto: ID {emp_id}")
        else:
            print("❌ Email già registrata")

def cli_scan(args):
    """Comando CLI: scan singolo dipendente"""
    employee_id = args.employee
    employee = db.get_employee(employee_id)
    
    if not employee:
        print(f"❌ Dipendente {employee_id} non trovato")
        return 1
    
    print(f"🔍 Scan per: {employee['name']}")
    project_dir = Path(args.dir) if args.dir else Path('.')
    
    engine = AuditEngine(project_dir)
    results = engine.run_full_audit()
    
    scan_id = db.save_scan_result(
        employee_id=employee_id,
        scan_type='full',
        score=results['overall_score'],
        details=results,
        critical=results['summary']['critical'],
        high=results['summary']['high']
    )
    
    print(f"✅ Scan completato - ID: {scan_id}")
    print(f"Punteggio: {results['overall_score']}/100")
    
    return 0

def cli_report(args):
    """Comando CLI: genera report"""
    if args.generate:
        stats = db.get_dashboard_stats()
        report = f"""# 📊 REPORT CONSOLIDATO SKILL-IACT

**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Statistiche Generali

- **Totale Dipendenti:** {stats['total_employees']}
- **Corso Completato:** {stats['course_completed']} ({stats['course_completed']/max(stats['total_employees'],1)*100:.1f}%)
- **Questionario Completato:** {stats['questionnaire_completed']}
- **Scan Totali:** {stats['total_scans']}
- **Punteggio Medio (30gg):** {stats['avg_score_30days']:.1f}/100

## Issue Rilevate

- **Critiche:** {stats['total_critical']}
- **Alte:** {stats['total_high']}

## Raccomandazioni

"""
        if stats['total_critical'] > 0:
            report += "🔴 **URGENTE:** Risolvere immediatamente le issue critiche\n"
        if stats['course_completed'] < stats['total_employees'] * 0.8:
            report += "⚠️ **FORMAZIONE:** Completare formazione per tutti i dipendenti\n"
        
        report_path = SCANS_DIR / "CONSOLIDATED_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report generato: {report_path}")

def main():
    parser = argparse.ArgumentParser(
        description='🛡️ SKILL-IACT: EU AI Act & AppSec Compliance Auditor'
    )
    subparsers = parser.add_subparsers(dest='command', help='Comandi disponibili')
    
    # Comando: audit
    audit_parser = subparsers.add_parser('audit', help='Esegui audit completo')
    audit_parser.add_argument('--dir', '-d', help='Directory progetto da scansionare')
    audit_parser.set_defaults(func=cli_audit)
    
    # Comando: users
    users_parser = subparsers.add_parser('users', help='Gestione dipendenti')
    users_parser.add_argument('--list', '-l', action='store_true', help='Lista dipendenti')
    users_parser.add_argument('--add', '-a', help='Aggiungi dipendente (nome:email)')
    users_parser.set_defaults(func=cli_users)
    
    # Comando: scan
    scan_parser = subparsers.add_parser('scan', help='Scan singolo dipendente')
    scan_parser.add_argument('--employee', '-e', type=int, required=True, help='ID dipendente')
    scan_parser.add_argument('--dir', '-d', help='Directory progetto')
    scan_parser.set_defaults(func=cli_scan)
    
    # Comando: report
    report_parser = subparsers.add_parser('report', help='Genera report')
    report_parser.add_argument('--generate', '-g', action='store_true', help='Genera report consolidato')
    report_parser.set_defaults(func=cli_report)
    
    # Comando: web
    web_parser = subparsers.add_parser('web', help='Avvia interfaccia web')
    web_parser.add_argument('--host', default='0.0.0.0', help='Host binding')
    web_parser.add_argument('--port', type=int, default=5000, help='Porta')
    web_parser.set_defaults(func=lambda args: app.run(host=args.host, port=args.port, debug=True))
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
