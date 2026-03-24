
# 1) Stakeholders

| ID     | Stakeholder name               | Description                                                                                      | Role                   | Main concerns                                                                                                                  |
|:-------|:-------------------------------|:-------------------------------------------------------------------------------------------------|:-----------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| STK-01 | Cittadino                      | Utenti finali, risiedono o frequentano la città, possono essere autenticati o meno (visitatori). | Utilizzatori           | Semplicità d'uso, attenzione alla privacy e ai dati personali, efficienza nella comunivazione e nellarisoluzione dei problemi. |
| STK-02 | Operatori Comunali             | Personale degli uffici tecnici incaricato della gestione delle segnalazioni.                     | Utilizzatori / Gestori | Carico di lavoro, precisione delle segnalazioni, comunicazione con il cittadino.                                               |
| STK-03 | Amministratori di Sistema      | Personale IT che gestisce l'infrastruttura (Cloud, DB, Docker).                                  | Gestori Tecnici        | Sicurezza dei dati, scalabilità dell'infrastruttura, monitoraggio di log e metriche.                                           |
| STK-04 | Comune di Torino               | Ente pubblico che adotta e finanzia il sistema.                                                  | Committente            | Efficienza operativa, feedback positivi, conformità legale.                                                                    |
| STK-05 | Sviluppatori                   | Incaricati dello sviluppo del sistema.                                                           | Sviluppatori           | Sviluppo delle funzionalità richieste, qualità del codice, tempi di sviluppo.                                                  |
| STK-06 | Analisti                       | Personale incaricato dell'analisi dei requisiti e della valutazione delle performance.           | Analisti               | Analisi dei dati, valutazione delle performance, feedback sugli aspetti funzionali.                                            |
| STK-07 | Servizi di archiviazione Cloud | Fornitori di servizi cloud per  storage delle immagini.                                          | Sistema Esterno        | Disponibilità, performance, costi.                                                                                             |
| STK-08 | Content Delivery Network (CDN) | Fornitori di servizi CDN per distribuzione rapida dei contenuti.                                 | Sistema Esterno        | Velocità di distribuzione, affidabilità, costi.                                                                                |
| STK-09 | Servizio di Autenticazione     | Fornitori di servizi per gestione dell'autenticazione e sicurezza.                               | Sistema Esterno        | Sicurezza, facilità d'integrazione, costi.                                                                                     |
| STK-10 | Servizio di Notifica           | Fornitori di servizi per invio di notifiche push o email.                                        | Sistema Esterno        | Affidabilità, facilità d'integrazione, costi.                                                                                  |
---

# 2) Context Diagram

Il diagramma di contesto mostra il funzionamento generale del sistema **Participium** e le sue interazioni con le entità esterne.

![Diagramma di Contesto](../../data/img/Context Diagram.jpg)

**Legenda:**
- **Arancione:** Rappresenta gli attori (persone o ruoli) che interagiscono direttamente con il sistema (Cittadini, Operatori, Amministratori).
- **Verde:** Rappresenta i sistemi e i servizi esterni integrati (OpenStreetMap, Resend, Cloud Storage).
- **Frecce:** Indicano la direzione del flusso di dati tra Participium e le entità.

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

