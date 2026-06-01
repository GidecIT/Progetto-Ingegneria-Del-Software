# Report Tecnico: Problemi di Concorrenza e Stabilità dei Test Selenium

## 1. Analisi delle Performance dei Test

### Situazione Iniziale
I test Selenium impiegavano originariamente tra i **20 e i 30 minuti** per una singola esecuzione. Questo era dovuto a:
- **Interazioni Fragili:** L'uso del metodo standard `.click()` di Selenium veniva spesso intercettato dall'header "sticky" del frontend, causando fallimenti silenziosi.
- **Cicli di Retry inefficienti:** In caso di fallimento, i test entravano in cicli di retry (fino a 6 iterazioni) con timeout multipli di diversi secondi, moltiplicando esponenzialmente il tempo di attesa.

### Miglioramenti Apportati
Ho ottimizzato il file `src/frontend/tests/selenium/conftest.py`:
- **JavaScript Click:** Implementato l'uso di `execute_script("arguments[0].click();", element)` per il logout e l'assegnazione dei report. Questo bypassa le limitazioni del driver Selenium riguardo agli elementi sovrapposti o sticky.
- **Logica di Logout:** Rafforzata la procedura di logout per garantire che ogni test inizi in uno stato pulito.
- **Risultato:** Il tempo di esecuzione è sceso a circa **6 minuti** (un miglioramento del ~75-80%).

---

## 2. Root Cause degli Errori Inconsistenti (Bug del Backend)

Nonostante i miglioramenti ai test, persistono fallimenti casuali (es. `AssertionError: Report X did not appear` o `TimeoutException`). L'indagine ha rivelato un problema critico nel **backend**.

### Il Problema: Race Condition su SQLite
Il frontend React utilizza massicciamente `Promise.all()` per caricare i dati (es. nella Operator Dashboard carica contemporaneamente report assegnati, pendenti e metadati). Questo causa l'invio di molteplici richieste API simultanee al server Flask.

1. **Concorrenza Flask:** Il server di sviluppo Flask (Werkzeug) gestisce queste richieste in thread separati.
2. **SQLAlchemy & selectinload:** Il backend usa SQLAlchemy con la strategia `selectinload` per caricare le relazioni.
3. **Collisione SQLite:** Quando più thread tentano di eseguire query complesse (con eager loading) contemporaneamente sullo stesso database SQLite locale, si verifica una corruzione temporanea del cursore o del result set.

### Prova Empirica (Errore nei Log del Backend)
Durante i test, il backend restituisce errori 500 con questo traceback:
```text
File "sqlalchemy/cyextension/resultproxy.pyx", line 77, in sqlalchemy.cyextension.resultproxy._apply_processors
IndexError: tuple index out of range
```
Questo è un errore noto di SQLAlchemy quando le sessioni non sono isolate correttamente in un ambiente multi-threaded con SQLite.

### Conseguenze sui Test
Quando il backend crasha (500 Error):
- La risposta manca degli header CORS, quindi il browser la blocca.
- Il frontend React rimane in uno stato "incompleto" o mostra un errore generico.
- Selenium fallisce perché l'elemento atteso (es. la riga del report assegnato) non compare mai nel DOM, non a causa di un bug nel test, ma perché l'API ha fallito.

---

## 3. Raccomandazioni per il Team di Sviluppo

Per risolvere definitivamente le inconsistenze, è necessario intervenire sul codice applicativo (non sui test):

1. **Soluzione Frontend (Immediata):**
   Sostituire i `Promise.all()` critici con chiamate sequenziali (`await` una dopo l'altra) nelle pagine principali (Operator Dashboard, Admin Page, Home). Questo riduce il carico concorrente sul database SQLite.

2. **Soluzione Backend (Strutturale):**
   - Configurare SQLAlchemy per usare `scoped_session` in modo più rigoroso per garantire l'isolamento dei thread.
   - **MIGRAZIONE DATABASE:** SQLite non è progettato per gestire questo livello di concorrenza web. Si raccomanda vivamente il passaggio a **PostgreSQL** o **MySQL** per gli ambienti di sviluppo e test condivisi.

3. **Infrastruttura di Test:**
   Se si continua a usare SQLite, i test Selenium dovrebbero essere eseguiti con un server backend configurato in modalità **single-threaded** (es. `flask run --no-threads`), sebbene questo rallenti ulteriormente le interazioni UI.
