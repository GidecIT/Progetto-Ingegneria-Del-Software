## 1 `participium.services.auth_service.AuthService.authenticate`

**Suggested test file:** `test_authenticate.py`

**Prototype:** `authenticate(identifier: str, password: str) -> User`

**Requisiti:** <br>
 Il sistema deve autenticare un utente tramite username o email e una password.
 
- Se le credenziali sono errate, il sistema deve restituire un errore di autenticazione (AuthenticationError).
- Se l'utente viene trovato, ma non è attivo, il sistema deve restituire un errore di autenticazione (AuthenticationError).
- Se le credenziali sono corrette, il sistema deve restituire l'oggetto User corrispondente.

**Criterio:** identifier

**Predicati:**
- identifier è None--> non valido
- identifier corrisponde a un username esistente --> valido
- identifier corrisponde a un'email esistente --> valido
- identifier non corrisponde ad un username o email esistente --> non valido

**Criterio:** password

**Predicati:**
- password è None--> non valido
- password corretta --> valido
- password non corretta --> non valido

**Criterio:** User.is_active e User.is_mail_verified

**Predicati:**
- User è attivo e l'email è verificata (is_active == True AND is_email_verified == True) --> valido
- User non è attivo (is_active == False) --> non valido
- User email non è verificata (email_verified == False) --> non valido

### Equivalence Classes

**Per identifier:**
- **EC1**: identifier valido
- **EC2**: identifier non valido
    
**Per password:**
- **EC3**: password valida
- **EC4**: password non valida

**Per User.is_active e User.is_mail_verified:**
- **EC5**: User attivo e email verificata
- **EC6**: User non attivo
- **EC7**: User email non verificata

### Combinations of Equivalence Classes 

- EC1 x EC3 x EC5 --> autenticazione riuscita
- EC2 x EC3 x EC5 --> identifier non valido
- EC1 x EC4 x EC5 --> password non valida
- EC1 x EC3 x EC6 --> User non attivo
- EC1 x EC3 x EC7 --> User email non verificata



| TC   | identifier        | password  | Expected | Fixture                                             |
|:-----|:------------------|:----------|:-----------|:----------------------------------------------------|
| AU01 | `mario_r`             | `pass123` | User | Utente esiste ed è attivo, email verificata|
| AU02 | `mario.r@polito.it`   | `pass123` | User | Utente esiste ed è attivo, email verificata |
| AU03 | `mario_r`             | `wrong`   | AuthenticationError | Utente esiste ed è attivo, email verificata |
| AU04 | `mario.r@polito.it`   | `wrong`   | AuthenticationError | Utente esiste ed è attivo, email verificata |
| AU05 | `unknown_user`        | `pass123` | AuthenticationError | Non esiste un utente con questo username |
| AU06 | `unknown@mail.it`     | `pass123` | AuthenticationError | Non esiste un utente con questa email |
| AU07 | `mario_r`             | `pass123` | AuthenticationError | Utente esiste, ma non è attivo |
| AU08 | `mario_r`             | `pass123` | AuthenticationError | Utente esiste, ma email non verificata |

### Boundary: identifier recognition
**Boundary around "identifier":**

| TC    | identifier | password  | Boundary covered  | Expected |
| :---- | :--------- | :-------- |:------------------|:---------|
| AU01 | `mario_r`  | `pass123` | Exact boundary    | User |
| AU02 | `m.r@polito.it` | `pass123` | Exact boundary    | User |
| AUB01 | None  | `pass123`  | Immediately below | AuthenticationError |
| AUB02 | "" | `pass123`  | Immediately below | AuthenticationError |
| AUB03 | " " | `pass123`  | Immediately below | AuthenticationError |

<br>

**Boundary around "password":**

| TC    | identifier | password  | Boundary covered   | Expected |
| :---- | :--------- | :---------|:-------------------|:---------|
| AU01 | `mario_r`  | `pass123`  | Exact boundary     | User |
| AUB04| `mario_r`   | None      | Immediately below  | AuthenticationError |
| AUB05 | `m.r@polito.it` | None | Immediately below  | AuthenticationError |
| AUB06 | `mario_r`  | ""        | Immediately below  | AuthenticationError |
| AUB07 | `mario_r`  | " "       | Immediately below  | AuthenticationError |

<br>


**Boundary around "stato User":**

| TC    | identifier | password  | stato User | Boundary covered  | Expected |
| :---- | :--------- | :------------- |:------------------|:------------------|:---------|
| AU01 | `mario_r`  | `pass123` | is_active == True AND is_email_verified == True | Exact boundary     | User |
| AUB08 | `mario_r`  | `pass123` | is_active == False | Immediately below  | AuthenticationError     |
| AUB09 | `mario_r`  | `pass123` | is_email_verified == False | Immediately below  | AuthenticationError     



