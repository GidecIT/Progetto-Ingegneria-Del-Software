# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

# 2) Use Case Narratives

| Use Case                    |                                                                                                                                                                                                               |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-01-Login|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Accedere al sistema per usufruire delle funzionalità riservate agli utenti registrati.|
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).|
| **Supporting actors**       | [Servizio di autenticazione (IF-10)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): garantire accessi autorizzati. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): accedere in sicurezza. |
| **Precondition**| L'utente deve aver completato la registrazione ([UC-05-Registrazione](#2-use-case-narratives)).|
| **Minimum guarantees**| Se l'autenticazione fallisce, l'utente non ottiene alcun privilegio di accesso e lo stato del sistema rimane invariato.|
| **Success guarantees**      | L'utente è autenticato e viene reindirizzato all'interno della piattaforma con i permessi corrispondenti al proprio ruolo.|
| **Trigger**|-|
| **Main success scenario**   | 1. L'utente clicca sul pulsante per il login nella home page o nella pagina di registrazione.|
|                             | 2. Il sistema mostra la pagina di login.|
|                             | 3. L'utente inserisce le proprie credenziali.|
|                             | 4. Il sistema valida le credenziali e verifica che l'account si attivo.|
|                             | 5. Il sistema autentica l'utente e assegna i permessi; il caso d'uso termina con successo.|
| **Extensions**              | 3a. L'utente annulla l'operazione.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema interrompe il processo; il caso d'uso termina con fallimento.|                                                                                                                                  |
|                             | 3b. L'utente chiede di resettare la password.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3b.1 Il sistema avvia [UC-12-RipristinoPassword](#2-use-case-narratives)|
|                             | 4a. Le credenziali inserite sono errate.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema mostra errore; il caso riprende dal punto 2.|
|                             | 4b. L'account del cittadino non ha l'email verificata.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;4b.1 Il sistema avvisa l'utente della necessità di confermare l'indirizzo email e il caso d'uso riprende dal punto 2.|

