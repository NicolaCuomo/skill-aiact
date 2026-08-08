#!/usr/bin/env python3
"""
EU AI Act Compliance Checks: Audit log, PII, Human-in-the-loop, Risk assessment
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class AIActChecker:
    """EU AI Act compliance checker for high-risk AI systems."""
    
    # Patterns for detection
    PATTERNS = {
        'audit_log': [
            (r'(?i)(log|logger)\.(info|debug|warning|error|critical)', 'Logging implemented'),
            (r'(?i)import\s+(logging|loguru)', 'Logging library imported'),
        ],
        'pii_handling': [
            (r'(?i)(email|phone|ssn|social.?security|credit.?card)', 'PII field detected'),
            (r'(?i)(gdpr|data.?protection|privacy.?policy)', 'GDPR/Privacy reference'),
            (r'(?i)encrypt.*(?:data|field|user)', 'Data encryption detected'),
        ],
        'human_in_loop': [
            (r'(?i)(human.?review|manual.?review|approve.?by)', 'Human review process'),
            (r'(?i)(override|intervention|escalate)', 'Human intervention capability'),
        ],
        'risk_assessment': [
            (r'(?i)(risk.?assess|risk.?level|risk.?score)', 'Risk assessment logic'),
            (r'(?i)(impact.?analysis|consequence)', 'Impact analysis'),
        ]
    }
    
    # Missing indicators (negative checks)
    MISSING_CHECKS = {
        'audit_log': [
            (r'(?i)def\s+\w+\(.*request.*\):', 'Function without logging'),
        ],
        'human_in_loop': [
            (r'(?i)(ai|model|predict|classify).*decision', 'Automated decision without HITL'),
        ]
    }
    
    def check(self, project_path: Path) -> List[Dict[str, Any]]:
        """Run all EU AI Act compliance checks on the project."""
        findings = []
        
        extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.rb'}
        
        has_audit_log = False
        has_pii_handling = False
        has_human_in_loop = False
        has_risk_assessment = False
        
        for file_path in project_path.rglob('*'):
            if not file_path.is_file() or file_path.suffix not in extensions:
                continue
            
            if any(part.startswith('.') or part == 'node_modules' or part == '__pycache__' 
                   for part in file_path.parts):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
            except Exception:
                continue
            
            relative_path = str(file_path.relative_to(project_path))
            
            # Check for positive patterns
            for compliance_type, patterns in self.PATTERNS.items():
                for pattern, description in patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line):
                            findings.append({
                                'category': 'EU AI Act',
                                'type': compliance_type.replace('_', ' ').title(),
                                'severity': 'LOW',
                                'file': relative_path,
                                'line': line_num,
                                'description': f'{description} - Good practice detected',
                                'remediation': None
                            })
                            
                            # Track found compliance features
                            if compliance_type == 'audit_log':
                                has_audit_log = True
                            elif compliance_type == 'pii_handling':
                                has_pii_handling = True
                            elif compliance_type == 'human_in_loop':
                                has_human_in_loop = True
                            elif compliance_type == 'risk_assessment':
                                has_risk_assessment = True
        
        # Check for missing critical compliance features
        if not has_audit_log:
            findings.append({
                'category': 'EU AI Act',
                'type': 'Audit Log',
                'severity': 'HIGH',
                'file': 'project-wide',
                'line': 'N/A',
                'description': 'No audit logging detected. EU AI Act requires traceability.',
                'remediation': 'Implement comprehensive logging for all AI system decisions and inputs.'
            })
        
        if not has_human_in_loop:
            findings.append({
                'category': 'EU AI Act',
                'type': 'Human In The Loop',
                'severity': 'HIGH',
                'file': 'project-wide',
                'line': 'N/A',
                'description': 'No human-in-the-loop mechanism detected for automated decisions.',
                'remediation': 'Add human review capability for high-impact AI decisions.'
            })
        
        if not has_risk_assessment:
            findings.append({
                'category': 'EU AI Act',
                'type': 'Risk Assessment',
                'severity': 'MEDIUM',
                'file': 'project-wide',
                'line': 'N/A',
                'description': 'No risk assessment logic detected.',
                'remediation': 'Implement risk scoring and impact analysis for AI outputs.'
            })
        
        return findings
