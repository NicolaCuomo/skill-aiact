#!/usr/bin/env python3
"""
SKILL-IACT: Command Line Interface

Main CLI entry point for running security and compliance audits.
Supports multiple output formats and check filtering.

Usage:
    python scripts/cli.py audit <path> [--checks CHECKS] [--format FORMAT] [--output FILE]
    python scripts/cli.py generate-fix <report_file>
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Import checkers
from audit_ai_act import AIActComplianceChecker
from audit_appsec import AppSecChecker


class AuditCLI:
    """
    Command-line interface for SKILL-IACT audit toolkit.
    
    Provides unified access to all audit modules with:
    - Multiple output formats (CLI, JSON, Markdown)
    - Check filtering (appsec, aiact, all)
    - Report generation and fix prompt creation
    """

    def __init__(self):
        self.checkers = {
            'aiact': AIActComplianceChecker(),
            'appsec': AppSecChecker()
        }
        self.all_findings: List[Dict[str, Any]] = []

    def run_audit(self, project_path: Path, checks: List[str] = None) -> List[Dict[str, Any]]:
        """
        Run specified audit checks on a project.
        
        Args:
            project_path: Path to the project directory
            checks: List of check types to run ('appsec', 'aiact', or 'all')
            
        Returns:
            Combined list of all findings
        """
        if checks is None or 'all' in checks:
            checks = list(self.checkers.keys())
        
        self.all_findings = []
        
        for check_name in checks:
            if check_name not in self.checkers:
                print(f"⚠️  Unknown check type: {check_name}", file=sys.stderr)
                continue
            
            checker = self.checkers[check_name]
            findings = checker.check(project_path)
            self.all_findings.extend(findings)
        
        # Sort findings by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
        self.all_findings.sort(key=lambda x: severity_order.get(x.get('severity', 'INFO'), 5))
        
        return self.all_findings

    def format_cli(self, findings: List[Dict[str, Any]]) -> str:
        """Format findings as CLI output."""
        if not findings:
            return "\n✅ No issues found! Project looks clean.\n"
        
        report = f"\n🔍 SKILL-IACT AUDIT REPORT - {len(findings)} issue(s) found\n"
        report += "=" * 70 + "\n"
        
        # Group by category
        by_category: Dict[str, List] = {}
        for finding in findings:
            cat = finding.get('category', 'Unknown')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(finding)
        
        for category, cat_findings in by_category.items():
            report += f"\n📁 {category}\n"
            report += "-" * 50 + "\n"
            
            for i, finding in enumerate(cat_findings, 1):
                icon = self._get_severity_icon(finding.get('severity', 'LOW'))
                report += f"\n[{i}] {icon} [{finding.get('severity', 'UNKNOWN')}]\n"
                report += f"    Type: {finding.get('type', 'N/A')}\n"
                report += f"    File: {finding.get('file', 'N/A')}:{finding.get('line', 'N/A')}\n"
                report += f"    Issue: {finding.get('description', 'N/A')}\n"
                if finding.get('remediation'):
                    report += f"    💡 Fix: {finding['remediation']}\n"
        
        report += "\n" + "=" * 70 + "\n"
        return report

    def format_json(self, findings: List[Dict[str, Any]], project_path: str) -> str:
        """Format findings as JSON."""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'project': project_path,
            'total_findings': len(findings),
            'summary': self._get_summary(findings),
            'findings': findings
        }
        return json.dumps(report_data, indent=2)

    def format_markdown(self, findings: List[Dict[str, Any]], project_path: str) -> str:
        """Format findings as Markdown report."""
        md = f"# 🔍 SKILL-IACT Audit Report\n\n"
        md += f"**Project:** `{project_path}`\n"
        md += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Total Findings:** {len(findings)}\n\n"
        
        # Summary table
        summary = self._get_summary(findings)
        md += "## 📊 Summary\n\n"
        md += "| Severity | Count |\n"
        md += "|----------|-------|\n"
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
            count = summary['by_severity'].get(severity, 0)
            if count > 0:
                icon = self._get_severity_icon(severity)
                md += f"| {icon} {severity} | {count} |\n"
        md += "\n"
        
        # Detailed findings
        md += "## 🔎 Detailed Findings\n\n"
        
        by_category: Dict[str, List] = {}
        for finding in findings:
            cat = finding.get('category', 'Unknown')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(finding)
        
        for category, cat_findings in by_category.items():
            md += f"### 📁 {category}\n\n"
            
            for finding in cat_findings:
                icon = self._get_severity_icon(finding.get('severity', 'LOW'))
                md += f"#### {icon} [{finding.get('severity', 'UNKNOWN')}] {finding.get('type', 'N/A')}\n\n"
                md += f"- **File:** `{finding.get('file', 'N/A')}`:{finding.get('line', 'N/A')}\n"
                md += f"- **Issue:** {finding.get('description', 'N/A')}\n"
                if finding.get('remediation'):
                    md += f"- **💡 Remediation:** {finding['remediation']}\n"
                md += "\n---\n\n"
        
        # Compliance score (if AI Act findings exist)
        aiact_findings = [f for f in findings if f.get('category') == 'EU AI Act']
        if aiact_findings:
            md += "## ⚖️ EU AI Act Compliance Score\n\n"
            checker = self.checkers.get('aiact')
            if checker and hasattr(checker, 'get_compliance_score'):
                score = checker.get_compliance_score()
                md += f"- **Score:** {score['score']}%\n"
                md += f"- **Status:** {score['status']}\n"
                md += f"- **Requirements Met:** {score['satisfied']}/{score['total']}\n\n"
        
        return md

    def generate_fix_prompt(self, findings: List[Dict[str, Any]]) -> str:
        """Generate an auto-fix prompt for AI developers."""
        critical_high = [f for f in findings if f.get('severity') in ['CRITICAL', 'HIGH']]
        
        if not critical_high:
            return "No Critical or High severity issues found. No fix prompt needed."
        
        prompt = """# 🛠️ Auto-Fix Prompt for SKILL-IACT Vulnerabilities

