## 1 `participium.services.auth_service.AuthService.authenticate`

**Suggested test file:** `test_authenticate.py`

**Prototype:** `authenticate(identifier: str, password: str) -> User`

**Requisiti:**
 Il sistema deve autenticare un utente tramite username o email e una password.
 
- Se le credenziali sono errate, il sistema deve restituire un errore di autenticazione (AuthenticationError).
- Se l'utente viene trovato, ma non è attivo, il sistema deve restituire un errore di autenticazione (AuthenticationError).
- Se le credenziali sono corrette, il sistema deve restituire l'oggetto User corrispondente.

**Criterio:** identifier

**Predicati:**
identifier è None--> non valido
identifier corrisponde a un username esistente --> valido
identifier corrisponde a un'email esistente --> valido
identifier non corrisponde ad un username o email esistente --> non valido

**Criterio:** password

**Predicati:**
password è None--> non valido
password corrisponde alla password hash dell'utente trovato --> valido
password non corrisponde alla password hash dell'utente trovato --> non valido

**Criterio:** stato User

**Predicati:**
User è attivo e l'email è verificata ( is_active == True AND is_email_verified == True) --> valido
User non è attivo ( is_active == False) --> non valido
User email non è verificata ( email_verified == False) --> non valido

### Equivalence Classes

**Per identifier:**
- **EC1**: identifier valido (username)
- **EC2**: identifier valido (email)
- **EC3**: identifier non esistente
- **EC4**: identifier == None

**Per password:**
- **EC5**: password valida per l'utente inserito
- **EC6**: password errata
- **EC7**: password == None

**Per stato User:**
- **EC8**: User attivo e email verificata
- **EC9**: User non attivo
- **EC10**: User email non verificata

### Combinations of Equivalence Classes 

- EC1 × EC5 × EC8 -> autenticazione riuscita con username
- EC2 × EC5 × EC8 -> autenticazione riuscita con email
- EC1/EC2 × EC6 × EC8 -> autenticazione fallita per password errata
- EC1/EC2 × EC7 × EC8 -> autenticazione fallita per password ==  None
- EC1/EC2 × EC5 × EC9-> autenticazione fallita per user non attivo
- EC1/EC2 × EC5 × EC10 -> autenticazione fallita per user email non verificata
- EC3 × qualsiasi password EC × qualsiasi stato User EC -> autenticazione fallita per identifier non valido
- EC4 × qualsiasi password EC × qualsiasi stato User EC -> autenticazione fallita per identifier == None



| TC   | identifier        | password  | EC covered | Expected | Fixture                                             |
|:-----|:------------------|:----------|:-----------|:---------|:----------------------------------------------------|
| AU01 | `mario_r`         | `pass123` | EC1, EC5, EC8   | User obj | Username e password corretti, user attivo e email verificata |
| AU02 | `mario.r@polito.it`   | `pass123` | EC2, EC5, EC8   | User obj | Email e password corretti, user attivo e email verificata |
| AU03 | `mario_r`         | `wrong`   | EC1, EC6   | None | Username corretto, password errata  |
| AU04 | `mario.r@polito.it`   | `wrong`   | EC2, EC6 | None | Email corretta, password errata |
| AU05 | `mario_r`         | None      | EC1, EC7   | None | Username corretto, password omessa |
| AU06 | `mario.r@polito.it`   | None      | EC2, EC7   | None | Email corretta, password omessa  |
| AU07 | `unknown_user`    | `pass123` | EC3   | None| Username inesistente |
| AU08 | `unknown@mail.it` | `pass123` | EC3| None| Email inesistente |
| AU09 | None              | `pass123` | EC4 | None| Identifier omesso  |
| AU10 | None              | None      | EC4, EC7   | None| Entrambi i campi omessi |
| AU11 | `mario_r`         | `pass123` | EC1, EC5, EC9   | None | Username e password corretti, user non attivo |
| AU12 | `mario_r`         | `pass123` | EC2, EC5, EC10   | None | Email e password corretti, user email non verificata |

### Boundary: identifier recognition

**Boundary around "username":**

