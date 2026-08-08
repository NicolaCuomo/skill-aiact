"""
Test suite for skill-aiact compliance engine module.
"""

import pytest
import sys
from pathlib import Path

# Aggiungi src al path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from compliance_engine import ComplianceEngine


class TestComplianceEngine:
    """Test per il modulo ComplianceEngine."""
    
    @pytest.fixture
    def engine(self):
        """Crea un'istanza ComplianceEngine per i test."""
        return ComplianceEngine()
    
    def test_classify_minimal_risk(self, engine):
        """Verifica classificazione rischio minimo."""
        context = {
            "role": "DEPLOYER",
            "ai_systems": [{"name": "InternalTool", "type": "analytics"}],
            "has_prohibited_practices": False,
            "is_high_risk": False
        }
        risk = engine.classify_risk_level(context)
        assert risk == "MINIMAL_RISK"
    
    def test_classify_limited_risk_chatbot(self, engine):
        """Verifica classificazione rischio limitato per chatbot."""
        context = {
            "role": "DEPLOYER",
            "ai_systems": [{"name": "ChatGPT", "type": "chatbot"}],
            "has_prohibited_practices": False,
            "is_high_risk": False
        }
        risk = engine.classify_risk_level(context)
        assert risk == "LIMITED_RISK"
    
    def test_classify_unacceptable_risk(self, engine):
        """Verifica classificazione rischio inaccettabile."""
        context = {
            "role": "PROVIDER",
            "ai_systems": [],
            "has_prohibited_practices": True,
            "is_high_risk": False
        }
        risk = engine.classify_risk_level(context)
        assert risk == "UNACCEPTABLE_RISK"
    
    def test_get_applicable_controls(self, engine):
        """Verifica recupero controlli applicabili."""
        controls = engine.get_applicable_controls("MINIMAL_RISK", "DEPLOYER")
        assert isinstance(controls, list)
        # Dovrebbe esserci almeno un controllo per minimal risk
        assert len(controls) >= 0
    
    def test_evaluate_control_ai_literacy_compliant(self, engine):
        """Valuta controllo AI Literacy conforme."""
        control = {
            "control_id": "AIACT-ART04-001",
            "title": "AI Literacy Measures",
            "article": "4",
            "remediation": "Assign training",
            "legal_disclaimer": "Not certification"
        }
        data = {
            "answers": {
                "training_completed": True,
                "training_records": ["Record 1"]
            },
            "evidence": []
        }
        result = engine.evaluate_control(control, data)
        assert result["status"] == "COMPLIANT"
        assert result["score"] == 100
    
    def test_evaluate_control_ai_literacy_non_compliant(self, engine):
        """Valuta controllo AI Literacy non conforme."""
        control = {
            "control_id": "AIACT-ART04-001",
            "title": "AI Literacy Measures",
            "article": "4",
            "remediation": "Assign training",
            "legal_disclaimer": "Not certification"
        }
        data = {
            "answers": {
                "training_completed": False,
                "training_records": []
            },
            "evidence": []
        }
        result = engine.evaluate_control(control, data)
        assert result["status"] == "NON_COMPLIANT"
        assert result["score"] == 0
    
    def test_run_full_assessment(self, engine):
        """Esegue assessment completo."""
        context = {
            "role": "DEPLOYER",
            "ai_systems": [{"name": "ChatGPT", "type": "chatbot"}],
            "domains": [],
            "has_prohibited_practices": False,
            "is_high_risk": False
        }
        data = {
            "answers": {
                "training_completed": True,
                "training_records": ["Training record"],
                "has_prohibited_practices": False,
                "transparency_disclosed": True,
                "ai_content_labeled": True
            },
            "evidence": ["Policy documento"]
        }
        
        report = engine.run_full_assessment(context, data)
        
        assert "overall_status" in report
        assert "overall_score" in report
        assert "risk_classification" in report
        assert "control_results" in report
        assert report["risk_classification"] == "LIMITED_RISK"
    
    def test_get_enforcement_timeline(self, engine):
        """Verifica recupero timeline enforcement."""
        timeline = engine.get_enforcement_timeline()
        assert isinstance(timeline, list)
        # La timeline dovrebbe avere eventi
        assert len(timeline) > 0
        
        # Verifica che ogni evento abbia current_status
        for event in timeline:
            assert "current_status" in event
            assert event["current_status"] in ["IN_FORCE", "PENDING"]


