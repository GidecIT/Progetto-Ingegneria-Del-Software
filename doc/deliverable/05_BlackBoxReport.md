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



| TC-ID | identifier | password | Expected | Fixture |
| :---- | :--------- | :------- | :------- | :------ |
| AU01 | `mario_r`             | `pass123` | User | Utente esiste ed è attivo, email verificata|
| AU02 | `mario.r@polito.it`   | `pass123` | User | Utente esiste ed è attivo, email verificata |
| AU03 | `mario_r`             | `wrong`   | AuthenticationError | Utente esiste ed è attivo, email verificata |
| AU04 | `mario.r@polito.it`   | `wrong`   | AuthenticationError | Utente esiste ed è attivo, email verificata |
| AU05 | `unknown_user`        | `pass123` | AuthenticationError | Non esiste un utente con questo username |
| AU06 | `unknown@mail.it`     | `pass123` | AuthenticationError | Non esiste un utente con questa email |
| AU07 | `mario_rossi`             | `pass123` | AuthenticationError | Utente esiste, ma non è attivo |
| AU08 | `mario_rossi@polito.it`             | `pass123` | AuthenticationError | Utente esiste, ma email non verificata |

### Boundary

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


**Boundary around User.is_active e User.is_mail_verified:**

| TC    | identifier | password  | stato User | Boundary covered  | Expected|
|:------|:-----------|:----------|:-----------|:------------------|:--------------------|
| AU01  | `mario_r`  | `pass123` | is_active == True AND is_email_verified == True | Exact boundary    | User |
| AUB08 | `mario_r`  | `pass123` | is_active == False | Immediately below | AuthenticationError |
| AUB09 | `mario_r`  | `pass123` | is_email_verified == False | Immediately below | AuthenticationError |

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

| TC-ID | value | Expected | Fixture |
| :---- | :---- | :------- | :------ |
| DT01 | `2002-12-31` | datetime | -  |
| DT02 | None | None     | - |
| DT03 | "" | ValueError | - |
| DT04 | `2056-31-04` | ValueError | - |
| DT05 | `1980-00-04` | ValueError | - |
| DT06 | `1998/03/04` | ValueError | - |
| DT07 | `2020-02-34` | ValueError | - |

### Boundary

**Boundary intorno a date valide**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB01 | 2024-02-29   | Exact boundary    | datetime |
| DTB02 | 2024-02-30   | Immediately above | ValueError |
| DTB03 | 2023-02-29   | Immediately below | ValueError |

**Boundary around months:**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB04 | 2024-12-31   | Exact boundary    | datetime |
| DTB05 | 2024-13-01   | Immediately above | ValueError |
| DTB06 | 2024-00-01   | Immediately below | ValueError |

**Boundary around days:**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| DTB07 | 2024-04-30   | Exact boundary    | datetime |
| DTB08 | 2024-04-31   | Immediately above | ValueError |
| DTB09 | 2024-04-00   | Immediately below | ValueError |


## 3 `participium.core.status_flow.ensure_transition_allowed`

Suggested test file: `test_status_flow.py`

Prototype: `ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus) -> bool`

Allowed transitions:<br>
`Pending  Approval -> Pending  Approval |  Assigned |  Rejected`; <br>
` Assigned ->  Assigned | In Progress | Suspended | Resolved`;<br>
`In Progress -> In Progress | Suspended | Resolved`;<br>
`Suspended -> Suspended | In Progress | Resolved`;<br>
` Rejected ->  Rejected`;<br>
`Resolved -> Resolved`.

**Requisiti:**

Il sistema deve controllare se la transizione di stato è permessa secondo il workflow definito.

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

- **EC1**: current_status == Pending  Approval
- **EC2**: current_status ==  Assigned
- **EC3**: current_status == In Progress
- **EC4**: current_status == Suspended
- **EC5**: current_status ==  Rejected
- **EC6**: current_status == Resolved

**Per next_status:**

