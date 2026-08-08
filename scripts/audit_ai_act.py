#!/usr/bin/env python3
"""
SKILL-IACT: EU AI Act Compliance Audit Module

Analyzes project files for EU AI Act compliance requirements:
- Risk classification (Art. 6)
- Transparency obligations (Art. 50)
- PII/Privacy handling (GDPR alignment)
- Human-in-the-loop mechanisms
- Audit logging and traceability
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Tuple


class AIActComplianceChecker:
    """
    EU AI Act compliance checker for high-risk AI systems.
    
    Checks for:
    - Article 6: Risk classification indicators
    - Article 50: Transparency obligations
    - GDPR-aligned PII handling
    - Human oversight mechanisms
    - Audit trail and logging
    """

    # Compliance requirements with detection patterns
    COMPLIANCE_REQUIREMENTS = {
        'audit_logging': {
            'description': 'System must maintain audit logs for traceability (Art. 12)',
            'positive_patterns': [
                (r'(?i)(log|logger)\.(info|debug|warning|error|critical|audit)', 'Logging call detected'),
                (r'(?i)import\s+(logging|loguru|structlog)', 'Logging library imported'),
                (r'(?i)(audit.?log|trace.?id|request.?id)', 'Audit/tracing identifier'),
                (r'(?i)write.*log|log.*write', 'Log write operation'),
            ],
            'negative_patterns': [
                (r'(?i)def\s+\w*\(.*(?:request|input|data).*\):', 'Function without logging'),
            ],
            'severity_missing': 'HIGH',
            'remediation': 'Implement comprehensive logging for all AI decisions, inputs, and outputs. Use structured logging with unique request IDs.'
        },
        'pii_handling': {
            'description': 'Proper handling of personal data (GDPR Art. 5, AI Act Art. 10)',
            'positive_patterns': [
                (r'(?i)(encrypt|anonymize|pseudonymize)\s*\(', 'Data protection function'),
                (r'(?i)(gdpr|privacy.?policy|data.?protection)', 'GDPR/Privacy reference'),
                (r'(?i)(consent|opt.?in|opt.?out)', 'Consent mechanism'),
                (r'(?i)(delete|erase).*data|data.*(delete|erase)', 'Data deletion capability'),
            ],
            'pii_indicators': [
                (r'(?i)(email|phone|ssn|social.?security|credit.?card|passport)', 'PII field type'),
                (r'(?i)(name|address|birthdate|dob).*=\s*request', 'PII from request'),
                (r'(?i)user_?(?:data|info|profile)', 'User data structure'),
            ],
            'severity_missing': 'HIGH',
            'remediation': 'Implement data encryption, anonymization, and explicit consent mechanisms. Document data processing activities.'
        },
        'human_in_loop': {
            'description': 'Human oversight for high-risk decisions (Art. 14)',
            'positive_patterns': [
                (r'(?i)(human.?review|manual.?review|operator.?review)', 'Human review process'),
                (r'(?i)(approve|reject|override).*(by|from)\s*(?:user|admin|human)', 'Approval workflow'),
                (r'(?i)(escalate|intervention|handover)', 'Human intervention capability'),
                (r'(?i)confidence.*threshold|risk.*score.*>', 'Risk-based routing'),
            ],
            'negative_patterns': [
                (r'(?i)(ai|model|predict|classify).*decision|decide.*(?:automatically|auto)', 'Fully automated decision'),
            ],
            'severity_missing': 'HIGH',
            'remediation': 'Add human review capability for high-impact AI decisions. Implement confidence thresholds that trigger manual review.'
        },
        'risk_assessment': {
            'description': 'Risk management system (Art. 9)',
            'positive_patterns': [
                (r'(?i)(risk.?assess|risk.?level|risk.?score|risk.?category)', 'Risk assessment logic'),
                (r'(?i)(impact.?analysis|consequence|harm)', 'Impact analysis'),
                (r'(?i)(mitigation|safeguard|control)', 'Risk mitigation measures'),
                (r'(?i)(high.?risk|unacceptable.?risk|prohibited)', 'Risk classification'),
            ],
            'severity_missing': 'MEDIUM',
            'remediation': 'Implement risk scoring and impact analysis for AI outputs. Document risk management procedures.'
        },
        'transparency': {
            'description': 'Transparency obligations (Art. 50)',
            'positive_patterns': [
                (r'(?i)(disclose|inform|notify).*(ai|automated|bot)', 'AI disclosure statement'),
                (r'(?i)(generated.?by|powered.?by|ai.*system)', 'AI attribution'),
                (r'(?i)(explain|interpretability|xai)', 'Explainability feature'),
                (r'(?i)(model.?card|system.?card|documentation)', 'Model documentation'),
            ],
            'severity_missing': 'MEDIUM',
            'remediation': 'Add clear disclosures when content is AI-generated. Provide model cards and system documentation.'
        },
        'data_governance': {
            'description': 'Data governance and quality (Art. 10)',
            'positive_patterns': [
                (r'(?i)(data.*quality|dataset.*bias|training.*data)', 'Data quality consideration'),
                (r'(?i)(validate|verify|clean).*data', 'Data validation'),
                (r'(?i)(representative|balanced|diverse).*dataset', 'Dataset considerations'),
            ],
            'severity_missing': 'MEDIUM',
            'remediation': 'Document data sources, quality checks, and bias mitigation strategies.'
        }
    }

    def __init__(self):
        self.findings: List[Dict[str, Any]] = []
        self.compliance_status: Dict[str, bool] = {}

    def check(self, project_path: Path) -> List[Dict[str, Any]]:
        """
        Run all EU AI Act compliance checks on the project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            List of findings with compliance status
        """
        self.findings = []
        self.compliance_status = {}
        
        # File extensions relevant for AI systems
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.rb', '.go', '.cs'}
        
        # Track which requirements are satisfied
        requirement_satisfied: Dict[str, bool] = {req: False for req in self.COMPLIANCE_REQUIREMENTS}
        
        # Scan all relevant files
        for file_path in project_path.rglob('*'):
            if not file_path.is_file() or file_path.suffix not in extensions:
                continue
                
            # Skip common non-source directories
            if self._should_skip_path(file_path):
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
            except Exception:
                continue
                
            relative_path = str(file_path.relative_to(project_path))
            
            # Check each compliance requirement
            for req_name, req_config in self.COMPLIANCE_REQUIREMENTS.items():
                # Check positive patterns
                for pattern, description in req_config.get('positive_patterns', []):
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            self._add_finding(
                                category='EU AI Act',
                                req_type=req_name,
                                severity='INFO',
                                file=relative_path,
                                line=line_num,
                                description=f"✓ {description}",
                                remediation=None,
                                is_positive=True
                            )
                            requirement_satisfied[req_name] = True
                            
                # Check PII indicators (special handling)
                if req_name == 'pii_handling':
                    for pattern, description in req_config.get('pii_indicators', []):
                        for line_num, line in enumerate(lines, 1):
                            if re.search(pattern, line):
                                self._add_finding(
                                    category='EU AI Act',
                                    req_type='pii_handling',
                                    severity='INFO',
                                    file=relative_path,
                                    line=line_num,
                                    description=f"⚠ {description} - ensure proper protection",
                                    remediation="Verify this PII field has encryption and access controls",
                                    is_positive=False
                                )
        
        # Generate summary findings for missing requirements
        for req_name, is_satisfied in requirement_satisfied.items():
            req_config = self.COMPLIANCE_REQUIREMENTS[req_name]
            
            if not is_satisfied:
                self._add_finding(
                    category='EU AI Act',
                    req_type=req_name.replace('_', ' ').title(),
                    severity=req_config['severity_missing'],
                    file='project-wide',
                    line='N/A',
                    description=f"✗ Missing: {req_config['description']}",
                    remediation=req_config['remediation'],
                    is_positive=False
                )
                self.compliance_status[req_name] = False
            else:
                self.compliance_status[req_name] = True
        
        return self.findings

    def get_compliance_score(self) -> Dict[str, Any]:
        """
        Calculate overall compliance score.
        
        Returns:
            Dictionary with score and breakdown
        """
        total_requirements = len(self.COMPLIANCE_REQUIREMENTS)
        satisfied_count = sum(1 for v in self.compliance_status.values() if v)
        
        score = (satisfied_count / total_requirements * 100) if total_requirements > 0 else 0
        
        return {
            'score': round(score, 1),
            'satisfied': satisfied_count,
            'total': total_requirements,
            'status': 'COMPLIANT' if score >= 80 else 'PARTIAL' if score >= 50 else 'NON-COMPLIANT',
            'breakdown': self.compliance_status
        }

    def _add_finding(self, category: str, req_type: str, severity: str, 
                     file: str, line: int, description: str, 
                     remediation: str, is_positive: bool) -> None:
        """Add a finding to the results."""
        self.findings.append({
            'category': category,
            'type': req_type,
            'severity': severity,
            'file': file,
            'line': line,
            'description': description,
            'remediation': remediation,
            'is_positive': is_positive
        })

    def _should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped during scanning."""
        skip_dirs = {'.git', '.svn', '.hg', 'node_modules', '__pycache__', 
                     'venv', '.venv', 'env', '.env', 'dist', 'build',
                     '.idea', '.vscode', 'coverage', '.pytest_cache'}
        
        return any(part in skip_dirs for part in path.parts)


