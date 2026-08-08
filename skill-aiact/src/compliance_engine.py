"""
Compliance Engine for skill-aiact
Data-driven audit engine that evaluates controls from control_matrix.json
against company context and generates risk classifications.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import sys
from pathlib import Path

# Aggiungi src al path per import assoluti
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from data_loader import DataLoader


class ComplianceEngine:
    """
    Motore di compliance data-driven che valuta i controlli
    dalla matrice normativa rispetto al contesto aziendale.
    """
    
    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        Inizializza il ComplianceEngine.
        
        Args:
            data_loader: Istanza DataLoader (opzionale, ne crea una se None)
        """
        self.loader = data_loader or DataLoader()
    
    def classify_risk_level(self, company_context: Dict) -> str:
        """
        Classifica il livello di rischio complessivo dell'azienda.
        
        Args:
            company_context: Contesto aziendale con:
                - role: Provider/Deployer/Importer/Distributor
                - ai_systems: Lista di sistemi AI utilizzati
                - domains: Ambiti di utilizzo (biometrics, education, employment, etc.)
                - has_prohibited_practices: Boolean
                - is_high_risk: Boolean (da classificazione preliminare)
        
        Returns:
            Uno di: "UNACCEPTABLE_RISK", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"
        """
        # Controlla pratiche vietate
        if company_context.get("has_prohibited_practices", False):
            return "UNACCEPTABLE_RISK"
        
        # Controlla se high-risk
        if company_context.get("is_high_risk", False):
            return "HIGH_RISK"
        
        # Controlla obblighi di trasparenza (Art. 50)
        transparency_triggers = [
            "chatbot",
            "deepfake",
            "emotion_recognition",
            "biometric_categorisation"
        ]
        
        ai_systems = company_context.get("ai_systems", [])
        for system in ai_systems:
            system_type = system.get("type", "").lower()
            for trigger in transparency_triggers:
                if trigger in system_type:
                    return "LIMITED_RISK"
        
        return "MINIMAL_RISK"
    
    def get_applicable_controls(self, risk_level: str, company_role: str) -> List[Dict]:
        """
        Recupera tutti i controlli applicabili dato rischio e ruolo.
        
        Args:
            risk_level: Livello di rischio classificato
            company_role: Ruolo aziendale (PROVIDER, DEPLOYER, etc.)
        
        Returns:
            Lista di controlli applicabili
        """
        all_controls = self.loader.control_matrix.get("controls", [])
        applicable = []
        
        risk_mapping = {
            "UNACCEPTABLE_RISK": ["UNACCEPTABLE_RISK"],
            "HIGH_RISK": ["HIGH_RISK", "MINIMAL_RISK", "LIMITED_RISK"],
            "LIMITED_RISK": ["LIMITED_RISK", "MINIMAL_RISK"],
            "MINIMAL_RISK": ["MINIMAL_RISK"]
        }
        
        applicable_risks = risk_mapping.get(risk_level, ["MINIMAL_RISK"])
        
        for control in all_controls:
            control_risk = control.get("risk_level", "MINIMAL_RISK")
            control_subjects = control.get("applicability", {}).get("subjects", [])
            
            # Controlla se il rischio è applicabile
            if control_risk not in applicable_risks:
                continue
            
            # Controlla se il ruolo è incluso
            if control_subjects and company_role not in control_subjects:
                continue
            
            applicable.append(control)
        
        return applicable
    
    def evaluate_control(self, control: Dict, company_data: Dict) -> Dict[str, Any]:
        """
        Valuta uno specifico controllo rispetto ai dati aziendali.
        
        Args:
            control: Il controllo dalla matrice
            company_data: Dati aziendali raccolti dal questionario
        
        Returns:
            Dict con esito valutazione:
                - status: COMPLIANT, PARTIAL, NON_COMPLIANT, NOT_APPLICABLE
                - evidence_found: Lista di evidenze trovate
                - gaps: Lista di gap identificati
                - score: 0-100
                - remediation: Azioni correttive raccomandate
        """
        result = {
            "control_id": control.get("control_id") or control.get("id"),
            "title": control.get("title"),
            "article": control.get("article"),
            "status": "NOT_APPLICABLE",
            "evidence_found": [],
            "gaps": [],
            "score": 0,
            "remediation": control.get("remediation", ""),
            "legal_disclaimer": control.get("legal_disclaimer", "")
        }
        
        # Mappa domande del controllo a risposte aziendali
        pmi_question = control.get("pmi_question", "")
        quiz_questions = control.get("quiz_questions", [])
        
        # Cerca risposte nel company_data
        answers = company_data.get("answers", {})
        evidence_items = company_data.get("evidence", [])
        
        # Logica di valutazione specifica per controllo
        control_id = control.get("control_id") or control.get("id")
        
        if control_id == "AIACT-ART04-001":
            # AI Literacy
            training_completed = answers.get("training_completed", False)
            training_records = answers.get("training_records", [])
            
            if training_completed and len(training_records) > 0:
                result["status"] = "COMPLIANT"
                result["score"] = 100
                result["evidence_found"] = training_records
            elif training_completed:
                result["status"] = "PARTIAL"
                result["score"] = 50
                result["gaps"].append("Training completato ma senza registri formali")
            else:
                result["status"] = "NON_COMPLIANT"
                result["score"] = 0
                result["gaps"].append("Nessuna formazione AI literacy identificata")
        
        elif control_id == "AIACT-ART05-001":
            # Prohibited Practices
            has_prohibited = answers.get("has_prohibited_practices", False)
            
            if not has_prohibited:
                result["status"] = "COMPLIANT"
                result["score"] = 100
                result["evidence_found"] = ["Dichiarazione assenza pratiche vietate"]
            else:
                result["status"] = "NON_COMPLIANT"
                result["score"] = 0
                result["gaps"].append("Potenziale pratica vietata identificata")
                result["remediation"] = "SOSPENDERE immediatamente l'uso del sistema e consultare legale specializzato"
        
        elif control_id == "AIACT-ART50-001":
            # Transparency
            transparency_disclosed = answers.get("transparency_disclosed", False)
            ai_content_labeled = answers.get("ai_content_labeled", False)
            
            if transparency_disclosed and ai_content_labeled:
                result["status"] = "COMPLIANT"
                result["score"] = 100
                result["evidence_found"] = ["Trasparenza implementata", "Contenuti AI etichettati"]
            elif transparency_disclosed or ai_content_labeled:
                result["status"] = "PARTIAL"
                result["score"] = 50
                result["gaps"].append("Trasparenza parziale")
            else:
                result["status"] = "NON_COMPLIANT"
                result["score"] = 0
                result["gaps"].append("Nessuna trasparenza implementata")
        
        else:
            # Valutazione generica basata su证据
            required_evidence = control.get("evidence_required", [])
            
            found_count = 0
            for evidence_type in required_evidence:
                for evidence_item in evidence_items:
                    if evidence_type.lower() in evidence_item.lower():
                        found_count += 1
                        result["evidence_found"].append(evidence_item)
                        break
            
            if found_count >= len(required_evidence):
                result["status"] = "COMPLIANT"
                result["score"] = 100
            elif found_count > 0:
                result["status"] = "PARTIAL"
                result["score"] = int((found_count / len(required_evidence)) * 100)
                missing = len(required_evidence) - found_count
                result["gaps"].append(f"{missing} evidenze mancanti")
            else:
                result["status"] = "NON_COMPLIANT"
                result["score"] = 0
                result["gaps"].append("Nessuna evidenza trovata")
        
        return result
    
    def run_full_assessment(self, company_context: Dict, company_data: Dict) -> Dict[str, Any]:
        """
        Esegue una valutazione completa di compliance.
        
        Args:
            company_context: Contesto aziendale (ruolo, sistemi AI, domini)
            company_data: Dati dal questionario e evidenze
        
        Returns:
            Report completo di assessment
        """
        # Classifica rischio
        risk_level = self.classify_risk_level(company_context)
        company_role = company_context.get("role", "DEPLOYER")
        
        # Recupera controlli applicabili
        applicable_controls = self.get_applicable_controls(risk_level, company_role)
        
        # Valuta ogni controllo
        control_results = []
        total_score = 0
        compliant_count = 0
        partial_count = 0
        non_compliant_count = 0
        
        for control in applicable_controls:
            result = self.evaluate_control(control, company_data)
            control_results.append(result)
            
            total_score += result["score"]
            
            if result["status"] == "COMPLIANT":
                compliant_count += 1
            elif result["status"] == "PARTIAL":
                partial_count += 1
            else:
                non_compliant_count += 1
        
        # Calcola punteggio complessivo
        avg_score = total_score / len(control_results) if control_results else 0
        
        # Determina stato complessivo
        if non_compliant_count == 0 and partial_count == 0:
            overall_status = "FULLY_COMPLIANT"
        elif non_compliant_count == 0:
            overall_status = "MOSTLY_COMPLIANT"
        elif non_compliant_count <= 2:
            overall_status = "PARTIALLY_COMPLIANT"
        else:
            overall_status = "NON_COMPLIANT"
        
        # Genera raccomandazioni prioritarie
        priority_actions = []
        for result in control_results:
            if result["status"] == "NON_COMPLIANT" and result["remediation"]:
                priority_actions.append({
                    "control_id": result["control_id"],
                    "title": result["title"],
                    "action": result["remediation"],
                    "priority": "HIGH"
                })
            elif result["status"] == "PARTIAL" and result["remediation"]:
                priority_actions.append({
                    "control_id": result["control_id"],
                    "title": result["title"],
                    "action": result["remediation"],
                    "priority": "MEDIUM"
                })
        
        # Ordina per priorità
        priority_actions.sort(key=lambda x: 0 if x["priority"] == "HIGH" else 1)
        
        return {
            "assessment_date": datetime.now().isoformat(),
            "baseline_version": self.loader.control_matrix.get("meta", {}).get("ai_act_version", "Unknown"),
            "company_role": company_role,
            "risk_classification": risk_level,
            "overall_status": overall_status,
            "overall_score": round(avg_score, 1),
            "controls_evaluated": len(control_results),
            "compliant": compliant_count,
            "partial": partial_count,
            "non_compliant": non_compliant_count,
            "control_results": control_results,
            "priority_actions": priority_actions,
            "disclaimer": "This assessment provides readiness indication only. It does NOT constitute legal certification of AI Act compliance."
        }
    
    def get_enforcement_timeline(self) -> List[Dict]:
        """
        Restituisce la timeline di enforcement con date e scadenze.
        
        Returns:
            Lista di eventi di enforcement ordinati per data
        """
        events = self.loader.timeline.get("events", [])
        
        # Ordina per data
        sorted_events = sorted(events, key=lambda x: x.get("date", ""))
        
        # Aggiungi status relativo a oggi
        today = datetime.now().strftime("%Y-%m-%d")
        for event in sorted_events:
            event_date = event.get("date", "")
            if event_date < today:
                event["current_status"] = "IN_FORCE"
            else:
                event["current_status"] = "PENDING"
        
        return sorted_events