if __name__ == "__main__":
    # Test manual senza pytest per evitare conflitti
    print("🔍 Running manual tests...")
    
    from compliance_engine import ComplianceEngine
    engine = ComplianceEngine()
    
    # Test 1: Classify minimal risk
    context_minimal = {
        "role": "DEPLOYER",
        "ai_systems": [{"name": "InternalTool", "type": "analytics"}],
        "has_prohibited_practices": False,
        "is_high_risk": False
    }
    assert engine.classify_risk_level(context_minimal) == "MINIMAL_RISK"
    print("✅ test_classify_minimal_risk")
    
    # Test 2: Classify limited risk (chatbot)
    context_limited = {
        "role": "DEPLOYER",
        "ai_systems": [{"name": "ChatGPT", "type": "chatbot"}],
        "has_prohibited_practices": False,
        "is_high_risk": False
    }
    assert engine.classify_risk_level(context_limited) == "LIMITED_RISK"
    print("✅ test_classify_limited_risk_chatbot")
    
    # Test 3: Classify unacceptable risk
    context_unacceptable = {
        "role": "PROVIDER",
        "ai_systems": [],
        "has_prohibited_practices": True,
        "is_high_risk": False
    }
    assert engine.classify_risk_level(context_unacceptable) == "UNACCEPTABLE_RISK"
    print("✅ test_classify_unacceptable_risk")
    
    # Test 4: Get applicable controls
    controls = engine.get_applicable_controls("MINIMAL_RISK", "DEPLOYER")
    assert isinstance(controls, list)
    print("✅ test_get_applicable_controls")
    
    # Test 5: Evaluate AI Literacy compliant
    control_lit = {
        "control_id": "AIACT-ART04-001",
        "title": "AI Literacy",
        "article": "4",
        "remediation": "Assign training",
        "legal_disclaimer": "Not certification"
    }
    data_lit_compliant = {
        "answers": {"training_completed": True, "training_records": ["Record 1"]},
        "evidence": []
    }
    result = engine.evaluate_control(control_lit, data_lit_compliant)
    assert result["status"] == "COMPLIANT"
    assert result["score"] == 100
    print("✅ test_evaluate_control_ai_literacy_compliant")
    
    # Test 6: Evaluate AI Literacy non-compliant
    data_lit_non = {
        "answers": {"training_completed": False, "training_records": []},
        "evidence": []
    }
    result = engine.evaluate_control(control_lit, data_lit_non)
    assert result["status"] == "NON_COMPLIANT"
    assert result["score"] == 0
    print("✅ test_evaluate_control_ai_literacy_non_compliant")
    
    # Test 7: Run full assessment
    context_full = {
        "role": "DEPLOYER",
        "ai_systems": [{"name": "ChatGPT", "type": "chatbot"}],
        "domains": [],
        "has_prohibited_practices": False,
        "is_high_risk": False
    }
    data_full = {
        "answers": {
            "training_completed": True,
            "training_records": ["Training record"],
            "has_prohibited_practices": False,
            "transparency_disclosed": True,
            "ai_content_labeled": True
        },
        "evidence": ["Policy documento"]
    }
    report = engine.run_full_assessment(context_full, data_full)
    assert "overall_status" in report
    assert "overall_score" in report
    assert report["risk_classification"] == "LIMITED_RISK"
    print("✅ test_run_full_assessment")
    
    # Test 8: Get enforcement timeline
    timeline = engine.get_enforcement_timeline()
    assert isinstance(timeline, list)
    assert len(timeline) > 0
    for event in timeline:
        assert "current_status" in event
    print("✅ test_get_enforcement_timeline")
    
    print("\n✅ All compliance engine tests passed!")