## 2 `participium.core.utils.parse_date`

Suggested test file: `test_parse_date.py`

Prototype: `parse_date(value: str | None) -> datetime | None`

**Requisiti:**

 Il sistema deve ricavare la data da una stringa in formato 'datetime'.
 
- Se la stringa è vuota, il sistema restituisce None.
- Se la stringa non è vuota, ma non è un formato ISO-8601 datetime valido, il sistema ritorna errore (ValueError).
- Se la stringa è non vuota ed è un formato ISO-8601 datetime valido, restituisce l'oggetto 'datetime' corrispondente.

**Criterio:** value

**Predicati:**
- value è None --> non valido 
- value è un formato ISO-8601 datetime valido --> valido 
- value non è un formato ISO-8601 datetime valido --> non valido

### Equivalence Classes

**Per value:**
- **EC1**: value valido
- **EC2**: value non valido

### Combinations of Equivalence Classes 
- EC1 --> restituisce datetime
- EC2 --> restituisce ValueError

| TC   | value  |Expected | Fixture|
|:-----|:------------------|:----------|:----------------------------------------------------|
| DT01 | `2002-12-31` | datetime | -  |
| DT02 | None | None     | - |
| DT03 | "" | ValueError | - |
| DT04 | `2056-31-04` | ValueError | - |
| DT05 | `1980-00-04` | ValueError | - |
| DT06 | `1998/03/04` | ValueError | - |
| DT07 | `2020-02-34` | ValueError | - |

### Boundary

**Boundary intorno a date valide**

| TC    | value        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB01 | 2024-02-29   | Exact boundary    | datetime |
| DTB02 | 2024-02-30   | Immediately above | ValueError |
| DTB03 | 2023-02-29   | Immediately below | ValueError |

**Boundary around months:**

| TC    | value        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB04 | 2024-12-31   | Exact boundary    | datetime |
| DTB05 | 2024-13-01   | Immediately above | ValueError |
| DTB06 | 2024-00-01   | Immediately below | ValueError |

**Boundary around days:**

| TC    | value        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB07 | 2024-04-30   | Exact boundary    | datetime |
| DTB08 | 2024-04-31   | Immediately above | ValueError |
| DTB09 | 2024-04-00   | Immediately below | ValueError |


## 3 `participium.core.status_flow.ensure_transition_allowed`

Suggested test file: `test_status_flow.py`

Prototype: `ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus) -> bool`

Allowed transitions:<br>
`Pending Approval -> Pending Approval | Assigned | Rejected`; <br>
`Assigned -> Assigned | In Progress | Suspended | Resolved`;<br>
`In Progress -> In Progress | Suspended | Resolved`;<br>
`Suspended -> Suspended | In Progress | Resolved`;<br>
`Rejected -> Rejected`;<br>
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
- reporter è None--> non valido
- reporter è un utente non autenticato --> non valido
- reporter è un utente autenticato --> valido

**Criterio:** category_id

**Predicati:**
- category_id è None--> non valido
- category_id è malformato --> non valido
- category_id fa riferimento a una categoria sconosciuta --> non valido 
- category_id fa riferimento a una categoria inattiva --> non valido
- category_id è valido e attivo --> valido

**Criterio:** title e description

**Predicati:**
- title o description è None o vuoto --> non valido
- title e descrizione sono stringhe non vuote --> valid

**Criterio:** latitude / longitude

**Predicati:**
- latitude o longitude è None --> non valido
- latitude o longitude non possono essere convertiti in valori numerici --> non valido
- latitude e longitude sono convertibili in valori numerici validi --> valid

**Criterio:** photos

**Predicati:**
- Non è presente alcuna foto valida --> non valido
- Sono presenti più di 3 foto valide --> non valido
- Sono presenti da 1 a 3 foto valide --> valid

**Criterio:** is_anonymous

**Predicati:**
- is_anonymous == True --> valido
- is_anonymous == False --> valido

### Equivalence Classes

**Per reporter:**
- **EC1**: reporter è un utente non autenticato o non attivo
- **EC2**: reporter è un utente autenticato e attivo
- 
**Per category_id:**
- **EC3**: category_id non valido
- **EC4**: category_id è valido e attivo

**Per title e description:**
- **EC5**: title o description non valido
- **EC6**: title e description sono validi

**Per latitude/longitude:**
- **EC7**: latitude o longitude non validi
- **EC8**: latitude e longitude validi

**Per photos:**
- **EC9**: numero di foto non valido
- **EC10**:  1 <= numero di foto  <= 3

