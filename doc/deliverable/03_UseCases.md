# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- `![](../data/img/use-case-diagram.png)`

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.
  
| Use Case                |                             |
|:------------------------|:----------------------------|
| ID                      |UC-02-Login                |
| Scope                   |Sistema web Participium                             |
| Level                   |User goal                             |
| Intention in Context    |Accedere al sistema per usufruire delle funzionalità riservate agli utenti registrati                             |
| Primary actor           |Utente registrato                              |
| Supporting actors       |                             |
| Stakeholders' interests |Comune di Torino:garantire che solo gli utenti verificati e autorizzati possono interagire con le segnalazioni o accedere ai dati amministrativi. Utente:accedere in sicurezza al proprio profilo e operare sulla piattaforma                             |
| Precondition            |L'utente deve aver completato la regstrazione e, nel caso dei cittadini, aver confermato l'indirizzo email tramite link di verifica                             |
| Minimum guarantees      |Se l'autenticazione fallisce,l'utete non ottiene alcun privilegio di accesso e lo stato del sistema rimane invariato                             |
| Success guarantees      |L'utente è autenticato e viene reindirizzato all'interno della piattaforma con i permessi corrispondenti al proprio ruolo                             |
| Trigger                 |L'utente richiedere di accedere al sistema cliccando sul pulsante login                              |
| Main success scenario   |1. L'utente chiede di loggarsi a Participium 2. Il sistema mostra la pagina di login 3. L'utente inserisce le proprie credenziali e verifica che l'account sia attivo 4. Il sistema valida le credenziali e verifica che l'account sia attiva 5. Il sistema autentica l'utente e gli assegna i permessi corretti 6. Il caso d'uso termina con successo                        |
| Extensions              |3a. L'utente annulla l'operazione: 3a.1 Il sistema interrompe il processo di login e il caso d'uso termina con un fallimento 4a. Le credenziali inserite non sono corrette: 4a.1 Il sistema mostra un messaggio di errore e il caso d'uso riprende dal punto 2 4b. L'account del cittadino non ha l'email verificata: 4b.1 Il sistema avvisa l'utente della necessità di confermare l'indirizzo email e il caso d'uso riprende dal punto 2                              |

| Use Case                |                             |
|:------------------------|:----------------------------|
| ID                      |                             |
| Scope                   |                             |
| Level                   |                             |
| Intention in Context    |                             |
| Primary actor           |                             |
| Supporting actors       |                             |
| Stakeholders' interests |                             |
| Precondition            |                             |
| Minimum guarantees      |                             |
| Success guarantees      |                             |
| Trigger                 |                             |
| Main success scenario   |                             |
| Extensions              |                             |


# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-XX | FR-XX  |
