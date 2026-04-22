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
- Se la transizione di stato è una auto-transizione (current_status == next_status), il sistema deve restituire `True`.
- Se la transizione di stato è permessa, il sistema deve restituire `True`.
- Se la transizione di stato non è permessa, il sistema deve restituire un errore di validazione (ValidationError).

**Criterio: current_status**

**Predicati:**
- current_status è uno degli stati possibili --> valido
- current_status è diverso dagli stati possibili o uguale a None --> non valido

**Criterio: next_status**

**Predicati:**
- next_status è uno degli stati possibili --> valido
- next_status non è uno stato permesso dal workflow nel workflow current_status --> non valido

### Equivalence Classes

**Per current_status:**

- **EC01**: current_status == Pending Approval
- **EC02**: current_status == Assigned
- **EC03**: current_status == In Progress
- **EC04**: current_status == Suspended
- **EC05**: current_status == Rejected
- **EC06**: current_status == Resolved

**Per next_status:**

- **EC07**: `next_status` è un valore di transizione permesso per lo stato corrente
- **EC08**: `next_status` è un valore di transizione non permesso per lo stato corrente


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

    EC01 × EC07 --> transizione ammessa per Pending Approval
    EC01 × EC08 --> transizione non ammessa per Pending Approval
    EC02 × EC07 --> transizione ammessa per Assigned
    EC02 × EC08 --> transizione non ammessa per Assigned
    EC03 × EC07 --> transizione ammessa per In Progress
    EC03 × EC08 --> transizione non ammessa per In Progress
    EC04 × EC07 --> transizione ammessa per Suspended
    EC04 × EC08 --> transizione non ammessa per Suspended
    EC05 × EC07 --> transizione ammessa per Rejected
    EC05 × EC08 --> transizione non ammessa per Rejected
    EC06 × EC07 --> transizione ammessa per Resolved
    EC06 × EC08 --> transizione non ammessa per Resolved

(NOTA: ridondanti? tutte quanti sono possibili)

### Combinations of Equivalence Classes 

| TC   | current_status     | next_status       | EC covered   | Expected          | Fixture                                |
|:-----|:-------------------|:------------------|:-------------------------|:------------------|:---------------------------------------|
|TR1 | Pending Approval | Pending Approval | EC01, EC07 | True | Self-transition |
|TR2 | Pending Approval | Assigned | EC01, EC07 | True | Transizione valida|
|TR3 | Pending Approval | Rejected | EC01, EC07 | True | Transizione valida|
|TR4 | Pending Approval | Resolved | EC01, EC08 | ValidationError | Transizione non valida|
|TR5 | Assigned | Assigned | EC02, EC07 | True | Self-transition |
|TR6 | Assigned | In Progress | EC02, EC07 | True | Transizione valida|
|TR7 | Assigned | Suspended | EC02, EC08 | True | Transizione valida|
|TR8 | Assigned | Resolved | EC02, EC08 | True | Transizione valida|
|TR9 | Assigned | Pending Approval | EC02, EC08 | ValidationError | Transizione non valida|
|TR10 | In Progress | In Progress | EC03, EC07 | True | Self-transition |
|TR11 | In Progress | Suspended | EC03, EC08 | True | Transizione valida|
|TR12 | In Progress | Resolved | EC03, EC08 | True | Transizione valida|
|TR13 | In Progress | Assigned | EC03, EC08 | ValidationError | Transizione non valida|
|TR14 | Suspended | Suspended | EC04, EC07 | True | Self-transition|
|TR15 | Suspended | In Progress | EC04, EC08 | True| Transizione valida|
|TR16 | Suspended | Resolved | EC04, EC08 | True | Transizione valida|
|TR17 | Suspended | Pending Approval | EC04, EC08 | ValidationError | Transizione non valida|
|TR18 | Rejected | Rejected | EC05, EC07 | True | Self-transition |
|TR19 | Rejected | Assigned | EC05, EC08 | ValidationError | Transizione non valida |
|TR20 | Resolved | Resolved | EC06, EC07 | True | Self-transition |
|TR21 | Resolved | In Progress | EC06, EC08 | ValidationError | Transizione non valida |



## 4 `participium.services.report_service.ReportService.create_report`

Suggested test file: `test_create_report.py`

Prototype: `create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report`

