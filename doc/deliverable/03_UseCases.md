``# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

# 2) Use Case Narratives

| Use Case                    |                                                                                                                                                                                                               |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-01-Login                                                                                                                                                                                                   |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                       |
| **Level**                   | User goal                                                                                                                                                                                                     |
| **Intention in Context**    | Accedere al sistema per usufruire delle funzionalità riservate agli utenti registrati.                                                                                                                        |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                                                                                                |
| **Supporting actors**       | [Servizio di autenticazione (IF-10)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                                            |
| **Stakeholders' interests** | [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): garantire accessi autorizzati. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): accedere in sicurezza. |
| **Precondition**            | L'utente deve aver completato la registrazione ([UC-05-Registrazione](#2-use-case-narratives)).                                                                                                               |
| **Minimum guarantees**      | Se l'autenticazione fallisce, l'utente non ottiene alcun privilegio di accesso.                                                                                                                               |
| **Success guarantees**      | L'utente è autenticato con i permessi corrispondenti al proprio ruolo.                                                                                                                                        |
| **Trigger**                 | -                                                                                                                                                                                                             |
| **Main success scenario**   | 1. L'utente clicca sul pulsante "Accedi" nella barra di navigazione superiore per richiedere l'accesso.                                                                                                       |
|                             | 2. Il sistema mostra la pagina di login.                                                                                                                                                                      |
|                             | 3. L'utente inserisce le proprie credenziali.                                                                                                                                                                 |
|                             | 4. Il sistema valida le credenziali e verifica l'account.                                                                                                                                                     |
|                             | 5. Il sistema autentica l'utente e assegna i permessi; il caso d'uso termina con successo.                                                                                                                    |
| **Extensions**              | 3a. L'utente annulla l'operazione: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema interrompe il processo; il caso d'uso termina con fallimento.                                                                 |
|                             | 3b. L'utente chiede di resettare la password: <br> &nbsp;&nbsp;&nbsp;&nbsp;3b.1 Il sistema avvia [UC-12-RipristinoPassword](#2-use-case-narratives); il caso d'uso termina con successo.                      |
|                             | 4a. Credenziali errate: <br> &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema mostra errore; il caso d'uso termina con fallimento dopo N tentativi.                                                                    |

---

| Use Case                    |                                                                                                                                                                                                         |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-02-InserimentoSegnalazione                                                                                                                                                                           |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                 |
| **Level**                   | User goal                                                                                                                                                                                               |
| **Intention in Context**    | Inviare una segnalazione geolocalizzata di un disservizio urbano al Comune di Torino.                                                                                                                   |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                                                                                          |
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces), [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces)                                                            |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Comunicare il problema. <br> [Comune di Torino (STK-04)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere dati accurati. |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                                                                                                               |
| **Minimum guarantees**      | Nessuna segnalazione viene creata se il processo viene interrotto.                                                                                                                                      |
| **Success guarantees**      | Viene creata una segnalazione "Pending Approval" e l'utente riceve conferma.                                                                                                                            |
| **Trigger**                 | -                                                                                                                                                                                                       |
| **Main success scenario**   | 1. Il cittadino clicca sul pulsante "+" o "Nuova Segnalazione" nella dashboard principale.                                                                                                              |
|                             | 2. Il sistema mostra la mappa ([IF-03](./02_RequirementsEngineering.md#3-interfaces)) e il modulo.                                                                                                      |
|                             | 3. Il cittadino seleziona la posizione sulla mappa.                                                                                                                                                     |
|                             | 4. Il sistema cattura le coordinate geografiche.                                                                                                                                                        |
|                             | 5. Il cittadino inserisce titolo, descrizione e categoria ([FR-13.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                    |
|                             | 6. Il cittadino carica da 1 a 3 foto ([NFR-04](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)).                                                                                     |
|                             | 7. Il cittadino seleziona opzionalmente l'anonimato pubblico ([FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                 |
|                             | 8. Il cittadino conferma l'invio cliccando sul tasto "Invia Segnalazione".                                                                                                                              |
|                             | 9. Il sistema valida i dati e carica i media ([IF-04](./02_RequirementsEngineering.md#3-interfaces)).                                                                                                   |
|                             | 10. Il sistema assegna lo stato "Pending Approval" e mostra successo; il caso d'uso termina con successo.                                                                                               |
| **Extensions**              | 2a. Mappa non disponibile: <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa l'utente; il caso d'uso termina con fallimento.                                                                          |
|                             | 6a. Più di 3 foto: <br> &nbsp;&nbsp;&nbsp;&nbsp;6a.1 Il sistema impedisce il caricamento; il caso d'uso termina con fallimento.                                                                         |
|                             | 9a. Dati mancanti: <br> &nbsp;&nbsp;&nbsp;&nbsp;9a.1 Il sistema evidenzia i campi; il caso d'uso termina con fallimento.                                                                                |

---

| Use Case                    |                                                                                                                                                                                                                                             |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-03-GestioneStatoSegnalazione                                                                                                                                                                                                             |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                                                     |
| **Level**                   | User goal                                                                                                                                                                                                                                   |
| **Intention in Context**    | Aggiornare lo stato di una segnalazione durante il processo di gestione comunale.                                                                                                                                                           |
| **Primary actor**           | [Operatore Comunale](./02_RequirementsEngineering.md#4-personas) (PER-05, PER-06)                                                                                                                                                           |
| **Supporting actors**       | [Servizio di notifica (IF-07)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                                                                                |
| **Stakeholders' interests** | [Operatore (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Tracciare avanzamento. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Ricevere aggiornamenti.                                             |
| **Precondition**            | L'operatore deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) e la segnalazione deve esistere.                                                                                                                                |
| **Minimum guarantees**      | Lo stato rimane invariato se l'aggiornamento fallisce.                                                                                                                                                                                      |
| **Success guarantees**      | Lo stato è aggiornato e vengono inviate le notifiche ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                                                               |
| **Trigger**                 | -                                                                                                                                                                                                                                           |
| **Main success scenario**   | 1. L'operatore seleziona una segnalazione dalla lista "In carico" nella dashboard amministrativa per visualizzarne i dettagli ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                      |
|                             | 2. L'operatore seleziona un nuovo stato dal menu a tendina "Stato Segnalazione".                                                                                                                                                            |
|                             | 3. L'operatore inserisce opzionalmente un commento interno nel campo di testo.                                                                                                                                                              |
|                             | 4. L'operatore clicca sul tasto "Aggiorna Stato".                                                                                                                                                                                           |
|                             | 5. Il sistema valida la transizione e aggiorna il database.                                                                                                                                                                                 |
|                             | 6. Il sistema invia notifiche al segnalante e follower ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.                                                                         |
| **Extensions**              | 2a. Operatore seleziona "Rejected": <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema obbliga la motivazione ([FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo (previa motivazione). |
|                             | 2b. Transizione non valida: <br> &nbsp;&nbsp;&nbsp;&nbsp;2b.1 Il sistema impedisce l'operazione; il caso d'uso termina con fallimento.                                                                                                      |

---

| Use Case                    |                                                                                                                                                                                                           |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-04-ConsultazioneMappaESegnalazioni                                                                                                                                                                     |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                   |
| **Level**                   | User goal                                                                                                                                                                                                 |
| **Intention in Context**    | Navigare sulla mappa, filtrare e visualizzare i dettagli delle segnalazioni pubblicate.                                                                                                                   |
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03, PER-04)                                                                                         |
| **Supporting actors**       | [OpenStreetMap (IF-03)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                                                     |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Informarsi sui problemi del quartiere.                                                                                              |
| **Precondition**            | Il sistema deve essere accessibile.                                                                                                                                                                       |
| **Minimum guarantees**      | Il sistema mostra i dati pubblici senza richiedere autenticazione.                                                                                                                                        |
| **Success guarantees**      | L'utente visualizza le segnalazioni filtrate correttamente.                                                                                                                                               |
| **Trigger**                 | -                                                                                                                                                                                                         |
| **Main success scenario**   | 1. L'utente accede alla homepage e clicca sul link "Esplora Mappa".                                                                                                                                       |
|                             | 2. Il sistema carica i pin geolocalizzati ([FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                                         |
|                             | 3. L'utente applica filtri (categoria, stato, tempo) tramite il pannello laterale.                                                                                                                        |
|                             | 4. Il sistema aggiorna la visualizzazione in tempo reale.                                                                                                                                                 |
|                             | 5. L'utente clicca su un pin specifico della segnalazione sulla mappa.                                                                                                                                    |
|                             | 6. Il sistema mostra un popup o una pagina con i dettagli completi ([FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.                           |
| **Extensions**              | 3a. Ricerca testuale: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema filtra per stringa ([FR-9](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.         |
|                             | 5a. Segnalazione anonima: <br> &nbsp;&nbsp;&nbsp;&nbsp;5a.1 Il sistema nasconde l'identità ([FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo. |

---

---

| Use Case                    |                                                                                                                                                        |
|:----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-05-Registrazione                                                                                                                                    |
| **Scope**                   | Sistema web Participium                                                                                                                                |
| **Level**                   | User goal                                                                                                                                              |
| **Intention in Context**    | Creare un nuovo account utente sulla piattaforma fornendo dati identificativi.                                                                         |
| **Primary actor**           | [Cittadino (visitatore)](./02_RequirementsEngineering.md#4-personas) (PER-04)                                                                          |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces)                                                                                  |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Ottenere l'accesso per effettuare segnalazioni.                                  |
| **Precondition**            | L'utente non deve essere già autenticato ([UC-07-Logout](#2-use-case-narratives)).                                                                     |
| **Minimum guarantees**      | I dati non vengono salvati se la validazione fallisce.                                                                                                 |
| **Success guarantees**      | Viene creato un account attivo dopo la verifica dell'email.                                                                                            |
| **Trigger**                 | -                                                                                                                                                      |
| **Main success scenario**   | 1. Il visitatore clicca sul pulsante "Registrati" nella home page o nella pagina di login.                                                             |
|                             | 2. Il sistema mostra il modulo di registrazione.                                                                                                       |
|                             | 3. Il visitatore inserisce nome, cognome, email e password.                                                                                            |
|                             | 4. Il visitatore spunta le caselle per l'accettazione di termini e privacy.                                                                            |
|                             | 5. L'utente spunta o meno il flag "Ricevi notifiche tramite email".                                                                                    |
|                             | 6. Il visitatore clicca sul tasto "Crea Account".                                                                                                      |
|                             | 7. Il sistema valida i dati (univocità email) ([FR-3](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                  |
|                             | 8. Il sistema crea l'account in stato "Pending" e invia una mail con link di verifica ([IF-06](./02_RequirementsEngineering.md#3-interfaces)).         |
|                             | 9. Il visitatore clicca sul link di verifica ricevuto nella propria casella email.                                                                     |
|                             | 10. Il sistema attiva l'account e mostra un messaggio di conferma; il caso d'uso termina con successo.                                                 |
| **Extensions**              | 7a. Email già presente: <br> &nbsp;&nbsp;&nbsp;&nbsp;7a.1 Il sistema segnala il conflitto; il caso d'uso termina con fallimento.                       |
|                             | 9a. Link di verifica scaduto: <br> &nbsp;&nbsp;&nbsp;&nbsp;9a.1 Il sistema permette di richiedere un nuovo invio; il caso d'uso termina con successo.  |

---

| Use Case                    |                                                                                                                                                                         |
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-06-GestioneProfilo                                                                                                                                                   |
| **Scope**                   | Sistema web Participium                                                                                                                                                 |
| **Level**                   | User goal                                                                                                                                                               |
| **Intention in Context**    | Aggiornare i dati personali, caricare una foto profilo e gestire le preferenze di notifica.                                                                             |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                                                          |
| **Supporting actors**       | [Media Storage (IF-04)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                   |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Personalizzare la propria esperienza e gestire la privacy.                                        |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                                                                               |
| **Minimum guarantees**      | Le modifiche non confermate non vengono salvate.                                                                                                                        |
| **Success guarantees**      | Il profilo e le preferenze vengono aggiornati correttamente.                                                                                                            |
| **Trigger**                 | -                                                                                                                                                                       |
| **Main success scenario**   | 1. L'utente clicca sulla propria icona profilo e seleziona "Impostazioni" o "Il mio profilo".                                                                           |
|                             | 2. Il sistema mostra i dati correnti, la foto profilo (se presente) e le impostazioni notifiche ([FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 3. L'utente carica o modifica la propria foto profilo ([IF-04](./02_RequirementsEngineering.md#3-interfaces)).                                                          |
|                             | 4. L'utente attiva/disattiva il flag "Ricevi notifiche tramite email".                                                                                                  |
|                             | 5. L'utente modifica eventuali campi anagrafici.                                                                                                                        |
|                             | 6. L'utente clicca sul pulsante "Salva Modifiche".                                                                                                                      |
|                             | 7. Il sistema valida i dati e aggiorna il database; il caso d'uso termina con successo.                                                                                 |
| **Extensions**              | 3a. Formato immagine non valido: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema avvisa l'utente sui formati ammessi; il caso d'uso termina con fallimento.                |
|                             | 7a. Errore di connessione al database: <br> &nbsp;&nbsp;&nbsp;&nbsp;7a.1 Il sistema mostra un messaggio di errore tecnico; il caso d'uso termina con fallimento.        |

| Use Case                    |                                                                                                                                           |
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-07-Logout                                                                                                                              |
| **Scope**                   | Sistema web Participium                                                                                                                   |
| **Level**                   | User goal                                                                                                                                 |
| **Intention in Context**    | Terminare la sessione in sicurezza.                                                                                                       |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                            |
| **Supporting actors**       | [Servizio di autenticazione (IF-10)](./02_RequirementsEngineering.md#3-interfaces)                                                        |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Proteggere l'account su dispositivi condivisi.                      |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                                                 |
| **Minimum guarantees**      | Nessuna.                                                                                                                                  |
| **Success guarantees**      | La sessione viene invalidata e l'accesso protetto revocato.                                                                               |
| **Trigger**                 | -                                                                                                                                         |
| **Main success scenario**   | 1. L'utente clicca sul pulsante "Esci" o "Logout" presente nel menu a tendina del profilo.                                                |
|                             | 2. Il sistema invalida la sessione lato server ([FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                    |
|                             | 3. Il sistema reindirizza l'utente alla home page pubblica; il caso d'uso termina con successo.                                           |
| **Extensions**              | 2a. Errore invalidazione: <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema forza la chiusura lato client; il caso d'uso termina con successo. |

---

| Use Case                    |                                                                                                                                                                                                   |
|:----------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-08-MessaggioOperatoreCittadino                                                                                                                                                                 |
| **Scope**                   | Sistema web Participium                                                                                                                                                                           |
| **Level**                   | User goal                                                                                                                                                                                         |
| **Intention in Context**    | Scambio di messaggi diretti tra operatore e cittadino su una segnalazione.                                                                                                                        |
| **Primary actor**           | [Operatore Comunale](./02_RequirementsEngineering.md#4-personas) (PER-05, PER-06)                                                                                                                 |
| **Supporting actors**       | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                                                                                    |
| **Stakeholders' interests** | [Operatore (STK-02)](./02_RequirementsEngineering.md#1-stakeholders): Richiedere chiarimenti. <br> [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Facilitare l'intervento. |
| **Precondition**            | Entrambi gli attori devono essere autenticati ([UC-01-Login](#2-use-case-narratives)) e legati alla segnalazione specifica.                                                                       |
| **Minimum guarantees**      | I messaggi sono privati e legati solo al ticket di riferimento.                                                                                                                                   |
| **Success guarantees**      | Il messaggio viene recapitato e notificato al destinatario.                                                                                                                                       |
| **Trigger**                 | -                                                                                                                                                                                                 |
| **Main success scenario**   | 1. L'utente (operatore o cittadino) clicca sulla scheda "Messaggi" all'interno del dettaglio di una segnalazione.                                                                                 |
|                             | 2. Il sistema mostra la cronologia dei messaggi scambiati ([FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                |
|                             | 3. L'utente scrive un nuovo testo nel campo di input e preme l'icona "Invia".                                                                                                                     |
|                             | 4. Il sistema salva il messaggio associandolo univocamente alla segnalazione.                                                                                                                     |
|                             | 5. Il sistema invia una notifica push o email al destinatario ([FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)); il caso d'uso termina con successo.                        |
| **Extensions**              | 3a. Messaggio vuoto: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema impedisce l'invio; il caso d'uso termina con fallimento.                                                                        |

---

| Use Case                    |                                                                                                                                               |
|:----------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-09-ConsultazioneLog                                                                                                                        |
| **Scope**                   | Sistema web Participium                                                                                                                       |
| **Level**                   | User goal                                                                                                                                     |
| **Intention in Context**    | Monitorare log tecnici e sicurezza.                                                                                                           |
| **Primary actor**           | [Amministratore](./02_RequirementsEngineering.md#4-personas) (PER-07)                                                                         |
| **Supporting actors**       | [Sistema di monitoraggio e logging (IF-08)](./02_RequirementsEngineering.md#3-interfaces)                                                     |
| **Stakeholders' interests** | [Amministratore (STK-03)](./02_RequirementsEngineering.md#1-stakeholders): Diagnosticare bug e monitorare intrusioni.                         |
| **Precondition**            | L'amministratore deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Admin.                                                  |
| **Minimum guarantees**      | I log sono in sola lettura e non modificabili.                                                                                                |
| **Success guarantees**      | L'amministratore visualizza le voci di log filtrate correttamente.                                                                            |
| **Trigger**                 | -                                                                                                                                             |
| **Main success scenario**   | 1. L'amministratore clicca sulla voce "Log di Sistema" nel menu laterale della dashboard amministrativa (**IF-02**).                          |
|                             | 2. Il sistema presenta l'elenco cronologico dei log persistenti ([FR-4](./02_RequirementsEngineering.md#6-functional-requirements-fr)).       |
|                             | 3. L'amministratore imposta i filtri di ricerca (livello errore, data, utente).                                                               |
|                             | 4. Il sistema aggiorna la tabella mostrando solo i log filtrati; il caso d'uso termina con successo.                                          |
| **Extensions**              | 3a. Nessun risultato: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema mostra un avviso "Nessun log trovato"; il caso d'uso termina con successo. |

---

| Use Case                    |                                                                                                                                                                                                                               |
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-10-CreazioneAccountAmministratore                                                                                                                                                                                          |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                                       |
| **Level**                   | User goal                                                                                                                                                                                                                     |
| **Intention in Context**    | Creare account per amministratori o operatori.                                                                                                                                                                                |
| **Primary actor**           | [Amministratore](./02_RequirementsEngineering.md#4-personas) (PER-07)                                                                                                                                                         |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                                                                         |
| **Stakeholders' interests** | [Amministratore (STK-03)](./02_RequirementsEngineering.md#1-stakeholders): Gestire il team tecnico e operativo.                                                                                                               |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Amministratore.                                                                                                                                 |
| **Minimum guarantees**      | Non vengono creati account duplicati.                                                                                                                                                                                         |
| **Success guarantees**      | Viene creato il nuovo account e inviata la mail di benvenuto.                                                                                                                                                                 |
| **Trigger**                 | -                                                                                                                                                                                                                             |
| **Main success scenario**   | 1. L'amministratore clicca sul pulsante "Aggiungi Nuovo Utente" nella sezione Gestione Staff della dashboard (**IF-02**).                                                                                                     |
|                             | 2. L'amministratore inserisce nome, email e ruolo del nuovo collaboratore.                                                                                                                                                    |
|                             | 3. L'amministratore seleziona i permessi specifici (Amministratore o Operatore) ([FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)). |
|                             | 4. Il sistema valida i dati e crea l'utenza nel database.                                                                                                                                                                     |
|                             | 5. Il sistema invia automaticamente le credenziali temporanee via mail ([IF-06](./02_RequirementsEngineering.md#3-interfaces)); il caso d'uso termina con successo.                                                           |
| **Extensions**              | 4a. Email già registrata: <br> &nbsp;&nbsp;&nbsp;&nbsp;4a.1 Il sistema nega la creazione mostrando errore; il caso d'uso termina con fallimento.                                                                              |

---

| Use Case                    |                                                                                                                                                                                                                         |
|:----------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-11-GenerazioneReport                                                                                                                                                                                                 |
| **Scope**                   | Sistema web Participium                                                                                                                                                                                                 |
| **Level**                   | User goal                                                                                                                                                                                                               |
| **Intention in Context**    | Estrarre dati statistici avanzati.                                                                                                                                                                                      |
| **Primary actor**           | [Amministratore (data analyst)](./02_RequirementsEngineering.md#4-personas) (PER-08)                                                                                                                                    |
| **Supporting actors**       | [Cloud Account (IF-09)](./02_RequirementsEngineering.md#3-interfaces)                                                                                                                                                   |
| **Stakeholders' interests** | [Analista (STK-06)](./02_RequirementsEngineering.md#1-stakeholders): Ottimizzare i servizi comunali.                                                                                                                    |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)) come Amministratore/Analista.                                                                                                                  |
| **Minimum guarantees**      | I dati privati rimangono riservati agli amministratori.                                                                                                                                                                 |
| **Success guarantees**      | Il report viene generato ed esportato in formato conforme.                                                                                                                                                              |
| **Trigger**                 | -                                                                                                                                                                                                                       |
| **Main success scenario**   | 1. L'amministratore clicca sulla voce "Statistiche e Report" nel menu principale della dashboard.                                                                                                                       |
|                             | 2. Il sistema propone i filtri di aggregazione (per categoria, per operatore, ecc.).                                                                                                                                    |
|                             | 3. L'amministratore seleziona i parametri per la generazione di dati privati ([FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                   |
|                             | 4. Il sistema genera e visualizza i grafici interattivi.                                                                                                                                                                |
|                             | 5. L'amministratore clicca sul tasto "Esporta CSV" ([FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                                                                             |
|                             | 6. Il sistema genera il file conforme allo standard e avvia il download ([NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con successo.                              |
| **Extensions**              | 3a. Non autorizzato: <br> &nbsp;&nbsp;&nbsp;&nbsp;3a.1 Il sistema nega l'accesso ai dati sensibili ([NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)); il caso d'uso termina con fallimento. |

---

| Use Case                    |                                                                                                                                                                  |
|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-12-RipristinoPassword                                                                                                                                         |
| **Scope**                   | Sistema web Participium                                                                                                                                          |
| **Level**                   | User Goal                                                                                                                                                        |
| **Intention in Context**    | Ripristinare la password smarrita.                                                                                                                               |
| **Primary actor**           | [Cittadino (visitatore/autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03, PER-04)                                                |
| **Supporting actors**       | [Servizio mail (IF-06)](./02_RequirementsEngineering.md#3-interfaces)                                                                                            |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Recuperare l'accesso autonomamente.                                                        |
| **Precondition**            | L'account deve essere già stato verificato ([UC-05-Registrazione](#2-use-case-narratives)).                                                                      |
| **Minimum guarantees**      | Il token è temporaneo e monouso.                                                                                                                                 |
| **Success guarantees**      | La password viene aggiornata con successo.                                                                                                                       |
| **Trigger**                 | -                                                                                                                                                                |
| **Main success scenario**   | 1. L'utente clicca sul link "Hai dimenticato la password?" nella schermata di login.                                                                             |
|                             | 2. L'utente inserisce la propria email nel campo richiesto.                                                                                                      |
|                             | 3. Il sistema invia una email contenente un token di ripristino monouso ([IF-06](./02_RequirementsEngineering.md#3-interfaces)).                                 |
|                             | 4. L'utente apre l'email e clicca sul link di ripristino.                                                                                                        |
|                             | 5. Il sistema valida il token e mostra il modulo per la nuova password.                                                                                          |
|                             | 6. L'utente inserisce e conferma la nuova password.                                                                                                              |
|                             | 7. L'utente clicca sul tasto "Conferma Ripristino".                                                                                                              |
|                             | 8. Il sistema aggiorna il database e invalida il token ([FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)).                                 |
|                             | 9. Il sistema reindirizza l'utente al login con un messaggio di successo; il caso d'uso termina con successo.                                                    |
| **Extensions**              | 2a. Email non trovata: <br> &nbsp;&nbsp;&nbsp;&nbsp;2a.1 Il sistema avvisa che l'email non è registrata; il caso d'uso termina con fallimento.                   |
|                             | 5a. Token invalido/scaduto: <br> &nbsp;&nbsp;&nbsp;&nbsp;5a.1 Il sistema informa l'utente dell'impossibilità di procedere; il caso d'uso termina con fallimento. |

---

| Use Case                    |                                                                                                                                                                                  |
|:----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ID**                      | UC-13-VisualizzazioneProprieSegnalazioni                                                                                                                                         |
| **Scope**                   | Sistema web Participium                                                                                                                                                          |
| **Level**                   | User goal                                                                                                                                                                        |
| **Intention in Context**    | Permettere al cittadino di consultare lo storico e lo stato attuale di tutte le segnalazioni da lui inviate.                                                                     |
| **Primary actor**           | [Cittadino (autenticato)](./02_RequirementsEngineering.md#4-personas) (PER-01, PER-02, PER-03)                                                                                   |
| **Supporting actors**       | -                                                                                                                                                                                |
| **Stakeholders' interests** | [Cittadino (STK-01)](./02_RequirementsEngineering.md#1-stakeholders): Verificare l'avanzamento dei propri ticket e avere uno storico personale.                                  |
| **Precondition**            | L'utente deve essere autenticato ([UC-01-Login](#2-use-case-narratives)).                                                                                                        |
| **Minimum guarantees**      | Se non sono presenti segnalazioni, il sistema mostra un elenco vuoto senza errori.                                                                                               |
| **Success guarantees**      | L'utente visualizza l'elenco corretto delle proprie segnalazioni con i relativi stati aggiornati.                                                                                |
| **Trigger**                 | -                                                                                                                                                                                |
| **Main success scenario**   | 1. L'utente clicca sulla voce "Le mie segnalazioni" presente nel menu del profilo o nella barra laterale della dashboard.                                                        |
|                             | 2. Il sistema interroga il database per recuperare i record associati all'ID utente.                                                                                             |
|                             | 3. Il sistema mostra una lista ordinata cronologicamente delle segnalazioni effettuate. ([FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr))                 |
|                             | 4. Per ogni voce, il sistema mostra titolo, data e lo stato corrente dell'intervento.                                                                                            |
|                             | 5. L'utente clicca su una specifica riga per aprirne il dettaglio completo ([UC-04](#2-use-case-narratives)); il caso d'uso termina con successo.                                |
| **Extensions**              | 1a. L'utente non ha segnalazioni: <br> &nbsp;&nbsp;&nbsp;&nbsp;1a.1 Il sistema mostra un messaggio "Non hai ancora effettuato segnalazioni"; il caso d'uso termina con successo. |

# Traceability Table

| UC ID | REQ ID                                                                                                                                                                                                                                                                                                                                                                     |
|:------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC-01 | [FR-5](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                               |
| UC-02 | [FR-13](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-13.2](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-04](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr) |
| UC-03 | [FR-14](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-14.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                      |
| UC-04 | [FR-8](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-8.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9.1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-10](./02_RequirementsEngineering.md#6-functional-requirements-fr)          |
| UC-05 | [FR-3](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                       |
| UC-06 | [FR-7](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-7.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                               |
| UC-07 | [FR-6](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                       |
| UC-08 | [FR-16](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-15](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                               |
| UC-09 | [FR-4](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-9.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                               |
| UC-10 | [FR-1](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                 |
| UC-11 | [FR-18](./02_RequirementsEngineering.md#6-functional-requirements-fr), [FR-11](./02_RequirementsEngineering.md#6-functional-requirements-fr), [NFR-05](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr), [NFR-06](./02_RequirementsEngineering.md#7-non-functional-requirements-nfr)                                                                     |
| UC-12 | [FR-5.1](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                     |
| UC-13 | [FR-7.2](./02_RequirementsEngineering.md#6-functional-requirements-fr)                                                                                                                                                                                                                                                                                                     |