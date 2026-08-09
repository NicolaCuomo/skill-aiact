# Test Cases & Benchmarks — EU AI Act Skill (`skill-aiact`)

Questo file contiene scenari pratici d'uso per testare e validare le risposte fornite dall'Agente AI quando utilizza la skill `skill-aiact`.

I test coprono la classificazione del rischio, gli adempimenti richiesti, le sanzioni e la timeline di applicazione del **Regolamento UE 2024/1689**.

---

## 🛑 Caso 1: Rischio Inaccettabile (Pratiche Vietate — Articolo 5)

### Scenario di Input (Prompt Utente)
> "Stiamo sviluppando un software per un comune che analizza i flussi delle telecamere pubbliche in tempo reale per identificare e tracciare le persone ricercate tramite riconoscimento facciale biometrico. È fattibile nell'UE?"

### Esito Atteso dall'Agente AI
- **Classificazione:** **Rischio Inaccettabile (VIETATO)** — Articolo 5(1)(h).
- **Motivazione Legale:** L'uso di sistemi di identificazione biometrica remota "in tempo reale" in spazi accessibili al pubblico per scopi di polizia è proibito, salvo eccezioni estremamente ristrette (es. ricerca di vittime di sequestro, minaccia imminente alla vita o ricerca di sospetti per reati gravi specifici con autorizzazione giudiziaria).
- **Azione Consigliata:** Sospendere lo sviluppo nello spazio pubblico in tempo reale. Valutare se l'uso è differito ("post-remoto") previa autorizzazione o riconsiderare l'architettura per evitare l'identificazione biometrica univoca.

---

## ⚠️ Caso 2: Alto Rischio (High-Risk — Articolo 6 & Allegato III)

### Scenario di Input (Prompt Utente)
> "La nostra startup HR sta creando un algoritmo per selezionare automaticamente i CV dei candidati e formulare un punteggio di idoneità prima del colloquio. Quali requisiti dobbiamo rispettare secondo l'AI Act?"

### Esito Atteso dall'Agente AI
- **Classificazione:** **Alto Rischio (High-Risk)** — Allegato III, Punto 4(a) (Assunzione e selezione delle persone fisiche).
- **Obblighi Principali da Elencare:**
  1. **Sistema di Gestione del Rischio (Art. 9):** Analisi e mitigazione continua dei rischi per i diritti fondamentali.
  2. **Qualità dei Dati (Art. 10):** Set di dati di addestramento privi di bias discriminatori.
  3. **Documentazione Tecnica e Registrazione (Art. 11 & 49):** Redazione fascicolo tecnico e registrazione nel database UE.
  4. **Sorveglianza Umana (Art. 14):** Presenza di un operatore umano che possa sovrascrivere o annullare il punteggio dell'AI.
  5. **Valutazione di Impatto sui Diritti Fondamentali (FRIA - Art. 27):** Obbligatoria per i deployer (es. le aziende che usano il software).
- **Timeline di Conformità:** Applicazione a 24 mesi dall'entrata in vigore del Regolamento.

---

## 👁️ Caso 3: Obblighi di Trasparenza Specifici (Articolo 50)

### Scenario di Input (Prompt Utente)
> "Abbiamo integrato un chatbot di supporto clienti sul nostro e-commerce che genera anche avatar video parlanti per spiegare le promozioni. Dobbiamo dichiarare che è un'AI?"

### Esito Atteso dall'Agente AI
- **Classificazione:** **Rischio Specifico / Obblighi di Trasparenza** — Articolo 50(1) e 50(4).
- **Obblighi da Elencare:**
  1. **Interazione Diretta (Art. 50(1)):** L'utente deve essere informato in modo chiaro e palese che sta interagendo con un sistema di intelligenza artificiale (chatbot).
  2. **Generazione di Contenuti / Deepfake (Art. 50(4)):** Gli avatar video sintetici (che appaiono come persone reali) devono recare un watermark visibile/invisibile o una marcatura che dichiari che il contenuto è stato generato o manipolato artificialmente.
- **Eccezioni:** Se è palese dal contesto o se il sistema è usato esclusivamente per scopi artistici/satirici (con riserve), la trasparenza si applica con modalità differenti.

---

## 🧠 Caso 4: Modelli GPAI (General Purpose AI — Articoli 51–55)

### Scenario di Input (Prompt Utente)
> "Stiamo ri-addestrando un Large Language Model da 70 miliardi di parametri da distribuire open source per sviluppatori europei. Rientriamo nella normativa GPAI?"

### Esito Atteso dall'Agente AI
- **Classificazione:** **GPAI (General Purpose AI Model)** — Capo V (Art. 51-55).
- **Valutazione del Rischio Sistemico:** Se la capacità computazionale usata per l'addestramento supera $10^{25}$ FLOPs, il modello viene classificato ad **Alto Rischio Sistemico** (Art. 51).
- **Obblighi Richiesti:**
  1. Redazione della documentazione tecnica sull'architettura e sull'addestramento.
  2. Politica sul rispetto del diritto d'autore UE (Copyright Directive).
  3. Pubblicazione di una sintesi dei contenuti usati per l'addestramento.
- **Rilievo Open Source:** Gli obblighi per i modelli open-source senza rischio sistemico sono semplificati (esentati da alcuni obblighi di documentazione interna, ma tenuti a rispettare copyright e trasparenza).

---

## 🟩 Caso 5: Rischio Minimo o Nullo

### Scenario di Input (Prompt Utente)
> "Uso un filtro antispam basato su intelligenza artificiale per la posta aziendale e un algoritmo che suggerisce i prodotti correlati nello shop online. Che adempimenti legal-tech devo fare?"

### Esito Atteso dall'Agente AI
- **Classificazione:** **Rischio Minimo o Assente**.
- **Esito:** Nessun obbligo normativo vincolante ai sensi dell'EU AI Act.
- **Azione Consigliata:** Adesione volontaria ai Codici di Condotta (Art. 95) ed eventuale rispetto delle normative generali preesistenti (GDPR per la gestione email/cookie).

---

## 🛠️ Come Eseguire il Benchmark della Skill

1. Carica il file `SKILL.md` nel tuo agente AI o ambiente di sviluppo.
2. Invia i prompt di test sopra riportati senza indicare la risposta.
3. Verifica che l'agente risponda includendo:
   - [x] Livello di rischio corretto.
   - [x] Riferimento esplicito all'Articolo dell'EU AI Act.
   - [x] Lista di adempimenti o indicazione di divieto.
   - [x] Tonalità professionale e disclaimer di supporto informativo.
