# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.
  
| Use Case                |                             |
|:------------------------|:----------------------------|
| ID                      |UC-01-Login                |
| Scope                   |Sistema web Participium                             |
| Level                   |User goal                             |
| Intention in Context    |Accedere al sistema per usufruire delle funzionalità riservate agli utenti registrati                             |
| Primary actor           |Utente registrato                              |
| Supporting actors       |                             |
| Stakeholders' interests |Comune di Torino: garantire che solo gli utenti verificati e autorizzati possano interagire con le segnalazioni o accedere ai dati amministrativi. <br> Utente:accedere in sicurezza al proprio profilo e operare sulla piattaforma                             |
| Precondition            |L'utente deve aver completato la regstrazione.|
| Minimum guarantees      |Se l'autenticazione fallisce,l'utete non ottiene alcun privilegio di accesso e lo stato del sistema rimane invariato                             |
| Success guarantees      |L'utente è autenticato e viene reindirizzato all'interno della piattaforma con i permessi corrispondenti al proprio ruolo                             |
| Trigger                 |L'utente richiedere di accedere al sistema cliccando sul pulsante login                              |
| Main success scenario   |1. L'utente chiede di loggarsi a Participium 2. Il sistema mostra la pagina di login 3. L'utente inserisce le proprie credenziali e verifica che l'account sia attivo 4. Il sistema valida le credenziali e verifica che l'account sia attiva 5. Il sistema autentica l'utente e gli assegna i permessi corretti 6. Il caso d'uso termina con successo                        |
| Extensions              |3a. L'utente annulla l'operazione: 3a.1 Il sistema interrompe il processo di login e il caso d'uso termina con un fallimento 4a. Le credenziali inserite non sono corrette: 4a.1 Il sistema mostra un messaggio di errore e il caso d'uso riprende dal punto 2 4b. L'account del cittadino non ha l'email verificata: 4b.1 Il sistema avvisa l'utente della necessità di confermare l'indirizzo email e il caso d'uso riprende dal punto 2                              |

| Use Case                |                             |
|:------------------------|:----------------------------|
| ID                      |UC-02-InserimentoSegnalazione|
| Scope                   |Sistema web Participium      |
| Level                   |User goal                    |
| Intention in Context    |Inviare una segnalazione geolocalizzata di un disservizio urbano al Comune di Torino. |
| Primary actor           |[Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03) |
| Supporting actors       |[OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces), [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces) |
| Stakeholders' interests |[Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Comunicare efficacemente il problema, garantire la propria privacy (anonimato pubblico), assicurarsi che la segnalazione venga ricevuta. <br> [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere dati accurati e geolocalizzati con evidenze visive per ottimizzare gli interventi. <br> [Operatore Comunale (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Ottenere informazioni chiare e foto per valutare l'entità del problema. |
| Precondition            |L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)). |
| Minimum guarantees      |Nessuna segnalazione viene creata nel database e nessun file viene caricato se il processo viene interrotto o fallisce. |
| Success guarantees      |Viene creata una nuova segnalazione con stato "Pending Approval", le foto sono archiviate, la posizione è registrata e l'utente riceve conferma. |
| Trigger                 |L'utente seleziona l'opzione per inserire una nuova segnalazione sulla mappa o tramite pulsante dedicato. |
| Main success scenario   |1. Il cittadino avvia la procedura di inserimento segnalazione. <br> 2. Il sistema mostra la mappa interattiva ([OpenStreetMap](./02_RequirementsEngineering.md#3-interfaces)) e il modulo di inserimento. <br> 3. Il cittadino seleziona la posizione del disservizio sulla mappa. <br> 4. Il sistema cattura le coordinate geografiche. <br> 5. Il cittadino inserisce titolo, descrizione e seleziona una [categoria](./02_RequirementsEngineering.md#6-functional-requirements-fr) (FR-13.2). <br> 6. Il cittadino carica da 1 a 3 [foto](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr) (NFR-04). <br> 7. Il cittadino seleziona opzionalmente l'opzione di [anonimato pubblico](./02_RequirementsEngineering.md#6-functional-requirements-fr) (FR-13.1). <br> 8. Il cittadino conferma l'invio. <br> 9. Il sistema valida i dati, carica le immagini su Cloud Storage e salva la segnalazione. <br> 10. Il sistema assegna lo stato "Pending Approval" e mostra un messaggio di successo. |
| Extensions              |2a. Il servizio mappa non è disponibile: 2a.1 Il sistema avvisa l'utente e termina il caso d'uso. <br> 6a. Il cittadino carica più di 3 foto: 6a.1 Il sistema impedisce il caricamento o mostra un errore. <br> 9a. Dati obbligatori mancanti o invalidi: 9a.1 Il sistema evidenzia i campi mancanti e torna al punto 5. <br> 9b. Errore nel caricamento delle immagini: 9b.1 Il sistema avvisa l'utente del fallimento e permette di riprovare l'invio. |

| Use Case                |                             |
|:------------------------|:----------------------------|
| ID                      |UC-03-GestioneStatoSegnalazione|
| Scope                   |Sistema web Participium      |
| Level                   |User goal                    |
| Intention in Context    |Aggiornare lo stato di una segnalazione durante il processo di gestione comunale. |
| Primary actor           |[Operatore Comunale](./02_RequirementsEngineering.md#4-personas) (PER-05, PER-06) |
| Supporting actors       |                             |
| Stakeholders' interests |[Operatore Comunale (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Gestire il carico di lavoro, tracciare l'avanzamento degli interventi. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere aggiornamenti trasparenti e tempestivi sulla risoluzione del problema. <br> [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Monitorare l'efficienza degli uffici tecnici. |
| Precondition            |L'operatore deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) e la segnalazione deve esistere nel sistema. |
| Minimum guarantees      |Lo stato della segnalazione rimane invariato se l'aggiornamento fallisce. |
| Success guarantees      |Lo stato della segnalazione è aggiornato, l'utente segnalante (e i follower) ricevono una [notifica](./02_RequirementsEngineering.md#6-functional-requirements-fr) (FR-15). |
| Trigger                 |L'operatore accede alla dashboard di gestione e seleziona una segnalazione da aggiornare. |
| Main success scenario   |1. L'operatore visualizza i dettagli di una segnalazione ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 2. L'operatore seleziona un nuovo stato dall'elenco predefinito (es. "Assigned", "In Progress", "Resolved"). <br> 3. L'operatore inserisce opzionalmente un commento o aggiornamento interno. <br> 4. L'operatore conferma l'aggiornamento. <br> 5. Il sistema valida il passaggio di stato, aggiorna il database e registra lo storico. <br> 6. Il sistema genera automaticamente notifiche in-platform ed email per il segnalante e i follower ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
| Extensions              |2a. L'operatore seleziona "Rejected": 2a.1 Il sistema obbliga l'inserimento di una motivazione ([FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 2b. Transizione di stato non valida: 2b.1 Il sistema segnala l'errore e impedisce l'operazione. |

# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-01 | FR-5, FR-5.1 |
| UC-02 | FR-13, FR-13.1, FR-13.2, FR-8, NFR-04 |
| UC-03 | FR-14, FR-14.1, FR-15, FR-16 |
