"""
Data Loader Module for skill-aiact
Loads and validates JSON registry files (sources, timeline, control_matrix)
Provides data-driven configuration for the compliance engine.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path


class DataLoader:
    """Carica e valida i file JSON del registro normativo."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Inizializza il DataLoader.
        
        Args:
            data_dir: Percorso alla directory data/ (default: ./data)
        """
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self._sources_cache: Optional[Dict] = None
        self._timeline_cache: Optional[Dict] = None
        self._matrix_cache: Optional[Dict] = None
    
    def _load_json(self, filename: str) -> Dict:
        """Carica un file JSON dalla directory data."""
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"File non trovato: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def sources(self) -> Dict:
        """Carica il registro delle fonti normative."""
        if self._sources_cache is None:
            self._sources_cache = self._load_json("sources_registry.json")
        return self._sources_cache
    
    @property
    def timeline(self) -> Dict:
        """Carica il registro delle timeline di enforcement."""
        if self._timeline_cache is None:
            data = self._load_json("timeline_registry.json")
            # Supporta sia 'events' che 'enforcement_dates'
            self._timeline_cache = {
                "meta": data.get("meta", {}),
                "events": data.get("enforcement_dates", data.get("events", []))
            }
        return self._timeline_cache
    
    @property
    def control_matrix(self) -> Dict:
        """Carica la matrice dei controlli."""
        if self._matrix_cache is None:
            self._matrix_cache = self._load_json("control_matrix.json")
        return self._matrix_cache
    
    def reload_all(self):
        """Ricarica tutti i dataset (utile dopo aggiornamenti)."""
        self._sources_cache = None
        self._timeline_cache = None
        self._matrix_cache = None
    
    def get_source_by_id(self, source_id: str) -> Optional[Dict]:
        """Recupera una fonte specifica per ID."""
        for source in self.sources.get("sources", []):
            # Supporta sia 'id' che 'source_id'
            if source.get("id") == source_id or source.get("source_id") == source_id:
                return source
        return None
    
    def get_control_by_id(self, control_id: str) -> Optional[Dict]:
        """Recupera un controllo specifico per ID."""
        for control in self.control_matrix.get("controls", []):
            # Supporta sia 'id' che 'control_id'
            if control.get("id") == control_id or control.get("control_id") == control_id:
                return control
        return None
    
    def check_source_freshness(self, source_id: str) -> Dict[str, Any]:
        """
        Verifica se una fonte è aggiornata rispetto al TTL.
        
        Returns:
            Dict con status: VERIFIED, REVIEW_REQUIRED, STALE
        """
        source = self.get_source_by_id(source_id)
        if not source:
            return {"status": "NOT_FOUND", "message": f"Fonte {source_id} non trovata"}
        
        last_verified = source.get("last_verified_date", "1970-01-01")
        ttl_days = source.get("ttl_days", 365)
        
        try:
            last_verified_date = datetime.strptime(last_verified, "%Y-%m-%d")
            expiry_date = last_verified_date + timedelta(days=ttl_days)
            today = datetime.now()
            
            if today > expiry_date:
                status = "STALE"
            elif today > expiry_date - timedelta(days=30):
                status = "REVIEW_REQUIRED"
            else:
                status = "VERIFIED"
            
            return {
                "status": status,
                "last_verified": last_verified,
                "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                "days_until_expiry": (expiry_date - today).days,
                "ttl_days": ttl_days
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Errore verifica freshness: {str(e)}"
            }
    
    def get_controls_by_article(self, article: str) -> List[Dict]:
        """Recupera tutti i controlli relativi a un articolo specifico."""
        return [
            c for c in self.control_matrix.get("controls", [])
            if c.get("article") == article
        ]
    
    def get_controls_by_risk_level(self, risk_level: str) -> List[Dict]:
        """Recupera controlli per livello di rischio."""
        return [
            c for c in self.control_matrix.get("controls", [])
            if c.get("risk_level") == risk_level
        ]
    
    def get_enforcement_dates(self) -> Dict[str, str]:
        """Restituisce tutte le date di enforcement come dict chiave-data."""
        dates = {}
        for event in self.timeline.get("events", []):
            dates[event["id"]] = event["date"]
        return dates
    
    def is_applicable(self, control: Dict, context: Dict) -> bool:
        """
        Verifica se un controllo è applicabile dato un contesto aziendale.
        
        Args:
            control: Il controllo dalla matrice
            context: Contesto aziendale (es. role, risk_classification, etc.)
        
        Returns:
            True se applicabile, False altrimenti
        """
        applicability = control.get("applicability", {})
        
        # Controlla ruoli richiesti
        required_roles = applicability.get("roles", [])
        if required_roles:
            company_role = context.get("role", "")
            if company_role not in required_roles:
                return False
        
        # Controlla classificazione rischio
        required_risk = applicability.get("risk_classification", [])
        if required_risk:
            company_risk = context.get("risk_classification", "")
            if company_risk not in required_risk:
                return False
        
        # Controlla condizioni specifiche
        conditions = applicability.get("conditions", [])
        for condition in conditions:
            field = condition.get("field")
            expected = condition.get("expected")
            actual = context.get(field)
            
            if actual != expected:
                return False
        
        return True
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        """
        Esegue validazione completa dell'integrità dei dati.
        
        Returns:
            Report di validazione con errori e warning
        """
        report = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checked_at": datetime.now().isoformat()
        }
        
        # Verifica fonti
        sources = self.sources.get("sources", [])
        source_ids = set()
        for source in sources:
            # Supporta sia 'id' che 'source_id'
            sid = source.get("id") or source.get("source_id")
            if not sid:
                report["errors"].append("Fonte missing ID/source_id")
                report["valid"] = False
            elif sid in source_ids:
                report["errors"].append(f"Fonte ID duplicato: {sid}")
                report["valid"] = False
            else:
                source_ids.add(sid)
            
            # Verifica link
            if not source.get("url"):
                report["warnings"].append(f"Fonte {sid} missing URL")
        
        # Verifica controlli
        controls = self.control_matrix.get("controls", [])
        control_ids = set()
        for control in controls:
            # Supporta sia 'id' che 'control_id'
            cid = control.get("id") or control.get("control_id")
            if not cid:
                report["errors"].append("Controllo missing ID/control_id")
                report["valid"] = False
            elif cid in control_ids:
                report["errors"].append(f"Controllo ID duplicato: {cid}")
                report["valid"] = False
            else:
                control_ids.add(cid)
            
            # Verifica riferimenti a fonti
            source_refs = control.get("source_references", [])
            for ref in source_refs:
                if ref not in source_ids:
                    report["warnings"].append(
                        f"Controllo {cid} referencia fonte inesistente: {ref}"
                    )
        
        # Verifica timeline
        events = self.timeline.get("events", [])
        for event in events:
            if not event.get("date"):
                report["errors"].append(f"Evento {event.get('id')} missing data")
                report["valid"] = False
        
        return report


# Funzione utility per accesso rapido
def load_data(data_dir: Optional[str] = None) -> DataLoader:
    """Factory function per creare un'istanza DataLoader."""
    return DataLoader(data_dir)


if __name__ == "__main__":
    # Test rapido del modulo
    print("🔍 Testing DataLoader...")
    
    loader = DataLoader()
    
    print("\n📊 Fonti caricate:", len(loader.sources.get("sources", [])))
    print("📅 Eventi timeline:", len(loader.timeline.get("events", [])))
    print("🎯 Controlli matrice:", len(loader.control_matrix.get("controls", [])))
    
    print("\n✅ Validazione integrità:")
    validation = loader.validate_data_integrity()
    print(f"   Valid: {validation['valid']}")
    if validation['errors']:
        print(f"   Errors: {len(validation['errors'])}")
        for err in validation['errors'][:3]:
            print(f"      - {err}")
    if validation['warnings']:
        print(f"   Warnings: {len(validation['warnings'])}")
    
    print("\n✅ DataLoader test completato!")
