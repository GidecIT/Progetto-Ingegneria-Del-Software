# 1) Stakeholders

| ID     | Stakeholder name   | Description | Role | Main concerns |
|:-------|:-------------------|:------------|:-----|:--------------|
| STK-01 | Cittadino          | Utenti finali, risiedono o frequentano la città. | Utilizzatori | Semplicità d'uso, attenzione alla privacy e ai dati personali, efficienza nella comunivazione e nellarisoluzione dei problemi. |
| STK-02 | Operatori Comunali | Personale degli uffici tecnici incaricato della gestione delle segnalazioni. | Utilizzatori / Gestori | Carico di lavoro, precisione delle segnalazioni, comunicazione con il cittadino. |
| STK-03 | Amministratori     | Personale IT che gestisce l'infrastruttura (Cloud, DB, Docker). | Gestori Tecnici | Sicurezza dei dati, scalabilità dell'infrastruttura, monitoraggio di log e metriche. |
| STK-04 | Comune di Torino   | L'ente pubblico che adotta e finanzia il sistema. | Committente | Efficienza operativa, feedback positivi, conformità legale. |
---

# 2) Context Diagram

Attach your context diagram as an image under `../data/img/` and link it here:

- `![](../data/img/context-diagram.png)`

---

# 3) Interfaces

| ID    | Interface                       | Actor       | Physical interface | Logical interface |
|:----------|:--------------------------------|:------------|:-------------------|:------------------|
| **IF-01** | Web App (Cittadino)             | Cittadino / Visitatore | Smartphone/PC con connessione ad Internet | Applicazione web responsive |
| **IF-02** | Dashboard amministrativa        | Operatore Comunale / Amministratori | PC con connessione ad Internet | Dashboard gestionale e di amministrazione |
| **IF-03** | Map Service API                 | Servizio OpenStreetMap (I5) | Connessione a Internet | API per geolocalizzazione |
| **IF-04** | Media Storage API               | Servizio di archiviazione cloud (I3) | Connessione a Internet | API per upload/download immagini segnalazioni |
| **IF-05** | Content Delivery Network        | CDN (I6) | Connessione a Internet | Interfaccia per distribuzione rapida contenuti |
| **IF-06** | Servizio mail                   | Cittadini  | Connessione a Internet | Protocollo SMTP per invio notifiche email |
| **IF-07** | Servizio di notifiche           | Cittadini | Connessione Internet | API per invio notifiche push |
| **IF-08** | Analytics/Logging Interface     | Sistema di Metriche e Log (I7) | Connessione a Internet | API/Dashboard per monitoraggio prestazioni e errori |
| **IF-09** | Servizio di archiviazione Cloud | Sistema di storage cloud | Connessione Internet | API per upload/download file |
| **IF-10** | Servizio di autenticazione      | Cittadini / Amministratori | Connessione Internet | API REST per login, registrazione e gestione profilo |
| **IF-11** | Sistema di monitoraggio         | Amministratori | Connessione Internet | Dashboard per metriche e log |

---

# 4) Personas

| ID     | Name   | Role               | Background / Context                                                                                           | Goals                                                                                                                  | Constraints                                                                  | Devices / Usage setting        | Accessibility / Additional needs                                                                     |
|:-------|:-------|:-------------------|:---------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------|:-------------------------------|:-----------------------------------------------------------------------------------------------------|
| **PER-01** | Marco  | Cittadino          | Residente a Torino, 35 anni. Nota spesso problemi urbani (buche, lampioni) nel tragitto casa-lavoro.           | Segnalare disservizi in meno di 2 minuti e ricevere aggiornamenti sullo stato.                                         | Scarsa pazienza per form complicati; preoccupato per la privacy dei dati.    | Smartphone (On-the-go), 4G/5G. | Interfaccia ad alto contrasto per uso all'aperto.                                                    |
| **PER-02** | Giulia | Operatore Comunale | Dipendente comunale, 50 anni. Gestisce decine di ticket al giorno e coordina le squadre di operatori comunali. | Filtrare segnalazioni fasulle, assegnare priorità e e smistarle correttamente ai reparti competenti senza errori.      | Deve rispettare i tempi di risposta previsti dal regolamento comunale (SLA). | PC Desktop (Ufficio), Tablet.  | Facilità di lettura di mappe e coordinate GPS. <br/>Ipovedente: necessita di font ridimensionabili." |
| **PER-03** | Sandro | Amministratore     | Sistemista esperto, 42 anni. Si occupa della stabilità della piattaforma e della sicurezza di essa.            | Assicurare che il sistema sia sempre online, non ci siano violazioni di sicurezza e che i dati siano salvati (Backup). | Deve operare con permessi limitati sui dati sensibili (GDPR).                | Laptop professionale, VPN/SSH. | Dashboard di monitoraggio e alert automatici.                                                        |

---

# 5) User Stories

| ID         | Persona/Role                | User story (As a… I want… so that…)                                                                                              |
|:-----------|:----------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| **US-01**  | Marco - Cittadino           | Come cittadino, voglio inviare una foto e la posizione GPS di un problema, così che il comune possa localizzarlo con precisione. |
| **US-02**  | Marco - Cittadino           | Come cittadino, voglio ricevere una notifica quando la mia segnalazione cambia stato, così da sentirmi coinvolto nel processo.   |
| **US-03**  | Giulia - Operatore Comunale | Come operatore, voglio visualizzare le segnalazioni su una mappa, così da ottimizzare i percorsi delle squadre di riparazione.   |
| **US-04**  | Giulia - Operatore Comunale | Come operatore, voglio poter rifiutare segnalazioni duplicate, così da non sprecare risorse su problemi già presi in carico.     |
| **US-05**  | Sandro - Amministratore     | Come admin, voglio che il login sia protetto, così da impedire accessi non autorizzati alla dashboard amministrativa.            |
| **US-06**  | Sandro - Amministratore     | Come admin, voglio consultare i log, così da individuare e risolvere rapidamente bug nel backend.                                |
| **US-07**  | Comune - Torino             | Come ente, voglio generare report sulle risoluzioni, così da dimostrare l'efficienza operativa del sistema ai cittadini.         |
---

# 6) Functional Requirements (FR)

| ID    | Requirement statement (The system shall…) | Priority | User story ID | Notes |
|:------|:------------------------------------------|:---------|:--------------|:------|
| FR-XX |                                           |          |               |       |


---

# 7) Non-Functional Requirements (NFR)

| ID     | Category | Requirement statement | Metric / Target | Verification                           | Priority | Notes |
|:-------|:---------|:----------------------|:----------------|:---------------------------------------|:---------|:------|
| NFR-XX |          |                       |                 |                                        |          |       |