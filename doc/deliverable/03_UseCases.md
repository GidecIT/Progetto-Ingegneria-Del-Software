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
| **Primary actor**           | Cittadino, Operatore Comunale, Amministratore|
| **Supporting actors**       | Servizio di autenticazione (IF-10).|
| **Stakeholders' interests** | Comune di Torino: garantire ai cittaadini accessi autorizzati e protetti. <br> Cittadino, Operatore Comunale, Amministratore: accedere in sicurezza ai propri account. |
| **Precondition**| L'utente deve aver completato la registrazione UC-05-Registrazione.
| **Minimum guarantees**| Se l'autenticazione fallisce, l'utente non ottiene alcun privilegio di accesso e lo stato del sistema rimane invariato.|
| **Success guarantees**      | L'utente è autenticato e viene reindirizzato all'interno della piattaforma con i permessi corrispondenti al proprio ruolo.|
| **Trigger**|-|
| **Main success scenario**   | 1. L'utente chiede di effettuare il login. <br>  2. Il sistema mostra la pagina di login. <br> 3. L'utente inserisce le proprie credenziali. <br> 4. Il sistema valida le credenziali e verifica che l'account si attivo.<br> 5. Il sistema autentica l'utente e assegna i permessi dovuti; il caso d'uso termina con successo.|
| **Extensions**              | 3a. L'utente annulla l'operazione.<br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema interrompe il processo; il caso d'uso termina con fallimento.<br> 3b. L'utente chiede di resettare la password. <br> &nbsp;&nbsp;&nbsp;&nbsp;3b.1 Il sistema avvia UC-11-RipristinoPassword <br> 4a. Le credenziali inserite sono errate.<br>  &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema mostra errore; il caso riprende dal punto 2. <br> 4b. L'account del cittadino non ha l'email verificata. <br> &nbsp;&nbsp;&nbsp;&nbsp;4b.1 Il sistema avvisa l'utente della necessità di confermare l'indirizzo email e il caso d'uso riprende dal punto 2. <br> 4c. L'account è disabilitato. <br> &nbsp;&nbsp;&nbsp;&nbsp;4c.1 Il sistema mostra un messaggio di errore; il caso d'uso riprende dal punto 2.|

