#!/usr/bin/env python3
"""
AppSec OWASP Checks: Secret leak, SQLi, Path Traversal, XSS
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class AppSecChecker:
    """OWASP Top 10 security vulnerability checker."""
    
    # Patterns for detection
    PATTERNS = {
        'secret_leak': [
            (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9]{16,}["\']', 'API Key hardcoded'),
            (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']+["\']', 'Password hardcoded'),
            (r'(?i)(secret|token)\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', 'Secret/Token hardcoded'),
            (r'AWS[A-Z0-9]{15}', 'AWS Access Key ID'),
            (r'(?i)private[_-]?key\s*[=:]', 'Private key reference'),
        ],
        'sql_injection': [
            (r'execute\s*\(\s*["\'].*%s.*["\']', 'SQL with %s formatting'),
            (r'cursor\.execute\s*\(\s*f["\']', 'SQL with f-string'),
            (r'\+\s*["\'].*SELECT.*["\']\s*\+', 'SQL string concatenation'),
            (r'(?i)WHERE.*=\s*["\']?\s*\+', 'Dynamic WHERE clause'),
        ],
        'path_traversal': [
            (r'open\s*\([^)]*\+[^)]*\)', 'File open with concatenation'),
            (r'read_file\s*\([^)]*\+[^)]*\)', 'Read file with user input'),
            (r'(?i)os\.path\.join\s*\([^)]*request', 'Path join with request data'),
        ],
        'xss': [
            (r'innerHTML\s*=', 'Direct innerHTML assignment'),
            (r'document\.write\s*\(', 'Document.write usage'),
            (r'(?i)render_template_string\s*\([^)]*request', 'Template with request data'),
            (r'(?i)\<script\>.*\<\/script\>', 'Inline script tag'),
        ]
    }
    
    def check(self, project_path: Path) -> List[Dict[str, Any]]:
        """Run all AppSec checks on the project."""
        findings = []
        
        # File extensions to scan
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.htm', '.vue', '.php', '.java', '.rb'}
        
        for file_path in project_path.rglob('*'):
            if not file_path.is_file() or file_path.suffix not in extensions:
                continue
            
            # Skip common non-source directories
            if any(part.startswith('.') or part == 'node_modules' or part == '__pycache__' 
                   for part in file_path.parts):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
            except Exception:
                continue
            
            relative_path = str(file_path.relative_to(project_path))
            
            for vuln_type, patterns in self.PATTERNS.items():
                for pattern, description in patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            findings.append({
                                'category': 'AppSec',
                                'type': vuln_type.replace('_', ' ').title(),
                                'severity': self._get_severity(vuln_type),
                                'file': relative_path,
                                'line': line_num,
                                'description': description,
                                'remediation': self._get_remediation(vuln_type)
                            })
        
        return findings
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type."""
        severity_map = {
            'secret_leak': 'CRITICAL',
            'sql_injection': 'CRITICAL',
            'path_traversal': 'HIGH',
            'xss': 'HIGH'
        }
        return severity_map.get(vuln_type, 'MEDIUM')
    
    def _get_remediation(self, vuln_type: str) -> str:
        """Get remediation suggestion for vulnerability type."""
        remediation_map = {
            'secret_leak': 'Use environment variables or a secrets manager. Never commit secrets to version control.',
            'sql_injection': 'Use parameterized queries or prepared statements. Avoid string formatting in SQL.',
            'path_traversal': 'Validate and sanitize file paths. Use allowlists for permitted directories.',
            'xss': 'Escape output, use Content Security Policy, avoid rendering untrusted data as HTML.'
        }
        return remediation_map.get(vuln_type, 'Review and fix according to security best practices.')
