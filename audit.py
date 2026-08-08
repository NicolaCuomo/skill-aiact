#!/usr/bin/env python3
"""
SKILL-IACT: Automated AppSec & EU AI Act Audit Kit
Usage: python3 audit.py [path/to/project] [--checks CHECKS] [--format FORMAT]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# Import check modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from checks.appsec_owasp import AppSecChecker
from checks.ai_act_compliance import AIActChecker
from checks.token_hygiene import TokenHygieneChecker


class AuditEngine:
    """Main audit engine orchestrating all checks."""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.checkers = {
            'appsec': AppSecChecker(),
            'aiact': AIActChecker(),
            'token': TokenHygieneChecker()
        }
        self.findings: List[Dict[str, Any]] = []
    
    def run(self, checks_filter: List[str] = None) -> List[Dict[str, Any]]:
        """Run all or filtered checks on the project."""
        if checks_filter is None:
            checks_filter = list(self.checkers.keys())
        
        for check_name in checks_filter:
            if check_name not in self.checkers:
                print(f"⚠️  Unknown check: {check_name}")
                continue
            
            checker = self.checkers[check_name]
            findings = checker.check(self.project_path)
            self.findings.extend(findings)
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        self.findings.sort(key=lambda x: severity_order.get(x.get('severity', 'LOW'), 4))
        
        return self.findings
    
    def report_cli(self, findings: List[Dict[str, Any]]) -> str:
        """Generate CLI report."""
        if not findings:
            return "\n✅ No issues found! Project looks clean.\n"
        
        report = f"\n🔍 AUDIT REPORT - {len(findings)} issue(s) found\n"
        report += "=" * 60 + "\n"
        
        for i, finding in enumerate(findings, 1):
            severity_icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}
            icon = severity_icon.get(finding.get('severity', 'LOW'), '⚪')
            
            report += f"\n[{i}] {icon} [{finding.get('severity', 'UNKNOWN')}] {finding.get('category', 'N/A')}\n"
            report += f"    Type: {finding.get('type', 'N/A')}\n"
            report += f"    File: {finding.get('file', 'N/A')}:{finding.get('line', 'N/A')}\n"
            report += f"    Issue: {finding.get('description', 'N/A')}\n"
            if finding.get('remediation'):
                report += f"    💡 Fix: {finding['remediation']}\n"
        
        report += "\n" + "=" * 60 + "\n"
        return report
    
    def report_json(self, findings: List[Dict[str, Any]]) -> str:
        """Generate JSON report."""
        return json.dumps({
            'project': str(self.project_path),
            'total_findings': len(findings),
            'findings': findings
        }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='SKILL-IACT: Automated AppSec & EU AI Act Audit'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to project directory (default: current directory)'
    )
    parser.add_argument(
        '--checks',
        nargs='+',
        choices=['appsec', 'aiact', 'token'],
        default=None,
        help='Specific checks to run (default: all)'
    )
    parser.add_argument(
        '--format',
        choices=['cli', 'json'],
        default='cli',
        help='Output format (default: cli)'
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"❌ Error: '{args.path}' is not a valid directory")
        sys.exit(1)
    
    engine = AuditEngine(args.path)
    findings = engine.run(args.checks)
    
    if args.format == 'json':
        print(engine.report_json(findings))
    else:
        print(engine.report_cli(findings))
    
    # Exit with error code if critical/high findings
    critical_high = sum(1 for f in findings if f.get('severity') in ['CRITICAL', 'HIGH'])
    sys.exit(1 if critical_high > 0 else 0)


if __name__ == '__main__':
    main()