**Context**: You are an expert AI Developer specializing in application security and EU AI Act compliance.

**Task**: Fix the following vulnerabilities identified by the SKILL-IACT audit:

## Vulnerabilities to Address

"""
        
        for i, finding in enumerate(critical_high, 1):
            prompt += f"### {i}. [{finding['severity']}] {finding['type']}\n"
            prompt += f"- **File:** `{finding['file']}`:{finding['line']}\n"
            prompt += f"- **Issue:** {finding['description']}\n"
            prompt += f"- **Remediation:** {finding.get('remediation', 'Apply security best practices')}\n\n"
        
        prompt += """
## Fix Instructions

For each vulnerability:

1. **Analyze** the file and line indicated
2. **Identify** the root cause
3. **Generate** a patch that:
   - Fixes the specific vulnerability
   - Maintains existing functionality
   - Follows security best practices
   - Includes explanatory comments

## Output Format

Provide fixes in unified diff format:

```diff
--- a/path/to/file.py
+++ b/path/to/file.py
@@ -line,count +line,count
- problematic code
+ fixed code
```

## Example Fixes

### Secret Leak (CRITICAL)
```diff
- API_KEY = "sk-1234567890abcdef"
+ import os
+ API_KEY = os.environ.get("API_KEY")
```

### SQL Injection (CRITICAL)
```diff
- cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
+ cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Missing Audit Log (HIGH)
```diff
+ import logging
+ logger = logging.getLogger(__name__)
+
  def process_request(data):
+     logger.info(f"Processing request: {data.get('id')}")
      # ... existing logic
```

---

**Note**: After applying patches, re-run `python scripts/cli.py audit` to verify resolution.
"""
        
        return prompt

    def _get_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics."""
        summary = {
            'total': len(findings),
            'by_severity': {},
            'by_category': {},
            'critical_high_count': 0
        }
        
        for finding in findings:
            severity = finding.get('severity', 'INFO')
            category = finding.get('category', 'Unknown')
            
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            if severity in ['CRITICAL', 'HIGH']:
                summary['critical_high_count'] += 1
        
        return summary

    def _get_severity_icon(self, severity: str) -> str:
        """Get emoji icon for severity level."""
        icons = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢',
            'INFO': 'ℹ️'
        }
        return icons.get(severity, '⚪')


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='skill-aiact',
        description='🛡️ SKILL-IACT: Automated AppSec & EU AI Act Audit Kit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s audit .                          Run full audit on current directory
  %(prog)s audit /path/to/project           Audit specific project
  %(prog)s audit . --checks appsec          Only run AppSec checks
  %(prog)s audit . --format json            Output as JSON
  %(prog)s audit . --output REPORT.md       Save report to file
  %(prog)s generate-fix REPORT.md           Generate fix prompt from report
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Audit command
    audit_parser = subparsers.add_parser('audit', help='Run security and compliance audit')
    audit_parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to project directory (default: current directory)'
    )
    audit_parser.add_argument(
        '--checks',
        nargs='+',
        choices=['appsec', 'aiact', 'all'],
        default=['all'],
        help='Specific checks to run (default: all)'
    )
    audit_parser.add_argument(
        '--format',
        choices=['cli', 'json', 'markdown'],
        default='cli',
        help='Output format (default: cli)'
    )
    audit_parser.add_argument(
        '--output',
        '-o',
        type=str,
        default=None,
        help='Output file path (default: stdout)'
    )
    
    # Generate-fix command
    fix_parser = subparsers.add_parser('generate-fix', help='Generate auto-fix prompt from report')
    fix_parser.add_argument(
        'report_file',
        type=str,
        help='Path to JSON report file'
    )
    fix_parser.add_argument(
        '--output',
        '-o',
        type=str,
        default=None,
        help='Output file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    cli = AuditCLI()
    
    if args.command == 'audit':
        project_path = Path(args.path)
        
        if not project_path.is_dir():
            print(f"❌ Error: '{args.path}' is not a valid directory", file=sys.stderr)
            sys.exit(1)
        
        # Run audit
        findings = cli.run_audit(project_path, args.checks)
        
        # Format output
        if args.format == 'json':
            output = cli.format_json(findings, str(project_path))
        elif args.format == 'markdown':
            output = cli.format_markdown(findings, str(project_path))
        else:
            output = cli.format_cli(findings)
        
        # Write output
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output)
            print(f"✅ Report saved to: {args.output}")
        else:
            print(output)
        
        # Exit with error code if critical/high findings
        critical_high = sum(1 for f in findings if f.get('severity') in ['CRITICAL', 'HIGH'])
        sys.exit(1 if critical_high > 0 else 0)
    
    elif args.command == 'generate-fix':
        report_path = Path(args.report_file)
        
        if not report_path.exists():
            print(f"❌ Error: Report file '{args.report_file}' not found", file=sys.stderr)
            sys.exit(1)
        
        try:
            report_data = json.loads(report_path.read_text())
            findings = report_data.get('findings', [])
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in report file: {e}", file=sys.stderr)
            sys.exit(1)
        
        fix_prompt = cli.generate_fix_prompt(findings)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(fix_prompt)
            print(f"✅ Fix prompt saved to: {args.output}")
        else:
            print(fix_prompt)


if __name__ == '__main__':
    main()