# Funzione utility
def run_assessment(context: Dict, data: Dict) -> Dict:
    """Factory function per eseguire assessment rapido."""
    engine = ComplianceEngine()
    return engine.run_full_assessment(context, data)


if __name__ == "__main__":
    # Test del compliance engine
    print("🔍 Testing ComplianceEngine...")
    
    engine = ComplianceEngine()
    
    # Contesto test
    test_context = {
        "role": "DEPLOYER",
        "ai_systems": [
            {"name": "ChatGPT", "type": "chatbot", "purpose": "customer_support"}
        ],
        "domains": [],
        "has_prohibited_practices": False,
        "is_high_risk": False
    }
    
    # Dati test
    test_data = {
        "answers": {
            "training_completed": True,
            "training_records": ["Corso AI Act completato da 5 dipendenti"],
            "has_prohibited_practices": False,
            "transparency_disclosed": True,
            "ai_content_labeled": False
        },
        "evidence": [
            "Registro formazione AI Act",
            "Policy uso AI aziendale"
        ]
    }
    
    print("\n📊 Classificazione rischio:", engine.classify_risk_level(test_context))
    
    print("\n🎯 Esecuzione assessment completo...")
    report = engine.run_full_assessment(test_context, test_data)
    
    print(f"\n   Stato complessivo: {report['overall_status']}")
    print(f"   Punteggio: {report['overall_score']}/100")
    print(f"   Controlli valutati: {report['controls_evaluated']}")
    print(f"   Conformi: {report['compliant']}")
    print(f"   Parziali: {report['partial']}")
    print(f"   Non conformi: {report['non_compliant']}")
    
    if report['priority_actions']:
        print("\n⚠️ Azioni prioritarie:")
        for action in report['priority_actions'][:3]:
            print(f"   [{action['priority']}] {action['title']}: {action['action'][:60]}...")
    
    print("\n✅ ComplianceEngine test completato!")
