## 1 `ReportService.create_report`

### Control Flow Graph

- ![](../../data/img/06_WhiteBoxCreateReport.png)

### Atomic Conditions
- C1: category_id is not None 
- C2: resolved_category_id
- C3: not category
- C4: not category.is_active
- C5: not title 
- C6: not description
- C7: latitude is None
- C8: longitude is None
- C9: for photo (esistono ancora photo in photos)
- C10: photo
- C11: photo.filename
- C12: not valid_photos
- C13: len(valid_photos) > 3
- C14: for photo (esistono ancora photo in valid_photos)

### Structural Lower Bound
La funzione create_report produce 8 esiti mutualmente esclusivi, 7 corrispondenti ad eccezioni di tipo ValidationError e 1 return finale di successo. Ogni esecuzione del test restituisce uno di questi esiti, quindi lo structural lower bound è 8.

***Lista mock***
- CATEGORY_REPOSITORY_ACTIVE: configura il metodo get_by_id affinchè torni un'istanza della classe Category con id=1 e is_active=True
- CATEGORY_REPOSITORY_INACTIVE: configura il metodo get_by_id affinchè torni un'istanza della classe Category con id=1 e is_active=False
- CATEGORY_REPOSITORY_NOT_FOUND: configura il metodo get_by_id affinchè torni None
- REPORT_REPOSITORY_ADD_SUCCESS: configura il metodo add come una no-op (operazione nulla) che simula il successo
- DATABASE_SESSION_FLUSH_MOCK: configura il metodo flush per completarsi senza eseguire operazioni reali sul database
- STORAGE_SERVICE_SAVE_SUCCESS: il metodo viene configurato per restituire una stringa "/img/photo.jpg"
- REPORT_REPOSITORY_ADD_PHOTO_SUCCESS: configura il metodo add_photo(photo) come una no-op (operazione nulla)
- REPORT_REPOSITORY_ADD_STATUS_SUCCESS: configura il metodo add_status_entry come una no-op
- DATABASE_SESSION_COMMIT_MOCK: configura il metodo commit() come una no-op (operazione nulla)
- REPORT_GET_SUCCESS: configura il metodo get_report(report_id) affinché restituisca l'istanza dell'oggetto Report creata durante l'esecuzione della funzione.

### Node Coverage
Nota: per p si intende una foto con fileName invece per p_no_fn una foto senza fileName
| ID   | `reporter` |`category_id`| `title`| `description` | `latitude` | `longitude` | `photos`| `is_anonymous` | Mock |Outcome atteso |
|------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------| ---------------|------------------------------|
|CRN-01| reporter1(id=1) | "uno" | "Buca profonda" | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True | - |ValidationError("A valid active category is required.") |
|CRN-02| reporter1(id=1) | None | "Buca profonda" | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p]| True | - |ValidationError ("A valid active category is required.") |
|CRN-03| reporter1(id=1) | 1 |  None  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True |  CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Title and description are required.") |
|CRN-04| reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | None | 9.1900 | [p,p] (con filename presente)| True | CATEGORY_REPOSITORY_ACTIVE |  ValidationError ("Latitude and longitude are required.") |
|CRN-05| reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | "Quaranta" | 9.1900 | [p,p] (con filename presente)| True |  CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Latitude and longitude must be valid numbers.") |
|CRN-06| reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [] | True | CATEGORY_REPOSITORY_ACTIVE |  ValidationError ("At least one photo is required.") |
|CRN-07| reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p, None, p_no_fn, p, p, p] | True | CATEGORY_REPOSITORY_ACTIVE | ValidationError ("A report can contain at most 3 photos.") |
|CRN-08| reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True | CATEGORY_REPOSITORY_ACTIVE, REPORT_REPOSITORY_ADD_SUCCESS, DATABASE_SESSION_FLUSH_MOCK, STORAGE_SERVICE_SAVE_SUCCESS, REPORT_REPOSITORY_ADD_PHOTO_SUCCESS, REPORT_REPOSITORY_ADD_STATUS_SUCCESS, DATABASE_SESSION_COMMIT_MOCK, REPORT_GET_SUCCESS     | Report |

### Edge Coverage
Stessi 8 test della Node coverage.