- **EC7**: `next_status` è un valore di transizione permesso per lo stato corrente
- **EC8**: `next_status` è un valore di transizione non permesso per lo stato corrente


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- **EC1 × EC7** --> transizione ammessa per Pending  Approval
- **EC1 × EC8** --> transizione non ammessa per Pending  Approval
- **EC2 × EC7** --> transizione ammessa per  Assigned
- **EC2 × EC8** --> transizione non ammessa per  Assigned
- **EC3 × EC7** --> transizione ammessa per In Progress
- **EC3 × EC8** --> transizione non ammessa per In Progress
- **EC4 × EC7** --> transizione ammessa per Suspended
- **EC4 × EC8** --> transizione non ammessa per Suspended
- **EC5 × EC7** --> transizione ammessa per  Rejected
- **EC5 × EC8** --> transizione non ammessa per  Rejected
- **EC6 × EC7** --> transizione ammessa per Resolved
- **EC6 × EC8** --> transizione non ammessa per Resolved

### Combinations of Equivalence Classes 

| TC-ID | current_status | next_status | Expected | Fixture |
| :---- | :------------- | :---------- | :------- | :------ |
|TR1 | Pending  Approval | Pending  Approval | True | Esiste una segnalazione in stato Pending  Approval |
|TR2 | Pending  Approval |  Assigned | True |  Esiste una segnalazione in stato Pending  Approval|
|TR3 | Pending  Approval |  Rejected | True |  Esiste una segnalazione in stato Pending  Approval|
|TR4 | Pending  Approval | Resolved | ValidationError |  Esiste una segnalazione in stato Pending  Approval|
|TR5 |  Assigned |  Assigned | True |  Esiste una segnalazione in stato  Assigned |
|TR6 |  Assigned | In Progress | True | Esiste una segnalazione in stato  Assigned|
|TR7 |  Assigned | Suspended | True | Esiste una segnalazione in stato  Assigned|
|TR8 |  Assigned | Resolved | True | Esiste una segnalazione in stato  Assigned|
|TR9 |  Assigned | Pending  Approval | ValidationError | Esiste una segnalazione in stato  Assigned|
|TR10 | In Progress | In Progress | True | Esiste una segnalazione in stato In Progress |
|TR11 | In Progress | Suspended | True | Esiste una segnalazione in stato In Progress|
|TR12 | In Progress | Resolved | True | Esiste una segnalazione in stato In Progress|
|TR13 | In Progress |  Assigned | ValidationError | Esiste una segnalazione in stato In Progress|
|TR14 | Suspended | Suspended | True | Esiste una segnalazione in stato Suspended|
|TR15 | Suspended | In Progress | True| Esiste una segnalazione in stato Suspended|
|TR16 | Suspended | Resolved | True | Esiste una segnalazione in stato Suspended|
|TR17 | Suspended | Pending  Approval | ValidationError | Esiste una segnalazione in stato Suspended|
|TR18 |  Rejected |  Rejected | True | Esiste una segnalazione in stato  Rejected |
|TR19 |  Rejected |  Assigned | ValidationError | Esiste una segnalazione in stato  Rejected |
|TR20 | Resolved | Resolved | True | Esiste una segnalazione in stato Resolved |
|TR21 | Resolved | In Progress | ValidationError | Esiste una segnalazione in stato Resolved |

## 4 `participium.services.report_service.ReportService.create_report`

Suggested test file: `test_create_report.py`

Prototype: `create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report`

**Requisiti:**

Il sistema deve permettere la creazione di un report da parte di un utente autenticato.

- Se il category_id è None, malformato o si riferisce a una categoria sconosciuta o inattiva, il sistema deve restituire un errore di validazione (ValidationError).
- Se la descrizione o il titolo sono None, vuoti o contengono solo spazi, il sistema deve restituire un errore di validazione (ValidationError).
- Se le coordinate geografiche sono None o non possono essere convertite in valori numerici, il sistema deve restituire un errore di validazione (ValidationError).
- Se la lista di foto contiene zero foto valide o più di 3 foto valide, il sistema deve restituire un errore di validazione (ValidationError).
- Se tutti i campi sono validi, il sistema deve restituire un oggetto di tipo Report.

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
- title e descrizione sono stringhe non vuote --> valido

**Criterio:** latitude / longitude

