#!/usr/bin/env python3
"""
SKILL-IACT: Application Security (AppSec) Audit Module

Scans project files for security vulnerabilities following OWASP Top 10:
- Secret leaks (API keys, passwords, tokens)
- SQL Injection vulnerabilities
- Path Traversal issues
- Cross-Site Scripting (XSS)
- Exposed .env files and git configuration
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Any, Set


class AppSecChecker:
    """
    OWASP Top 10 security vulnerability checker.
    
    Detects:
    - Hardcoded secrets and credentials
    - SQL injection patterns
    - Path traversal vulnerabilities
    - XSS vectors
    - Misconfigured .gitignore and exposed files
    """

    # Vulnerability patterns organized by type
    VULNERABILITY_PATTERNS = {
        'secret_leak': {
            'description': 'Hardcoded secrets detected',
            'severity': 'CRITICAL',
            'patterns': [
                (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9]{16,}["\']', 'API Key hardcoded'),
                (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']+["\']', 'Password hardcoded'),
                (r'(?i)(secret|token|auth[_-]?token)\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', 'Secret/Token hardcoded'),
                (r'AWS[A-Z0-9]{15}', 'AWS Access Key ID detected'),
                (r'(?i)private[_-]?key\s*[=:]', 'Private key reference'),
                (r'sk-[a-zA-Z0-9]{32,}', 'OpenAI API Key detected'),
                (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
                (r'xox[baprs]-[a-zA-Z0-9-]{10,}', 'Slack Token detected'),
            ],
            'remediation': 'Use environment variables or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault). Never commit secrets to version control.'
        },
        'sql_injection': {
            'description': 'Potential SQL injection vulnerability',
            'severity': 'CRITICAL',
            'patterns': [
                (r'cursor\.execute\s*\(\s*f["\']', 'SQL with f-string interpolation'),
                (r'execute\s*\([^)]*%\s*%', 'SQL with % formatting'),
                (r'\+\s*["\'].*SELECT', 'SQL string concatenation'),
            ],
            'remediation': 'Use parameterized queries or prepared statements. Never concatenate user input into SQL queries.'
        },
        'path_traversal': {
            'description': 'Potential path traversal vulnerability',
            'severity': 'HIGH',
            'patterns': [
                (r'open\s*\([^)]*\+[^)]*\)', 'File open with string concatenation'),
                (r'read_file\s*\([^)]*\+[^)]*\)', 'Read file with dynamic path'),
                (r'(?i)os\.path\.join\s*\([^)]*request', 'Path join with request data'),
            ],
            'remediation': 'Validate and sanitize file paths. Use allowlists for permitted directories. Avoid using user input directly in file operations.'
        },
        'xss': {
            'description': 'Potential XSS vulnerability',
            'severity': 'HIGH',
            'patterns': [
                (r'innerHTML\s*=', 'Direct innerHTML assignment'),
                (r'document\.write\s*\(', 'Document.write usage'),
                (r'(?i)dangerouslySetInnerHTML', 'React dangerouslySetInnerHTML usage'),
                (r'v-html\s*=', 'Vue v-html directive (potential XSS)'),
            ],
            'remediation': 'Escape all output, use Content Security Policy (CSP), and avoid rendering untrusted data as HTML. Use framework-safe methods.'
        },
        'eval_injection': {
            'description': 'Dangerous code evaluation',
            'severity': 'CRITICAL',
            'patterns': [
                (r'\beval\s*\(', 'eval() usage'),
                (r'\bexec\s*\(', 'exec() usage'),
            ],
            'remediation': 'Avoid eval/exec with dynamic input. Use safe alternatives like ast.literal_eval() for Python or JSON.parse() for JavaScript.'
        }
    }

    # File-level checks
    FILE_CHECKS = {
        '.gitignore': {
            'check_type': 'content',
            'required_patterns': ['.env', '*.pem', '*.key', 'credentials'],
            'severity': 'MEDIUM',
            'description': '.gitignore missing critical patterns',
            'remediation': 'Add .env, *.pem, *.key, and credentials to .gitignore.'
        }
    }

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []

    def check(self, project_path: Path) -> List[Dict[str, Any]]:
        """
        Run all AppSec checks on the project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            List of security findings
        """
        self.findings = []
        
        # Source code extensions to scan
        source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', 
                            '.htm', '.vue', '.php', '.java', '.rb', '.go', '.cs'}
        
        # Track files checked
        env_files_found: List[Path] = []
        
        for file_path in project_path.rglob('*'):
            if not file_path.is_file():
                continue
                
            # Skip common non-source directories
            if self._should_skip_path(file_path):
                continue
            
            relative_path = str(file_path.relative_to(project_path))
            
            # Check for .env files
            if file_path.name == '.env' or file_path.name.endswith('.env'):
                env_files_found.append(file_path)
            
            # Check .gitignore content
            if file_path.name == '.gitignore':
                self._check_gitignore(file_path, relative_path)
                continue
            
            # Scan source files for vulnerability patterns
            if file_path.suffix in source_extensions:
                self._scan_source_file(file_path, relative_path)
        
        # Report .env files not in gitignore
        for env_file in env_files_found:
            self._add_finding(
                category='AppSec',
                vuln_type='Exposed .env File',
                severity='HIGH',
                file=str(env_file.relative_to(project_path)),
                line='N/A',
                description='.env file detected - verify it is properly protected',
                remediation='Ensure .env is in .gitignore. Consider using a secrets manager.'
            )
        
        return self.findings

    def _scan_source_file(self, file_path: Path, relative_path: str) -> None:
        """Scan a source file for vulnerability patterns."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
        except Exception:
            return
        
        for vuln_type, config in self.VULNERABILITY_PATTERNS.items():
            for pattern, description in config['patterns']:
                for line_num, line in enumerate(lines, 1):
                    try:
                        if re.search(pattern, line):
                            self._add_finding(
                                category='AppSec',
                                vuln_type=vuln_type.replace('_', ' ').title(),
                                severity=config['severity'],
                                file=relative_path,
                                line=line_num,
                                description=description,
                                remediation=config['remediation']
                            )
                    except re.error:
                        # Skip invalid regex patterns
                        pass

    def _check_gitignore(self, file_path: Path, relative_path: str) -> None:
        """Check .gitignore for required security patterns."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
        except Exception:
            return
        
        required_patterns = self.FILE_CHECKS['.gitignore']['required_patterns']
        
        for pattern in required_patterns:
            if pattern.lower() not in content:
                self._add_finding(
                    category='AppSec',
                    vuln_type='Git Configuration',
                    severity='MEDIUM',
                    file=relative_path,
                    line='N/A',
                    description=f".gitignore missing '{pattern}' pattern",
                    remediation=f"Add '{pattern}' to .gitignore to prevent accidental commits."
                )

    def _add_finding(self, category: str, vuln_type: str, severity: str,
                     file: str, line: int, description: str, remediation: str) -> None:
        """Add a security finding to the results."""
        self.findings.append({
            'category': category,
            'type': vuln_type,
            'severity': severity,
            'file': file,
            'line': line,
            'description': description,
            'remediation': remediation
        })

    def _should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped during scanning."""
        skip_dirs = {'.git', '.svn', '.hg', 'node_modules', '__pycache__',
                     'venv', '.venv', 'env', '.env', 'dist', 'build',
                     '.idea', '.vscode', 'coverage', '.pytest_cache',
                     'vendor', 'bower_components'}
        
        return any(part in skip_dirs for part in path.parts)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of findings.
        
        Returns:
            Dictionary with counts by severity
        """
        summary = {
            'total': len(self.findings),
            'by_severity': {},
            'by_type': {}
        }
        
        for finding in self.findings:
            severity = finding['severity']
            vuln_type = finding['type']
            
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            summary['by_type'][vuln_type] = summary['by_type'].get(vuln_type, 0) + 1
        
        return summary


def main():
    """Standalone execution for testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audit_appsec.py <project_path>")
        sys.exit(1)
    
    project_path = Path(sys.argv[1])
    
    if not project_path.is_dir():
        print(f"Error: '{project_path}' is not a valid directory")
        sys.exit(1)
    
    checker = AppSecChecker()
    findings = checker.check(project_path)
    summary = checker.get_summary()
    
    print(f"\n{'='*60}")
    print(f"Application Security (AppSec) Audit Report")
    print(f"{'='*60}\n")
    
    print(f"Total Findings: {summary['total']}")
    print("\nBy Severity:")
    for severity, count in sorted(summary['by_severity'].items()):
        icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')
        print(f"  {icon} {severity}: {count}")
    
    print(f"\n{'-'*60}")
    print(f"Detailed Findings:\n")
    
    # Sort by severity
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    sorted_findings = sorted(findings, key=lambda x: severity_order.get(x['severity'], 4))
    
    for i, finding in enumerate(sorted_findings, 1):
        icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(finding['severity'], '⚪')
        print(f"[{i}] {icon} [{finding['severity']}] {finding['type']}")
        print(f"    File: {finding['file']}:{finding['line']}")
        print(f"    Issue: {finding['description']}")
        print(f"    💡 Fix: {finding['remediation']}\n")
    
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