| TC    | identifier | password  | Boundary covered  | Expected |
| :---- | :--------- | :-------- |:------------------|:---------|
| AUB01 | `mario_r`  | `pass123` | Exact boundary    | User obj |
| AUB02 | `mario_rx` | `pass123` | Immediately above | AuthenticationError     |
| AUB03 | `mario_`   | `pass123` | Immediately below | AuthenticationError     |
| AUB04 | `MARIO_R`  | `pass123` | Immediately above  | AuthenticationError     |

**Boundary around "email":**

| TC    | identifier          | password  | Boundary covered  | Expected |
| :---- | :------------------ | :-------- |:------------------|:-----|
| AUB05 | `m.r@polito.it`     | `pass123` | Exact boundary    | User obj |
| AUB06 | `m.r@polito.it.com` | `pass123` | Immediately above | AuthenticationError |
| AUB07 | `m.r@polito.i`      | `pass123` | Immediately below | AuthenticationError |
| AUB08 | `m.r@polito.it `    | `pass123` | Immediately above | AuthenticationError |

### Boundary: password comparison

| TC    | identifier | password   | Boundary covered   | Expected |
| :---- | :--------- | :--------- |:-------------------|:---------|
| AUB09 | `mario_r`  | `pass123`  | Exact boundary     | User obj |
| AUB10 | `mario_r`  | `Pass123`  | Immediately below  | AuthenticationError     |
| AUB11 | `mario_r`  | `pass12`   | Immediately below  | AuthenticationError     |
| AUB12 | `mario_r`  | `pass1234` | Immediately above  | AuthenticationError     |
| AUB13 | `mario_r`  | `p@ss123`  | Immediately below  | AuthenticationError     |

### Boundary: stato User
| TC    | identifier | password  | stato User | Boundary covered  | Expected |
| :---- | :--------- | :------------- |:------------------|:------------------|:---------|
| AUB14 | `mario_r`  | `pass123` | is_active == True AND is_email_verified == True | Exact boundary     | User obj |
| AUB15 | `mario_r`  | `pass123` | is_active == False | Immediately below  | AuthenticationError     |
| AUB16 | `mario_r`  | `pass123` | is_email_verified == False | Immediately below  | AuthenticationError     |



## 2 `participium.core.utils.parse_date`

Suggested test file: `test_parse_date.py`

Prototype: `parse_date(value: str | None) -> datetime | None`

| TC-ID | value | Expected | Fixture |
| :---- | :---- | :------- | :------ |
|  |  |  |  |

## 3 `participium.core.status_flow.ensure_transition_allowed`

Suggested test file: `test_status_flow.py`

Prototype: `ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus) -> bool`

Allowed transitions:
`Pending Approval -> Pending Approval | Assigned | Rejected`;
`Assigned -> Assigned | In Progress | Suspended | Resolved`;
`In Progress -> In Progress | Suspended | Resolved`;
`Suspended -> Suspended | In Progress | Resolved`;
`Rejected -> Rejected`;
`Resolved -> Resolved`.

**Requisiti:**

- Il sistema deve permettere la transizione tra gli stati di un report secondo le regole del seguente workflow:

        Pending Approval -> Pending Approval, Assigned, Rejected
        Assigned -> Assigned, In Progress, Suspended, Resolved
        In Progress -> In Progress, Suspended, Resolved
        Suspended -> Suspended, In Progress, Resolved
        Rejected -> Rejected
        Resolved -> Resolved

- Il sistema deve permettere le auto-transizioni (current_status == next_status) per ogni stato esistente.
- In caso di transizione permessa, il sistema deve restituire `True`.
- In caso di transizione non permessa dalle regole del workflow, il sistema restituisce un errore di transazione.

**Criterio: current_status**

**Predicati:**

- current_status == PENDING_APPROVAL --> valido
- current_status == ASSIGNED --> valido
- current_status == IN_PROGRESS --> valido
- current_status == SUSPENDED --> valido
- current_status == REJECTED --> valido
- current_status == RESOLVED --> valido
- current_status != any ReportStatus || current_status è None--> non valido

**Criterio: next_status**

**Predicati:**