**Requisiti:**
- Se il reporter è None o non ha un id valido, il sistema deve restituire un errore di validazione (ValidationError).
- Se il category_id è None, malformato o si riferisce a una categoria sconosciuta o a una categoria inattiva, il sistema deve restituire un errore di validazione (ValidationError).
- Se la descrizione o il titolo sono None o vuoti, il sistema deve restituire un errore di validazione (ValidationError).
- Se le coordinate geografiche sono None o non possono essere convertite in valori numerici, il sistema deve restituire un errore di validazione (ValidationError).
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
- EC2 x EC5 x EC8 x EC11 x EC13 --> Report creato con successo
- EC1 x EC5 x EC8 x EC11 x EC13 --> reporter non valido
- EC2 x EC3 x EC8 x EC11 x EC13 --> category_id None
- EC2 x EC4 x EC8 x EC11 x EC13 --> category_id malformato o sconosciuto
- EC2 x EC5 x EC6 x EC11 x EC13 --> title o description None o vuoti
- EC2 x EC5 x EC7 x EC11 x EC13 --> title o description non validi
- EC2 x EC5 x EC8 x EC9 x EC13 --> latitude o longitude None
- EC2 x EC5 x EC8 x EC10 x EC13 --> latitude o longitude non validi
- EC2 x EC5 x EC8 x EC11 x EC12 --> numero di foto non valido


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

Requisiti: 


| TC-ID | report_id | operator | next_status_value | note | Expected | Fixture |
| :---- | :-------- | :------- | :---------------- | :--- | :------- | :------ |
|  |  |  |  |  |  |  |

## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

Requisiti:
    - il sistema deve restituire una lista di report basata su filtri opzionali
    - se nessun filtro è fornito, deve restituire una lista con tutte le segnalazioni 
    - il sistema deve fornire una lista con tutte le segnalazioni con categoria uguale a category_id (se fornito) 
    - il sistema deve fornire una lista con tutte le segnalazioni con stato uguale a status (se fornito) 
    - il sistema deve fornire una lista con tutte le segnalazioni con data uguale o successiva a date_from (se fornita)
    - il sistema deve fornire una lista con tutte le segnalazioni con data uguale o precedente a date_to (se fornita)
    - il sistema deve fornire una lista con le segnalazioni ordinate in base al parametro sort (di default decrescente)

Criterio: category_id
Predicati:
    - category_id è int -> valido
    - category_id è None -> valido (filtro assente)

Criterio: status 
Predicati:
    - status è uno degli stati possibili --> valido 
    - status non è presente --> valido(filtro assente)

Criterio: date_from
Predicati:
    - date_from è None -> valido (filtro assente) 
    - date_from è una datetime -> valido 

Criterio: date_to 
Predicati:
    - date_to è None -> valido (filtro assente) 
    - date_to è una datetime -> valido 

Criterio: sort 
Predicati:
    - sort == "desc" -> valido 
    - sort == "asc" -> valido 

### Equivalence Classes

**Per category_id**
- **EC01**: category_id è None
- **EC02**: category_id valido (int) ed esiste
- **EC03**: category_id valido (int) ma non esiste

**Per status**
- **EC04**: status è None 
- **EC05**: status è un valore valido (ReportStatus)

**Per date_from**
- **EC06**: date_from è None
- **EC07**: date_from è una data valida

**Per date_to**
- **EC08**: date_to è None
- **EC09**: date_to è una data valida

**Per sort**
- **EC10**: "desc"
- **EC11**: "asc"


### Combinations of Equivalence Classes 
- EC01 x EC04 x EC06 x EC08 x EC10 --> nessun filtro attivo quindi tutti i report in ordine decrescente
- EC02 x EC05 x EC07 x EC09 x EC11 --> tutti i filtri attivi, ordine crescente
- EC02 x EC04 x EC06 x EC08 x EC11 --> solo category_id attivo, ordine crescente
- EC01 x EC05 x EC06 x EC08 x EC10 --> solo status attivo, ordine decrescente
- EC01 x EC04 x EC07 x EC08 x EC10 --> solo date_from attivo, ordine decrescente
- EC01 x EC04 x EC06 x EC09 x EC10 --> solo date_to attivo, ordine decrescente
- EC01 x EC04 x EC07 x EC09 x EC10 --> solo le date attive, ordine decrescente
- EC03 x EC04 x EC06 x EC08 x EC10 --> category_id non esiste, ordine decrescente
- EC02 x EC05 x EC06 x EC08 x EC11 --> category_id non esiste, ordine decrescente


| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
|-------|-------------|--------|-----------|---------|------|----------|---------|
| PR-01  | None | None | None | None | desc |Tutti i report ordinati in modo decrescente | Lista di report  diversi tra di loro|
| PR-02  | 1 | None | None | None | asc | Solo i report con category_id==1 in ordine crescente| Lista di report  diversi tra di loro|
| PR-03  | None | ASSIGNED | None | None | desc | Solo i report con status ASSIGNED in ordine decrescente | Lista di report  diversi tra di loro|
| PR-04  | None | None | 2024-02-01 | None | desc | Solo i report dopo la data 2024-02-01 (compresa) in ordine decrescente | Lista di report diversi tra di loro|
| PR-05  | None | None | None | 2024-02-01 | desc | Solo i report prima della data 2024-02-01 (compresa) in ordine decrescente | Lista di report diversi tra di loro|
| PR-06  | None | None | 2024-02-01 | 2024-03-01 | desc | Tutti i report dopo la data 2024-02-01 (compresa) e prima della data 2024-03-01 in ordine decrescente | Lista di report diversi tra di loro|
| PR-07  | 1 | SUSPENDED | None | None | asc| Tutti i report che rispettano i filtri in ordine crescente | Lista di report diversi tra di loro|
| PR-08  | 1 | SUSPENDED | 2024-02-01 | 2024-03-01 | asc| Tutti i report che rispettano i filtri in ordine crescente | Lista di report diversi tra di loro|
| PR-09  | None | None | None | None | desc | Lista vuota | Lista vuota |
| PR-10  | 9999 | None | None | None | desc | Lista vuota | Lista di report con category_id 9999 inesistente|

### Boundary
**Boundary around "category_id":**
| TC    | category_id  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB01 |  0 | Exact boundary   | Lista di report con category_id 0 |
| PRB02 |  6 | Immediately above   | Lista vuota |
| PRB03 |  -1 | Immediately below   | Lista vuota |

**Boundary around "date_from":**
| TC    | date_from  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB04 |  2024-02-01 00:00:00 | Exact boundary   | Lista di report con date da 2024-02-01 00:00:00 |
| PRB05 |  2024-02-01 00:00:01 | Immediately above   | Lista di report con date da 2024-02-01 00:00:01 |
| PRB06 |  2024-01-31 23:59:59 | Immediately below   | Lista di report con date da 2024-01-31 23:59:59 |

**Boundary around "date_to":**
| TC    | date_to  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB07 |  2024-02-01 00:00:00 | Exact boundary   | Lista con date fino a 2024-02-01 00:00:00 |
| PRB08 |  2024-02-01 00:00:01 | Immediately above   | Lista con date fino a 2024-02-01 00:00:01 |
| PRB09 |  2024-01-31 23:59:59 | Immediately below   | Lista con date fino a 2024-01-31 23:59:59 |

**Boundary around "date_from" and "date_to"**
| TC    | date_from  | date_to | Boundary covered  | Expected |
| :---- | :-------- |:--------|:------------------|:---------|
| PRB10 |  2024-02-01 00:00:00 | 2024-02-01 00:00:00 | Exact boundary   | Lista con report in data 2024-02-01 |
| PRB08 |  2024-03-01 00:00:00 | 2024-02-01 00:00:00   |  | Lista vuota |


| PR-07  | None | None | 2024-03-01  | 2024-02-01 | desc | Lista vuota | Lista di report diversi tra di loro|

## 7 `participium.services.messaging_service.MessagingService.send_message`

Suggested test file: `test_send_message.py`

Prototype: `send_message(report: Report, sender: User, body: str) -> Message`

**Requisiti**:
- Se o il report o l'id del report sono None il sistema deve generare un ValidationError. 
- Se o il mittente o l'id del mittente sono None il sistema deve generare un ValidationError.
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
- EC1 x EC8 x EC11 -> fallimento per report None
- EC2 x EC8 x EC11 -> fallimento per report id None
- EC3 x EC8 x EC11 -> fallimento per reporter id None
- EC4 x EC5 x EC11 -> fallimento per sender None
- EC4 x EC6 x EC11 -> fallimento per sender id None
- EC4 x EC7 x EC11 -> fallimento per sender id diverso da reporter id
- EC4 x EC8 x EC9 -> fallimento per body None
- EC4 x EC8 x EC10 -> fallimento per body vuoto o con solo whitespace

Combinazioni possibili secondo i predicati:
Definiamo i seguenti oggetti da usare nei test:
- **user1**: utente con un campo id valido e uguale ad 1.
- **user2**: utente con un campo id valido e uguale ad 2.
- **user3**: utente con un campo id None.
- **report1**: report fatto dall'utente 1.
- **report2**: report con un campo reporter_id None.
- **report3**: report con un campo id None.

| TC-ID | report | sender | body | EC covered | Expected | Fixture |
| :---- | :----- | :----- | :--- | :--------- | :------- | :------ |
| MS01 | None | None | None | EC1, EC5, EC9 | ValidationError | Tutti e tre i campi omessi  |
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