**Predicati:**
- latitude o longitude è None --> non valido
- latitude o longitude non possono essere convertiti in valori numerici --> non valido
- latitude e longitude sono convertibili in valori numerici validi --> valido

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

**Per category_id:**
- **EC1**: category_id non valido
- **EC2**: category_id è valido e attivo

**Per title e description:**
- **EC3**: title o description non valido
- **EC4**: title e description sono validi

**Per latitude/longitude:**
- **EC5**: latitude o longitude non validi
- **EC6**: latitude e longitude validi

**Per photos:**
- **EC7**: numero di foto non valido
- **EC8**: 1 <= numero di foto <= 3

**Per is_anonymous:**
- **EC9**: is_anonymous è True o False --> valido

### Combinations of Equivalence Classes 
- EC2 x EC4 x EC6 x EC8 x EC9 --> Report creato con successo
- EC1 x EC4 x EC6 x EC8 x EC9 --> Report non creato, category_id non valido
- EC2 x EC3 x EC6 x EC8 x EC9 --> Report non creato, title o description non validi
- EC2 x EC4 x EC5 x EC8 x EC9 --> Report non creato, latitude o longitude non validi
- EC2 x EC4 x EC6 x EC7 x EC9 --> Report non creato, numero di foto non valido
  
<br>
Test realizzati considerando le 10 categorie descritte nella specifica iniziale, considerando gli id associati da 0 a 9.
<br><br>

| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | Expected | Fixture |
| :---- | :------- | :---------- | :---- | :---------- | :------- | :-------- | :----- | :----------- | :------- | :------ |
|CR1| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | Report |  L'utente è autenticato, la categoria 4 è valida e attiva |
|CR2| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | True | Report |  L'utente è autenticato, la categoria 4 è valida e attiva |
|CR3| user | 5 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | True | ValidationError |  L'utente è autenticato, la categoria 5 è inattiva |
|CR4| user | None | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | True | ValidationError |  L'utente è autenticato |
|CR5| user | "" | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | ValidationError |  L'utente è autenticato | 
|CR6| user | df | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | True | ValidationError |  L'utente è autenticato|
|CR7| user | 4 | "" | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [foto_buca.jpg] | False | ValidationError |  L'utente è autenticato, la categoria 4 è valida e attiva|
|CR8| user | 4 | Buca profonda |None| 45.0710 | 7.6856 | [foto_buca.jpg] | False | ValidationError |  L'utente è autenticato, la categoria 4 è valida e attiva |
|CR9| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | "" | [foto_buca.jpg] | True | ValidationError |  L'utente è autenticato, la categoria 4 è valida e attiva |
|CR10| user | 4 | Buca profonda | Buca profonda in piazza Castello| Quarantacinque | 7.6856 | [foto_buca.jpg] | False | ValidationError |  L'utente è autenticato, la categoria 4 è valida e attiva |
|CR11| user | 4 | Buca profonda | Buca profonda in piazza Castello| 45.0710 | 7.6856 | [] | False | ValidationError |  L'utente è autenticato, la categoria 4 è valida e attiva |

### Boundary

**Boundary around "category_id":**

| TC    | category_id | Boundary covered  | Expected        |
| :---- | :---------- |:------------------|:----------------|
| CRB01 | 0           | Exact boundary    | Report          |
| CRB02 | 9           | Exact boundary    | Report          |
| CRB04 | -1          | Immediately below | ValidationError |
| CRB05 | 10          | Immediately above | ValidationError |


**Boundary around "title e description":**

| TC    | title | description | Boundary covered  | Expected |
| :---- | :------------ | :----------------- |:------------------|:---------|
| CRB06 | a  | a | Exact boundary    | Report |
| CRB07 | ""  | a | Immediately below    | ValidationError |
| CRB08 | a  | "" | Immediately below    | ValidationError |

**Boundary around "latitude/longitude":**

| TC    | latitude | longitude | Boundary covered  | Expected |
| :---- | :----------------- |:-------- | :------------------|:---------|
| CRB09 | 0.0  | 0.0  | Exact boundary    | Report |
| CRB10 | "" | 0.0 | Immediately below    | ValidationError |
| CRB11 | 0.0 | "" | Immediately below    | ValidationError |

