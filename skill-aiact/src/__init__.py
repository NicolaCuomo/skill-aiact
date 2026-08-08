"""
skill-aiact - EU AI Act & AppSec Compliance Engine

The Vibe-Coder's Safety Net: Automated AppSec (OWASP), EU AI Act Evidence Vault 
& AI Literacy Engine with Real-Time Regulatory Source Monitoring.
"""

from .data_loader import DataLoader, load_data
from .compliance_engine import ComplianceEngine, run_assessment

__version__ = "1.0.0"
__author__ = "skill-aiact Compliance Team"
__license__ = "MIT"

__all__ = [
    "DataLoader",
    "load_data",
    "ComplianceEngine",
    "run_assessment",
]