| ID     | Name      | Role                    | Background / Context                                                                                                  | Goals                                                                                                                  | Constraints                                                                                      | Devices / Usage setting                      | Accessibility / Additional needs                                                               |
|:-------|:----------|:------------------------|:----------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|:---------------------------------------------|:-----------------------------------------------------------------------------------------------|
| PER-01 | Marco     | Cittadino (autenticato) | Residente a Torino in zona centrale, 35 anni. Nota spesso problemi urbani (buche, lampioni) nel tragitto casa-lavoro. | Segnalare disservizi in meno di 2 minuti e ricevere aggiornamenti sullo stato.                                         | Scarsa pazienza per form complicati; preoccupato per la privacy dei dati.                        | Smartphone (On-the-go), 4G/5G.               | Interfaccia ad alto contrasto per uso all'aperto.                                              |
| PER-02 | Pietro    | Cittadino (autenticato) | Studente universitario fuori sede, 20 anni. Vive in periferia e utilizza molto la bicicletta e i mezzi pubblici.      | Segnalare piste ciclabili ostruite o fermate dell'autobus danneggiate per migliorare la mobilità.                      | Budget limitato (usa solo Wi-Fi pubblico o pochi giga); preferisce il login tramite Social/SPID. | Smartphone (entry-level), Tablet.            | Necessita di feedback sonori per la conferma dell'invio segnalazione.                          |
| PER-03 | Giuseppe  | Cittadino (visitatore)  | Pensionato, 78 anni. Vive nel quartiere storico. Ha uno smartphone ma lo usa solo per le basi (WhatsApp/Chiamate).    | Segnalare un lampione spento davanti casa senza dover creare account o usare lo SPID, che trova troppo complicato.     | Non ha/non sa usare lo SPID o l'identità digitale; teme di sbagliare e "rompere" l'app.          | Smartphone (uso saltuario), Wi-Fi domestico. | Font molto grandi; icone intuitive; possibilità di invio seganalzione "anonimo".               |
| PER-04 | Giulia    | Operatore Comunale      | Dipendente comunale, 50 anni. Gestisce decine di ticket al giorno e coordina le squadre di operatori comunali.        | Filtrare segnalazioni fasulle, assegnare priorità e smistarle correttamente ai reparti competenti senza errori.        | Deve rispettare i tempi di risposta previsti dal regolamento comunale (SLA).                     | PC Desktop (Ufficio), Tablet.                | Facilità di lettura di mappe e coordinate GPS. Ipovedente: necessita di font ridimensionabili. |
| PER-05 | Matteo    | Operatore Comunale      | Tecnico sul campo, 28 anni. Riceve gli incarichi sul tablet e deve recarsi sul luogo per verificare il danno.         | Documentare l'avvenuta riparazione con foto e chiudere il ticket in tempo reale.                                       | Lavora spesso sotto la pioggia o con i guanti; deve operare in zone con poco segnale.            | Tablet rugged (rinforzato), GPS.             | Interfaccia con tasti grandi e utilizzabile con mani bagnate/guanti.                           |
| PER-06 | Sandro    | Amministratore          | Sistemista esperto, 42 anni. Si occupa della stabilità della piattaforma e della sicurezza di essa.                   | Assicurare che il sistema sia sempre online, non ci siano violazioni di sicurezza e che i dati siano salvati (Backup). | Deve operare con permessi limitati sui dati sensibili (GDPR).                                    | Laptop professionale, VPN/SSH.               | Dashboard di monitoraggio e alert automatici.                                                  |
| PER-07 | Alessia   | Amministratore          | Data Analyst e Responsabile Trasparenza, 38 anni. Analizza i flussi di dati per ottimizzare i servizi comunali.       | Estrarre report periodici sui tempi di intervento e identificare le zone della città con più disservizi.               | Deve garantire l'anonimato dei cittadini nei report pubblici (Open Data).                        | PC Desktop, Monitor multipli.                | Visualizzazioni grafiche avanzate e compatibilità con screen reader per audit.                 |
---

# 5) User Stories

| ID    | Persona/Role                      | User story (As a… I want… so that…)                                                                                                                                   |
|:------|:----------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| US-01 | Marco - Cittadino (autenticato)   | Come cittadino, voglio inviare una foto e la posizione GPS di un problema, così che il comune possa localizzarlo con precisione.                                      |
| US-02 | Marco - Cittadino (autenticato)   | Come cittadino, voglio ricevere una notifica quando la mia segnalazione cambia stato, così da sentirmi coinvolto nel processo.                                        |
| US-03 | Pietro - Cittadino (autenticato)  | Come studente pendolare, voglio segnalare malfunzionamenti alle stazioni di ricarica bici, così da poter pianificare i miei spostamenti senza imprevisti.             |
| US-04 | Giuseppe - Cittadino (autenticato) | Come utente anziano, così da non rinunciare a partecipare per colpa della burocrazia digitale. |
| US-05 | Giulia - Operatore Comunale       | Come operatore, voglio visualizzare le segnalazioni su una mappa, così da ottimizzare i percorsi delle squadre di riparazione.                                        |
| US-06 | Giulia - Operatore Comunale       | Come coordinatrice, voglio assegnare i ticket alle squadre in base alla zona di competenza, così da ridurre i tempi di spostamento dei mezzi.                         |
| US-07 | Matteo - Operatore stradale       | Come tecnico sul campo, voglio poter allegare la foto del lavoro terminato direttamente dal tablet, così da chiudere l'intervento senza tornare in ufficio.           |
| US-8 | Matteo - Operatore Comunale       | Come operatore, voglio poter rifiutare segnalazioni duplicate, così da non sprecare risorse su problemi già presi in carico.                                          |
| US-9 | Sandro - Amministratore           | Come admin, voglio che il login sia protetto, così da impedire accessi non autorizzati alla dashboard amministrativa.                                                 |
| US-10 | Sandro - Amministratore           | Come admin, voglio consultare i log, così da individuare e risolvere rapidamente bug nel backend.                                                                     |
| US-11 | Alessia - Amministratore          | Come data analyst, voglio generare grafici sull'andamento stagionale dei guasti, così da suggerire manutenzioni preventive al comune.                                 |
| US-12 | Alessia - Amministratore               | Come data analyst, voglio generare report sulle risoluzioni, così da dimostrare l'efficienza operativa del sistema ai cittadini.                                              |---