**Requisiti:**
- Se title o body sono None-->Il sistema restituisce un ValidationError.
- Se notification_type è None o il tipo a cui fa riferimento è sconosciuto-->Il sistema restituisce un ValidationError.
- Se user non ha un id valido(diverso da None)-->Il sistema restituisce un ValidationError.
- Se report non ha un id valido-->Il sistema restituisce un ValidationError.
- Se tutti i cambi obbligaotiri sono presenti e validi e i campi opzionali sono validi o omessi --> Il sistema restituisce un oggetto Notification


**Criterio:** user

**Predicati:**

- user è un utente con id-->valido
- user è None--> valido (esempio di messaggio broadcast)?
- user è fornito ma non ha un id valido--> non valido

**Criterio:** notification_type

**Predicati:**

- notification_type è un tipo valido dell'enum-->valido
- notification_type è None o sconosciuti--> non valido

**Criterio:** title e body

**Predicati:**

- title o body sono None o vuoti-->non valido
- title e body sono stringhe non vuote-->valido

**Criterio:** report

**Predicati:**

- report è fornito e con un valido id-->valido
- reort è None-->valido
- report è fornito ma non ha un id valido-->non valido

### Equivalence Classes

**Per user:**
- **EC1**: user valido (con id)
- **EC2**: user == None
- **EC3**: user non valido (senza id)

**Per notification_type:**
- **EC4**: tipo di notification_type è valido
- **EC5**: tipo di notification_type non è valido o è None

**Per title e body:**
- **EC6**: title e body sono stringhe valide
- **EC7**: title o body None
- **EC8**: title o body stringhe vuote 

**Per report:**
- **EC9**: report valido (con id)
- **EC10**: report == None
- **EC11**: report non valido (senza id)

### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC1 x EC4 x EC6 x EC9 -> Successo con utente e report completi
- EC2 x EC4 x EC6 x EC10 -> Successo con campi opzionali a None
- EC3 x EC4 x EC6 x EC9 -> Fallimento per user senza id
- EC1 x EC5 x EC6 x EC9 -> Fallimento per type non valido
- EC1 x EC4 x EC7 x EC9 -> Fallimento per title/body None
- EC1 x EC4 x EC8 x EC9 -> Fallimento per title/body vuoti
- EC1 x EC4 x EC6 x EC11 -> Fallimento per report senza id


Definiamo i seguenti oggetti da usare nei test:
- **user1**: utente con id valido.
- **user_invalid**: utente con campo id uguale a None.
- **report1**: report con id valido.
- **report_invalid**: report con campo id uguale a None.
- **type1**: tipo di notifica valido

| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :------- | :------ |
| CN01 | user1 | type1 | "Nuovo aggiornamento" | "Il tuo report è in lavorazione" | report1 | Notification | Tutti i parametri validi forniti |
| CN02 | None  | type1 | "Manutenzione" | " I server saranno offline" | None | Notification | Parametri opzionali omessi |
| CN03 | user_invalid | type1 | "Titolo" | "Corpo" | report1 | ValidationError | user fornito ma senza id |
| CN04 | user1 | None | "Titolo" | "Corpo" | report1 | ValidationError | NotificationType omesso |
| CN05 | user1 | type1 | None |	"Corpo" | report1 | ValidationError | Titolo omesso |
| CN06 | user1 | type1 | "Titolo" | None | report1 | ValidationError | Body omesso |
| CN07 | user1 | type1 | "" | "Corpo" | report1 | ValidationError | Titolo vuoto |
| CN08 | user1 | type1 | "Titolo" | "" | report1 | ValidationError | Body vuoto |
| CN09 | user1 | type1 | "Titolo" | "Corpo" | report_invalid | ValidationError | Report fornito ma senza id |

### Boundary: password and hash comparison

**Boundary around matching:**

| TC | user | notification_type | title | body | report | Boundary covered | EC covered | Expected |
| :- | :--- | :---------------- | :---- | :--- | :----- | :--------------- | :--------- | :------- |
| CNB01 | user1 | type1 | "A" |	"B" | report1 |	Minima lunghezza valida | EC1, EC4, EC6, EC9 | Notification |
| CNB02	| user1 | type1 | " " | "B" | report1 |	Solo spazio bianco (titolo) | EC1, EC4, EC8, EC9 | ValidationError |
| CNB03 | user1 | type1 | " " | "B" | report1 |	Stringa vuota (titolo) | EC1, EC4, EC8, EC9 | ValidationError |
| CNB04 | user1 | type1 | "A" | " " | report1 | Solo spazio bianco (body) | EC1, EC4, EC8, EC9 | ValidationError |


## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
|  |  |  |  |  |  |  |  |  |