**Boundary around "photos":**

| TC    | photos | Boundary covered  | Expected |
| :---- | :----- |:------------------|:---------|
| CR01 | [foto_buca.jpg] | Exact boundary    | Report|
| CR11 | [] | Immediately below    | ValidationError |
| CRB12 | [foto1.jpg, foto2.jpg, foto3.jpg] | Exact boundary    | Report |
| CRB13 | [foto1.jpg, foto2.jpg, foto3.jpg, foto4.jpg] | Immediately above | ValidationError |

## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`


**Requisiti:** <br>
Il sistema deve potere permettere l'aggiornamento di stato di un report.<br>

- Se l'operatore non ha i permessi adatti alla modifica del report (User.Role != Role.OPERATOR AND User.Role != Role.ADMIN), il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se l'operatore è None, il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se l'operatore tenta di aggiornare un report al di fuori della propria categoria assegnata, il sistema restituisce un errore di autorizzazione (AuthorizationError).
- Se il report non esiste, il sistema restituisce errore (NotFoundError).
- Se next_status_value non rispetta l'ordine del workflow o non esiste, il sistema restituisce un errore di validazione (ValidationError).
- Se l'operatore respinge il report (next_status_value == Rejected) senza una nota, il sistema restituisce un errore di validazione (ValidationError)
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
- **EC7**: note vuota o None
- **EC8**: note valida

**Per operator.category_id**
- **EC9**: operator.category_id == report.category_id
- **EC10**: operator.category_id != report.category_id

### Combinations of Equivalence Classes

- EC1 x EC3 x EC5 x EC8 x EC9 --> Aggiornamento riuscito
- EC1 x EC3 x EC5 x EC7 x EC9 --> Aggiornamento riuscito (senza nota)
- EC2 x EC3 x EC5 x EC7 x EC9 --> Report inesistente
- EC1 x EC4 x EC5 x EC8 x EC9 --> Operatore non autorizzato
- EC1 x EC3 x EC6 x EC8 x EC9 --> Transizione di stato non ammessa
- EC1 x EC3 x EC5 x EC7 x EC9 --> Nota mancante per report rifiutato
- EC1 x EC3 x EC5 x EC7 x EC10 --> Categoria operatore non corrispondente a quella del report

| TC-ID | report_id | operator | next_status_value | note                    | Expected           | Fixture |
| :---- | :-------- | :------- | :---------------- |:------------------------|:-------------------|:-----------|
| US01  | 10 | op_cat_1 | Assigned | None | Report | La segnalazione è in stato Pending Approval, l'operatore ha i permessi |
| US02  | 10 | op_cat_1 | Assigned | "Report già segnalato"  | Report | La segnalazione è in stato Pending Approval, l'operatore ha i permessi |
| US03  | 999 | op_cat_1 | Assigned | None | NotFoundError | La segnalazione non esiste |
| US04  | 10 | user_no_perm | Assigned | None | AuthorizationError | La segnalazione esiste, l'operatore non ha i permessi  |
| US05  | 10 | op_cat_2 | Assigned | None | AuthorizationError | La segnalazione esiste, l'operatore non appartiene alla stessa categoria del report |
| US06  | 10 | op_cat_1 | Rejected | None | ValidationError | La segnalazione esiste, l'operatore ha i permessi |
| US07  | 10 | op_cat_1 | Rejected | "Lo stato non mi piace" | ValidationError | La segnalazione è in stato Resolved, l'operatore ha i permessi |

### Boundary

**Boundary around report_id:**

| TC | report_id | operator | next_status_value | Boundary covered  | Expected |
| :--- |:----------| :--- | :--- |:-----| :--- |
| USB01 | 1 | op_valido  |   Assigned | Exact boundary    | Report |
| USB02 | -1 | op_valido |   Assigned | Immediately below | NotFoundError |


**Boundary around next_status_value and note:**

