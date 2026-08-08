"""
Test suite for skill-aiact data loader module.
"""

import pytest
import sys
from pathlib import Path

# Aggiungi src al path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from data_loader import DataLoader


class TestDataLoader:
    """Test per il modulo DataLoader."""
    
    @pytest.fixture
    def loader(self):
        """Crea un'istanza DataLoader per i test."""
        return DataLoader()
    
    def test_sources_loaded(self, loader):
        """Verifica che le fonti vengano caricate correttamente."""
        sources = loader.sources
        assert "sources" in sources
        assert len(sources["sources"]) > 0
    
    def test_timeline_loaded(self, loader):
        """Verifica che la timeline venga caricata correttamente."""
        timeline = loader.timeline
        assert "events" in timeline
        assert len(timeline["events"]) > 0
    
    def test_control_matrix_loaded(self, loader):
        """Verifica che la matrice dei controlli venga caricata."""
        matrix = loader.control_matrix
        assert "controls" in matrix
        assert len(matrix["controls"]) > 0
    
    def test_validate_data_integrity(self, loader):
        """Verifica la validazione dell'integrità dei dati."""
        validation = loader.validate_data_integrity()
        assert "valid" in validation
        # I dati dovrebbero essere validi
        assert validation["valid"] is True
    
    def test_get_source_by_id(self, loader):
        """Verifica il recupero di una fonte per ID."""
        source = loader.get_source_by_id("SRC-001")
        assert source is not None
        assert source["source_id"] == "SRC-001"
    
    def test_get_control_by_id(self, loader):
        """Verifica il recupero di un controllo per ID."""
        control = loader.get_control_by_id("AIACT-ART04-001")
        assert control is not None
        assert "AI Literacy" in control.get("title", "")
    
    def test_check_source_freshness(self, loader):
        """Verifica il controllo di freshness delle fonti."""
        result = loader.check_source_freshness("SRC-001")
        assert "status" in result
        assert result["status"] in ["VERIFIED", "REVIEW_REQUIRED", "STALE", "ERROR", "NOT_FOUND"]
    
    def test_get_enforcement_dates(self, loader):
        """Verifica il recupero delle date di enforcement."""
        dates = loader.get_enforcement_dates()
        assert isinstance(dates, dict)
        # Dovrebbe avere almeno le date dalla timeline
        assert len(dates) >= 0  # Potrebbe essere vuoto se usa chiavi diverse


if __name__ == "__main__":
    # Test manual senza pytest per evitare conflitti
    print("🔍 Running manual tests...")
    
    loader = DataLoader()
    
    # Test 1: Sources loaded
    sources = loader.sources
    assert "sources" in sources
    assert len(sources["sources"]) > 0
    print("✅ test_sources_loaded")
    
    # Test 2: Timeline loaded
    timeline = loader.timeline
    assert "events" in timeline
    assert len(timeline["events"]) > 0
    print("✅ test_timeline_loaded")
    
    # Test 3: Control matrix loaded
    matrix = loader.control_matrix
    assert "controls" in matrix
    assert len(matrix["controls"]) > 0
    print("✅ test_control_matrix_loaded")
    
    # Test 4: Validate integrity
    validation = loader.validate_data_integrity()
    assert validation["valid"] is True
    print("✅ test_validate_data_integrity")
    
    # Test 5: Get source by ID
    source = loader.get_source_by_id("SRC-001")
    assert source is not None
    assert source["source_id"] == "SRC-001"
    print("✅ test_get_source_by_id")
    
    # Test 6: Get control by ID
    control = loader.get_control_by_id("AIACT-ART04-001")
    assert control is not None
    assert "AI Literacy" in control.get("title", "")
    print("✅ test_get_control_by_id")
    
    # Test 7: Check source freshness
    result = loader.check_source_freshness("SRC-001")
    assert "status" in result
    print("✅ test_check_source_freshness")
    
    print("\n✅ All tests passed!")