# 6) Functional Requirements (FR)

| ID    | Requirement statement (The system shall…) | Priority | User story ID | Notes |
|:------|:------------------------------------------|:---------|:--------------|:------|
| FR-XX |                                           |          |               |       |


---

# 7) Non-Functional Requirements (NFR)

| ID     | Category | Requirement statement | Metric / Target | Verification                           | Priority | Notes |
|:-------|:---------|:----------------------|:----------------|:---------------------------------------|:---------|:------|
| NFR-01 |Usabilità |L'applicazione web deve essere respon sive per l'uso da mobile                      |Il layout si adatta senza scrolling orizzontale su schermi da minimo 320 pixel di larghezza                 |Ispezione visiva e UI test automatici su emulatori                                        | Alta         |    Essenziale poichè la maggior parte delle segnalazioni avvengono direttamente in strada   |
| NFR-02| Prestazioni| La mappa pubblica deve caricarsi rapidamente| Rendering iniziale con 1000 segnalazioni "aperte" in meno di 3 secondi su rete 4G| Perfomamnce testing automatizzato|Alta| La mappa è l'elemento centrale, la velocità di caricamento sulle reti mobili è essenziale sia elevata|
| NFR-03| Sicurezza | Tutela rigorosa dell'opzione di anonimato pubblico| Zero occorrenze di dati identificativi ( nome,cognome,email) nei payload API pubblici| Analisi statica del codice e Penetration Test| Alta| Bilancia la trasparenza pubblica con la privacy del cittadino|
| NFR-04| Prestazioni| Elaborazione efficiente degli allegati, fino a tre foto| Upload ed elaborazione di tre immagini, massimo 5 MB cadauno, in meno di 5 secondi totali nel lato server| Load testing sull'endpoint di upload| Media| Si limita la dimensione per garantire la velocità in mobilità mantenendo una qualità visiva utile agli uffici|
| NFR-05| Sicurezza| Accesso alle statistiche private limitato agli amministratori| Il 100% dei tentativi di accesso da utenti non-admin genera errore HTTP 403| Test automatizzati di autorizzazione| Alta| Previene la fuga di dati aggregati non destinati alla consultazione pubblica|
| NFR-06| Interporabilità| Esportazione dati tabellari in formato CSV| Conformità totale allo standard RFC 4180, nessun errore in Excel/Sheets| Ispezione tramite validatori CSV| Media| Garantisce trasparenza e usabilità dei dati offline per analisi esterne da parte di cittadini|
| NFR-07| Affidabilità| Invio tempestivo delle notifiche email| Il 95% delle email consegnate al server SMTP entro 2 minuti dal cambio di stato| Analisi automatizzata dei log| Media| Una comunicazione rapida è necessaria per mantenere alto l'engagment del cittadino|
| NFR-08| Accessibilità| Interfaccia pubblica accessibile a cittadini con disabilità| Conformità livello AA delle linee guida WCAG 2.1| Test con tool automatici e navigazione con screen reader| Alta| Requisito normativo e morale essenziale per un servizio di pubblica amministrazione| 
| NFR-09| Portabilità| Sistema facilmente distribuibile per l'adozione open-source| Avvio completo (DB, Backend,Frontend) via script in meno di 15 minuti su server| Test di deployment in ambiente isolato| Media| Se l'installazione fosse complessa nessun altro comune adoterrebbe la piattaforma|
| NFR-10| Disponibilità| Alta disponibilità per inserimento segnalazioni e consultazioni| L'uptime del sito web e delle API pubbliche deve essere garantito per almeno il 99,9% del tempo ogni mese | Monitoraggio sintetico continuo| Alta| Il servizio deve essere sempre attivo, specialmente per segnalare problemi in situazioni di emergenza urbana|