| TC    | report_id | operator | next_status_value | note | Boundary covered  | Expected |
|:------| :--- | :--- |:-------|:-----|:------| :--- |
| USB03 | 10 | op_valido | Rejected| "N"  | Exact boundary    | Report |
| USB04 | 10 | op_valido | Rejected| None | Immediately below | ValidationError |
| USB05 | 10 | op_valido | Rejected| ""   | Immediately below | ValidationError |


**Boundary around "operator.category_id" e "report.category_id":**

| TC    | operator.category_id | report.category_id | Boundary covered  | Expected        |
|:------|:-------|:-------|:------------------|:-------|
| USB06 | 0| 0 | Exact boundary    | Report |
| USB07 | -1| 0 | Immediately below | ValidationError |
| USB08 | 0| 1 | Immediately above | ValidationError |


## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

**Requisiti:**

Il sistema deve restituire una lista di segnalazioni pubbliche basata su filtri opzionali<br>

- Se nessun filtro è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche
- Se category_id è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con categoria uguale a category_id
- Se status è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con stato uguale a status
- Se date_from è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con data di creazione uguale o successiva a date_from
- Se date_to è fornito, il sistema deve restituire una lista con tutte le segnalazioni pubbliche con data di creazione uguale o precedente a date_to
- Se sort è fornito, il sistema deve restituire una lista con le segnalazioni pubbliche ordinate in base al parametro sort (di default decrescente)

**Criterio:** category_id

**Predicati:**
- category_id è presente --> valido
- category_id non è presente --> valido (filtro assente)

**Criterio:** status 

**Predicati:**
- status è uno degli stati possibili --> valido 
- status non è presente --> valido (filtro assente)

**Criterio:** date_from

**Predicati:**
- date_from non è presente --> valido (filtro assente) 
- date_from è presente --> valido 

**Criterio:** date_to 

**Predicati:**
- date_to non è presente --> valido (filtro assente) 
- date_to è presente --> valido 

**Criterio:** sort 

**Predicati:**
- sort == "desc" --> valido 
- sort == "asc" --> valido 

### Equivalence Classes

**Per category_id**
- **EC1**: category_id valido 

**Per status**
- **EC2**: status è valido 

**Per date_from**
- **EC3**: date_from è valida

**Per date_to**
- **EC4**: date_to è valida

**Per sort**
- **EC5**: ordinamento valido


### Combinations of Equivalence Classes 
- EC1 x EC2 x EC3 x EC4 x EC5 --> Lista di segnalazioni pubbliche filtrata e ordinata

Nota: la funzione 'list_public_reports' ritorna sempre list[Report]. Nella tabella seguente viene utilizzata la colonna "Expected" per descrivere il contenuto atteso della lista in riferimento ai filtri applicati e alla loro combinazione.

| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
|-------|-------------|--------|-----------|---------|------|----------|---------|
| PR01  | None | None | None | None | desc | Segnalazioni pubbliche ordinate in modo decrescente | Esistono segnalazioni pubbliche |
| PR02  | 1 | None | None | None | asc | Segnalazioni pubbliche con category_id==1 in ordine crescente|  Esistono segnalazioni pubblicheo|
| PR03  | None |  Assigned | None | None | desc | Segnalazioni pubbliche con status  Assigned in ordine decrescente |  Esistono segnalazioni pubblicheo|
| PR04  | None | None | 2024-02-01 | None | desc | Solo le segnalazioni pubbliche dopo la data 2024-02-01 (compresa) in ordine decrescente |  Esistono segnalazioni pubbliche|
| PR05  | None | None | None | 2024-02-01 | desc | Solo le segnalazioni pubbliche prima della data 2024-02-01 (compresa) in ordine decrescente |  Esistono segnalazioni pubbliche|
| PR06  | None | None | 2024-02-01 | 2024-03-01 | desc | Tutte le segnalazioni pubbliche dopo la data 2024-02-01 (compresa) e prima della data 2024-03-01 (compresa) in ordine decrescente |  Esistono segnalazioni pubbliche|
| PR07  | 1 | Suspended | None | None | asc| Tutte le segnalazioni pubbliche con category_id 1 e status Suspended in ordine crescente |  Esistono segnalazioni pubbliche|
| PR08  | 1 | Suspended | 2024-02-01 | 2024-03-01 | asc| Tutte le segnalazioni pubbliche con category_id 1 e status Suspended con data compresa (estremi inclusi) tra 2024-02-01 e 2024-03-01 in ordine crescente |  Esistono segnalazioni pubbliche|
| PR09  | None | None | None | None | desc | Lista vuota | Lista vuota |
| PR10  | 9999 | None | None | None | desc | Lista vuota | Esistono segnalazioni pubbliche, nessuna segnalazione con category_id uguale a 9999|

