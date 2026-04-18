## 1 `participium.services.auth_service.AuthService.authenticate`

**Suggested test file:** `test_authenticate.py`

**Prototype:** `authenticate(identifier: str, password: str) -> User`

**Requisiti:**

- Il sistema deve permettere all'utente di autenticarsi, accettando come identifier sia il suo username che il suo indirizzo email fornito, oltre alla propria password.
- Il sistema deve invalidare la richiesta se identifier o password non sono forniti (null).
- L'accesso è considerato valido solo se esiste una corrispondenza univoca nel database tra l'identificativo fornito e la password (hash) associata a quell'utente specifico.
- In caso di credenziali valide, il sistema deve restituire l'oggetto User corrispondente.
- In caso di credenziali non valide (identifier inesistente o password errata), il sistema deve restituire un errore di autenticazione.

**Criterio:** identifier

**Predicati:**

- identifier == null --> non valido
- identifier != null & identifier == any User.username --> valido
- identifier != null & identifier != any User.username --> non valido
- identifier != null & identifier == any User.email --> valido
- identifier != null & identifier != any User.email --> non valido

**Criterio:** password

**Predicati:**

(NOTA p.4: serve al caso in cui identifier sia vuoto o non esistente (d.c. oggetto 'User' nullo o non trovato), escludendo la ricerca di una qualsiasi password corrispondente in tutto il DB come invece facciamo per le EC di identifier)

- password == null --> non valido
- password != null & password == User.password_hash --> valida
- password != null & password != User.password_hash --> non valida
- password != null & (User == null) --> non valida 

### Equivalence Classes

**Per identifier:**

- **EC1**: `identifier == null`
- **EC2**: `identifier != null` & `identifier == any User.username`
- **EC3**: `identifier != null` & `identifier != any User.username`
- **EC4**: `identifier != null` & `identifier == any User.email`
- **EC5**: `identifier != null` & `identifier != any User.email`

**Per password:**
- **EC6**: `password == null`
- **EC7**: `password != null` & `password == User.password_hash`
- **EC8**: `password != null` & `password != User.password_hash`
- **EC9**: `password != null` & `User == null`

### Combinations of Equivalence Classes 

Combinazioni possibili secondo i predicati:

    EC1 × EC6
    EC1 × EC9
    EC2 × EC6
    EC2 × EC7
    EC2 × EC8
    EC3 × EC6
    EC3 × EC9
    EC4 × EC6
    EC4 × EC7
    EC4 × EC8
    EC5 × EC6
    EC5 × EC9