**Per is_anonymous:**
- **EC11**: is_anonymous è True o False --> valido
- **EC12**: is_anonymous non è un valore valido --> non valido

### Combinations of Equivalence Classes 
- EC2 x EC4 x EC6 x EC8 x EC10 x EC11 --> Report creato con successo
- 
- EC1 x EC4 x EC6 x EC8 x EC10 --> reporter non valido
- EC2 x EC3 x EC8 x EC7 x EC9 --> category_id None
- EC2 x EC4 x EC8 x EC7 x EC9 --> category_id malformato o sconosciuto
- EC2 x EC5 x EC6 x EC7 x EC9 --> title o description None o vuoti
- EC2 x EC5 x EC7 x EC7 x EC9 --> title o description non validi
- EC2 x EC5 x EC8 x EC9 x EC10 --> latitude o longitude None
- EC2 x EC5 x EC8 x EC10 x EC10 --> latitude o longitude non validi
- EC2 x EC5 x EC8 x EC11 x EC9 --> numero di foto non valido


| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | EC covered | Expected | Fixture |
| :---- | :------- | :---------- | :---- | :---------- | :------- | :-------- | :----- | :----------- | :------- | :------- | :------ |
|CR1| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | EC2, EC5, EC8, EC11, EC13  | Report |  |
|CR2| None | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | EC1, EC5, EC8, EC11, EC13 | ValidationError | Reporter non valido |
|CR3| user | "" | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC3, EC8, EC11, EC13| False | ValidationError | Categoria Nonea | 
|CR4| user | df | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC4, EC8, EC11, EC13 | False | ValidationError | Categoria non vallida|
|CR5| user | 4 | "" | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC5, EC6, EC11, EC13 | False | ValidationError | Titolo vuoto|
|CR6| user | 4 | Buca profonda |""| 45.0710 | 7.6856 | [foto_buca.jpg] | EC2, EC5, EC7, EC11, EC13 | False | ValidationError | Descrizione non valida |
|CR8| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | "" | [foto_buca.jpg] | EC2,EC5,EC8,EC9,EC13 | False | ValidationError | Longitude Nonea |
|CR9| user | 4 | Buca profonda | Buca profonda in piazza Castello| Quarantacinque | "7.6856" | [foto_buca.jpg] | EC2,EC5,EC8,EC10,EC13 | False | ValidationError | Formato Latitude non convertibile |
|CR10| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [] | EC2, EC5, EC8, EC11, EC12 | False | ValidationError | Nessuna foto presente|

### Boundary

**Boundary around "category_id":**
Boundary test per 'category_id' realizzati considerando le 10 categorie descritte nella specifica iniziale, con id associati da 0 a 9.

| TC    | category_id | Boundary covered  | Expected        |
| :---- | :---------- |:------------------|:----------------|
| AUB01 | 4           | Exact boundary    | Report          |
| AUB02 | 10         | Immediately above | ValidationError |
| AUB03 | -1          | Immediately below | ValidationError |

**Boundary around "title e description":**
| TC    | title/description | Boundary covered  | Expected |
| :---- | :----------------- |:------------------|:---------|
| CR1 | "Buca profonda" / "Buca profonda in piazza Castello"   | Exact boundary    | Report obj |
| CR5 | "" / "Buca profonda in piazza Castello" | Immediately below | ValidationError |
| CR6 | "Buca profonda" / "" | Immediately below | ValidationError |
| AUB04 | " " / "Buca profonda in piazza Castello" | Immediately below | ValidationError |
| AUB05 | "Buca profonda" / " " | Immediately below | ValidationError |

**Boundary around "latitude/longitude":**
| TC    | latitude/longitude | Boundary covered  | Expected |
| :---- | :----------------- |:------------------|:---------|
| AUB04 | 45.0710 / 7.6856   | Exact boundary    | Report |
| AUB05 | 2324.52 / 7.6856 | Immediately above    | ValidationError |
| AUB06 | 45.0710 / -235.89 | Immediately below    | ValidationError |

**Boundary around "photos":**
| TC    | photos | Boundary covered  | Expected |
| :---- | :----- |:------------------|:---------|
| AUB07 | [foto_buca.jpg] | Exact boundary    | Report|
| AUB08 | [] | Immediately below    | ValidationError |
| AUB09 | [foto1.jpg, foto2.jpg, foto3.jpg, foto4.jpg] | Immediately above | ValidationError |

## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`


