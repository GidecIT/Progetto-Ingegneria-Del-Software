## Panoramica dei Problemi Rilevati
Durante la suite di test automatizzati, sono stati isolati tre comportamenti del backend non conformi alle specifiche Swagger. Il backend è tollerante verso input errati, rispondendo con `200 OK` invece di bloccare la richiesta con un `400 Bad Request`.

---

## Tabella Riassuntiva dei Bug

| Endpoint | Input Inviato | Stato Atteso (Swagger) | Stato Reale (Backend) | Gestione lato backend                                  |
| :--- | :--- | :--- | :--- |:-------------------------------------------------------|
| **`GET /stats/public`** | `?granularity=INVALID` | **400 Bad Request** | **200 OK** | Applica il valore di default `day`                     |
| **`PUT /admin/categories/{id}`** | `{"is_active": "not-a-boolean"}` | **400 Validation Error** | **200 OK** | Forza la stringa in un booleano (`False`)              |
| **`GET /reports`** | `?sort=INVALID` | **400 Bad Request** | **200 OK** | Ignora il filtro e applica il valore di default `desc` |

---

## Dettaglio delle Anomalie

### 1. Mancata validazione del parametro `granularity`
* **Descrizione:** Lo Swagger vincola il parametro a una lista chiusa (`day`, `week`, `month`). La funzione del backend `update_category_api()` recupera il dato e se non appartiene alla lista di valori lo forza a `day` senza validazione.
* **Soluzione Richiesta:** Aggiungere un controllo `if granularity not in ["day", "week", "month"]:` nel punto d'ingresso della rotta e sollevare un errore `400`.

### 2. Bypass del tipo di dato sul campo Booleano `is_active`
* **Descrizione:** La funzione helper `_as_bool()` nel backend effettua un casting permissivo, trasformando qualsiasi stringa non riconosciuta in `False` anziché rigettare l'input.
* **Soluzione Richiesta:** Modificare la logica di validazione affinché sollevi una `ValidationError` se il valore non è un booleano puro (`True`/`False`), evitando conversioni arbitrarie.

### 3. Mancata validazione del parametro `sort`
* **Descrizione:** Lo Swagger vincola il parametro a una due possibili valori `asc` o `desc`. La funzione helper nel backend `_report_filters()` estrae il dato e se non appartiene alla coppia di valori lo forza a `desc` senza validazione.
* **Soluzione Richiesta:** Modificare la logica di validazione affinché sollevi una `ValidationError` se il valore non è compreso nella coppia attesa.