| TC   | identifier        | password  | EC covered | Expected | Fixture                                             |
|:-----|:------------------|:----------|:-----------|:---------|:----------------------------------------------------|
| AU01 | `mario_r`         | `pass123` | EC2, EC7   | User obj | Identifier (username) e password corretti|
| AU02 | `m.r@polito.it`   | `pass123` | EC4, EC7   | User obj | Identifier (email) e password corretti|
| AU03 | `mario_r`         | `wrong`   | EC2, EC8   | None | Identifier (username) corretto, password errata  |
| AU04 | `m.r@polito.it`   | `wrong`   | EC4, EC8   | None | Identifier (email) corretto, password errata |
| AU05 | `mario_r`         | null      | EC2, EC6   | None | Identifier (username) corretto, password omessa |
| AU06 | `m.r@polito.it`   | null      | EC4, EC6   | None | Identifier (email) corretto, password omessa  |
| AU07 | `unknown_user`    | `pass123` | EC3, EC9   | None| Identifier (username) inesistente, password fornita |
| AU08 | `unknown@mail.it` | `pass123` | EC5, EC9   | None| Identifier (email), password fornita  |
| AU09 | `unknown_user`    | null      | EC3, EC6   | None| Identifier (username), password omessa    |
| AU10 | `unknown@mail.it` | null      | EC5, EC6   | None| Identifier (email), password omessa |
| AU11 | null              | `pass123` | EC1, EC9   | None| Identifier omesso, password fornita  |
| AU12 | null              | nul`      | EC1, EC6   | None| Entrambi i campi omessi |

### Boundary: identifier recognition

**Boundary around "username":**

| TC    | identifier | password  | Boundary covered  | Expected |
| :---- | :--------- | :-------- |:------------------|:---------|
| AUB01 | `mario_r`  | `pass123` | Exact boundary    | User obj |
| AUB02 | `mario_rx` | `pass123` | Immediately above | None     |
| AUB03 | `mario_`   | `pass123` | Immediately below | None     |
| AUB04 | `MARIO_R`  | `pass123` | Immediately above  | None     |

**Boundary around "email":**

| TC    | identifier          | password  | Boundary covered  | Expected |
| :---- | :------------------ | :-------- |:------------------|:-----|
| AUB05 | `m.r@polito.it`     | `pass123` | Exact boundary    | User obj |
| AUB06 | `m.r@polito.it.com` | `pass123` | Immediately above | None |
| AUB07 | `m.r@polito.i`      | `pass123` | Immediately below | None |
| AUB08 | `m.r@polito.it `    | `pass123` | Immediately above | None |

### Boundary: password comparison

| TC    | identifier | password   | Boundary covered   | Expected |
| :---- | :--------- | :--------- |:-------------------|:---------|
| AUB09 | `mario_r`  | `pass123`  | Exact boundary     | User obj |
| AUB10 | `mario_r`  | `Pass123`  | Immediately below  | None     |
| AUB11 | `mario_r`  | `pass12`   | Immediately below  | None     |
| AUB12 | `mario_r`  | `pass1234` | Immediately above  | None     |
| AUB13 | `mario_r`  | `p@ss123`  | Immediately below  | None     |

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
- current_status != any ReportStatus || current_status == null --> non valido

**Criterio: next_status**

**Predicati:**

- next_status == stato permesso dalle regole nel workflow per current_status --> valido
- next_status == stato NON permesso dal workflow nel workflow current_status --> non valido
- next_status != any ReportStatus || next_status == null --> non valido

### Equivalence Classes

**Per current_status:**

- **EC01**: `current_status == PENDING_APPROVAL`
- **EC02**: `current_status == ASSIGNED`
- **EC03**: `current_status == IN_PROGRESS`
- **EC04**: `current_status == SUSPENDED`
- **EC05**: `current_status == REJECTED`
- **EC06**: `current_status == RESOLVED`
- **EC07**: `current_status != any ReportStatus` || `current_status == null`

**Per next_status:**

- **EC08**: `next_status` è un valore permesso per lo stato corrente
- **EC09**: `next_status` è un valore NON permesso per lo stato corrente
- **EC10**: `next_status != any ReportStatus` || `next_status == null`

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
| TR13 | null               | `ASSIGNED`        | EC07, EC08 | `ValidationError` | Current status omesso                  |
| TR14 | `INVALID`          | `ASSIGNED`        | EC07, EC08 | `ValidationError` | Current status non esistente           |
| TR15 | `PENDING_APPROVAL` | null              | EC01, EC10 | `ValidationError` | Next status omesso                     |
| TR16 | `PENDING_APPROVAL` | `UNKNOWN`         | EC01, EC10 | `ValidationError` | Next status non esistente              |

### Boundary: workflow transitions

**Boundary around allowed transitions:**

| TC    | current_status     | next_status       | Boundary covered| EC Covered | Expected          |
| :---- |:-------------------|:------------------|:-----------------|:-----------|:------------------|
| TRB01 | `PENDING_APPROVAL` | `PENDING_APPROVAL`| Exact boundary (self) | EC1, EC8   | `True`|
| TRB02 | `PENDING_APPROVAL` | `REJECTED`        | Exact boundary     | EC1, EC8   | `True`|
| TRB03 | `ASSIGNED`         | `RESOLVED`        | Exact boundary     | EC2, EC8   | `True`|
| TRB04 | `SUSPENDED`        | `IN_PROGRESS`     | Exact boundary    | EC4, EC8   | `True`|
| TRB05 | null               | `ASSIGNED`        | Immediately below | EC7, EC8   | `ValidationError` |
| TRB06 | `PENDING_APPROVAL` | null              | Immediately below | EC1, EC10  | `ValidationError` |
| TRB07 | `INVALID_STATE`    | `ASSIGNED`        | Immediately below | EC7, EC8   | `ValidationError` |
| TRB08 | `PENDING_APPROVAL` | `UNKNOWN`         | Immediately below | EC1, EC10  | `ValidationError` |
| TRB09 | `REJECTED`         | `RESOLVED`        | Immediately above | EC5, EC9   | `ValidationError` |

## 4 `participium.services.report_service.ReportService.create_report`

Suggested test file: `test_create_report.py`

Prototype: `create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report`

| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | Expected | Fixture |
| :---- | :------- | :---------- | :---- | :---------- | :------- | :-------- | :----- | :----------- | :------- | :------ |
|  |  |  |  |  |  |  |  |  |  |  |

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

| TC-ID | report | sender | body | Expected | Fixture |
| :---- | :----- | :----- | :--- | :------- | :------ |
|  |  |  |  |  |  |

## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

| TC-ID | password | password_hash | Expected | Fixture |
| :---- | :------- | :------------ | :------- | :------ |
|  |  |  |  |  |

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