- next_status == stato permesso dalle regole nel workflow per current_status --> valido
- next_status == stato NON permesso dal workflow nel workflow current_status --> non valido
- next_status != any ReportStatus || next_status è None--> non valido

### Equivalence Classes

**Per current_status:**

- **EC01**: `current_status == PENDING_APPROVAL`
- **EC02**: `current_status == ASSIGNED`
- **EC03**: `current_status == IN_PROGRESS`
- **EC04**: `current_status == SUSPENDED`
- **EC05**: `current_status == REJECTED`
- **EC06**: `current_status == RESOLVED`
- **EC07**: `current_status != any ReportStatus` || `current_status == None`

**Per next_status:**

- **EC08**: `next_status` è un valore permesso per lo stato corrente
- **EC09**: `next_status` è un valore NON permesso per lo stato corrente
- **EC10**: `next_status != any ReportStatus` || `next_status == None`

### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

    EC01 × EC08
    EC01 × EC09
    EC01 × EC10
    EC02 × EC08
    EC02 × EC09
    EC02 × EC10
    EC03 × EC08
    EC03 × EC09
    EC03 × EC10
    EC04 × EC08
    EC04 × EC09
    EC04 × EC10
    EC05 × EC08
    EC05 × EC09
    EC05 × EC10
    EC06 × EC08
    EC06 × EC09
    EC06 × EC10
    EC07 × EC08
    EC07 × EC09
    EC07 × EC10

(NOTA: ridondanti? tutte quanti sono possibili)

### Combinations of Equivalence Classes 

| TC   | current_status     | next_status       | EC covered | Expected          | Fixture                                |
|:-----|:-------------------|:------------------|:-----------|:------------------|:---------------------------------------|
| TR01 | `PENDING_APPROVAL` | `ASSIGNED`        | EC01, EC08 | `True`            | Transizione ammessa dal workflow       |
| TR02 | `PENDING_APPROVAL` | `RESOLVED`        | EC01, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR03 | `ASSIGNED`         | `IN_PROGRESS`     | EC02, EC08 | `True`            | Transizione ammessa dal workflow       |
| TR04 | `ASSIGNED`         | `REJECTED`        | EC02, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR05 | `IN_PROGRESS`      | `SUSPENDED`       | EC03, EC08 | `True`            | Transizione ammessa dal workflow       |
| TR06 | `IN_PROGRESS`      | `PENDING_APPROVAL`| EC03, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR07 | `SUSPENDED`        | `RESOLVED`        | EC04, EC08 | `True`            | Transizione ammessa dal workflow       |
| TR08 | `SUSPENDED`        | `ASSIGNED`        | EC04, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR09 | `REJECTED`         | `REJECTED`        | EC05, EC08 | `True`            | Auto-transizione sempre ammessa        |
| TR10 | `REJECTED`         | `IN_PROGRESS`     | EC05, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR11 | `RESOLVED`         | `RESOLVED`        | EC06, EC08 | `True`            | Auto-transizione sempre ammessa        |
| TR12 | `RESOLVED`         | `ASSIGNED`        | EC06, EC09 | `ValidationError` | Transizione non ammessa dal workflow   |
| TR13 | None               | `ASSIGNED`        | EC07, EC08 | `ValidationError` | Current status omesso                  |
| TR14 | `INVALID`          | `ASSIGNED`        | EC07, EC08 | `ValidationError` | Current status non esistente           |
| TR15 | `PENDING_APPROVAL` | None              | EC01, EC10 | `ValidationError` | Next status omesso                     |
| TR16 | `PENDING_APPROVAL` | `UNKNOWN`         | EC01, EC10 | `ValidationError` | Next status non esistente              |

### Boundary: workflow transitions

**Boundary around allowed transitions:**

