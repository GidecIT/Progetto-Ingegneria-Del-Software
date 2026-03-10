# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| S1 |   Applicazione Web (UI+Client)  |      |    Portale unico reponsive per cittadini e operatori   |
| S2 |   Autenticazione & servizi Utente  |      |  Include: la registrazione con conferma per email, possibilità di anonimato per segnalazione e gestione profilo.Possibilità di vari ruoli: cittadini, uffici comunali e amministratori e consultazione libera per visitatori (senza login)  |
| S3 |   API gateway/BFF  |      |   Per separare il pannello cittadini dal pannello degli operatori/admin  |
| S4 |   Servizio di geolocalizzazione  |      |  Basato su OpenStreetMap  |
| S5 |   Servizio di notifiche e messagistica   |      |  Include: le notifiche in piattaforma, l'inviio di email (opzionali) ed il canale di messagistica diretta tra cittadino e operatori comunali|
| S6 |   Servizio di gestione delle segnalazioni  |      |   Gestisce l'inserimento della segnalazione (titolo, descrizione, massimo 3 foto) ed i 6 stati possibili, inoltre comprende la possibilità di: ricercare, filtrare, tracciare segnalazioni ed esportare in CSV|
| S7 |   Servizio di admin e moderazione  |      |   Comprende i vari strumenti per gli uffici comunali e per gli amministratori come: revisione, assegnazione, sospensione o rifiuto delle segnalazioni in ingresso |
| S8 |   Servizio di statistica e reportistica  |      |  Calcolo delle statistiche pubbliche e private  |
| I1 |   Cloud Account  |      |    |
| I2 |   Pipeline CI / CD & Repository GIT  |      |    |
| I3 |   Object Storage   |      |  per salvare le immagini  |
| I4 |   Database PostgreSQL  |      |  con l'estensione PostGIS per gestire le coordinate geografiche  |
| I5 |   OpenStreetMap  |      |    |
| I6 |   Configurazione Content Delivery Network  |      |    |
| I7 |   Sistema di Metriche e Log  |      |    |
| I8 |   Backup  |      |    |
| I9 |   Servizio Mail (Resend)  |      |    |
| I10 |   Docker Kubernetes  |      |    |


---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID  | Work package | Traced PBS outputs (IDs) |
|:----|:-------------|:--------------------------|
| #.# |              |                           |


---

# Gantt, dependencies, and critical path

## Activity table
| ID | Activity | Duration | Dependencies | Start | End | Critical | Milestone |
|:---|:---------|:---------|:-------------|:------|:----|:------|:---------|
| R# |          |          |              |       |     |       |          |


## Critical path
`X → X → X → ...`



---

# Risk Management

**Scales and thresholds**
- **Probability (P)**: 1 (rare) … 5 (almost certain)
- **Impact (I)**: 1 (minor) … 5 (critical)
- **Exposure**: `P × I` (range 1–25)

Risk level thresholds (by exposure):
- **Low**: 1–5
- **Medium**: 6–10
- **High**: 11–16
- **Very High**: >16



## Risks table
| ID | Risk | Category | P | I | P×I | Level | Mitigation / Response strategy |
|:---|:-----|:---------|--:|--:|----:|:------|:-------------------------------|
|  |      |          |   |   |     |       |                                |


