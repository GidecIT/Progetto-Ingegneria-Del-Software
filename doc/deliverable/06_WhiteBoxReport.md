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

- ![](../data/img/xxx.xxx)

### Atomic Conditions

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test

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

### Structural Lower Bound

### Node Coverage

### Edge Coverage

### Condition Coverage

### Loop Coverage

### Path Coverage

### Minimal Suite Test