**Requisiti:** <br>
Il sistema deve potere permettere l'aggiornamento di stato di un report.
- Se l'operatore non ha i permessi adatti alla modifica del report (User.Role != Role.OPERATOR AND User.Role != Role.ADMIN), il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se l'operatore è None, il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se l'operatore tenta di aggiornare un report al di fuori della propria categoria assegnata, il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se il report non esiste, il sistema restituisce errore (NotFoundError).
- Se next_status_value non rispetta l'ordine del workflow o non esiste, il sistema restituisce un errore di validazione (ValidationError).
- Se l'operatore respinge il report (next_status_value == REJECTED) senza una nota, il sistema restituisce un errore di validazione (ValidationError)
- Se tutti gli input inseriti sono validi, il sistema restituisce l'oggetto Report con lo stato aggiornato.

**Criterio**: report_id

**Predicati**:
- report_id è None --> non valido
- report_id non corrisponde a un report esistente --> non valido
- report_id corrisponde a un report esistente --> valido

**Criterio**: operator 

**Predicati**:
- operator è None --> non valido
- operator non corrisponde a un operatore esistente --> non valido
- operator non possiede i permessi adatti alla modifica --> non valido
- operator possiede una categoria diversa da quella del report --> non valido
- operator corrisponde a un operatore esistente con i permessi adatti alla modifica  --> valido
- operator corrisponde a un operatore esistente con categoria uguale rispetto a quella del report  --> valido

**Criterio**: next_status_value

**Predicati**:
- next_status_value è None --> non valido
- next_status è uno degli stati possibili ed è permesso dal workflow --> valido
- next_status non è uno stato permesso dal workflow oppure è None --> non valido

**Criterio**: note 

**Predicati**:
- note è None o "" --> valido
- note non è None o non è "" --> valido

**Criterio**: operator.category_id

**Predicati**:

-  operator.category_id è None --> valido
-  operator.category_id è valido --> valido

### Equivalence Classes

**Per report_id**
- **EC1**: report_id valido
- **EC2**: report_id non valido

**Per operator**
- **EC3**: operator valido
- **EC4**: operator non valido

**Per next_status_value**
- **EC5**: next_status_value valido
- **EC6**: next_status_value non valido

**Per note**
- **EC7**: note valido
- **EC8**: note non valido

**Per operator.category_id**
- **EC9**: operator.category_id == report.category_id
- **EC10**: operator.category_id != report.category_id

### Combinations of Equivalence Classes

- EC1 x EC3 x EC6 x EC8 x EC9 --> aggiornamento riuscito
- EC2 x EC3 x EC5 x EC8 x EC9 --> report inesistente
- EC1 x EC4 x EC6 x EC8 x EC9 --> operatore non autorizzato
- EC1 x EC3 x EC7 x EC8 x EC9 --> transizione di stato non ammessa
- EC1 x EC3 x EC6 x EC9 x EC9 --> nota mancante su report rifiutato
- EC1 x EC5 x EC6 x EC8 x EC10 --> operatore al di fuori della propria categoria

| TC-ID | report_id | operator | next_status_value | note | Expected | Fixture |
|:------| :--- | :--- | :--- | :--- |:-------------------|:----------------|
| US01  | 10 | op_cat_1 | "ASSIGNED" | None | Report| Il report esiste|
| US02  | 999 | op_cat_1 | "ASSIGNED" | None | NotFoundError| Il report non esiste |
| US03  | 10 | user_no_perm | "ASSIGNED" | None | AuthorizationError | Il report esiste |
| US04  | 10 | op_cat_2 | "ASSIGNED" | None | AuthorizationError | Il report esiste |
| US05  | 10 | op_cat_1 | "REJECTED" | None | ValidationError| Il report esiste |
| US06  | 10 | op_cat_1 | "RESOLVED" | None | ValidationError| Il report esiste |

### Boundary

**Boundary around report_id:**

| TC | report_id | operator | next_status_value | Boundary covered  | Expected |
| :--- |:----------| :--- | :--- |:------------------| :--- |
| USB01 | 1 | op_valido | "ASSIGNED" | Exact boundary    | Report |
| USB02 | 01 | op_valido | "ASSIGNED" | Immediately above | NotFoundError |


**Boundary around next_status_value and note:**

| TC    | report_id | operator | next_status_value | note | Boundary covered  | Expected |
|:------| :--- | :--- |:------------------|:-----|:------------------| :--- |
| USB07 | 10 | op_valido | Current Status    | None | Exact boundary    | Report |
| USB08 | 10 | op_valido | "RIFIUTATA"       | "A"  | Immediately below | ValidationError |
| USB10 | 10 | op_valido | "REJECTED"        | "B"  | Exact boundary    | Report |
| USB11 | 10 | op_valido | "REJECTED"        | None | Immediately below | ValidationError |
| USB12 | 10 | op_valido | "REJECTED"        | ""   | Immediately below | ValidationError |
| USB13 | 10 | op_valido | "ASSIGNED"        | ""   | Exact boundary    | Report |

## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

**Requisiti:**
- il sistema deve restituire una lista di segnalazioni pubbliche basata su filtri opzionali
- se nessun filtro è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche
- se category_id è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con categoria uguale a category_id
- se status è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con stato uguale a status
- se date_from è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con data di creazione uguale o successiva a date_from
- se date_to è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con data di creazione uguale o precedente a date_to
- se sort è fornito, il sistema deve restituire una lista con le segnalazioni pubbliche ordinate in base al parametro sort (di default decrescente)

**Criterio:** category_id

**Predicati:**
- category_id è int -> valido
- category_id è None -> valido (filtro assente)

**Criterio:** status 

**Predicati:**
- status è uno degli stati possibili --> valido 
- status non è presente --> valido(filtro assente)

**Criterio:** date_from

**Predicati:**
- date_from è None -> valido (filtro assente) 
- date_from è una datetime -> valido 

**Criterio:** date_to 

**Predicati:**
- date_to è None -> valido (filtro assente) 
- date_to è una datetime -> valido 

**Criterio:** sort 

**Predicati:**
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
- EC01 x EC04 x EC06 x EC08 x EC10 --> nessun filtro attivo quindi tutti le segnalazioni pubbliche in ordine decrescente
- EC02 x EC05 x EC07 x EC09 x EC11 --> tutti i filtri attivi, ordine crescente
- EC02 x EC04 x EC06 x EC08 x EC11 --> solo category_id attivo, ordine crescente
- EC01 x EC05 x EC06 x EC08 x EC10 --> solo status attivo, ordine decrescente
- EC01 x EC04 x EC07 x EC08 x EC10 --> solo date_from attivo, ordine decrescente
- EC01 x EC04 x EC06 x EC09 x EC10 --> solo date_to attivo, ordine decrescente
- EC01 x EC04 x EC07 x EC09 x EC10 --> solo le date attive, ordine decrescente
- EC03 x EC04 x EC06 x EC08 x EC10 --> category_id non esiste, ordine decrescente
- EC02 x EC05 x EC06 x EC08 x EC11 --> category_id e status attivi, ordine crescente


| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
|-------|-------------|--------|-----------|---------|------|----------|---------|
| PR-01  | None | None | None | None | desc |Tutti le segnalazioni pubbliche ordinate in modo decrescente | Lista di report  diversi tra di loro|
| PR-02  | 1 | None | None | None | asc | Solo le segnalazioni pubbliche con category_id==1 in ordine crescente| Lista di report  diversi tra di loro|
| PR-03  | None | ASSIGNED | None | None | desc | Solo le segnalazioni pubbliche con status ASSIGNED in ordine decrescente | Lista di report  diversi tra di loro|
| PR-04  | None | None | 2024-02-01 | None | desc | Solo le segnalazioni pubbliche dopo la data 2024-02-01 (compresa) in ordine decrescente | Lista di report diversi tra di loro|
| PR-05  | None | None | None | 2024-02-01 | desc | Solo le segnalazioni pubbliche prima della data 2024-02-01 (compresa) in ordine decrescente | Lista di report diversi tra di loro|
| PR-06  | None | None | 2024-02-01 | 2024-03-01 | desc | Tutte le segnalazioni pubbliche dopo la data 2024-02-01 (compresa) e prima della data 2024-03-01 (compresa) in ordine decrescente | Lista di report diversi tra di loro|
| PR-07  | 1 | SUSPENDED | None | None | asc| Tutte le segnalazioni pubbliche con category_id 1 e status SUSPENDED in ordine crescente | Lista di report diversi tra di loro|
| PR-08  | 1 | SUSPENDED | 2024-02-01 | 2024-03-01 | asc| Tutte le segnalazioni pubbliche con category_id 1 e status SUSPENDED con data compresa (estremi inclusi) tra 2024-02-01 e 2024-03-01 in ordine crescente | Lista di report diversi tra di loro|
| PR-09  | None | None | None | None | desc | Lista vuota | Lista vuota |
| PR-10  | 9999 | None | None | None | desc | Lista vuota | Lista di segnalazioni pubbliche con category_id diversa da 9999|
NOTA: PR-09 copre lo stesso input di PR-01 ma con fixture vuota, per verificare il comportamento in assenza di dati

### Boundary: 

**Boundary around "category_id":**

| TC    | category_id  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB01 |  1 | Exact boundary   | Lista di segnalazioni pubbliche con category_id 1 |
| PRB02 |  7 | Immediately above   | Lista vuota |
| PRB03 |  0 | Immediately below   | Lista vuota |
NOTA: considero come immediately above il 7 in quanto le categorie sono 6 e considero che gli id partano da 1