### Condition Coverage
| Test |  `reporter` | `category_id` | `title` | `description` | `latitude` | `longitude` | `photos` | `is_anonymous` | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 |C14 | Mock |Outcome atteso |
| :--- |  :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:| :---:| :---: | :---: | :---: | :---: | :---: |:--- |
| CRC-01 | reporter1(id=1) | "uno" | "Buca profonda" | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True | T | - | - | - | - | - | - | - | - | - | - |- | - | - | - | ValidationError("A valid active category is required.") |
| CRC-02 | reporter1(id=1) | None | "Buca profonda" | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True | F | F | T | -(SC) | - | - | - | - | - | - | - | - | - |- | - | ValidationError("A valid active category is required.") |
| CRC-03 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p] | True | T | T | F | T | - | - | - | - | - | - | - | - |- | - |   CATEGORY_REPOSITORY_INACTIVE | ValidationError ("A valid active category is required.") |
| CRC-04 | reporter1(id=1) | 1 |  None  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p]| True | T | T | F | F | T | -(SC) | - | - | - | - | - | - |- | - |   CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Title and description are required.") |
| CRC-05 | reporter1(id=1) | 1 |  "Buca profonda"  | None | 45.4642 | 9.1900 | [p,p]| True | T | T | F | F | F | T | - | - | - | - | - | - |- | - |   CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Title and description are required.") |
| CRC-06 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | None | 9.1900 | [p,p]| True | T | T | F | F | F | F | T | -(SC) | - | - | - |- | - | - |   CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Latitude and longitude are required.") |
| CRC-07 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | None | [p,p] | True | T | T | F | F | F | F | F | T | - | - | - | - |- | - |   CATEGORY_REPOSITORY_ACTIVE | ValidationError ("Latitude and longitude are required.") |
| CRC-08 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [] | True | T | T | F | F | F | F | F | F | F | - | - | T |- | - | CATEGORY_REPOSITORY_ACTIVE | ValidationError ("At least one photo is required.") |
| CRC-09 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p, None, p_no_fn, p, p, p]  | True | T | T | F | F | F | F | F | F | T/F | T/F | T/F | F | T |- |  CATEGORY_REPOSITORY_ACTIVE | ValidationError ("A report can contain at most 3 photos.") |
| CRC-10 | reporter1(id=1) | 1 |  "Buca profonda"  | "Si segnala una buca di ampie dimensioni" | 45.4642 | 9.1900 | [p,p]  | True | T | T | F | F | F | F | F | F | T/F | T | T | F | F |T/F |  CATEGORY_REPOSITORY_ACTIVE, REPORT_REPOSITORY_ADD_SUCCESS, DATABASE_SESSION_FLUSH_MOCK, STORAGE_SERVICE_SAVE_SUCCESS, REPORT_REPOSITORY_ADD_PHOTO_SUCCESS, REPORT_REPOSITORY_ADD_STATUS_SUCCESS, DATABASE_SESSION_COMMIT_MOCK, REPORT_GET_SUCCESS  | Report |


nota: le condizioni dei cicli for (C9 e C14) sono indicate come T/F poiché il flusso esegue il corpo del ciclo (True) e prosegue verso l'istruzione successiva solo dopo che la lista è stata interamente scorsa (False). In assenza di interruzioni forzate (break o return), il test esercita necessariamente entrambi i rami della condizione di uscita

nota: CRC-09 usa una lista eterogenea per coprire tutte le condizioni atomiche (C10 e C11) in un solo ciclo. Anche in questo caso è valido lo short-circuit: se la foto manca (C10=F), il sistema non controlla il nome del file (C11)

### Loop Coverage

### Path Coverage

### Minimal Suite Test

## 2 `MessagingService._resolve_recipient`

### Control Flow Graph

- ![](../../data/img/resolve_recipient-CFG.png)

### Atomic Conditions
- C1: `sender.role == Role.ADMIN`
- C2: `sender.role == Role.OPERATOR`
- C3: `message.sender is not None`
- C4: `message.sender.role == Role.ADMIN`
- C5: `message.sender.role == Role.OPERATOR`
- C6: `status_event.changed_by is not None`
- C7: `status_event.changed_by.role == Role.ADMIN`
- C8: `status_event.changed_by.role == Role.OPERATOR`

### Structural Lower Bound
Il metodo ha 4 punti di uscita mutualmente esclusivi (3 return di un oggetto User e un return None). Per coprire tutti i rami dei cicli e le condizioni atomiche, sono necessari almeno 4 test case, e quindi lo questo corrisponde allo structural lower bound.

