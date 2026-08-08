# FIX_PROMPT_TEMPLATE.md

## 🛠️ Auto-Fix Prompt per Vulnerabilità SKILL-IACT

Copia e incolla questo prompt nell'AI Developer per ottenere la patch automatica.

---

**Contesto**: Sei un AI Developer esperto in sicurezza applicativa e compliance EU AI Act.

**Task**: Risolvi le seguenti vulnerabilità identificate dall'audit SKILL-IACT:

### Vulnerabilità da Correggere

```
{VULNERABILITIES_JSON}
```

### Istruzioni di Riparazione

Per ogni vulnerabilità:

1. **Analizza** il file e la riga indicata
2. **Identifica** la causa root del problema
3. **Genera** una patch che:
   - Risolve la vulnerabilità specifica
   - Mantiene la funzionalità esistente
   - Segue le best practice di sicurezza
   - Include commenti esplicativi

4. **Formato Output**:
   ```diff
   --- a/path/to/file.py
   +++ b/path/to/file.py
   @@ -line,count +line,count
   - codice problematico
   + codice corretto
   ```

### Esempi di Fix

#### Secret Leak (CRITICAL)
```diff
- API_KEY = "sk-1234567890abcdef"
+ import os
+ API_KEY = os.environ.get("API_KEY")
```

#### SQL Injection (CRITICAL)
```diff
- cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
+ cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

#### Path Traversal (HIGH)
```diff
- with open(user_input_path) as f:
+ import os
+ safe_path = os.path.basename(user_input_path)
+ with open(os.path.join(ALLOWED_DIR, safe_path)) as f:
```

#### Missing Audit Log (EU AI Act - HIGH)
```diff
+ import logging
+ logger = logging.getLogger(__name__)
+ 
  def process_request(data):
+     logger.info(f"Processing request: {data.get('id')}")
      # ... existing logic
```

#### Human-in-the-Loop (EU AI Act - HIGH)
```diff
  def ai_decision(input_data):
      result = model.predict(input_data)
+     if result.risk_score > THRESHOLD:
+         return {"status": "pending_review", "result": result}
      return result
```

---

**Nota**: Dopo aver applicato le patch, riesegui `python3 audit.py` per verificare la risoluzione.