**Boundary around "date_from":**

| TC    | date_from  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB04 |  2024-02-01 00:00:00 | Exact boundary   | Lista di segnalazioni pubbliche con date da 2024-02-01 00:00:00 |
| PRB05 |  2024-02-01 00:00:01 | Immediately above   | Lista di segnalazioni pubbliche con date da 2024-02-01 00:00:01 |
| PRB06 |  2024-01-31 23:59:59 | Immediately below   | Lista di segnalazioni pubbliche con date da 2024-01-31 23:59:59 |

**Boundary around "date_to":**

| TC    | date_to  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB07 |  2024-02-01 00:00:00 | Exact boundary   | Lista di segnalazioni pubbliche con date fino a 2024-02-01 00:00:00 |
| PRB08 |  2024-02-01 00:00:01 | Immediately above   | Lista di segnalazioni pubbliche  con date fino a 2024-02-01 00:00:01 |
| PRB09 |  2024-01-31 23:59:59 | Immediately below   | Lista di segnalazioni pubbliche  con date fino a 2024-01-31 23:59:59 |

**Boundary around "date_from" and "date_to"**

| TC    | date_from  | date_to | Boundary covered  | Expected |
| :---- | :-------- |:--------|:------------------|:---------|
| PRB10 |  2024-02-01 00:00:00 | 2024-02-01 00:00:00 | Exact boundary   | Lista di segnalazioni pubbliche in data 2024-02-01 |
| PRB11 |  2024-03-01 00:00:00 | 2024-02-01 00:00:00   | Inverted interval | Lista vuota |


## 7 `participium.services.messaging_service.MessagingService.send_message`

Suggested test file: `test_send_message.py`

Prototype: `send_message(report: Report, sender: User, body: str) -> Message`

**Requisiti**:
- Se il mittente non può accedere al thread di messaggistica del report in questione il sistema deve generare un AuthorizationError.
- Se il testo del messaggio è vuoto il sistema deve generare un ValidationError.  
- Se il sistema non riesce a risolvere un destinatario del messaggio deve generare un ValidationError.
- Se sia l'utente che il report esistono e hanno un id valido, l'utente può accedere ai messaggi del report e il testo del messaggio non è vuoto, il sistema ritorna un oggetto di tipo Message.

**Criterio:** report

**Predicati:**

- report esiste -> valido 

**Criterio:** sender

**Predicati:**

- il sender non può accedere al thread
- il sender può accedere al thread

**Criterio:** body

**Predicati:**

- body è una stringa vuota --> non valido
- body è una stringa contenente solo caratteri di tipo whitespace --> non valido
- body contiene non solo caratteri di tipo whitespace --> valido

### Equivalence Classes

**Per report:**
- **EC1**: report valido

**Per sender:**
- **EC2**: sender non può accedere al thread
- **EC3**: sender può accedere al thread

**Per body:**
- **EC4**: body vuoto o con solo whitespace
- **EC5**: body valido

### Combinations of Equivalence Classes 

- EC1 x EC3 x EC5 -> oggetto _Message_ ritornato con successo
- EC1 x EC2 x EC5 -> _AuthorizationError_ perchè il sender non può accedere al thread
- EC1 x EC3 x EC4 -> _ValidationError_ causato da contenuto di body errato

Combinazioni possibili secondo i predicati:
Definiamo i seguenti oggetti da usare nei test:
- **user1**: utente con un campo id valido e uguale ad 1.
- **user2**: utente con un campo id valido e uguale ad 2.
- **report1**: report fatto dall'utente 1.

| TC-ID | report | sender | body | EC covered | Expected | Fixture |
| :---- | :----- | :----- | :--- | :--------- | :------- | :------ |
| MS01 | report1 | user1 | "" | EC1, EC3, EC4 | ValidationError | Body vuoto |
| MS02 | report1 | user2 | "ciao" | EC1, EC2, EC5 | AuthorizationError | Report non fatto dal mittente |
| MS03 | report1 | user1 | "ciao" | EC1, EC3, EC5 | Message | Tutto valido |

### Boundary

**Boundary around body content:**

| TC    | report | sender | body | Boundary covered | EC covered | Expected |
| :---- | :----- | :----- | :--- | :--------------- | :--------- | :------- |
| MSB01 | report1| user1  | "."  | Exact boundary | EC1, EC3, EC5 | Message |
| MSB02 | report1| user1  | " "  | Immediately below | EC1, EC3, EC4 | ValidationError |
| MSB03 | report1| user1  | ""   | Immediately below | EC1, EC3, EC4 | ValidationError |


## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

**Requisiti:**
- Il sistema deve permettere la verifica di una password in chiaro rispetto ad un hash memorizzato.
- Se la password corrisponde correttamente all'hash fornito il sistema deve restituire `True`.
- Se la password non corrisponde all'hash fornito il sistema deve restituire `False`.

**Criterio:** password

**Predicati:**

- password fornita --> valido

**Criterio:** password_hash

**Predicati:**

- Le hash della password corrispondono (password_hash == hash(password)) --> valido
- Le hash della password non corrispondono (password_hash != hash(password)) --> non valido


### Equivalence Classes

**Per password:**
- **EC1**: password != None

**Per password_hash:**
- **EC2**: hash corrispondono
- **EC3**: hash non corrispondono


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC1 x EC2 -> hash corrispondono, funzione ritorna vero
- EC1 x EC3 -> hash non corrispondono, funzione ritorna falso

Definiamo i seguenti oggetti da usare nei test:
- **pwd1**: stringa "pass123".
- **hash1**: hash corretto di "pass123".
- **hash2**: hash non corrispondente a "pass123".

| TC-ID | password | password_hash | EC covered | Expected | Fixture |
| :---- | :------- | :------------ | :--------- | :------- | :------ |
| VP01 | "pass123" | hash("pass123") | EC1, EC2 | True | Password e hash corretti |
| VP02 | "pass123" | hash("xxx") | EC1, EC3 | False | Hash errato |
| VP03 | ""        | hash("")        | Stringa vuota | EC1, EC2 | True |

### Boundary: password and hash comparison

**Boundary around matching:**

| TC    | password | password_hash | Boundary covered | EC covered | Expected |
| :---- | :------- | :------------ | :--------------- | :--------- | :------- |
| VP01  | "pass123" | hash("pass123") | Exact Boundary    | EC1, EC2  | True |
| VPB02 | "pass123" | hash("Pass123") | Immediately above | EC1, EC3 | False |
| VPB03 | "pass123" | hash("pass12")  | Immediately below | EC1, EC3 | False |
| VPB04 | "pass123" | hash("pass1234")| Immediately above | EC1, EC3 | False |

## 9 `participium.services.notification_service.NotificationService.create_notification`

Suggested test file: `test_create_notification.py`

Prototype: `create_notification(user: User | None, notification_type: NotificationType, title: str, body: str, report: Report | None = None) -> Notification | None`


**Requisiti:**
- Se user ha un id diverso da None --> Il sistema restituisce un oggetto Notification persistente.
- Se user ha id None-->Il sistema restituisce un None.
- Se tutti i cambi obbligatori sono presenti e validi e i campi opzionali sono validi o omessi --> Il sistema restituisce un oggetto Notification.


**Criterio:** user

**Predicati:**

- user è un utente con id-->valido
- user è None--> valido

**Criterio:** report

**Predicati:**

- report è fornito e con un valido id-->valido
- reort è None-->valido

### Equivalence Classes

**Per user:**
- **EC1**: user valido
- **EC2**: user is None

**Per report:**
- **EC3**: report valido
- **EC4**: report is None

### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC1 × EC3 -> Creazione con utente e report forniti
- EC1 × EC4 -> Creazione con utente fornito e report omesso
- EC2 × EC3 -> Creazione con utente omesso e report fornito
- EC2 × EC4 -> Creazione con utente e report omessi


| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :------- | :------ |
| CN01 | user1 | type1 | "Aggiornamento" | "Messaggio" | report1 | Notification | Utente presente, report presente |
| CN02 | user1 | type1 | "Aggiornamento" | "Messaggio" | None | Notification | Utente presente, report omesso |
| CN03 | None | type1 | "Aggiornamento" | "Messaggio" | report1 | None | Utente omesso, report presente|
| CN04 | None | type1 | "Aggiornamento" | "Messaggio" | None | None | Sia utente che report omessi |

### Boundary: text fields content


**Boundary around text field**

| TC-ID | user | notification_type | title | body | report | Boundary covered | Expected |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :--------------- | :------- |
| CNB01 | user1 | type1 | "A" |	"B" | report1 |	Minima lunghezza valida | Notification |
| CNB02	| user1 | type1 | "" | "B" | report1 | Stringa vuota per titolo | Notification |
| CNB03 | user1 | type1 | "A" |	"" | report1 | Stringa vuota per body |	Notification |

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

**Requisiti:**
- Se l'aggiornamento va a buon fine, il sistema deve restituire l'oggetto User aggiornato.
- Se il parametro username fornito è già in uso da un altro account all'interno del sistema, il sistema deve sollevare un'eccezione (ValidationError).
- I parametri opzionali omessi (None) non devono modificare il valore preesistente nel profilo dell'utente.

