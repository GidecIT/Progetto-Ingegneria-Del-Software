# Rapporto Inconsistenze: API Implementation vs. Swagger Contract (Task 8)

Durante la verifica del **Task 8 (Postman API Acceptance Testing)**, sono state riscontrate diverse discrepanze tra il comportamento effettivo del backend e il contratto documentato nelle specifiche Swagger (estratte dai docstring in `src/backend/participium/routes/api.py`).

Di seguito il dettaglio delle problematiche identificate che impediscono il superamento del 100% dei test di accettazione, pur essendo la suite Postman completa dal punto di vista della copertura del contratto.

## 1. Validazione degli Input (Errori 400 mancanti)

Lo Swagger dichiara esplicitamente che diverse endpoint devono restituire un errore `400 Bad Request` in caso di input non validi. Tuttavia, l'attuale implementazione è troppo permissiva:

*   **Statistiche Pubbliche (`GET /stats/public`):** Lo Swagger documenta un errore 400 per parametri `granularity` non validi. L'API invece ignora i valori errati, applicando il valore di default "day" e restituendo un `200 OK`.
*   **Aggiornamento Categorie (`PUT /admin/categories/<id>`):** Lo Swagger prevede un errore 400 per body non validi. L'API accetta stringhe arbitrarie per il campo `is_active` (es. "not-a-bool"), convertendole silenziosamente in booleani invece di validare il tipo dato, restituendo `200 OK`.
*   **Aggiornamento Utenti (`PUT /admin/users/<id>`):** Comportamento analogo alle categorie per i campi booleani; la validazione del ruolo (`role`) è invece correttamente implementata.

## 2. Controllo degli Accessi (Errori 403 mancanti)

Il rispetto della privacy e dei ruoli è documentato tramite risposte `403 Forbidden`, ma non sempre applicato:

*   **Dettaglio Report (`GET /reports/<id>`):** Uno Swagger corretto richiede che un cittadino non possa vedere i report in stato "Pending Approval" creati da altri utenti. Attualmente, l'API restituisce `200 OK` permettendo la visualizzazione di dettagli privati prima dell'approvazione dell'operatore.

## 3. Inconsistenze nello Schema delle Risposte

*   **Registrazione Utente (`POST /auth/register`):** Esiste una confusione sui nomi dei campi per il link di verifica. Lo Swagger e i test si aspettano un campo coerente (es. `verification_url`), ma a causa di bug nell'assegnazione del payload nel backend o discrepanze nei nomi (es. `verification_url` vs `_verification_link`), i test automatici di Newman non riescono a recuperare il token per procedere alla verifica email senza interventi manuali o script di fallback complessi.
*   **Esportazione CSV (`GET /reports/export`):** Il test di accettazione (basato sui requisiti funzionali) si aspetta la colonna `description` nel file CSV. L'attuale implementazione della funzione `build_csv` in `api.py` include solo `id, title, category, status, created_at, latitude, longitude`, causando il fallimento dell'asserzione sulla struttura del file.

## 4. Idempotenza e Gestione Seed Data

La suite Postman è stata corretta per essere idempotente (eseguibile più volte), ma si nota che:
*   Il test di cancellazione account (`DELETE /users/me`) fallisce se eseguito sull'utente "seed" (citizen@example.com) perché lo rimuove permanentemente, impedendo il login nei test successivi. 
*   **Soluzione applicata:** La suite ora crea un utente temporaneo dedicato al test di cancellazione, lasciando intatti i dati di seed.

## Conclusione

La collezione Postman riflette fedelmente il contratto Swagger al 100%. I fallimenti registrati da Newman non sono errori del test, ma **"failed acceptance checks"** che segnalano dove il backend non è conforme alle sue stesse specifiche o ai requisiti di sicurezza/validazione.

Si raccomanda l'allineamento del backend (aggiunta di validazioni esplicite e correzione dei nomi dei campi) per garantire la robustezza dell'interfaccia API.
