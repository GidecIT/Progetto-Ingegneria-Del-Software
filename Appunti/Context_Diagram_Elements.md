# Analisi del Diagramma di Contesto - Participium

Il Diagramma di Contesto definisce il confine del sistema **Participium** (rappresentato come un'unica entità centrale) e le sue interazioni con gli attori esterni (entità che scambiano dati con esso).

## 1. Entità Centrale: Participium
Rappresenta l'intero ecosistema software: l'applicazione web (frontend), le API (backend) e il database. Gestisce la logica di business, l'archiviazione dei dati e il coordinamento dei servizi esterni.

## 2. Attori Esterni (User Roles)

### A. Cittadino / Visitatore
*   **Interazione In entrata:** Fornisce dati per la registrazione, invia segnalazioni (testo, categoria, geolocalizzazione, foto), gestisce il proprio profilo e interagisce tramite messaggistica.
*   **Interazione In uscita:** Riceve conferme di invio, notifiche di aggiornamento stato (tramite interfaccia web) e visualizza la mappa pubblica delle segnalazioni.

### B. Operatore Comunale
*   **Interazione In entrata:** Inserisce aggiornamenti sullo stato delle segnalazioni (es. "In lavorazione", "Risolto"), invia messaggi di chiarimento ai cittadini.
*   **Interazione In uscita:** Riceve la lista delle segnalazioni assegnate, i dettagli tecnici del problema e i messaggi dai cittadini.

### C. Amministratore di Sistema
*   **Interazione In entrata:** Configura parametri di sistema (categorie, permessi), gestisce gli account degli operatori.
*   **Interazione In uscita:** Accede a dashboard di statistiche avanzate, report di performance e log di sistema.

## 3. Sistemi Esterni (Service Providers)

### D. OpenStreetMap (Map Service)
*   **Interazione In uscita (dal sistema):** Richiesta di tile cartografiche e servizi di reverse-geocoding (conversione coordinate in indirizzi).
*   **Interazione In entrata (al sistema):** Fornisce i layer della mappa e le informazioni geografiche necessarie per il posizionamento dei marker.

### E. Resend (Email Service)
*   **Interazione In uscita (dal sistema):** Invio di payload contenenti i dati delle email (destinatario, oggetto, corpo del messaggio).
*   **Interazione In entrata (al sistema):** Feedback sulla consegna delle email (delivery/bounce status).

### F. Cloud Object Storage (e.g., AWS S3)
*   **Interazione In uscita (dal sistema):** Upload delle immagini caricate dai cittadini e richieste di link pre-firmati per la visualizzazione.
*   **Interazione In entrata (al sistema):** Conferma di avvenuto caricamento e stream dei file multimediali durante la consultazione.

---

## Flussi di Dati Principali (Esempi)
1.  **Segnalazione:** `Cittadino -> Sistema` (Dati segnalazione) -> `Sistema -> Cloud Storage` (Foto) -> `Sistema -> OpenStreetMap` (Validazione posizione).
2.  **Aggiornamento Stato:** `Operatore -> Sistema` (Nuovo Stato) -> `Sistema -> Resend` (Notifica Email) -> `Sistema -> Cittadino` (Notifica UI).
3.  **Monitoraggio:** `Sistema -> Amministratore` (Statistiche/Analytics).
