# 1) Stakeholders

| ID     | Stakeholder name | Description | Role | Main concerns |
|:-------|:-----------------|:------------|:-----|:--------------|
| STK-01 |Cittadino         | Utenti finali, risiedono o frequentano la città. | Utilizzatori | Semplicità d'uso, attenzione alla privacy e ai dati personali, efficienza nella comunivazione e nellarisoluzione dei problemi. |
| STK-02 |Operatori Comunali| Personale degli uffici tecnici incaricato della gestione delle segnalazioni. | Utilizzatori / Gestori | Carico di lavoro, precisione delle segnalazioni, comunicazione con il cittadino. |
| STK-03 |Amministratori di Sistema| Personale IT che gestisce l'infrastruttura (Cloud, DB, Docker). | Gestori Tecnici | Sicurezza dei dati, scalabilità dell'infrastruttura, monitoraggio di log e metriche. |
| STK-04 |Comune di Torino   | L'ente pubblico che adotta e finanzia il sistema. | Committente | Efficienza operativa, feedback positivi, conformità legale. |
| STK-05 |Sviluppatori | Incaricati dello sviluppo del sistema. | Sviluppatori | Sviluppo delle funzionalità richieste, qualità del codice, tempi di sviluppo. |
| STK-06 |Analisti  | Personale incaricato dell'analisi dei requisiti e della valutazione delle performance. | Analisti | Analisi dei dati, valutazione delle performance, feedback sugli aspetti funzionali. |
| STK-07 |Servizi di archiviazione Cloud | Fornitori di servizi cloud per  storage delle immagini. | Sistema Esterno | Disponibilità, performance, costi. |
| STK-08 |Content Delivery Network (CDN) | Fornitori di servizi CDN per distribuzione rapida dei contenuti. | Sistema Esterno | Velocità di distribuzione, affidabilità, costi. |
| STK-09 |Servizio di Autenticazione | Fornitori di servizi per gestione dell'autenticazione e sicurezza. | Sistema Esterno | Sicurezza, facilità d'integrazione, costi. |
| STK-10 |Servizio di Notifica | Fornitori di servizi per invio di notifiche push o email. | Sistema Esterno | Affidabilità, facilità d'integrazione, costi. |
---

# 2) Context Diagram

Attach your context diagram as an image under `../data/img/` and link it here:

- `![](../data/img/context-diagram.png)`

---

# 3) Interfaces

| ID    | Interface | Actor       | Physical interface | Logical interface |
|:------|:----------|:------------|:-------------------|:------------------|
| **IF-01** | Web App (Cittadino) | Cittadino / Visitatore | Smartphone/PC con connessione ad Internet | Applicazione web responsive |
| **IF-02** |Dashboard amministrativa | Operatore Comunale / Amministratori | PC con connessione ad Internet | Dashboard gestionale e di amministrazione |
| **IF-03** | Map Service API | Servizio OpenStreetMap [(I5)](./01_ProjectManagement.md)  | Connessione a Internet | API per geolocalizzazione |
| **IF-04** | Media Storage API | Object Storage [(I3)](./01_ProjectManagement.md)  | Connessione a Internet | API per upload/download immagini segnalazioni |
| **IF-05** | Content Delivery Network | CDN [(I6)](./01_ProjectManagement.md) | Connessione a Internet | Interfaccia per distribuzione rapida contenuti |
| **IF-06** | Servizio mail | Cittadini  | Connessione a Internet | Protocollo SMTP per invio notifiche email |
| **IF-07** | Servizio di notifiche | Cittadini | Connessione Internet | API per invio notifiche push |
| **IF-08** | Analytics/Logging Interface | Sistema di Metriche e Log [(I7)](./01_ProjectManagement.md)  | Connessione a Internet | API/Dashboard per monitoraggio prestazioni e errori |
| **IF-09** | Servizio Cloud | Cloud Account [(I1)](./01_ProjectManagement.md) | Connessione Internet | Piattaforma per hosting |
| **IF-10** | Servizio di autenticazione | Cittadini / Amministratori | Connessione Internet | API REST per login, registrazione e gestione profilo |
| **IF-11** |Sistema di monitoraggio| Amministratori | Connessione Internet | Dashboard per metriche e log |

---


# 4) Personas

| ID     | Name | Role | Background / Context | Goals | Constraints | Devices / Usage setting | Accessibility / Additional needs |
|:-------|:-----|:-----|:---------------------|:------|:------------|:------------------------|:---------------------------------|
| PER-XX |      |      |                      |       |             |                         |                                  |

---

# 5) User Stories

| ID    | Persona/Role | User story (As a… I want… so that…) |
|:------|:-------------|:------------------------------------|
| US-XX |              |                                     |

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