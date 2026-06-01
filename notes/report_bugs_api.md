## Panoramica dei Problemi Rilevati

Durante la suite di test automatizzati su Postman, sono stati isolati due comportamenti del backend non conformi rispetto alle specifiche formali definite nello **Swagger**. In entrambi i casi, il backend si dimostra eccessivamente tollerante verso input errati o malformati, rispondendo con un successo (`200 OK`) anziché bloccare la richiesta con un errore di validazione (`400 Bad Request`).

---

## Tabella Riassuntiva dei Bug

| Endpoint | Input Inviato                    | Stato Atteso (Swagger) | Stato Reale (Backend) | Gestione lato backend                      |
| :--- |:---------------------------------| :--- | :--- |:-------------------------------------------|
| **`GET /stats/public?granularity=INVALID`** | `granularity=INVALID`            | **400 Bad Request** | **200 OK** | Ignora l'input e applica il default `day`) |
| **`PUT /admin/categories/{id}`** | `{"is_active": "not-a-boolean"}` | **400 Validation Error** | **200 OK** | Forza una stringa in un booleano           |

---

## Dettaglio delle Anomalie

### 1. Mancata validazione parametro `granularity`
* **Descrizione:** Lo Swagger vincola il parametro a una lista chiusa (`day`, `week`, `month`). Il codice Python recupera il valore tramite `request.args.get("granularity", "day")` senza verificarne l'appartenenza alla whitelist.
* **Comportamento Reale:** Se si passa un valore inventato, il server restituisce i dati su scala giornaliera con status `200`.
* **Soluzione Richiesta:** Aggiungere un controllo `if granularity not in ["day", "week", "month"]:` nel punto d'ingresso della rotta e ritornare un errore `400 Bad Request`.

### 2. Bypass del tipo di dato su sul campo Booleano `is_active`
* **Descrizione:** L'endpoint richiede l'autenticazione Admin. Una volta superata, se viene inviata una stringa di testo al posto di un valore booleano puro (`true`/`false`), il backend non valida il tipo primitivo.
* **Comportamento Reale:** Python esegue un casting arbitrario o ignora l'errore di tipo, aggiorna la risorsa nel database (forzandola a `false`) e risponde con `200 OK` mostrando l'oggetto modificato.
* **Soluzione Richiesta:** Aggiungere un controllo `if not isinstance(data["is_active"], bool)` sul tipo di dato presente nel body della risposta.
