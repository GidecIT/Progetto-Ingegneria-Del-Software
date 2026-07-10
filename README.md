# Participium

> Piattaforma web di **partecipazione civica**: i cittadini segnalano problemi urbani su una mappa e ne seguono la gestione da parte del Comune.

Progetto realizzato per l'esame di **Ingegneria del Software** al **Politecnico di Torino** — **Gruppo 25**.

---

## Indice

- [Il progetto](#il-progetto)
- [Cos'è Participium](#cosè-participium)
- [Cosa abbiamo fatto](#cosa-abbiamo-fatto)
- [Struttura della repository](#struttura-della-repository)
- [Come eseguire il progetto](#come-eseguire-il-progetto)
- [Come eseguire i test](#come-eseguire-i-test)

---

## Il progetto

Il progetto d'esame partiva da una **specifica di sistema** fornita dai docenti (il documento `Participium.md`) e chiedeva di portare avanti l'intero ciclo di vita del software, dalla pianificazione fino al deployment, applicando le tecniche viste a lezione.

Il lavoro era organizzato in **10 task incrementali**, ciascuno con un deliverable preciso da consegnare (documenti nella cartella `doc/deliverable/`, codice e test nella cartella `src/`). Ogni task partiva da template/stub predisposti e doveva essere completato mantenendo **coerenza** con i documenti prodotti nei task precedenti.

Le specifiche complete di ogni task si trovano nella cartella [`task/`](task/).

I task coprivano tre macro-fasi:

1. **Documentazione e progettazione** (Task 1–4): project management, requirements engineering, casi d'uso, architettura e design.
2. **Testing** (Task 5–9): black-box, white-box, coverage, acceptance API e acceptance UI su un'implementazione reale del sistema.
3. **Deployment** (Task 10): messa in esecuzione dell'intero stack tramite Docker.

---

## Cos'è Participium

**Participium** è un sistema di partecipazione civica pensato per il **Comune di Torino**, ispirato a piattaforme reali come [IRIS](https://iris.sad.ve.it/) (Venezia). L'obiettivo è offrire ai cittadini un canale strutturato e trasparente per **segnalare problemi urbani** (buche, lampioni rotti, rifiuti, barriere architettoniche, ecc.) e **seguirne la gestione** nel tempo.

L'oggetto centrale del sistema è la **segnalazione** (*Report*): un problema geo-localizzato inviato da un cittadino registrato, corredato da titolo, descrizione, categoria e fino a 3 foto. Le segnalazioni vengono pubblicate su una mappa cittadina e possono essere cercate, filtrate e tracciate lungo il loro ciclo di stati (in attesa di approvazione, assegnata, in lavorazione, sospesa, respinta, risolta).

Funzionalità principali previste dalla specifica:

- registrazione cittadino con verifica email e profilo personale;
- invio segnalazioni su **mappa OpenStreetMap**, con opzione di anonimato pubblico;
- consultazione pubblica in vista **mappa** e vista **tabella**, con filtri, ordinamento ed **export CSV**;
- possibilità di **seguire** una segnalazione e ricevere aggiornamenti;
- **notifiche** in-app ed email sui cambi di stato;
- **messaggistica** diretta tra cittadini e operatori comunali;
- **statistiche** pubbliche e private (per amministratori).

Il progetto è concepito come soluzione **open-source** adottabile anche da altre pubbliche amministrazioni.

---

## Cosa abbiamo fatto

Come gruppo abbiamo completato tutti e 10 i task. Di seguito una sintesi di ciò che ogni task richiedeva e del deliverable prodotto.

| # | Task | In cosa consisteva | Deliverable |
|---|------|--------------------|-------------|
| **1** | Project Management | PBS, WBS, diagramma di Gantt e risk management, con motivazione delle scelte di pianificazione | `doc/deliverable/01_ProjectManagement.md` |
| **2** | Requirements Engineering | Stakeholder, context diagram, interfacce, personas, user stories e requisiti | `doc/deliverable/02_RequirementsEngineering.md` |
| **3** | Use Cases | Diagramma dei casi d'uso, narrative complete e tabella di tracciabilità verso i requisiti | `doc/deliverable/03_UseCases.md` |
| **4** | Architecture & Design | Class diagram (glossario) e deployment diagram del sistema | `doc/deliverable/04_GlossaryAndDeployment.md` |
| **5** | Black-Box Testing | Progettazione dei test black-box del backend a partire dal contratto (firme, modelli, eccezioni) | `doc/deliverable/05_BlackBoxReport.md` + `src/backend/tests/blackbox/` |
| **6** | White-Box Testing | Test white-box progettati dal control-flow interno delle funzioni (node/edge/condition/path coverage) | `doc/deliverable/06_WhiteBoxReport.md` + `src/backend/tests/whitebox/` |
| **7** | Coverage Testing | Suite automatica (unit, integration, e2e) per massimizzare la code coverage sull'implementazione | `src/backend/tests/{unit,integration,e2e}/` |
| **8** | Postman API Acceptance | Test di accettazione delle API via HTTP sul backend in esecuzione, con verifica dell'access control | `src/backend/postman/` |
| **9** | Selenium UI Acceptance | Test di accettazione a livello browser sul frontend, tramite la REST API pubblica | `src/frontend/tests/selenium/` |
| **10** | Docker Deployment | Deploy locale di backend, frontend e database tramite Docker Compose, configurabile via variabili d'ambiente | `docker/` |

> La documentazione ufficiale dei requisiti si trova in [`doc/OfficialDocumentation.md`](doc/OfficialDocumentation.md); i diagrammi (context, use case, class, deployment) sono in [`data/`](data/) sia come immagini sia come sorgenti esportabili.

---


## Struttura della repository

```
Progetto-Ingegneria-Del-Software/
├── doc/                  # Documentazione del sistema e deliverable dei task
│   ├── Participium.md              # Descrizione del sistema (EN)
│   ├── Participium_it.md           # Descrizione del sistema (IT)
│   ├── OfficialDocumentation.md    # Documentazione ufficiale dei requisiti
│   └── deliverable/                # Deliverable prodotti (Task 1–6)
├── task/                 # Testo/specifica di ogni task assegnato
├── data/                 # Diagrammi, immagini e sorgenti (JSON/SVG/PDF)
├── src/
│   ├── backend/          # API Flask, servizi, modelli, repository e test
│   └── frontend/         # Applicazione React/Vite e test Selenium
├── docker/               # Dockerfile e docker-compose per il deployment
└── ASSIGNMENT.md         # Descrizione della struttura del repository di partenza
```

---

## Come eseguire il progetto

### Backend

```bash
cd src/backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python wsgi.py
```

- API: `http://localhost:5050`
- Swagger UI: `http://localhost:5050/apidocs/`

### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

- Applicazione: `http://localhost:5173`

### Docker (stack completo)

```bash
cd docker
docker compose up --build
```

> Per le opzioni di configurazione (variabili d'ambiente, database, seed) fare riferimento ai README dedicati in `src/backend/README.md` e `src/frontend/README.md`.

---

## Come eseguire i test

### Test del backend (pytest)

I test del backend usano **pytest** e vanno lanciati dalla cartella `src/backend`, con l'ambiente virtuale attivo e le dipendenze già installate. Ogni categoria ha una propria sottocartella e un marker dedicato, quindi si può eseguire l'intera suite oppure solo una parte.

```bash
cd src/backend

# Tutti i test
python -m pytest

# Per categoria — per cartella...
python -m pytest tests/blackbox      # Task 5 — black-box
python -m pytest tests/whitebox      # Task 6 — white-box
python -m pytest tests/unit          # Task 7 — unit
python -m pytest tests/integration   # Task 7 — integration
python -m pytest tests/e2e           # Task 7 — end-to-end

# ...oppure tramite marker
python -m pytest -m blackbox
python -m pytest -m "unit or integration"
```

### Coverage (Task 7)

Report di coverage sull'implementazione, eseguito da `src/backend`:

```bash
python -m pytest --cov=participium --cov-config=.coveragerc \
  --cov-report=term-missing --cov-report=html
```

Il report HTML viene generato sotto `reports/coverage/`.

### Postman / Newman (Task 8)

Test di accettazione delle API sul **backend in esecuzione** (`http://localhost:5050`). La collection è eseguibile da riga di comando con [Newman](https://github.com/postmanlabs/newman) (`npm install -g newman`), oppure importando i due file direttamente in Postman.

```bash
# con il backend avviato in un altro terminale
newman run src/backend/postman/Participium.postman_collection.json \
  -e src/backend/postman/Participium.postman_environment.json
```

### Selenium — acceptance UI (Task 9)

I test Selenium guidano un browser reale e richiedono che **backend e frontend siano entrambi avviati** (`http://localhost:5050` e `http://localhost:5173`), oltre a **Google Chrome** installato. Hanno un proprio `requirements.txt`.

```bash
# 1) avvia il backend  (src/backend)  ->  python wsgi.py
# 2) avvia il frontend (src/frontend) ->  npm run dev

# 3) in un terzo terminale:
cd src/frontend/tests/selenium
python3 -m venv .venv
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

> I test si aspettano i dati di seed di default (utenti cittadino / operatore / admin). Assicurarsi che il backend sia avviato con il seed abilitato (vedi `src/backend/README.md`).

---

*Progetto sviluppato a scopo didattico per il corso di Ingegneria del Software.*