| Use Case                    ||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-02-InserimentoSegnalazione|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Inviare una segnalazione geolocalizzata di un disservizio urbano al Comune di Torino.|
| **Primary actor**           | Cittadino|
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces), [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | Cittadino: Comunicare efficacemente il problema riscontrato, garantire la propria privacy (anonimato pubblico), assicurarsi che la segnalazione venga ricevuta.<br>Comune di Torino: Ricevere segnalazioni accurate e geolocalizzate con evidenze visive per ottimizzare gli interventi.
| **Precondition**            | L'utente deve essere autenticato UC-01-Login.|
| **Minimum guarantees**      | Nessuna segnalazione viene creata se il processo viene interrotto.|
| **Success guarantees**      | Viene creata una segnalazione con stato "Pending Approval", le foto vengono archiviate, la posizione registrata e l'utente riceve conferma visiva.|
| **Trigger**|-|
| **Main success scenario**   | 1. L'utente clicca sul pulsante per inserire una nuova segnalazione avviando la procedura di inserimento. <br>  2. Il sistema mostra la mappa e il modulo. <br>  3. Il cittadino seleziona la posizione del disservizio sulla mappa; il sistema cattura le coordinate geografiche. <br> 4. Il cittadino inserisce le informazioni relative alla segnalazione. ([FR-13](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 5. Il cittadino carica fino a 3 foto relative alla segnalazione. <br> 6. Il cittadino seleziona opzionalmente l'anonimato pubblico ([FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 7. Il cittadino conferma l'invio cliccando il tasto per inviare la segnalazione. <br> 8. Il sistema valida i dati, carica le immagini su Cloud Storage  e salva la segnalazione. <br> 9. Il sistema assegna lo stato "Pending Approval" e mostra successo; il caso d'uso termina con successo.|
| **Extensions**              | 2a. Non è possibile visualizzare correttamente la mappa.<br>&nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa l'utente e il caso d'uso termina con fallimento.<br> 3.a Il cittadino seleziona una posizione non valida (fuori dai confini di Torino).<br>&nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema segnala l'errore e impedisce la selezione; il caso d'uso riprende dal punto 3. <br>  8a. L''utente non ha inserito tutti i dati necessari.<br>&nbsp;&nbsp;&nbsp;&nbsp;8a.1 Il sistema evidenzia i campi mancanti; il caso d'uso riprende dal punto 5. <br> 8b. L'utente non ha caricato alcuna foto.<br>&nbsp;&nbsp;&nbsp;&nbsp;8b.1 Il sistema ; il caso d'uso termina con fallimento.|

| Use Case||
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-03-GestioneStatoSegnalazione|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Aggiornare lo stato di una segnalazione durante il processo di gestione comunale.|
| **Primary actor**| Operatore Comunale.|
| **Supporting actors**| [Servizio di notifica (IF-07)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | Operatore Comunale; Gestire il carico di lavoro, tracciare l'avanzamento degli interventi. <br> Cittadino: Ricevere aggiornamenti trasparenti e tempestivi sulla risoluzione del problema.<br> Comune di Torino: Monitorare l'efficienza degli uffici tecnici. |
| **Precondition**            | L'operatore deve essere autenticato UC-01-Login. e la segnalazione deve esistere nel sistema.|
| **Minimum guarantees**| Lo stato rimane invariato se l'aggiornamento fallisce.|
| **Success guarantees**| Lo stato della segnalazione è aggiornato, l'utente segnalante e i followers della seganalazione ricevono una notifica ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
| **Trigger**| -|
| **Main success scenario**   | 1. L'operatore chiede di modificare una segnalazione. <br> 2. L'operatore assegna un nuovo stato alla segnalazione scegliendo tra quelli disponibili. <br> 3. L'operatore inserisce opzionalmente un commento interno nel campo di testo. <br>  4. L'operatore conferma l'aggiornamento di stato, cliccando sul tasto di conferma. <br> 5. Il sistema valida il passaggio di stato, aggiorna il database e registra lo storico. <br> 6. Il sistema genera automaticamente notifiche in-platform ed email (opzionalmente) per il segnalante e i follower ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.|
| **Extensions**              | 2a. La transizione di stato non è valida. <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema segnala l'errore e impedisce l'operazione; il caso d'uso riprende dal punto 2.<br>  2b. La segnlazione è già stata completata (Resolved o Rejected). &nbsp;&nbsp;&nbsp;&nbsp; <br> &nbsp;&nbsp;&nbsp;&nbsp; 2b.1 Il sistema segnala l'errore e impedisce l'operazione; il caso d'uso riprende dal punto 2.<br>  4a. Errore di connessione al database. <br> &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema mostra un messaggio di errore; il caso d'uso termina con fallimento.|

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-04-VisualizzazioneSegnalazioni|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Visualizzare le segnalazioni presenti sia sulla mappa che nella vista tabellare.|
| **Primary actor**           | Cittadino.|
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | Cittadino: Verificare se un problema è già stato segnalato, monitorare i disservizi nella città. <br> Comune di Torino: Garantire trasparenza e ridurre segnalazioni duplicate. |
| **Precondition**            |-|
| **Minimum guarantees**      |-|
| **Success guarantees**      | L'utente visualizza le segnalazioni correttamente.|
| **Trigger**                 | -|
| **Main success scenario**   | 1. L'utente chiede di consultazione le segnalazioni. <br> 2. Il sistema carica la mappa con i pin geolocalizzati ([FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr)) e la lista delle segnalazioni ([FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 3. L'utente visualizza le segnalazioni sulla mappa e nella lista, visualizzandone titolo, categoria, stato e data. Il caso d'uso termina con successo.|
| **Extensions**              | 2a. Il sistema OpenStreetMap non è disponibile.<br>&nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa l'utente e mostra solo la lista delle segnalazioni; il caso d'uso termina con successo.|

| Use Case||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**   | UC-05-Registrazione|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Creare un nuovo account utente sulla piattaforma fornendo dati identificativi.|
| **Primary actor**           | Cittadino(Visitatore).|
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | Cittadino: Ottenere l'accesso per effettuare segnalazioni.                          |
| **Precondition**            | L'utente non deve essere già registrato ([UC-07-Logout](#2-use-case-narratives)).|
| **Minimum guarantees**      | I dati relativi al nuovo utente non vengono salvati se la validazione fallisce.|
| **Success guarantees**      | Viene creato un account attivo dopo la verifica dell'email.|
| **Trigger**|-|
| **Main success scenario**   | 1. Il visitatore chiede di registrarsi. <br> 2. Il sistema mostra il modulo di registrazione. <br> 3. Il visitatore compila il form. <br> 4. Il visitatore conferma la registrazione. <br> 5. Il sistema crea l'account e invia una mail con link di verifica. <br>  6. Il visitatore accede alla propria email e verifica l'account cliccando il link. <br> 7. Il sistema attiva l'account e mostra un messaggio di conferma; il caso d'uso termina con successo.|
| **Extensions**              | 4a. Username o email già presente. <br> &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema segnala il conflitto; il caso d'uso riprende dal punto 3. <br> 4b. La password non soddisfa i criteri di sicurezza. <br> &nbsp;&nbsp;&nbsp;&nbsp;4b.1 Il sistema segnala l'errore; il caso d'uso riprende dal punto 3. <br> 6a. Link di verifica scaduto.<br> &nbsp;&nbsp;&nbsp;&nbsp;6a.1 Il sistema permette di richiedere un nuovo invio; il caso d'uso riprende dal punto 6.|

| Use Case||
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-06-GestioneProfilo |
| **Scope**                   | Sistema web Participium |
| **Level**                   | User goal |
| **Intention in Context**    | Aggiornare i dati personali, caricare una foto profilo e gestire le preferenze di notifica.|
| **Primary actor**           | Cittadino (autenticato) |
| **Supporting actors**       | Media Storage (IF-04) |
| **Stakeholders' interests** | [Cittadino (STK-01): Personalizzare la propria esperienza e gestire la privacy.|
| **Precondition**            | L'utente deve essere autenticato (UC-01-Login).|
| **Minimum guarantees**      | Le modifiche non confermate non vengono salvate.|
| **Success guarantees**      | Il profilo e le preferenze vengono aggiornati correttamente.|
| **Trigger**                 |- |
| **Main success scenario**   | 1. L'utente seleziona l'impostazione relative alla gestione del profilo. <br> 2. Il sistema mostra i dati correnti, la foto profilo (se presente) e le impostazioni notifiche ([FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr)).  <br> 3. L'utente carica o modifica la propria foto profilo. <br> 4. L'utente attiva/disattiva il flag "Ricevi notifiche tramite email". <br> 5. L'utente modifica eventuali campi anagrafici. <br> 6. L'utente sceglie l'opzione per salvare le modifiche. <br> 7. Il sistema valida i dati e aggiorna il database; il caso d'uso termina con successo.|
| **Extensions**              | 3a. Formato immagine non valido. <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema avvisa l'utente sui formati ammessi; il caso d'uso termina con fallimento. <br> 7a. Errore di connessione al database. <br> &nbsp;&nbsp;&nbsp;&nbsp; 7a.1 Il sistema mostra un messaggio di errore tecnico; il caso d'uso termina con fallimento.|

| Use Case||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| **ID**   | UC-07-Logout|
| **Scope**     | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Terminare la sessione in sicurezza. |
| **Primary actor**           | Cittadino (autenticato) |
| **Supporting actors**       | Servizio di autenticazione (IF-10) |
| **Stakeholders' interests** | Cittadino (STK-01): Proteggere l'account su dispositivi condivisi. |
| **Precondition**            | L'utente deve essere autenticato UC-01-Login. |
| **Minimum guarantees**      | - |
| **Success guarantees**      | La sessione viene invalidata e l'accesso protetto revocato. |
| **Trigger**                 | - |
| **Main success scenario**   | 1. L'utente seleziona l'opzione per eseguire il logout. <br> 2. Il sistema invalida la sessione lato server ([FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br>  3. Il sistema reindirizza l'utente alla home page pubblica; il caso d'uso termina con successo.                        |
| **Extensions**              | 2a Errore invalidazione.  <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema forza la chiusura lato client; il caso d'uso termina con successo.             |


| Use Case                    ||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-08-MessaggioOperatoreCittadino|
| **Scope**                   | Sistema web Participium |
| **Level** | User goal |
| **Intention in Context**    | Scambio di messaggi diretti tra operatore e cittadino su una segnalazione. |
| **Primary actor**           | Operatore Comunale |
| **Supporting actors**       | Cittadino (autenticato) |
| **Stakeholders' interests** | Operatore Comunale (STK-02): Richiedere chiarimenti. <br> Cittadino (STK-01): Facilitare l'intervento. |
| **Precondition**            | Entrambi gli attori devono essere autenticati (UC-01-Login). e legati alla segnalazione specifica. |
| **Minimum guarantees**      | I messaggi sono privati e legati solo al ticket di riferimento. |
| **Success guarantees**      | Il messaggio viene recapitato e notificato al destinatario. |
| **Trigger**                 | - |
| **Main success scenario**   | 1. L'utente seleziona l'opzione per visualizzare i messaggi all'interno del dettaglio di una segnalazione.  <br>  2. Il sistema mostra la cronologia dei messaggi scambiati ([FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br>  3. L'utente scrive un nuovo testo del messaggio e lo invia. <br>  4. Il sistema salva il messaggio associandolo univocamente alla segnalazione.     <br>  5. Il sistema invia una notifica al destinatario ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.                                 |
| **Extensions**              | 3a. Messaggio vuoto.   <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema impedisce l'invio; il caso d'uso termina con fallimento. |

| Use Case                    ||
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-09-CreazioneAccountAmministratore |
| **Scope**                   | Sistema web Participium |
| **Level** | User goal |
| **Intention in Context**    | Creare account per amministratori o operatori.|
| **Primary actor**           | Amministratore (gestore tecnico) |
| **Supporting actors**       | Servizio mail (IF-06) |
| **Stakeholders' interests** | Amministratore (STK-03): Gestire il team tecnico e operativo. |
| **Precondition**            | L'utente deve essere autenticato (UC-01-Login) come Amministratore. |
| **Minimum guarantees**      | Non vengono creati account duplicati. |
| **Success guarantees**      | Viene creato il nuovo account e inviata la mail di benvenuto. |
| **Trigger**                 | - |
| **Main success scenario**   | 1. L'amministratore sceglie l'opzione per aggiungere un nuovo utente dalla dashboard <br> 2. L'amministratore inserisce nome, email e ruolo del nuovo collaboratore.          <br> 3. L'amministratore seleziona i permessi specifici (Amministratore o Operatore) ([FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)).<br>  4. Il sistema valida i dati e crea l'utenza nel database.           <br>5. Il sistema invia automaticamente le credenziali temporanee via mail ([IF-06](./02_RequirementsEngineering.md#3-interfaces)); il caso d'uso termina con successo.                                                           |
| **Extensions**              | 4a. Email già registrata.             <br> &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema nega la creazione mostrando errore; il caso d'uso termina con fallimento. |

| Use Case                    ||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-10-GenerazioneReport |
| **Scope**                   | Sistema web Participium |
| **Level** | User goal |
| **Intention in Context**    | Estrarre dati statistici avanzati. |
| **Primary actor**           | Amministratore (data analyst) |
| **Supporting actors**       | Cloud Account (IF-09) |
| **Stakeholders' interests** | Amministratore (data analyst) (STK-03): Ottimizzare i servizi comunali. |
| **Precondition**            | L'utente deve essere autenticato (UC-01-Login) come Amministratore (data analyst). |
| **Minimum guarantees**      | I dati privati rimangono riservati agli amministratori. |
| **Success guarantees**      | Il report viene generato ed esportato in formato conforme. |
| **Trigger**                 | - |
| **Main success scenario**   | 1. L'amministratore seleziona l'opzione per generare statistiche e report dalla dashboard.     <br>  2. Il sistema propone i filtri di aggregazione. <br>  3. L'amministratore seleziona i parametri per la generazione di dati privati ([FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)).  <br> 4. Il sistema genera e visualizza i grafici interattivi.     <br>  5. L'amministratore seleziona l'opzione per generare il file CSV. ([FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br>  6. Il sistema genera il file conforme allo standard e avvia il download ([NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con successo.    |
| **Extensions**              | 3a. Non autorizzato.   <br>  &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema nega l'accesso ai dati sensibili ([NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con fallimento. |

| Use Case                    |                                                                                                                                                                        |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-11-RipristinoPassword                                                                                                                                               |
| **Scope**                   | Sistema web Participium.                                                                                                                                               |
| **Level** | User goal.                                                                                                                                                             |
| **Intention in Context**    | Ripristinare la password smarrita.                                                                                                                                     |
| **Primary actor**           | Cittadino.                                                     |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces).                                                                                                 |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Recuperare l'accesso autonomamente.                                                              |
| **Precondition**            | L'account deve essere già stato verificato ([UC-05-Registrazione](#2-use-case-narratives)).                                                                            |
| **Minimum guarantees**      | Il token è temporaneo e monouso e se il ripristino fallisce la password rimane invariata.                                                                              |
| **Success guarantees**      | La password viene aggiornata con successo.                                                                                                                             |
| **Trigger**                 | -                                                                                                                                                                      |
| **Main success scenario**   | 1. L'utente clicca sul link "Hai dimenticato la password?" nella schermata di login.   <br> 2. L'utente inserisce la propria email nel campo richiesto.  <br>  3. Il sistema invia una email contenente un token di ripristino monouso ([IF-06](./02_RequirementsEngineering.md#3-interfaces)).  <br>  4. L'utente apre l'email e clicca sul link di ripristino.   <br>  5. Il sistema valida il token e mostra il modulo per la nuova password.  <br>  6. L'utente inserisce e conferma la nuova password nel form mostrato a sistema.  <br>  7. L'utente clicca sul tasto "Conferma Ripristino".  <br>  8. Il sistema valida la complessità della password, aggiorna il database e invalida il token ([FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br>  9. Il sistema reindirizza l'utente al login con un messaggio di successo; il caso d'uso termina con successo.                                                          |
| **Extensions**              | 2a. L'email non è associata a nessun account attivo.   <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa che l'email non è registrata; il caso d'uso termina con fallimento.        <br> 5a. Token invalido/scaduto.    <br>&nbsp;&nbsp;&nbsp;&nbsp;5a.1 Il sistema informa l'utente dell'impossibilità di procedere; il caso d'uso termina con fallimento.  <br> 8a. La password non rispetta i requisiti di sicurezza ([FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> &nbsp;&nbsp;&nbsp;&nbsp;8a.1 Il sistema segnala l'errore; il caso d'uso riprende dal punto 6.                                                                          |

| Use Case||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-12-VisualizzazioneProprieSegnalazioni|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Permettere al cittadino di consultare lo storico e lo stato attuale di tutte le segnalazioni da lui inviate.                                                     |
| **Primary actor**      | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03).                                                                  |
| **Supporting actors**       |-|
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Verificare l'avanzamento dei propri ticket e avere uno storico personale.                  |
| **Precondition**            | L'utente deve essere autenticato UC-01-Login.|
| **Minimum guarantees**      | Se non sono presenti segnalazioni, il sistema mostra un elenco vuoto senza errori.|
| **Success guarantees**      | L'utente visualizza l'elenco corretto delle proprie segnalazioni con i relativi stati aggiornati.|
| **Trigger**                 | -|
| **Main success scenario**   | 1. L'utente clicca sulla voce "Le mie segnalazioni" presente nel menu del profilo o nella barra laterale della dashboard. <br>  2. Il sistema interroga il database per recuperare i record associati all'ID utente.   <br> 3. Il sistema mostra una lista ordinata cronologicamente delle segnalazioni effettuate ([FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 4. Per ogni voce, il sistema mostra titolo, data e lo stato corrente dell'intervento.   <br>  5. L'utente clicca su una specifica riga per aprirne il dettaglio completo ([UC-13](#2-use-case-narratives)); il caso d'uso termina con successo.                |
| **Extensions**              | 1a. L'utente non ha segnalazioni.  <br>  &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra un messaggio "Non hai ancora effettuato segnalazioni"; il caso d'uso termina con successo.|

| Use Case||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**  | UC-13-VisualizzazioneDettaglioSegnalazione|
| **Scope**| Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Accedere alla scheda completa di una segnalazione per leggerne la descrizione, visualizzarne le foto e visualizzare lo storico degli aggiornamenti.|
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | [OpenStreetMap](./02_RequirementsEngineering.md#3-interfaces) (IF-03).|
| **Stakeholders' interests** | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas): Comprendere i dettagli di un problema specifico e seguire gli aggiornamenti di stato.||
| **Precondition**            | La segnalazione selezionata esiste ed è accessibile.|
| **Minimum guarantees**      | La visualizzazione non altera lo stato o i contenuti della segnalazione.|
| **Success guarantees**      | Il cittadino visualizza la pagina di dettaglio completa contenente i dati della segnalazione e le relative interazioni pubbliche.|
| **Trigger**                 | Il cittadino clicca su una specifica segnalazione dalla visualizzazione della mappa.|
| **Main success scenario**   | 1. Il sistema recupera i dati associati alla segnalazione selezionata (titolo, descrizione, categoria, posizione, foto allegate, stato corrente, storico degli aggiornamenti).  <br>  2. Il sistema mostra a schermo la pagina con tutte le informazioni raccolte ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo. |
| **Extensions**              | 1a. La segnalazione non è raggiungibile (poiché rimossa o a causa di un errore di sistema).   <br>  &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra un messaggio di errore e il caso d'uso termina con un fallimento.|

| Use Case                    ||
|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-14-VisualizzazioneStoricoAggiornamenti|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Verificare lo storico degli stati di una segnalazione per monitorare la gestione del problema nel tempo.                                   |
| **Primary actor**           | [Cittadino](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | -|
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Verificare lo stato della segnalazione e monitorarne i progressi nel tempo.   |
| **Precondition**            | L'utente deve aver selezionato una segnalazione.|
| **Minimum guarantees**      | Se il sistema non riesce a recuperare lo storico, l'utente visualizza comunque i dati correnti della segnalazione.|
| **Success guarantees**      | Il sistema mostra tutti i cambi di stato nel tempo.|
| **Trigger**                 | -|
| **Main success scenario**   | 1. L'utente accede alla pagina di dettaglio di una segnalazione.   <br>  2. Il sistema recupera dal database lo storico dei cambi di stato ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 3. Il sistema visualizza i passaggi di stato mostrandone le relative date; il caso d'uso termina con successo.|
| **Extensions**              | 2a. Lo storico è vuoto.    <br>  &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra i dati correnti della segnalazione e il caso d'uso termina con successo.                    |

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-15-FollowSegnalazione|
| **Scope**                   | Sistema web.|
| **Level** | User goal.|
| **Intention in Context**    | Seguire una segnalazione esistente per ricevere aggiornamenti sulla sua evoluzione.                                                                                               |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | [Servizio di Notifica (IF-07)](./02_RequirementsEngineering.md#3-interfaces).|
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Rimanere informato sugli sviluppi della risoluzione delle segnalazioni di interesse.|
| **Precondition**            | L'utente deve essere autenticato ([UC-01](#2-use-case-narratives)) e deve star vedendo i dettagli di una segnalazione.|
| **Success guarantees**      | Il sistema predispone l'invio di notifiche all'utente ad ogni cambio di stato della segnalazione seguita ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
| **Trigger**| -|
| **Main success scenario**   | 1. Il cittadino preme il pulsante "Segui". <br>  2. Il sistema associa l'identificativo utente alla segnalazione nel database.   <br> 3. Il sistema conferma visivamente l'attivazione del follow; il caso d'uso termina con successo.                                                                                  |
| **Extensions**              | 1a. L'utente segue già la segnalazione.   <br> &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra l'opzione "Smetti di seguire".                                                                                                     |

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-16-AnalisiAvanzataAmministratore|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Analizzare dati complessi per monitorare l'efficienza del servizio e prevenire abusi (es. top segnalanti).|
| **Primary actor**           | [Amministratore](./02_RequirementsEngineering.md#4-personas) (PER-08).|
| **Supporting actors**       | [Modulo Statistiche (S3.1)](./01_ProjectManagement.md).|
| **Stakeholders' interests** | [Amministratore](./02_RequirementsEngineering.md#1-stakeholders): Ottimizzare i flussi di lavoro e identificare criticità sistemiche. <br> [Comune di Torino](./02_RequirementsEngineering.md#1-stakeholders): Disporre di reportistica per la pianificazione urbana. |
| **Precondition**            | L'amministratore deve essere autenticato con permessi elevati.|
| **Success guarantees**      | Il sistema genera report e grafici basati su metriche private non accessibili al pubblico ([FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)).|
| **Trigger**|-|
| **Main success scenario**   | 1. L'amministratore accede all'area riservata della Dashboard.   <br>  2. Seleziona i parametri da considerare nell'analisi.   <br>  3. Il sistema elabora i dati tramite query.  <br>  4. Il sistema visualizza i grafici avanzati e le tabelle analitiche; il caso d'uso termina con successo.|
| **Extensions**              | 3a. L'elaborazione fallisce.  <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un messaggio di errore, il caso d'uso riprende dal punto 2.|

| Use Case||
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-17-AnalisiStatistichePubbliche|
| **Scope**                   | Sistema web Participium.|
| **Level** | User goal.|
| **Intention in Context**    | Consultare dati aggregati e trend generali per comprendere lo stato dei problemi urbani in città.|
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas).|
| **Supporting actors**       | [Portale pubblico (S8)](./01_ProjectManagement.md).|
| **Stakeholders' interests** | [Cittadino](./02_RequirementsEngineering.md#1-stakeholders): Avere una visione d'insieme dei disservizi più comuni nel proprio comune.                           |
| **Precondition**            | Il portale deve essere online e accessibile.|
| **Success guarantees**      | L'utente visualizza grafici anonimi e aggiornati, basati su categorie e trend temporali ([FR-17](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
| **Trigger**                 | -                                                                                                                                                                |
| **Main success scenario**   | 1. L'utente accede alla sezione "Statistiche" del portale pubblico.   <br>  2. Il sistema mostra le statistiche pubbliche.    <br>  3. L'utente filtra i dati per periodo (giorno, settimana, mese).  <br>  4. Il sistema aggiorna dinamicamente le visualizzazioni; il caso d'uso termina con successo.                                                                     |
| **Extensions**              | 3a. Il filtro selezionato non restituisce dati.    <br>  &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un messaggio informativo, il caso d'uso riprende dal punto 2.                                                     |

| Use Case                    ||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-18-RicercaSegnalazioni|
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
| **Main success scenario**   | 1. L'utente scrive del testo nella barra di ricerca delle segnalazioni. <br> 2. Il sistema cerca le segnalazioni corrispondenti al testo inserito. <br> 3. Il sistema aggiorna la visualizzazione mostrando solo le segnalazioni corrispondenti; il caso d'uso termina con successo.|
| **Extensions**              | 2a. Nessuna segnalazione soddisfa i criteri inseriti dall'utente. <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra un risultato vuoto e il caso d'uso termina.|

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      |UC-19-FiltraggioSegnalazioni|
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
| **Main success scenario**   | 1. L'utente seleziona uno o più filtri di ricerca nell'interfaccia. <br> 2. Il sistema cerca le segnalazioni corrispondenti ai criteri impostati dall'utente (filtri applicati e parole inserite nella barra di ricerca) nel database ([FR-09](./02_RequirementsEngineering.md#6-functional-requirements-fr)). <br> 3. Il sistema aggiorna la visualizzazione mostrando solo i risultati filtrati. Il caso d'uso termina con successo.|
| **Extensions**              | 2a. Nessuna segnalazione soddisfa i criteri inseriti dall'utente. <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema mostra un risultato vuoto e il caso d'uso termina.|


| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-20-Notifiche|
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
| **Main success scenario**|1. Il sistema individua gli utenti che seguono la segnalazione. <br>2. Il sistema invia una notifica in piattaforma a tutti gli utenti interessati comunicando il cambio di stato appena registrato. <br>3. Se l'utente ha attivato la ricezione di notifiche via email, il sistema invia una mail con le stesse informazioni. Il caso d'uso termina con successo.|
| **Extensions**|3a Il servizio di notifica non è disponibile. <br> 3a.1 Il caso d'uso termina con errore.|

| Use Case||
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**| UC-21-ApprovazioneSegnalazione|
| **Scope**| Sistema web Participium.|
| **Level**|User goal.|
| **Intention in Context**|Approvare una segnalazione effettuata da un cittadino.|
| **Primary actor**           | Operatore Comunale.|
| **Supporting actors**||
| **Stakeholders' interests** | Cittadino: . |
| **Precondition**|Un cittadino ha effettuato una segnalazione.|
| **Minimum guarantees**|-|
| **Success guarantees**|La segnalazione viene approvata e lo stato viene aggiornato in 'Assigned'|
| **Trigger**|-|
| **Main success scenario**|1. L'operatore comunale chiede di approvare una segbalazione. <br> 2. l'operatore accede ai dettagli della segnalazione. <br> 3. L'operatore conferma l'approvazione. <br> 4. Il sistema aggiorna lo stato della segnalazione da 'Pending' a 'Assigned'. Il caso d'uso termina con successo.|
| **Extensions**|3.a L'operatore rifiuta la segnalazione. fornendone una motivazione valida. <br> &nbsp;&nbsp;&nbsp;&nbsp; 3.a.1 Il sistema aggiorna lo stato della segnalazione da 'Pending' a 'Rejected'; il caso d'uso termina con errore.|



# Traceability Table

| UC ID | REQ ID|
|:------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC-01 | [FR-5](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-02 | [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.2](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-04](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)                                                                 |
| UC-03 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                               |
| UC-04 | [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr) |
| UC-05 | [FR-3](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                       |
| UC-06 | [FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-7.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-07 | [FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                       |
| UC-08 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                               |
| UC-9 | [FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                 |
| UC-10 | [FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr), [NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)                                                                                                                                     |
| UC-11 | [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                     |
| UC-12 | [FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                     |
| UC-13 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-14 | [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-15 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-16 | [FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-17 | [FR-17](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                                                                                      |
| UC-18 | [FR-09](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
 UC-19 | [FR-09.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-09.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
| UC-20 | [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
| UC-21 | [FR-14](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)|