| TC    | current_status     | next_status       | Boundary covered| EC Covered | Expected          |
| :---- |:-------------------|:------------------|:-----------------|:-----------|:------------------|
| TRB01 | `PENDING_APPROVAL` | `PENDING_APPROVAL`| Exact boundary (self) | EC1, EC8   | `True`|
| TRB02 | `PENDING_APPROVAL` | `REJECTED`        | Exact boundary     | EC1, EC8   | `True`|
| TRB03 | `ASSIGNED`         | `RESOLVED`        | Exact boundary     | EC2, EC8   | `True`|
| TRB04 | `SUSPENDED`        | `IN_PROGRESS`     | Exact boundary    | EC4, EC8   | `True`|
| TRB05 | None               | `ASSIGNED`        | Immediately below | EC7, EC8   | `ValidationError` |
| TRB06 | `PENDING_APPROVAL` | None              | Immediately below | EC1, EC10  | `ValidationError` |
| TRB07 | `INVALID_STATE`    | `ASSIGNED`        | Immediately below | EC7, EC8   | `ValidationError` |
| TRB08 | `PENDING_APPROVAL` | `UNKNOWN`         | Immediately below | EC1, EC10  | `ValidationError` |
| TRB09 | `REJECTED`         | `RESOLVED`        | Immediately above | EC5, EC9   | `ValidationError` |

## 4 `participium.services.report_service.ReportService.create_report`

Suggested test file: `test_create_report.py`

Prototype: `create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report`

**Requisiti:**
- Se il reporter è Noneo o non ha un id valido, il sistema deve restituire un errore di validazione (ValidationError).
- Se il category_id è Noneo, malformato o si riferisce a una categoria sconosciuta o a una categoria inattiva, il sistema deve restituire un errore di validazione (ValidationError).
- Se la descrizione o il titolo sono Nonei o vuoti, il sistema deve restituire un errore di validazione (ValidationError).
- Se le coordinate geografiche sono Nonee o non possono essere convertite in valori numerici, il sistema deve restituire un errore di validazione (ValidationError).
- Se la lista di foto contiene zero foto valide  o più di 3 foto valide, il sistema deve restituire un errore di validazione (ValidationError).
- Se tutti i campi sono validi, il sistema deve restituire un oggetto di tipo Report.

**Criterio:** reporter
**Predicati:**
reporter è None--> non valido
reporter è un utente non autenticato --> non valido
reporter è un utente auteenticato --> valido

**Criterio:** category_id
**Predicati:**
category_id è None--> non valido
category_id è malformato --> non valido
category_id fa riferimento a una categoria sconosciuta --> non valido 
category_id fa riferimento a una categoria inattiva --> non valido
category_id è valido e attivo --> valido

**Criterio:** title e description
**Predicati:**
title o descriptionè None o vuoto --> non valido
title e descrizione sono stringhe non vuote --> valid

**Criterio:** latitude / longitude
**Predicati:**
latitude o longitude è None --> non valido
latitude o longitude non possono essere convertiti in valori numerici --> non valido
latitude e longitude sono convertibili in valori numerici validi --> valid

**Criterio:** photos
**Predicati:**
Non è presente alcuna foto valida --> non valido
Sono presenti più di 3 foto valide --> non valido
Sono presenti da 1 a 3 foto valide --> valid

### Equivalence Classes

**Per reporter:**
- **EC1**: reporter è un utente non autenticato o non attivo
- **EC2**: reporter è un utente autenticato e attivo
- 
**Per category_id:**
- **EC3**: category_id is None
- **EC4**: category_id non valido
- **EC5**: category_id è valido e attivo

**Per title e description:**
- **EC6**: title o description è None 
- **EC7**: title o description non valido
- **EC8**: title e description sono validi

**Per latitude/longitude:**
- **EC9**: latitude o longitude is None
- **EC10**: latitude o longitude non validi
- **EC11**: latitude e longitude validi

**Per photos:**
- **EC12**: numero di foto non valido
- **EC13**:  1 <= numero di foto  <= 3