### Node Coverage
| ID | `sender.role` | `reversed(messages)` | `reversed(report.status_history)` | Risultato atteso |
|---|---|---|---|---|
| RR-N1 | ADMIN | - | - | report.reporter |
| RR-N2 | CITIZEN | [Msg(ADMIN)] | - | Msg.sender |
| RR-N3 | CITIZEN | [Msg(CITIZEN)] | [Status(OPERATOR)] | Status.changed_by |
| RR-N4 | CITIZEN | [] | [] | None |

### Edge Coverage
Coperta dagli stessi test della Node Coverage.

### Condition Coverage
| ID | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Risultato atteso |
|---|---|---|---|---|---|---|---|---|---|
| RR-C1 | T | - | - | - | - | - | - | - | report.reporter |
| RR-C2 | F | T | - | - | - | - | - | - | report.reporter |
| RR-C3 | F | F | T | T | - | - | - | - | message.sender |
| RR-C4 | F | F | T | F | T | - | - | - | message.sender |
| RR-C5 | F | F | F | - | - | T | T | - | status_event.changed_by |
| RR-C6 | F | F | T | F | F | T | F | T | status_event.changed_by |
| RR-C7 | F | F | F | - | - | F | - | - | None |

### Loop Coverage
- loop su `messages`
    - 0 iterazioni: `messages` vuoto (RR-L1)
    - 1 iterazione: `messages` con un elemento (RR-L2)
    - 2+ iterazioni: `messages` con due o più elementi, ricerca continua oltre il primo (RR-L3)
- lop su `report.status_history`
    - 0 iterazioni: `status_history` vuoto (RR-L4)
    - 1 iterazione: `status_history` con un elemento (RR-L5)
    - 2+ iterazioni: `status_history` con due o più elementi, ricerca continua oltre il primo (RR-L6)

| ID | `messages` (roles) | `status_history` (roles) | Risultato atteso |
|---|---|---|---|
| RR-L1 | [] | [ADMIN] | status_history[0].changed_by |
| RR-L2 | [ADMIN] | [] | messages[0].sender |
| RR-L3 | [ADMIN, CITIZEN] | [] | messages[0].sender |
| RR-L4 | [CITIZEN] | [] | None |
| RR-L5 | [CITIZEN] | [OPERATOR] | status_history[0].changed_by |
| RR-L6 | [CITIZEN] | [OPERATOR, CITIZEN] | status_history[0].changed_by |

### Path Coverage
Coperto dai test sopra.

### Minimal Suite Test
1. **RR-01**: `sender` è ADMIN. Verifica il ritorno del reporter.
2. **RR-02**: `sender` è CITIZEN, `messages` contiene un OPERATOR. Verifica la risoluzione tramite messaggi.
3. **RR-03**: `sender` è CITIZEN, `messages` vuoto (o senza OP), `status_history` contiene un ADMIN. Verifica la risoluzione tramite cronologia stati.
4. **RR-04**: `sender` è CITIZEN, liste vuote. Verifica il ritorno `None`.
5. **RR-05**: Gestisce i casi con mittenti o autori di stato `None` (C3/C6 = False).

## 3 `NotificationService.notify_status_change`

### Control Flow Graph

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test


## 4 `NotificationService.count_unread_message_notifications_by_report`

### Control Flow Graph

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test


## 5 `UserService.update_user`

### Control Flow Graph

- ![](../data/img/xxx.xxx)