def main():
    """Standalone execution for testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audit_ai_act.py <project_path>")
        sys.exit(1)
    
    project_path = Path(sys.argv[1])
    
    if not project_path.is_dir():
        print(f"Error: '{project_path}' is not a valid directory")
        sys.exit(1)
    
    checker = AIActComplianceChecker()
    findings = checker.check(project_path)
    score = checker.get_compliance_score()
    
    print(f"\n{'='*60}")
    print(f"EU AI Act Compliance Audit Report")
    print(f"{'='*60}\n")
    
    print(f"Overall Score: {score['score']}% ({score['status']})")
    print(f"Requirements Satisfied: {score['satisfied']}/{score['total']}\n")
    
    print("Requirement Status:")
    for req, satisfied in score['breakdown'].items():
        icon = "✓" if satisfied else "✗"
        print(f"  {icon} {req.replace('_', ' ').title()}")
    
    print(f"\n{'-'*60}")
    print(f"Findings ({len(findings)} total):\n")
    
    # Group by severity
    for severity in ['HIGH', 'MEDIUM', 'INFO']:
        severity_findings = [f for f in findings if f['severity'] == severity]
        if severity_findings:
            print(f"\n[{severity}] - {len(severity_findings)} finding(s)")
            for finding in severity_findings[:5]:  # Limit display
                print(f"  • {finding['type']}: {finding['description']}")
                if finding['file'] != 'project-wide':
                    print(f"    → {finding['file']}:{finding['line']}")
                if finding['remediation']:
                    print(f"    💡 {finding['remediation']}")
    
    print(f"\n{'='*60}\n")


if __name__ == '__main__':
    main()