### Combinations of Equivalence Classes 
EC2 x EC5 x EC8 x EC11 x EC13 --> Report creato con successo
EC1 x EC5 x EC8 x EC11 x EC13 --> reporter non valido
EC2 x EC3 x EC8 x EC11 x EC13 --> category_id Noneo
EC2 x EC4 x EC8 x EC11 x EC13 --> category_id malformato o sconosciuto
EC2 x EC5 x EC6 x EC11 x EC13 --> title o description Nonei o vuoti
EC2 x EC5 x EC7 x EC11 x EC13 --> title o description non validi
EC2 x EC5 x EC8 x EC9 x EC13 --> latitude o longitude Nonei
EC2 x EC5 x EC8 x EC10 x EC13 --> latitude o longitude non validi
EC2 x EC5 x EC8 x EC11 x EC12 --> numero di foto non valido


| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | EC covered | Expected | Fixture |
| :---- | :------- | :---------- | :---- | :---------- | :------- | :-------- | :----- | :----------- | :------- | :------- | :------ |
|CR1| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | EC2, EC5, EC8, EC11, EC13  | Report |  |
|CR2| None | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | EC1, EC5, EC8, EC11, EC13 | ValidationError | Reporter non valido |
|CR3| user | "" | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC3, EC8, EC11, EC13| False | ValidationError | Categoria Nonea | 
|CR4| user | df | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC4, EC8, EC11, EC13 | False | ValidationError | Categoria non vallida|
|CR5| user | 4 | "" | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC5, EC6, EC11, EC13 | False | ValidationError | Titolo vuoto|
|CR6| user | 4 | Buca profonda |&&&%&£/$"(")"$$&"| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC5, EC7, EC11, EC13 | False | ValidationError | Descrizione non valida |
|CR8| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | "" | [foto_buca.jpg] | EC2,EC5,EC8,EC9,EC13 | False | ValidationError | Longitude Nonea |
|CR9| user | 4 | Buca profonda | Buca profonda in piazza Castello| Quarantacinque | "7.6856" | [foto_buca.jpg] | EC2,EC5,EC8,EC10,EC13 | False | ValidationError | Formato Latitude non convertibile |
|CR10| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [] | EC2, EC5, EC8, EC11, EC12 | False | ValidationError | Nessuna foto presente |

### Boundary: identifier recognition

**Boundary around "category_id":**
Boundary test per 'category_id' realizzati considerando le 10 categorie descritte nella specifica iniziale, con id associati da 0 a 9.

| TC    | category_id | Boundary covered  | Expected |
| :---- | :---------- |:------------------|:---------|
| AUB01 | 4           | Exact boundary    | Report obj |
| AUB02 | 10         | Immediately above | ValidationError |
| AUB03 | -1          | Immediately below | ValidationError |

**Boundary around "latitude/longitude":**
| TC    | latitude/longitude | Boundary covered  | Expected |
| :---- | :----------------- |:------------------|:---------|
| AUB04 | 45.0710 / 7.6856   | Exact boundary    | Report obj |
| AUB05 | 2324.52 / 7.6856 | Immediately above    | ValidationError |
| AUB06 | 45.0710 / -235.89 | Immediately below    | ValidationError |

**Boundary around "photos":**
| TC    | photos | Boundary covered  | Expected |
| :---- | :----- |:------------------|:---------|
| AUB07 | [foto_buca.jpg] | Exact boundary    | Report obj |
| AUB08 | [] | Immediately below    | ValidationError |
| AUB09 | [foto1.jpg, foto2.jpg, foto3.jpg, foto4.jpg] | Immediately above    | ValidationError |



## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`

| TC-ID | report_id | operator | next_status_value | note | Expected | Fixture |
| :---- | :-------- | :------- | :---------------- | :--- | :------- | :------ |
|  |  |  |  |  |  |  |

## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
| :---- | :---------- | :----- | :-------- | :------ | :--- | :------- | :------ |
|  |  |  |  |  |  |  |  |


## 7 `participium.services.messaging_service.MessagingService.send_message`

Suggested test file: `test_send_message.py`

Prototype: `send_message(report: Report, sender: User, body: str) -> Message`