NOTA: PR09 copre lo stesso input di PR01 ma con fixture vuota, per verificare il comportamento in assenza di dati

### Boundary 

**Boundary around "category_id":**

| TC    | category_id  | Boundary covered  | Expected |
| :---- | :-------- |:------------------|:---------|
| PRB01 |  0 | Exact boundary   | Lista di segnalazioni pubbliche con category_id 0 |
| PRB02 |  10 | Immediately above   | Lista vuota |
| PRB03 |  -1 | Immediately below   | Lista vuota |

**Boundary around "date_from" e "date_to":**

**Boundary intorno a date valide**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| PRB04 | 2024-02-29   | Exact boundary    | datetime |
| PRB05 | 2024-02-30   | Immediately above | ValueError |
| PRB06 | 2023-02-29   | Immediately below | ValueError |

**Boundary around months:**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| PRB07 | 2024-12-31   | Exact boundary    | datetime |
| PRB08 | 2024-13-01   | Immediately above | ValueError |
| PRB09 | 2024-00-01   | Immediately below | ValueError |

**Boundary around days:**

| TC    | date        | Boundary covered  | Expected |
|:------|:-------------|:------------------|:---------|
| PRB10 | 2024-04-30   | Exact boundary    | datetime |
| PRB11 | 2024-04-31   | Immediately above | ValueError |
| PRB12 | 2024-04-00   | Immediately below | ValueError |


## 7 `participium.services.messaging_service.MessagingService.send_message`

Suggested test file: `test_send_message.py`

Prototype: `send_message(report: Report, sender: User, body: str) -> Message`

**Requisiti**:

Il sistema deve permettere l'invio di un messaggio.

- Se il mittente non può accedere al thread di messaggistica del report in questione il sistema deve generare un errore di validazione (ValidationError).
- Se il testo del messaggio è vuoto il sistema deve generare un errore di validazione (ValidationError). 
- Se il sistema non riesce a risolvere un destinatario del messaggio deve generare un errore di validazione (ValidationError).
- Se sia l'utente che il report esistono e hanno un id valido, l'utente può accedere ai messaggi del report e il testo del messaggio non è vuoto, il sistema ritorna un oggetto di tipo Message.

**Criterio:** report

**Predicati:**

- report esiste --> valido 

**Criterio:** sender

**Predicati:**

- il sender non può accedere al thread --> non valido
- il sender può accedere al thread --> valido

**Criterio:** body

**Predicati:**

- body è una stringa vuota --> non valido
- body è una stringa contenente solo caratteri di tipo whitespace --> non valido
- body contiene caratteri validi --> valido

**Criterio:** recipient_id

**Predicati:**
- recipient_id non risolvibile --> non valido
- recipient_id risolvibile --> valido

### Equivalence Classes

**Per report:**
- **EC1**: report valido

**Per sender:**
- **EC2**: sender non può accedere al thread
- **EC3**: sender può accedere al thread

**Per body:**
- **EC4**: body non valido
- **EC5**: body valido

**Per recipient_id:**
- **EC6**: recipient_id non risolvibile
- **EC7**: recipient_id risolvibile

### Combinations of Equivalence Classes 

- EC1 x EC3 x EC5 x EC7 --> Messaggio inviato con successo
- EC1 x EC2 x EC5 x EC7 --> Sender non può accedere al thread
- EC1 x EC3 x EC4 x EC7 --> Body non valido
- EC1 x EC3 x EC5 x EC6 --> Recipient_id non risolvibile