| Use Case                    ||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-02-InserimentoSegnalazione|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Inviare una segnalazione geolocalizzata di un disservizio urbano al Comune di Torino.|
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).|
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces), [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Comunicare efficacemente il problema riscontrato, garantire la propria privacy (anonimato pubblico), assicurarsi che la segnalazione venga ricevuta.<br>[Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere segnalazioni accurate e geolocalizzate con evidenze visive per ottimizzare gli interventi.
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).|
| **Minimum guarantees**      | Nessuna segnalazione viene creata se il processo viene interrotto.|
| **Success guarantees**      | Viene creata una segnalazione con stato "Pending Approval", le foto vengono archiviate, la posizione registrata e l'utente riceve conferma visiva.|
| **Trigger**|-|
| **Main success scenario**   | 1. L'utente clicca sul pulsante per inserire una nuova segnalazione nella dashboard principale, avviando la procedura di inserimento.|
|                             | 2. Il sistema mostra la mappa ([IF-03](./02_RequirementsEngineering.md#3-interfaces)) e il modulo.|
|                             | 3. Il cittadino seleziona la posizione del disservizio sulla mappa.|
|                             | 4. Il sistema cattura le coordinate geografiche.|
|                             | 5. Il cittadino inserisce le informazioni relative alla segnalazione. ([FR-13](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 6. Il cittadino carica fino a 3 foto relative alla segnalazione. ([NFR-04](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)).|
|                             | 7. Il cittadino seleziona opzionalmente l'anonimato pubblico ([FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 8. Il cittadino conferma l'invio cliccando il tasto per inviare la segnalazione.|
|                             | 9. Il sistema valida i dati, carica le immagini su Cloud Storage ([IF-04](./02_RequirementsEngineering.md#3-interfaces)) e salva la segnalazione.|
|                             | 10. Il sistema assegna lo stato "Pending Approval" e mostra successo; il caso d'uso termina con successo.|
| **Extensions**              | 2a. Non è possibile visualizzare correttamente la mappa.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa l'utente e il caso d'uso termina con fallimento.|
|                             | 6a. L'utente ha inserito più di 3 foto.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;6a.1 Il sistema impedisce il caricamento; il caso d'uso termina con fallimento.|
|                             | 9a. L''utente non ha inserito tutti i dati necessari.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;9a.1 Il sistema evidenzia i campi mancanti; il caso d'uso riprende dal punto 5.|
|                             | 9b. Errore nel caricamento delle immagini.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;9b.1 Il sistema avvisa l'utente del fallimento e il caso d'uso riprende dal punto 6.|

| Use Case||
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-03-GestioneStatoSegnalazione|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Aggiornare lo stato di una segnalazione durante il processo di gestione comunale.|
| **Primary actor**| [Operatore Comunale](./02_RequirementsEngineering.md#4-personas) (PER-05, PER-06).|
| **Supporting actors**| [Servizio di notifica (IF-07)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Operatore Comunale (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Gestire il carico di lavoro, tracciare l'avanzamento degli interventi. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere aggiornamenti trasparenti e tempestivi sulla risoluzione del problema.<br> [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Monitorare l'efficienza degli uffici tecnici. |
| **Precondition**            | L'operatore deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) e la segnalazione deve esistere nel sistema.|
| **Minimum guarantees**| Lo stato rimane invariato se l'aggiornamento fallisce.|
| **Success guarantees**| Lo stato della segnalazione è aggiornato, l'utente segnalante e i followers della seganalazione ricevono una notifica ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
| **Trigger**| -|
| **Main success scenario**   | 1. L'operatore seleziona una segnalazione dalla lista "In carico" nella dashboard amministrativa per visualizzarne i dettagli ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 2. L'operatore assegna un nuovo stato alla segnalazione scegliendo tra quelli disponibili.|
|                             | 3. L'operatore inserisce opzionalmente un commento interno nel campo di testo.|
|                             | 4. L'operatore conferma l'aggiornamento di stato, cliccando sul tasto di conferma.|
|                             | 5. Il sistema valida il passaggio di stato, aggiorna il database e registra lo storico.|
|                             | 6. Il sistema genera automaticamente notifiche in-platform ed email (opzionalmente) per il segnalante e i follower ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.|
| **Extensions**              | 2a. Operatore seleziona "Rejected".|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema obbliga la motivazione ([FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo (previa motivazione).|
|                             | 2b. Transizione di stato non valida.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2b.1 Il sistema segnala l'errore e impedisce l'operazione; il caso d'uso termina con fallimento.|

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-04-ConsultazioneSegnalazioni|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Navigare sulla mappa, filtrare e visualizzare i dettagli delle segnalazioni pubblicate.|
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03, PER-04).|
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Verificare se un problema è già stato segnalato, monitorare i disservizi nel proprio quartiere. <br> [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Garantire trasparenza e ridurre segnalazioni duplicate. |
| **Precondition**            | Il sistema deve essere accessibile.|
| **Minimum guarantees**      | Il sistema mostra le segnalazioni presenti nel database.|
| **Success guarantees**      | L'utente visualizza le segnalazioni correttamente, visionandole sia sulla mappa che nella vista tabellare.|
| **Trigger**                 | -|
| **Main success scenario**   | 1. L'utente accede alla pagina di consultazione delle segnalazioni.|
|                             | 2. Il sistema carica la mappa con i pin geolocalizzati ([FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr)) e la lista delle segnalazioni ([FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 3. L'utente visualizza le segnalazioni sulla mappa e nella lista, visualizzandone titolo, categoria, stato e data.|
|                             | 3. DA ELIMINAREEEEEEEEEEEEEEEEEEEEEEEEEEEEE <BR>L'utente applica filtri per categoria, stato o intervallo temporale tramite il pannello laterale ([FR-9.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 4. Il sistema aggiorna la visualizzazione in tempo reale in base ai filtri applicati.|
|                             | 5. L'utente seleziona una segnalazione specifica dalla mappa o dalla vista tabellare ([FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 6. Il sistema mostra la pagina di dettaglio con titolo, descrizione, categoria, foto e stato corrente ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.|
| **Extensions**              | 3a. L'utente effettua una ricerca testuale.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema filtra le segnalazioni che corrispondono alla stringa inserita ([FR-9](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.|
|                             | 5a. Segnalazione anonima.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;5a.1 Il sistema nasconde l'identità ([FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.|

| Use Case                    |                                                                                                                                                |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-05-Registrazione                                                                                                                            |
| **Scope**                   | Sistema web Participium.                                                                                                                       |
| **Level** | User goal.                                                                                                                                     |
| **Intention in Context**    | Creare un nuovo account utente sulla piattaforma fornendo dati identificativi.|
| **Primary actor**           | [Cittadino (visitatore)](./02_RequirementsEngineering.md#4-personas) (PER-04).|
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Ottenere l'accesso per effettuare segnalazioni.                          |
| **Precondition**            | L'utente non deve essere già registrato ([UC-07-Logout](#2-use-case-narratives)).|
| **Minimum guarantees**      | I dati relativi al nuovo utente non vengono salvati se la validazione fallisce.|
| **Success guarantees**      | Viene creato un account attivo dopo la verifica dell'email.|
| **Trigger**|-|
| **Main success scenario**   | 1. Il visitatore clicca sul pulsante per la registrazione nella home page o nella pagina di login.|
|                             | 2. Il sistema mostra il modulo di registrazione.|
|                             | 3. Il visitatore compila il form con i suoi dati.|
|                             | 4. Il visitatore spunta le caselle per accettare i termini e la privacy.|
|                             | 5. Il visitatore conferma la registrazione.|
|                             | 6. Il sistema valida i dati (univocità email) ([FR-3](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 7. Il sistema crea l'account e invia una mail con link di verifica ([IF-06](./02_RequirementsEngineering.md#3-interfaces)). |
|                             | 8. Il visitatore accede alla propria email e verifica l'account cliccando il link.|
|                             | 9. Il sistema attiva l'account e mostra un messaggio di conferma; il caso d'uso termina con successo.|
| **Extensions**              | 7a. Email già presente.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;7a.1 Il sistema segnala il conflitto. Il caso d'uso riprende dal punto 3.|
|                             | 8a. Link di verifica scaduto.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;8a.1 Il sistema permette di richiedere un nuovo invio; il caso d'uso riprende dal punto 8.|

| Use Case||
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-06-GestioneProfilo|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Aggiornare i dati personali, caricare una foto profilo e gestire le preferenze di notifica.|
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).|
| **Supporting actors**       | [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Personalizzare la propria esperienza e gestire la privacy.|
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).|
| **Minimum guarantees**      | Le modifiche non confermate non vengono salvate.|
| **Success guarantees**      | Il profilo e le preferenze vengono aggiornati correttamente.|
| **Trigger**                 |-|
| **Main success scenario**   | 1. L'utente clicca sulla propria icona profilo e seleziona "Impostazioni" o "Il mio profilo".|
|                             | 2. Il sistema mostra i dati correnti, la foto profilo (se presente) e le impostazioni notifiche ([FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 3. L'utente carica o modifica la propria foto profilo ([IF-04](./02_RequirementsEngineering.md#3-interfaces)).|
|                             | 4. L'utente attiva/disattiva il flag "Ricevi notifiche tramite email".|
|                             | 5. L'utente modifica eventuali campi anagrafici.|
|                             | 6. L'utente clicca sul pulsante "Salva Modifiche".|
|                             | 7. Il sistema valida i dati e aggiorna il database; il caso d'uso termina con successo.|
| **Extensions**              | 3a. Formato immagine non valido.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema avvisa l'utente sui formati ammessi; il caso d'uso termina con fallimento.|
|                             | 7a. Errore di connessione al database.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;7a.1 Il sistema mostra un messaggio di errore tecnico; il caso d'uso termina con fallimento.|


| Use Case                    |                                                                                                                        |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-07-Logout                                                                                                           |
| **Scope**                   | Sistema web Participium.                                                                                               |
| **Level** | User goal.                                                                                                             |
| **Intention in Context**    | Terminare la sessione in sicurezza.                                                                                    |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).                        |
| **Supporting actors**       | [Servizio di autenticazione (IF-10)](./02_RequirementsEngineering.md#3-interfaces).                                    |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Proteggere l'account su dispositivi condivisi.   |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                              |
| **Minimum guarantees**      | Nessuna.                                                                                                               |
| **Success guarantees**      | La sessione viene invalidata e l'accesso protetto revocato.                                                            |
| **Trigger**                 | -                                                                                                                      |
| **Main success scenario**   | 1. L'utente clicca sul pulsante "Esci" o "Logout" presente nel menu a tendina del profilo.                             |
|                             | 2. Il sistema invalida la sessione lato server ([FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 3. Il sistema reindirizza l'utente alla home page pubblica; il caso d'uso termina con successo.                        |
| **Extensions**              | 2a. Errore invalidazione.                                                                                              |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema forza la chiusura lato client; il caso d'uso termina con successo.             |

| Use Case                    |                                                                                                                                                                                                            |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-08-MessaggioOperatoreCittadino                                                                                                                                                                          |
| **Scope**                   | Sistema web Participium.                                                                                                                                                                                   |
| **Level** | User goal.                                                                                                                                                                                                 |
| **Intention in Context**    | Scambio di messaggi diretti tra operatore e cittadino su una segnalazione.                                                                                                                                 |
| **Primary actor**           | [Operatore Comunale](./02_RequirementsEngineering.md#4-personas) (PER-05, PER-06).                                                                                                                         |
| **Supporting actors**       | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).                                                                                                            |
| **Stakeholders' interests** | [Operatore Comunale (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Richiedere chiarimenti. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Facilitare l'intervento. |
| **Precondition**            | Entrambi gli attori devono essere autenticati ([UC-01-Login](#2-use-case-narratives)) e legati alla segnalazione specifica.                                                                                |
| **Minimum guarantees**      | I messaggi sono privati e legati solo al ticket di riferimento.                                                                                                                                            |
| **Success guarantees**      | Il messaggio viene recapitato e notificato al destinatario.                                                                                                                                                |
| **Trigger**                 | -                                                                                                                                                                                                          |
| **Main success scenario**   | 1. L'utente (operatore o cittadino) clicca sulla scheda "Messaggi" all'interno del dettaglio di una segnalazione.                                                                                          |
|                             | 2. Il sistema mostra la cronologia dei messaggi scambiati ([FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                         |
|                             | 3. L'utente scrive un nuovo testo nel campo di input e preme l'icona "Invia".                                                                                                                              |
|                             | 4. Il sistema salva il messaggio associandolo univocamente alla segnalazione.                                                                                                                              |
|                             | 5. Il sistema invia una notifica push o email al destinatario ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.                                 |
| **Extensions**              | 3a. Messaggio vuoto.                                                                                                                                                                                       |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema impedisce l'invio; il caso d'uso termina con fallimento.                                                                                                           |

| Use Case                    |                                                                                                                                         |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-09-ConsultazioneLog                                                                                                                  |
| **Scope**                   | Sistema web Participium.                                                                                                                |
| **Level** | User goal.                                                                                                                              |
| **Intention in Context**    | Monitorare log tecnici e sicurezza.                                                                                                     |
| **Primary actor**           | [Amministratore (di sistema)](./02_RequirementsEngineering.md#4-personas) (PER-07).                                                     |
| **Supporting actors**       | [Sistema di monitoraggio e logging (IF-08)](./02_RequirementsEngineering.md#3-interfaces).                                              |
| **Stakeholders' interests** | [Amministratore (di sistema, STK-03)](./02_RequirementsEngineering.md#1-stakeholders): Diagnosticare bug e monitorare intrusioni.       |
| **Precondition**            | L'amministratore deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Admin.                                            |
| **Minimum guarantees**      | I log sono in sola lettura e non modificabili.                                                                                          |
| **Success guarantees**      | L'amministratore visualizza le voci di log filtrate correttamente.                                                                      |
| **Trigger**                 | -                                                                                                                                       |
| **Main success scenario**   | 1. L'amministratore clicca sulla voce "Log di Sistema" nel menu laterale della dashboard amministrativa (**IF-02**).                    |
|                             | 2. Il sistema presenta l'elenco cronologico dei log persistenti ([FR-4](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 3. L'amministratore imposta i filtri di ricerca (livello errore, data, utente).                                                         |
|                             | 4. Il sistema aggiorna la tabella mostrando solo i log filtrati; il caso d'uso termina con successo.                                    |
| **Extensions**              | 3a. Nessun risultato.                                                                                                                   |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un avviso "Nessun log trovato"; il caso d'uso termina con successo.                      |

| Use Case                    |                                                                                                                                                                                                                               |
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-10-CreazioneAccountAmministratore                                                                                                                                                                                          |
| **Scope**                   | Sistema web Participium.                                                                                                                                                                                                      |
| **Level** | User goal.                                                                                                                                                                                                                     |
| **Intention in Context**    | Creare account per amministratori o operatori.                                                                                                                                                                                |
| **Primary actor**           | [Amministratore (di sistema)](./02_RequirementsEngineering.md#4-personas) (PER-07).                                                                                                                                           |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces).                                                                                                                                                        |
| **Stakeholders' interests** | [Amministratore (di sistema, STK-03)](./02_RequirementsEngineering.md#1-stakeholders): Gestire il team tecnico e operativo.                                                                                                   |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Amministratore.                                                                                                                                 |
| **Minimum guarantees**      | Non vengono creati account duplicati.                                                                                                                                                                                         |
| **Success guarantees**      | Viene creato il nuovo account e inviata la mail di benvenuto.                                                                                                                                                                 |
| **Trigger**                 | -                                                                                                                                                                                                                             |
| **Main success scenario**   | 1. L'amministratore clicca sul pulsante "Aggiungi Nuovo Utente" nella sezione Gestione Staff della dashboard (**IF-02**).                                                                                                     |
|                             | 2. L'amministratore inserisce nome, email e ruolo del nuovo collaboratore.                                                                                                                                                    |
|                             | 3. L'amministratore seleziona i permessi specifici (Amministratore o Operatore) ([FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 4. Il sistema valida i dati e crea l'utenza nel database.                                                                                                                                                                     |
|                             | 5. Il sistema invia automaticamente le credenziali temporanee via mail ([IF-06](./02_RequirementsEngineering.md#3-interfaces)); il caso d'uso termina con successo.                                                           |
| **Extensions**              | 4a. Email già registrata.                                                                                                                                                                                                     |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema nega la creazione mostrando errore; il caso d'uso termina con fallimento.                                                                                                             |

| Use Case                    |                                                                                                                                                                                               |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-11-GenerazioneReport                                                                                                                                                                       |
| **Scope**                   | Sistema web Participium.                                                                                                                                                                      |
| **Level** | User goal.                                                                                                                                                                                    |
| **Intention in Context**    | Estrarre dati statistici avanzati.                                                                                                                                                            |
| **Primary actor**           | [Amministratore (data analyst)](./02_RequirementsEngineering.md#4-personas) (PER-08).                                                                                                         |
| **Supporting actors**       | [Cloud Account (IF-09)](./02_RequirementsEngineering.md#3-interfaces).                                                                                                                        |
| **Stakeholders' interests** | [Amministratore (data analyst, STK-06)](./02_RequirementsEngineering.md#1-stakeholders): Ottimizzare i servizi comunali.                                                                      |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Amministratore/Analista.                                                                                        |
| **Minimum guarantees**      | I dati privati rimangono riservati agli amministratori.                                                                                                                                       |
| **Success guarantees**      | Il report viene generato ed esportato in formato conforme.                                                                                                                                    |
| **Trigger**                 | -                                                                                                                                                                                             |
| **Main success scenario**   | 1. L'amministratore clicca sulla voce "Statistiche e Report" nel menu principale della dashboard.                                                                                             |
|                             | 2. Il sistema propone i filtri di aggregazione (per categoria, per operatore, ecc.).                                                                                                          |
|                             | 3. L'amministratore seleziona i parametri per la generazione di dati privati ([FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                         |
|                             | 4. Il sistema genera e visualizza i grafici interattivi.                                                                                                                                      |
|                             | 5. L'amministratore clicca sul tasto "Esporta CSV" ([FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                   |
|                             | 6. Il sistema genera il file conforme allo standard e avvia il download ([NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con successo.    |
| **Extensions**              | 3a. Non autorizzato.                                                                                                                                                                          |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema nega l'accesso ai dati sensibili ([NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con fallimento. |

| Use Case                    |                                                                                                                                                                        |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-12-RipristinoPassword                                                                                                                                               |
| **Scope**                   | Sistema web Participium.                                                                                                                                               |
| **Level** | User goal.                                                                                                                                                             |
| **Intention in Context**    | Ripristinare la password smarrita.                                                                                                                                     |
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03, PER-04).                                                     |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces).                                                                                                 |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Recuperare l'accesso autonomamente.                                                              |
| **Precondition**            | L'account deve essere già stato verificato ([UC-05-Registrazione](#2-use-case-narratives)).                                                                            |
| **Minimum guarantees**      | Il token è temporaneo e monouso e se il ripristino fallisce la password rimane invariata.                                                                              |
| **Success guarantees**      | La password viene aggiornata con successo.                                                                                                                             |
| **Trigger**                 | -                                                                                                                                                                      |
| **Main success scenario**   | 1. L'utente clicca sul link "Hai dimenticato la password?" nella schermata di login.                                                                                   |
|                             | 2. L'utente inserisce la propria email nel campo richiesto.                                                                                                            |
|                             | 3. Il sistema invia una email contenente un token di ripristino monouso ([IF-06](./02_RequirementsEngineering.md#3-interfaces)).                                       |
|                             | 4. L'utente apre l'email e clicca sul link di ripristino.                                                                                                              |
|                             | 5. Il sistema valida il token e mostra il modulo per la nuova password.                                                                                                |
|                             | 6. L'utente inserisce e conferma la nuova password nel form mostrato a sistema.                                                                                        |
|                             | 7. L'utente clicca sul tasto "Conferma Ripristino".                                                                                                                    |
|                             | 8. Il sistema valida la complessità della password, aggiorna il database e invalida il token ([FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 9. Il sistema reindirizza l'utente al login con un messaggio di successo; il caso d'uso termina con successo.                                                          |
| **Extensions**              | 2a. L'email non è associata a nessun account attivo.                                                                                                                   |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa che l'email non è registrata; il caso d'uso termina con fallimento.                                                     |
|                             | 5a. Token invalido/scaduto.                                                                                                                                            |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;5a.1 Il sistema informa l'utente dell'impossibilità di procedere; il caso d'uso termina con fallimento.                                        |
|                             | 8a. La password non rispetta i requisiti di sicurezza ([FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                        |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;8a.1 Il sistema segnala l'errore; il caso d'uso riprende dal punto 6.                                                                          |

| Use Case                    |                                                                                                                                                                  |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-13-VisualizzazioneProprieSegnalazioni                                                                                                                         |
| **Scope**                   | Sistema web Participium.                                                                                                                                         |
| **Level** | User goal.                                                                                                                                                       |
| **Intention in Context**    | Permettere al cittadino di consultare lo storico e lo stato attuale di tutte le segnalazioni da lui inviate.                                                     |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).                                                                  |
| **Supporting actors**       | -                                                                                                                                                                |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Verificare l'avanzamento dei propri ticket e avere uno storico personale.                  |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                                                                        |
| **Minimum guarantees**      | Se non sono presenti segnalazioni, il sistema mostra un elenco vuoto senza errori.                                                                               |
| **Success guarantees**      | L'utente visualizza l'elenco corretto delle proprie segnalazioni con i relativi stati aggiornati.                                                                |
| **Trigger**                 | -                                                                                                                                                                |
| **Main success scenario**   | 1. L'utente clicca sulla voce "Le mie segnalazioni" presente nel menu del profilo o nella barra laterale della dashboard.                                        |
|                             | 2. Il sistema interroga il database per recuperare i record associati all'ID utente.                                                                             |
|                             | 3. Il sistema mostra una lista ordinata cronologicamente delle segnalazioni effettuate ([FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 4. Per ogni voce, il sistema mostra titolo, data e lo stato corrente dell'intervento.                                                                            |
|                             | 5. L'utente clicca su una specifica riga per aprirne il dettaglio completo ([UC-14](#2-use-case-narratives)); il caso d'uso termina con successo.                |
| **Extensions**              | 1a. L'utente non ha segnalazioni.                                                                                                                                |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra un messaggio "Non hai ancora effettuato segnalazioni"; il caso d'uso termina con successo.                        |

| Use Case                    |                                                                                                                                                                                          |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-14-VisualizzazioneDettaglioSegnalazione                                                                                                                                               |
| **Scope**                   | Sistema web Participium.                                                                                                                                                                 |
| **Level** | User goal.                                                                                                                                                                               |
| **Intention in Context**    | Accedere alla scheda completa di una segnalazione per leggerne la descrizione, visualizzarne le foto e visualizzare lo storico degli aggiornamenti.                                      |
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).                                                                                                        |
| **Supporting actors**       | [OpenStreetMap](./02_RequirementsEngineering.md#3-interfaces) (IF-03).                                                                                                                   |
| **Stakeholders' interests** | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas): Comprendere i dettagli di un problema specifico e seguire gli aggiornamenti di stato.                  |                                                                                                                                                                                                         |
| **Precondition**            | La segnalazione selezionata esiste ed è accessibile.                                                                                                                                     |
| **Minimum guarantees**      | La visualizzazione non altera lo stato o i contenuti della segnalazione.                                                                                                                 |
| **Success guarantees**      | Il cittadino visualizza la pagina di dettaglio completa contenente i dati della segnalazione e le relative interazioni pubbliche.                                                        |
| **Trigger**                 | Il cittadino clicca su una specifica segnalazione dalla visualizzazione della mappa.                                                                                                     |
| **Main success scenario**   | 1. Il sistema recupera i dati associati alla segnalazione selezionata (titolo, descrizione, categoria, posizione, foto allegate, stato corrente, storico degli aggiornamenti).           | 
|                             | 2. Il sistema mostra a schermo la pagina con tutte le informazioni raccolte ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo. |                                                                                                                                                                                                                                                                                                                                                          |
| **Extensions**              | 1a. La segnalazione non è raggiungibile (poiché rimossa o a causa di un errore di sistema).                                                                                              |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra un messaggio di errore e il caso d'uso termina con un fallimento.                                                                         |

| Use Case                    |                                                                                                                                            |
|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-15-VisualizzazioneStoricoAggiornamenti                                                                                                  |
| **Scope**                   | Sistema web Participium.                                                                                                                   |
| **Level** | User goal.                                                                                                                                 |
| **Intention in Context**    | Verificare lo storico degli stati di una segnalazione per monitorare la gestione del problema nel tempo.                                   |
| **Primary actor**           | [Cittadino](./02_RequirementsEngineering.md#4-personas).                                                                                   |
| **Supporting actors**       | -                                                                                                                                          |
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Verificare lo stato della segnalazione e monitorarne i progressi nel tempo.   |
| **Precondition**            | L'utente deve aver selezionato una segnalazione.                                                                                           |
| **Minimum guarantees**      | Se il sistema non riesce a recuperare lo storico, l'utente visualizza comunque i dati correnti della segnalazione.                         |
| **Success guarantees**      | Il sistema mostra tutti i cambi di stato nel tempo.                                                                                        |
| **Trigger**                 | -                                                                                                                                          |
| **Main success scenario**   | 1. L'utente accede alla pagina di dettaglio di una segnalazione.                                                                           |
|                             | 2. Il sistema recupera dal database lo storico dei cambi di stato ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 3. Il sistema visualizza i passaggi di stato mostrandone le relative date; il caso d'uso termina con successo.                             |
| **Extensions**              | 2a. Lo storico è vuoto.                                                                                                                    |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra i dati correnti della segnalazione e il caso d'uso termina con successo.                    |

| Use Case                    |                                                                                                                                                                                   |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-16-FollowSegnalazione                                                                                                                                                          |
| **Scope**                   | Sistema web.                                                                                                                                                                      |
| **Level** | User goal.                                                                                                                                                                        |
| **Intention in Context**    | Seguire una segnalazione esistente per ricevere aggiornamenti sulla sua evoluzione.                                                                                               |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas).                                                                                                            |
| **Supporting actors**       | [Servizio di Notifica (IF-07)](./02_RequirementsEngineering.md#3-interfaces).                                                                                                     |
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Rimanere informato sugli sviluppi della risoluzione delle segnalazioni di interesse.                                 |
| **Precondition**            | L'utente deve essere autenticato ([UC-01](#2-use-case-narratives)) e deve star vedendo i dettagli di una segnalazione.                                                            |
| **Success guarantees**      | Il sistema predispone l'invio di notifiche all'utente ad ogni cambio di stato della segnalazione seguita ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
| **Trigger**                 | -                                                                                                                                                                                 |
| **Main success scenario**   | 1. Il cittadino preme il pulsante "Segui".                                                                                                                                        |
|                             | 2. Il sistema associa l'identificativo utente alla segnalazione nel database.                                                                                                     |
|                             | 3. Il sistema conferma visivamente l'attivazione del follow; il caso d'uso termina con successo.                                                                                  |
| **Extensions**              | 1a. L'utente segue già la segnalazione.                                                                                                                                           |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra l'opzione "Smetti di seguire".                                                                                                     |

| Use Case                    |                                                                                                                                                                                                                                                                       |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-17-AnalisiAvanzataAmministratore                                                                                                                                                                                                                                   |
| **Scope**                   | Sistema web Participium.                                                                                                                                                                                                                                              |
| **Level** | User goal.                                                                                                                                                                                                                                                            |
| **Intention in Context**    | Analizzare dati complessi per monitorare l'efficienza del servizio e prevenire abusi (es. top segnalanti).                                                                                                                                                            |
| **Primary actor**           | [Amministratore](./02_RequirementsEngineering.md#4-personas) (PER-08).                                                                                                                                                                                                |
| **Supporting actors**       | [Modulo Statistiche (S3.1)](./01_ProjectManagement.md).                                                                                                                                                                                                               |
| **Stakeholders' interests** | [Amministratore](./02_RequirementsEngineering.md#1-stakeholders): Ottimizzare i flussi di lavoro e identificare criticità sistemiche. <br> [Comune di Torino](./02_RequirementsEngineering.md#1-stakeholders): Disporre di reportistica per la pianificazione urbana. |
| **Precondition**            | L'amministratore deve essere autenticato con permessi elevati.                                                                                                                                                                                                        |
| **Success guarantees**      | Il sistema genera report e grafici basati su metriche private non accessibili al pubblico ([FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                                                    |
| **Trigger**                 | -                                                                                                                                                                                                                                                                     |
| **Main success scenario**   | 1. L'amministratore accede all'area riservata della Dashboard.                                                                                                                                                                                                        |
|                             | 2. Seleziona i parametri da considerare nell'analisi.                                                                                                                                                                                                                 |
|                             | 3. Il sistema elabora i dati tramite query.                                                                                                                                                                                                                           |
|                             | 4. Il sistema visualizza i grafici avanzati e le tabelle analitiche; il caso d'uso termina con successo.                                                                                                                                                              |
| **Extensions**              | 3a. L'elaborazione fallisce.                                                                                                                                                                                                                                          |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un messaggio di errore, il caso d'uso riprende dal punto 2.                                                                                                                                                            |

| Use Case                    |                                                                                                                                                                  |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-18-AnalisiStatistichePubbliche                                                                                                                                |
| **Scope**                   | Sistema web Participium.                                                                                                                                         |
| **Level** | User goal.                                                                                                                                                       |
| **Intention in Context**    | Consultare dati aggregati e trend generali per comprendere lo stato dei problemi urbani in città.                                                                |
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).                                                                                |
| **Supporting actors**       | [Portale pubblico (S8)](./01_ProjectManagement.md).                                                                                                              |
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Avere una visione d'insieme dei disservizi più comuni nel proprio comune.                           |
| **Precondition**            | Il portale deve essere online e accessibile.                                                                                                                     |
| **Success guarantees**      | L'utente visualizza grafici anonimi e aggiornati, basati su categorie e trend temporali ([FR-17](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
| **Trigger**                 | -                                                                                                                                                                |
| **Main success scenario**   | 1. L'utente accede alla sezione "Statistiche" del portale pubblico.                                                                                              |
|                             | 2. Il sistema mostra le statistiche pubbliche.                                                                                                                   |
|                             | 3. L'utente filtra i dati per periodo (giorno, settimana, mese).                                                                                                 |
|                             | 4. Il sistema aggiorna dinamicamente le visualizzazioni; il caso d'uso termina con successo.                                                                     |
| **Extensions**              | 3a. Il filtro selezionato non restituisce dati.                                                                                                                  |
|                             | &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un messaggio informativo, il caso d'uso riprende dal punto 2.                                                     |

| Use Case                    ||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-19-RicercaSegnalazioni|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Consultare segnalazioni specifiche tramite ricerca per nome o descrizione.|
| **Primary actor**| [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | -|
| **Stakeholders' interests** | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#1-stakeholders): trovare rapidamente le segnalazioni di interesse. <br> [Comune di Torino](./02_RequirementsEngineering.md#1-stakeholders): garantire trasparenza pubblica offrendo strumenti efficaci per velocizzare la consultazione. |
| **Precondition**            | Il sistema contiene segnalazioni pubblicate.|
| **Minimum guarantees**      | |
| **Success guarantees**      | L'utente ottiene e visualizza un sottoinsieme di segnalazioni corrispondenti ai criteri di ricerca.|
| **Trigger**                 | |
| **Main success scenario**   | 1. L'utente scrive del testo nella barra di ricerca delle segnalazioni. |
|                             | 2. Il sistema cerca le segnalazioni corrispondenti al testo inserito.|
|                             | 3. Il sistema aggiorna la visualizzazione mostrando solo le segnalazioni corrispondenti; il caso d'uso termina con successo.|
| **Extensions**              | 2a. Nessuna segnalazione soddisfa i criteri inseriti dall'utente.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra un risultato vuoto e il caso d'uso termina.|

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      |UC-20-FiltraggioSegnalazioni|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Consultare segnalazioni specifiche che soddisfano i filtri (categoria, stato, periodo temporale).|
| **Primary actor**| [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | |
| **Stakeholders' interests** | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#1-stakeholders): visualizzare segnalazioni corrispondenti ai criteri di ricerca e visualizzarle secondo l'ordine desiderato. <br> [Comune di Torino](./02_RequirementsEngineering.md#1-stakeholders): garantire trasparenza pubblica offrendo strumenti efficaci per velocizzare la consultazione. |
| **Precondition**            | Il sistema contiene segnalazioni pubblicate.|
| **Minimum guarantees**      | |
| **Success guarantees**      | L'utente ottiene e visualizza un sottoinsieme di segnalazioni corrispondenti ai filtri selezionati.|
| **Trigger**                 | |
| **Main success scenario**   | 1. L'utente seleziona uno o più filtri di ricerca nell'interfaccia.|
|                             | 2. Il sistema cerca le segnalazioni corrispondenti ai criteri impostati dall'utente (filtri applicati e parole inserite nella barra di ricerca) nel database ([FR-09](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
|                             | 3. Il sistema aggiorna la visualizzazione mostrando solo i risultati filtrati. Il caso d'uso termina con successo.|
| **Extensions**              | 2a. Nessuna segnalazione soddisfa i criteri inseriti dall'utente.|
|                             | &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra un risultato vuoto e il caso d'uso termina.|


| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-21-Notifiche|
| **Scope**| Sistema web Participium.|
| **Level**|Subfunction|
| **Intention in Context**| Informare gli utenti che seguono (Follow) la segnalazione di un avanzamento di stato.|
| **Primary actor**           | [Operatore Comunale](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**|Servizio di notifca, Servizio Mail|
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): essere informato sui cambiamenti di stato delle segnalazioni a cui è interessato. |
| **Precondition**|Lo stato della segnalazione è cambiato e l'utente la sta seguendo.|
| **Minimum guarantees**|Nessuna notifica viene inviata se nessun utente sta seguendo la segnalazione.|
| **Success guarantees**| L'utente riceve una notifica in piattaforma e via email se ha espresso tale preferenza.|
| **Trigger**| Un operatore comunale modifica lo stato di una segnalazione.|
| **Main success scenario**|1. Il sistema individua gli utenti che seguono la segnalazione.|
| |2. Il sistema invia una notifica in piattaforma a tutti gli utenti interessati comunicando il cambio di stato appena registrato.|
| |3. Se l'utente ha attivato la ricezione di notifiche via email, il sistema invia una mail con le stesse informazioni. Il caso d'uso termina con successo.|
| **Extensions**|3a. Il servizio di notifica non è disponibile. Il caso d'uso termina con errore.|



|________________________________|

# Traceability Table

| UC ID | REQ ID                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|:------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC-01 | [FR-5](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-02 | [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.2](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-04](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)                                                                 |
| UC-03 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                               |
| UC-04 | [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr) |
| UC-05 | [FR-3](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                       |
| UC-06 | [FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-7.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-07 | [FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                       |
| UC-08 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-09 | [FR-4](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                       |
| UC-10 | [FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                 |
| UC-11 | [FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr), [NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)                                                                                                                                     |
| UC-12 | [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                     |
| UC-13 | [FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                     |
| UC-14 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-15 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-16 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-17 | [FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-18 | [FR-17](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-19 | [FR-09](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
 UC-20 | [FR-09.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-09.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
| UC-21 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)|