**Requisiti**:
- Se o il report o l'id del report sono Nonei il sistema deve generare un ValidationError. 
- Se o il mittente o l'id del mittente sono Nonei il sistema deve generare un ValidationError.
- Se il mittente non può accedere al thread di messaggistica del report in questione il sistema deve generare un AuthorizationError.
- Se il testo del messaggio è vuoto il sistema deve generare un ValidationError.  
- Se il sistema non riesce a risolvere un destinatario del messaggio deve generare un ValidationError.
- Se sia l'utente che il report esistono e hanno un id valido, l'utente può accedere ai messaggi del report e il testo del messaggio non è vuoto, il sistema ritorna un oggetto di tipo Message.

**Criterio:** report

**Predicati:**

- report è None--> non valido
- report.id è None--> non valido 
- report.reporter_id è None--> non valido 
- report esiste con il proprio id e reporter id validi --> valido 


**Criterio:** sender

**Predicati:**

- sender è None--> non valido
- sender.id è None--> non valido
- il sender non ha lo stesso id del reporter (sender.id != report.reporter_id) --> non valido
- sender esiste e ha lo stesso id del reporter (sender.id == report.reporter_id) --> valido


**Criterio:** body

**Predicati:**

- body è None--> non valido
- body è vuoto oppure contiene solo caratteri di tipo whitespace --> non valido
- body contiene non solo caratteri di tipo whitespace --> valido

### Equivalence Classes

**Per report:**
- **EC1**: report == None
- **EC2**: report.id == None
- **EC3**: report.reporter_id == None
- **EC4**: report id e reporter id validi

**Per sender:**
- **EC5**: sender == None
- **EC6**: sender.id == None
- **EC7**: sender.id != report.reporter_id
- **EC8**: sender id valido

**Per body:**
- **EC9**: body == None
- **EC10**: body vuoto o con solo whitespace 
- **EC11**: body valido 


### Combinations of Equivalence Classes 

- EC4 x EC8 x EC11 -> oggetto messaggio ritornato con successo
- EC1 x EC8 x EC11 -> fallimento per report Noneo
- EC2 x EC8 x EC11 -> fallimento per report id Noneo
- EC3 x EC8 x EC11 -> fallimento per reporter id Noneo
- EC4 x EC5 x EC11 -> fallimento per sender Noneo
- EC4 x EC6 x EC11 -> fallimento per sender id Noneo
- EC4 x EC7 x EC11 -> fallimento per sender id diverso da reporter id
- EC4 x EC8 x EC9 -> fallimento per body Noneo
- EC4 x EC8 x EC10 -> fallimento per body vuoto o con solo whitespace

Combinazioni possibili secondo i predicati:
Definiamo i seguenti oggetti da usare nei test:
- **user1**: utente con un campo id valido e uguale ad 1.
- **user2**: utente con un campo id valido e uguale ad 2.
- **user3**: utente con un campo id Noneo.
- **report1**: report fatto dall'utente 1.
- **report2**: report con un campo reporter_id Noneo.
- **report3**: report con un campo id Noneo.

| TC-ID | report | sender | body | EC covered | Expected | Fixture |
| :---- | :----- | :----- | :--- | :--------- | :------- | :------ |
| MS01 | None | None | None |EC1, EC5, EC9 | ValidationError | Tutti e tre i campi omessi  |
| MS02 | None | user1 | None | EC1, EC8, EC9 | ValidationError | User valido ma altri due campi omessi |
| MS03 | report1 | None | None | EC4, EC5, EC9 | ValidationError | Report valido ma altri due campi omessi |
| MS04 | None | None | "ciao" | EC1, EC5, EC11 | ValidationError | Body valido ma altri due campi omessi |
| MS05 | report1 | user1 | None | EC4, EC8, EC9 | ValidationError | Body omesso |
| MS06 | report1 | None | "ciao" | EC4, EC5, EC11 | ValidationError  | User omesso |
| MS07 | None | user1 | "ciao" | EC4, EC8, EC11 | ValidationError  | Report omesso |
| MS08 | report1 | user1 | "" | EC4, EC8, EC10 | ValidationError | Body vuoto |
| MS09 | report1 | user2 | "ciao" | EC4, EC7, EC11 | AuthorizationError | Report non fatto dal mittente |
| MS10 | report1 | user3 | "ciao" | EC4, EC6, EC11 | ValidationError  | User senza un campo id |
| MS11 | report2 | user1 | "ciao" | EC2, EC6, EC11 | ValidationError  | Report senza un campo reporter_id |
| MS12 | report3 | user1 | "ciao" | EC3, EC5, EC11 | ValidationError | Report senza un campo id |
| MS13 | report1 | user1 | "ciao" | EC4, EC8, EC11 | Message | Tutto valido |