| TC-ID | report | sender | body | Expected | Fixture |
| :---- | :----- | :----- | :--- | :------- | :------ |
| MS01 | report1 | user1 | "Segnalazione"    | Message | Segnalazione esistente, sender autorizzato, recipient_id risolvibile |
| MS02 | report1 | user2 | "Segnalazione" | AuthorizationError | Segnalazione esistente, sender non autorizzato, recipient_id risolvibile |
| MS03 | report1 | user1 | "" | ValidationError | Segnalazione esistente, sender autorizzato, recipient_id risolvibile |
| MS04 | report1 | user1 | "   " | ValidationError | Segnalazione esistente, sender autorizzato, recipient_id risolvibile |
| MS05 | report1 | user1 | None | ValidationError | Segnalazione esistente, sender autorizzato, recipient_id risolvibile |
| MS06 | report1 | user1 | "Segnalazione" | ValidationError | Segnalazione esistente, sender autorizzato, recipient_id non risolvibile |

### Boundary

**Boundary around body content:**

| TC    | report | sender | body | Boundary covered  | Expected |
|:------| :----- | :----- | :--- |:------------------| :--------- |
| MSB01 | report1 | user1 | "a"  | Exact boundary    | Message |
| MSB03 | report1 | user1 | ""   | Immediately below | ValidationError |
| MSB04 | report1 | user1 | "   "  | Immediately below| ValidationError |


## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

**Requisiti:**

Il sistema deve permettere la verifica di una password in chiaro rispetto a un hash memorizzato.

- Se la password corrisponde correttamente all' hash fornito il sistema deve restituire `True`.
- Se la password non corrisponde all' hash fornito il sistema deve restituire `False`.

**Criterio:** password

**Predicati:**

- password fornita --> valido

**Criterio:** password_hash

**Predicati:**

- password hash fornita --> valido

### Equivalence Classes

**Per password:**
- **EC1**: password valida

**Per password_hash:**
- **EC2**: password hash valida


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC1 x EC2 --> Verifica password riuscita o fallita a seconda della corrispondenza tra password e hash

| TC-ID | password | password_hash | Expected | Fixture |
| :--- | :-------- | :------------    | :---- | :------ |
| VP01 | "pass123" | hash("pass123")  | True  | - |
| VP02 | "pass123" | hash("xxx")      | False | - |


### Boundary

**Boundary around password and password_hash:**

| TC    | password | password_hash | Boundary covered | Expected |
|:------| :------- | :------------ | :--------------- | :------- |
| VPB01 | "pass123" | hash("pass123") | Exact Boundary    | True |
| VPB02 | "pass123" | hash("Pass123") | Immediately above | False |
| VPB03 | "pass123" | hash("pass12")  | Immediately below | False |
| VPB04 | "pass123" | hash("pass1234")| Immediately above | False |

## 9 `participium.services.notification_service.NotificationService.create_notification`

Suggested test file: `test_create_notification.py`

Prototype: `create_notification(user: User | None, notification_type: NotificationType, title: str, body: str, report: Report | None = None) -> Notification | None`


**Requisiti:**

Il sistema deve permettere la creazione di una notifica, opzionalmente associata a una segnalazione.

- Se user ha un id diverso da None, il sistema restituisce un oggetto Notification persistente.
- Se user ha id None, il sistema restituisce un None.
- Se report è fornito, la notifica è associata alla segnalazione.


**Criterio:** user

**Predicati:**

- user è fornito --> valido
- user è None --> valido

**Criterio:** notification_type

**Predicati:**

- notification_type è uno dei tipi di notifica definiti --> valido

**Criterio:** title e body

**Predicati:**

- title e body sono stringhe --> valido

**Criterio:** report

**Predicati:**

- report è fornito e con un valido id --> valido
- report è None --> valido

### Equivalence Classes

**Per user:**
- **EC1**: user valido

**Per title e body:**
- **EC2**: title e body validi

**Per notification_type:**
- **EC3**: notification_type valido

**Per report:**
- **EC4**: report valido


### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

- EC1 × EC2 x EC3 x EC4 --> Notifica creata con successo

