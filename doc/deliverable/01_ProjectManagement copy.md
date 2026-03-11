# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| **SOFTWARE** | 
| S1 | Applicazione Web (UI + Client) | - | Frontend per l'interazione utente. |
| S2 | Area Riservata Cittadino | - | Gestione profilo e preferenze personali. |
| S3 | Dashboard gestionale Amministratori | - | Pannello di controllo e visualizzazione statistiche per amministratori. |
| S3.1 | Modulo Statistiche | - | Visualizzazione statistiche e reportistica. |
| S4 | Servizio Notifiche e Messaggistica | - | Email, notifiche e messaggi in piattaforma. |
| S5 | API Gateway / BFF | - | - |
| S6 | Servizio di Geolocalizzazione | - | Mappa integrata nella applicazione.Funzioni di ricerca, filtri geografici e tracciabilità. |
| S7 | Servizio di Segnalazione | - | Creazione e invio delle segnalazioni. |
| S8 | Consultazione e Monitoraggio | - | Consultazione pubblica, include la funzione "Follow". |
| S8.1 | Esportazione CSV | - | Export dei dati a partire dalla visualizzazione tabellare. |
| **INFRASTRUTTURA** | 
| I1 | Cloud Account | - | Setup ambienti cloud (es. AWS, Azure, GCP). |
| I2 | Pipeline CI / CD & Repo GIT | - | - |
| I3 | Object Storage | - | Archiviazione delle immagini. |
| I4 | Database PostgreSQL | - | Progettazione del DB relazionale. |
| I5 | Integrazione OpenStreetMap | - | Integrazione mappe della città. |
| I6 | Content Delivery Network (CDN) | - |  |
| I7 | Sistema di Metriche e Log | - | Monitoraggio errori, prestazioni e log. |
| I8 | Sistema di Backup | - | Procedure di  salvataggio dati e recovery. |
| I9 | Servizio Mail (Resend) | - | - |
| I10 | Docker Kubernetes | - | Containerizzazione per scalabilità infrastrutturale. |
| **DOCUMENTAZIONE** |
| D1 | Vision & Scope | Documento | Definizione obiettivi, visione e scopo. |
| D2 | Documento dei Requisiti | Documento | Analisi funzionale dettagliata. |
| D3 | Architettura | Documento | Schemi logici, fisici e diagrammi di funzionamento del sistema. |
| D4 | Documentazione API (Swagger) | Tecnico | |
| D5 | Strategia di Test | Documento | Piano di test unit, test d'integrazione e test di accettazione. ???????|
| D6 | Manualistica di Deploy / Utilizzo | Tecnico | Istruzioni per installazione e manutenzione. |
| D7 | Guida Utente | Supporto | Manuale d'uso per utilizzatori. |
| D8 | Sicurezza, Privacy & Legale | Legale | Termini d'uso e sicurezza. |
| D9 | Pianificazione Progetto | Gestione | ?????????? |
---

# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID  | Work package | Traced PBS outputs (IDs) |
|:----|:-------------|:--------------------------|
|1|Project Management|D1,D9|
|2|Requirement Elicitation|D1,D2|
|3|Architettura, User Experience & API Design|S5,D3,D4|
|4|Cloud Development||
|5| Sviluppo Backend||
|6|Sviluppo Frontend||
|6.a|Frontend Cittadino||
|6.b|Frontend Amministratore||
|7|Media Storage|I3,I6,I7|
|8|Integrazione Open Street Map|S6,I5|
|9|Implementazione WebApp|S1|
|10|Gestione sistema di notifica|S4,I9|
|11|System Integration & functional testing|D5|
|12|Non functional Validation|D5,D8|
|13|Gestione del rilascio |D6,D7|
|14|Finalizzazione documenti |D3,D4,D6,D7,D8,D9|


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


