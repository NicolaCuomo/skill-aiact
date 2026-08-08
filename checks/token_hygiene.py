#!/usr/bin/env python3
"""
Token Hygiene Checks: Prompt bloat, file >1k token optimization
"""

import re
from pathlib import Path
from typing import List, Dict, Any


class TokenHygieneChecker:
    """Token usage and prompt efficiency checker for AI-assisted development."""
    
    # Approximate token counting (1 token ≈ 4 characters in English)
    CHARS_PER_TOKEN = 4
    
    # Thresholds
    PROMPT_BLOAT_THRESHOLD = 500  # tokens
    FILE_SIZE_THRESHOLD = 1000  # tokens (~4000 chars)
    
    def check(self, project_path: Path) -> List[Dict[str, Any]]:
        """Run all token hygiene checks on the project."""
        findings = []
        
        # Files to check for prompt bloat
        prompt_extensions = {'.md', '.txt', '.prompt', '.py', '.js'}
        
        for file_path in project_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            if any(part.startswith('.') or part == 'node_modules' or part == '__pycache__' 
                   for part in file_path.parts):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            
            relative_path = str(file_path.relative_to(project_path))
            char_count = len(content)
            estimated_tokens = char_count // self.CHARS_PER_TOKEN
            
            # Check for large files
            if estimated_tokens > self.FILE_SIZE_THRESHOLD:
                findings.append({
                    'category': 'Token Hygiene',
                    'type': 'Large File',
                    'severity': 'LOW',
                    'file': relative_path,
                    'line': 'N/A',
                    'description': f'File is ~{estimated_tokens} tokens ({char_count} chars). Consider splitting.',
                    'remediation': f'Split into smaller modules or remove unnecessary content to reduce below {self.FILE_SIZE_THRESHOLD} tokens.'
                })
            
            # Check for prompt bloat in prompt-like files
            if file_path.suffix in prompt_extensions:
                if self._is_prompt_file(file_path.name, content):
                    if estimated_tokens > self.PROMPT_BLOAT_THRESHOLD:
                        findings.append({
                            'category': 'Token Hygiene',
                            'type': 'Prompt Bloat',
                            'severity': 'MEDIUM',
                            'file': relative_path,
                            'line': 'N/A',
                            'description': f'Prompt is ~{estimated_tokens} tokens. Exceeds {self.PROMPT_BLOAT_THRESHOLD} token threshold.',
                            'remediation': 'Trim unnecessary context, use references instead of inline content, split into modular prompts.'
                        })
                
                # Check for repetitive patterns (wasteful token usage)
                repetition_issues = self._check_repetition(content)
                for line_num, issue in repetition_issues:
                    findings.append({
                        'category': 'Token Hygiene',
                        'type': 'Repetitive Content',
                        'severity': 'LOW',
                        'file': relative_path,
                        'line': line_num,
                        'description': f'Repetitive pattern detected: {issue}',
                        'remediation': 'Remove redundant content or use references/abstractions.'
                    })
        
        return findings
    
    def _is_prompt_file(self, filename: str, content: str) -> bool:
        """Check if file appears to be a prompt template."""
        prompt_indicators = [
            r'(?i)you are an? ai',
            r'(?i)your task is to',
            r'(?i)please (analyze|review|fix|generate)',
            r'(?i)instructions?:',
            r'(?i)prompt:',
        ]
        
        for indicator in prompt_indicators:
            if re.search(indicator, content[:1000]):  # Check first 1000 chars
                return True
        
        return filename.endswith('.prompt') or 'prompt' in filename.lower()
    
    def _check_repetition(self, content: str) -> List[tuple]:
        """Check for repetitive patterns that waste tokens."""
        issues = []
        lines = content.split('\n')
        
        # Check for repeated lines
        seen_lines = {}
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if len(stripped) > 20:  # Ignore short lines
                if stripped in seen_lines:
                    issues.append((i, f'Line repeated from line {seen_lines[stripped]}'))
                else:
                    seen_lines[stripped] = i
        
        # Check for repeated blocks (3+ consecutive lines)
        for i in range(len(lines) - 3):
            block = '\n'.join(lines[i:i+3]).strip()
            if len(block) > 50:
                remaining = '\n'.join(lines[i+3:])
                if block in remaining:
                    issues.append((i+1, 'Repeated block of 3+ lines'))
                    break  # Only report once per file
        
        return issues[:5]  # Limit to 5 issues per file