### Boundary: messaging constraints

**Boundary around body content:**

| TC    | report | sender | body | Boundary covered | EC covered | Expected |
| :---- | :----- | :----- | :--- | :--------------- | :--------- | :------- |
| MSB01 | report1| user1  | "a"  | Minima lunghezza valida | EC4, EC8, EC11 | Message |
| MSB02 | report1| user1  | " "  | Solo spazio bianco | EC4, EC8, EC10 | ValidationError |
| MSB03 | report1| user1  | ""   | Stringa vuota | EC4, EC8, EC10 | ValidationError |


## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

**Requisiti:**
- Il sistema deve permettere la verifica di una password in chiaro rispetto ad un hash memorizzato.
- Il sistema deve restituire `True` se la password corrisponde correttamente all'hash fornito.
- Il sistema deve restituire `False` se la password non corrisponde all'hash fornito.
- Il sistema deve invalidare la richiesta se la password o l'hash non sono forniti (None).

**Criterio:** password

**Predicati:**

- password è None--> non valido
- password != None --> valido


**Criterio:** password_hash

**Predicati:**

- password_hash è None--> non valido
- Le hash della password corrispondono (password_hash == hash(password)) --> valido
- Le hash della password non corrispondono (password_hash != hash(password)) --> non valido


### Equivalence Classes

**Per password:**
- **EC1**: password == None
- **EC2**: password != None

**Per password_hash:**
- **EC3**: password_hash == None
- **EC4**: hash corrispondono
- **EC5**: hash non corrispondono


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC2 x EC4 -> hash corrispondono, funzione ritorna vero
- EC2 x EC5 -> hash non corrispondono, funzione ritorna falso
- EC1 x EC5 -> errore causato da password Nonea
- EC2 x EC3 -> errore causato da hash Nonea

Definiamo i seguenti oggetti da usare nei test:
- **pwd1**: stringa "pass123".
- **hash1**: hash corretto di "pass123".
- **hash2**: hash non corrispondente a "pass123".

| TC-ID | password | password_hash | EC covered | Expected | Fixture |
| :---- | :------- | :------------ | :--------- | :------- | :------ |
| VP01 | pwd1 | hash1 | EC2, EC4 | True | Password e hash corretti |
| VP02 | pwd1 | hash2 | EC2, EC5 | False | Password corretta, hash errato |
| VP03 | pwd1 | None | EC2, EC3 | ValidationError | Password fornita, hash omesso |
| VP04 | None | hash1 | EC1, EC5 | ValidationError | Password omessa, hash fornito |
| VP05 | None | None | EC1, EC3 | ValidationError | Entrambi i campi omessi |


### Boundary: password and hash comparison

**Boundary around matching:**

| TC    | password | password_hash | Boundary covered | EC covered | Expected |
| :---- | :------- | :------------ | :--------------- | :--------- | :------- |
| VPB01 | "pass123" | hash("pass123") | Uguaglianza | EC2, EC4 | True |
| VPB02 | "pass123" | hash("Pass123") | Differenza lettera maiuscola | EC2, EC5 | False |
| VPB03 | "pass123" | hash("pass12")  | Un carattere in meno | EC2, EC5 | False |
| VPB04 | "pass123" | hash("pass1234")| Un carattere in più | EC2, EC5 | False |
| VPB05 | ""        | hash("")        | Stringa vuota | EC2, EC4 | True |

## 9 `participium.services.notification_service.NotificationService.create_notification`

Suggested test file: `test_create_notification.py`

Prototype: `create_notification(user: User | None, notification_type: NotificationType, title: str, body: str, report: Report | None = None) -> Notification | None`

| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :------- | :------ |
|  |  |  |  |  |  |  |  |

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
|  |  |  |  |  |  |  |  |  |