### Atomic Conditions
- C1: username is not None
- C2: username != user.username
- C3: user_repository.get_by_username(username) returns a user
- C4: email is not None
- C5: email != user.email
- C6: user_repository.get_by_email(email) returns a user
- C7: payload.get(field) is not None (nel ciclo for)
- C8: isinstance(value, str) (nel ciclo for)
- C9: payload.get("role") is not None
- C10: "category_id" in payload
- C11: category is not None (risultato di _resolve_operator_category)
- C12: payload.get("is_active") is not None
- C13: payload.get("email_notifications_enabled") is not None
### Structural Lower Bound
La funzione update_user produce tre esiti mutualmente esclusivi. Due di
questi sono eccezioni di tipo ValidationError. Il terzo esito corrisponde al completamento con successo dell'aggiornamento. Ogni esecuzione del test restituisce uno di questi esiti, quindi lo structural lower bound è 3.
### Node Coverage
| ID | user_id | Stato iniziale utente | payload | Outcome atteso |
| :--- | :--- | :--- | :--- | :--- |
| UUN-01 | 1 | { "username": "old_user" } | {'username': 'new_user'} | ValidationError("Username already in use.") |
| UUN-02 | 1 | { "email": "old@email.com" } | {'email': 'new@email.com'} | ValidationError("Email already in use.") |
| UUN-03 | 1 | { "first_name": "Old Name" } | {'first_name': 'New Name', 'is_active': False} | User (oggetto aggiornato) |
### Edge Coverage
Coperta dagli stessi test della Node Coverage.
### Condition Coverage
| Test | user_id | Stato iniziale | payload | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | Outcome atteso |
| :--- | :--- | :--- | :--- |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:--- |
| UUC-01 | 1 | { "username": "u" } | {} | F | - | - | F | - | - | F | - | F | F | - | F | F | User (nessuna modifica) |
| UUC-02 | 1 | { "username": "u" } | {'username': 'u'} | T | F | -(SC) | F | - | - | T | T | F | F | - | F | F | User (nessuna modifica) |
| UUC-03 | 1 | { "username": "u1" } | {'username': 'u2'} | T | T | F | F | - | - | T | T | F | F | - | F | F | User (username aggiornato) |
| UUC-04 | 1 | { "username": "u1" } | {'username': 'u2'} | T | T | T | F | - | - | - | - | - | - | - | - | - | ValidationError (username) |
| UUC-05 | 1 | { "email": "e" } | {'email': 'e'} | F | - | - | T | F | -(SC) | T | T | F | F | - | F | F | User (nessuna modifica) |
| UUC-06 | 1 | { "email": "e1" } | {'email': 'e2'} | F | - | - | T | T | F | T | T | F | F | - | F | F | User (email aggiornata) |
| UUC-07 | 1 | { "email": "e1" } | {'email': 'e2'} | F | - | - | T | T | T | - | - | - | - | - | - | - | ValidationError (email) |
| UUC-08 | 1 | { "role": "CITIZEN" } | {'role': 'OPERATOR'} | F | - | - | F | - | - | F | - | T | F | F | F | F | User (category_id a None) |
| UUC-09 | 1 | { "role": "CITIZEN" } | {'role': 'OPERATOR', 'category_id': 1} | F | - | - | F | - | - | F | - | T | T | T | F | F | User (category_id a 1) |
| UUC-10 | 1 | {} | {'is_active': False} | F | - | - | F | - | - | F | - | F | F | - | T | F | User (is_active a False) |
| UUC-11 | 1 | {} | {'email_notifications_enabled': False} | F | - | - | F | - | - | F | - | F | F | - | F | T | User (notifiche a False) |
| UUC-12 | 1 | {} | {'first_name': 123} | F | - | - | F | - | - | T | F | F | F | - | F | F | User (first_name a 123) |
### Loop Coverage
- loop su ["username", "first_name", "last_name", "email"]
  - 0 iterazioni: il payload non contiene nessuno dei campi testuali, quindi il ciclo viene saltato (UUL-01).
  - 1 iterazione: il payload contiene solo uno dei campi testuali, eseguendo il ciclo una volta (UUL-02).
  - 2+ iterazioni: il payload contiene due o più campi testuali, eseguendo il ciclo più volte (UUL-03).

| ID | payload | Descrizione | Risultato atteso |
| :- | :------ | :---------- | :--------------- |
| UUL-01 | {'is_active': False} | 0 iterazioni: Il payload non contiene campi testuali, quindi il ciclo viene saltato. | User (oggetto aggiornato) |
| UUL-02 | {'first_name': 'Mario'} | 1 iterazione: Il payload contiene un solo campo testuale, eseguendo il ciclo una volta. | User (oggetto aggiornato) |
| UUL-03 | {'first_name': 'Mario', 'last_name': 'Rossi'} | 2+ iterazioni: Il payload contiene due campi testuali, eseguendo il ciclo più volte. | User (oggetto aggiornato) |
### Path Coverage
Coperto dai test sopra.
### Minimal Suite Test
1. **UU-01**: Verifica il percorso di successo con l'aggiornamento di più campi (es. first_name, is_active). Corrisponde al test UUN-03.
2. **UU-02**: Testa la gestione di un conflitto di username e la conseguente ValidationError. Corrisponde al test UUN-01.
UU-03: Testa la gestione di un conflitto di email e la conseguente ValidationError. Corrisponde al test UUN-02.
UU-04: Verifica l'aggiornamento del ruolo a OPERATOR con assegnazione di category_id. Corrisponde al test UUC-09.
UU-05: Testa il caso in cui il payload è vuoto, assicurando che non avvenga nessuna modifica. Corrisponde al test UUC-01.