| TC-ID | user | notification_type | title | body| report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :---| :----- | :------- | :------ |
| CN01 | user1 | MESSAGE | Aggiornamento | "Messaggio" | report1 | Notification | Utente esiste, Segnalazione presente |
| CN02 | user1 | MESSAGE | Aggiornamento | "Messaggio" | None | Notification | utente esiste|
| CN03 | None | MESSAGE | Aggiornamento | "Messaggio" | report1 | None | Segnalazione presente|
| CN04 | None | MESSAGE | Aggiornamento | "Messaggio" | None | None | - |

### Boundary

**Boundary around title and body**

| TC    | user | title | body | Boundary covered  | Expected |
| :---- | :--- | :---- | :--- | :------------------| :------- |
| CNB01 | user1 | "a"  | "b"  | Exact boundary    | Notification |
| CNB02 | user1 | ""   | "b"  | Immediately below | Notification |
| CNB03 | user1 | "a"  | ""   | Immediately below | Notification |


## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

**Requisiti:**

Il sistema deve permettere l'aggiornamento dei campi modificabili del profilo utente.

- Se l'aggiornamento va a buon fine, il sistema deve restituire l'oggetto User aggiornato.
- Se il parametro username fornito è già in uso da un altro account all'interno del sistema, il sistema deve sollevare un'eccezione (ValidationError).
- I parametri opzionali omessi (None) non devono modificare il valore preesistente nel profilo dell'utente.

**Criterio**: user

**Predicati**:
- user è fornito --> valido

**Criterio**: username

**Predicati**:

- username è None --> valido
- username è fornito e non è in uso --> valido
- username è fornito ma è già in uso --> non valido

**Criterio**: first_name

**Predicati**:
- firstname è None --> valido
- firstname è fornito --> valido

**Criterio**: last_name

**Predicati**:
- lastname è None --> valido
- lastname è fornito --> valido

**Criterio**: email_notifications_enabled

**Predicati**:
- email_notifications_enabled è None --> valido
- email_notifications_enabled è fornito --> valido

**Criterio**: profile_picture

**Predicati**:
- profile_picture è None --> valido
- profile_picture è fornito --> valido

### Equivalence Classes

**Per user:**
- **EC1**: user valido

**Per username:**
- **EC2**: username valido
- **EC3**: username non valido

**Per first_name:**
- **EC4**: first_name valido

**Per last_name:**
- **EC5**: last_name valido

**Per email_notifications_enabled:**
- **EC6**: email_notifications_enabled valido

**Per profile_picture:**
- **EC7**: profile_picture valido

### Combinations of Equivalence Classes

- EC1 × EC2 x EC4 x EC5 x EC6 x EC7 --> Profilo aggiornato con successo
- EC1 × EC3 x EC4 x EC5 x EC6 x EC7 --> Username già in uso

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
| UP01 | user1 | "nuovo" | "Mario" | "Rossi" | True| valid_pic | User| User1 esiste|
| UP02 | user2 | "nuovo" | "Mario" | "Rossi" | True | valid_pic | ValidationError| User2 esiste, l'username "nuovo" è già in uso|
| UP03 | user1 | None    | "Mario" |"Rossi"  | None | valid_pic | User  | User1 esiste|
| UP04 | user1 | None     | None   | None    | False| None      | User  | User1 esiste| 


### Boundary

**Boundary around "username"**:

| TC    | user | username | Boundary covered  | Expected |
| :---- | :--- | :------- | :------------------| :------- |
| UPB01 | user1 | "a"  | Exact boundary    | User |
| UPB02 | user1 | ""   | Immediately below | User |
| UP04  | user1 | None  | Immediately below | User |

**Boundary around "first_name"**:

| TC    | user | first_name | Boundary covered  | Expected |
| :---- | :--- | :--------- | :------------------| :------- |
| UPB03 | user1 | "a"  | Exact boundary    | User |
| UPB04 | user1 | ""   | Immediately below | User |
| UP04  | user1 | None  | Immediately below | User |

**Boundary around "last_name"**:

| TC    | user | last_name | Boundary covered  | Expected |
| :---- | :--- | :-------- | :------------------| :------- |
| UPB05 | user1 | "a"  | Exact boundary    | User |
| UPB06 | user1 | ""   | Immediately below | User |
| UP04  | user1 | None  | Immediately below | User |