**Criterio**: username

**Predicati**:

- username è None -> valido
- username è fornito e non è in uso -> valido
- username è fornito ma è già in uso -> non valido

**Criterio**: first_name

**Predicati**:
- firstname è None -> valido
- firstname è fornito -> valido

**Criterio**: last_name

**Predicati**:
- lastname è None -> valido
- lastname è fornito -> valido

**Criterio**: email_notifications_enabled

**Predicati**:
- email_notifications_enabled è None -> valido
- email_notifications_enabled è fornito -> valido

**Criterio**: profile_picture

**Predicati**:
- profile_picture è None -> valido
- profile_picture è fornito -> valido

### Equivalence Classes

**Per username:**
- **EC1**: username valido
- **EC2**: username non valido

**Per first_name:**
- **EC3**: first_name valido

**Per last_name:**
- **EC4**: last_name valido

**Per email_notifications_enabled:**
- **EC5**: email_notifications_enabled valido

**Per profile_picture:**
- **EC6**: profile_picture valido

### Combinations of Equivalence Classes

- EC1 × EC3 × EC4 × EC5 × EC6 -> username disponibile
- EC2 × EC3 × EC4 × EC5 × EC6 -> username non valido

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected       | Fixture            |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- |:---------------|:-------------------|
| UP01 | user_target | "nuovo_username" | "Mario" | "Rossi" | True | valid_pic | User| User registrato|
| UP02 | user_target | "utente_occupato" | "Mario" | "Rossi" | True | valid_pic | ValidationError| User già esistente |
| UP03 | user_target | None | "Mario" |	"Rossi" | None | valid_pic | User| User registrato|
| UP04 | user_target | None | None | None |	None | None | User  | User registrato| 


### Boundary

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

**Requisiti:**
- Se l'aggiornamento va a buon fine, il sistema deve restituire l'oggetto User aggiornato.
- Se il parametro username fornito è già in uso da un altro account all'interno del sistema, il sistema deve sollevare un'eccezione (ValidationError).
- I parametri opzionali omessi (None) non devono modificare il valore preesistente nel profilo dell'utente.

**Criterio**: username

**Predicati**:

- username è None -> valido
- username è fornito e non è in uso -> valido
- username è fornito ma è già in uso -> non valido

**Criterio**: first_name

**Predicati**:
- firstname è None -> valido
- firstname è fornito -> valido

**Criterio**: last_name

**Predicati**:
- lastname è None -> valido
- lastname è fornito -> valido

**Criterio**: email_notifications_enabled

**Predicati**:
- email_notifications_enabled è None -> valido
- email_notifications_enabled è fornito -> valido

**Criterio**: profile_picture

**Predicati**:
- profile_picture è None -> valido
- profile_picture è fornito -> valido

### Equivalence Classes

**Per username:**
- **EC1**: username valido
- **EC2**: username non valido

**Per first_name:**
- **EC3**: first_name valido

**Per last_name:**
- **EC4**: last_name valido

**Per email_notifications_enabled:**
- **EC5**: email_notifications_enabled valido

**Per profile_picture:**
- **EC6**: profile_picture valido

### Combinations of Equivalence Classes

- EC1 × EC3 × EC4 × EC5 × EC6 -> username disponibile
- EC2 × EC3 × EC4 × EC5 × EC6 -> username non valido

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected       | Fixture            |
| :---- | :--- | :------- | :--------- | :-------- |:-------------| :-------------- |:---------------|:-------------------|
| UP01 | user_target | "nuovo_username" | "Mario" | "Rossi" | True| valid_pic | User| User registrato|
| UP02 | user_target | "utente_occupato" | "Mario" | "Rossi" | True | valid_pic | ValidationError| User già esistente |
| UP03 | user_target | None | "Mario" |"Rossi" | None| valid_pic | User| User registrato|
| UP04 | user_target | None | None | None | False| None | User  | User registrato| 


### Boundary

**Boundary around "username"**:

| TC    | user| username| first_name | last_name | email_notifications_enabled |profile_picture | Boundary covered  | Expected        |
|:------|:------------|:------|:-----------|:----------|:---------| :-------------- |:------|:--------|
| UPB01 | user_target | "a" | "b" | "c" | None|None | Exact Boundary    | User|
| UPB02 | user_target | " "|"Mario"|"Rossi"|None | None | Immediately below | User|
| UPB03 | user_target | "" | "" | "" |False| None | Immediately below | User|
| UPB04 | user_target | "existing_user"| "Luigi" | "Verdi"| None | None | Immediately above | ValidationError |
