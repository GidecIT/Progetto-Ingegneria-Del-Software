# 1) Stakeholders

| ID     | Stakeholder name | Description | Role | Main concerns |
|:-------|:-----------------|:------------|:-----|:--------------|
| STK-## |                  |             |      |               |

---

# 2) Context Diagram

Attach your context diagram as an image under `../data/img/` and link it here:

- `![](../data/img/context-diagram.png)`

---

# 3) Interfaces

| ID    | Interface | Actor       | Physical interface | Logical interface |
|:------|:----------|:------------|:-------------------|:------------------|
| IF-XX |           |             |                    |                   |

---

# 4) Personas

| ID     | Name | Role | Background / Context | Goals | Constraints | Devices / Usage setting | Accessibility / Additional needs |
|:-------|:-----|:-----|:---------------------|:------|:------------|:------------------------|:---------------------------------|
| PER-XX |      |      |                      |       |             |                         |                                  |

---

# 5) User Stories

| ID    | Persona/Role | User story (As a… I want… so that…) |
|:------|:-------------|:------------------------------------|
| US-XX |              |                                     |

---

# 6) Functional Requirements (FR)

| ID    | Requirement statement (The system shall…) | Priority | User story ID | Notes |
|:------|:------------------------------------------|:---------|:--------------|:------|
| FR-XX |                                           |          |               |       |


---

# 7) Non-Functional Requirements (NFR)

| ID     | Category | Requirement statement | Metric / Target | Verification                           | Priority | Notes |
|:-------|:---------|:----------------------|:----------------|:---------------------------------------|:---------|:------|
| NFR-01 |Usabilità |L'applicazione web deve essere respon sive per l'uso da mobile                      |Il layout si adatta senza scrolling orizzontale su schermi da minimo 320 pixel di larghezza                 |Ispezione visiva e UI test automatici su emulatori                                        | Alta         |    Essenziale poichè la maggior parte delle segnalazioni avvengono direttamente in strada   |
| NFR-02| Prestazioni| La mappa pubblica deve caricarsi rapidamente| Rendering iniziale con 1000 segnalazioni "aperte" in meno di 3 secondi su rete 4G| Perfomamnce testing automatizzato|Alta| La mappa è l'elemento centrale, la velocità di caricamento sulle reti mobili è essenziale sia elevata|
| NFR-03| Sicurezza | Tutela rigorosa dell'opzione di anonimato pubblico| Zero occorrenze di dati identificativi ( nome,cognome,email) nei payload API pubblici| Analisi statica del codice e Penetration Test| Alta| Bilancia la trasparenza pubblica con la privacy del cittadino|
| NFR-04| Prestazioni| Elaborazione efficiente degli allegati, fino a tre foto| Upload ed elaborazione di tre immagini, massimo 5 MB cadauno, in meno di 5 secondi totali nel lato server| Load testing sull'endpoint di upload| Media| Si limita la dimensione per garantire la velocità in mobilità mantenendo una qualità visiva utile agli uffici|
| NFR-05| Sicurezza| Accesso alle statistiche private limitato agli amministratori| Il 100% dei tentativi di accesso da utenti non-admin genera errore HTTP 403| Test automatizzati di autorizzazione| Alta| Previene la fuga di dati aggregati non destinati alla consultazione pubblica|
| NFR-06| Interporabilità| Esportazione dati tabellari in formato CSV| Conformità totale allo standard RFC 4180, nessun errore in Excel/Sheets| Ispezione tramite validatori CSV| Media| Garantisce trasparenza e usabilità dei dati offline per analisi esterne da parte di cittadini|
| NFR-07| Affidabilità| Invio tempestivo delle notifiche email| Il 95% delle email consegnate al server SMTP entro 2 minuti dal cambio di stato| Analisi automatizzata dei log| Media| Una comunicazione rapida è necessaria per mantenere alto l'engagment del cittadino|
| NFR-08| Accessibilità| Interfaccia pubblica accessibile a cittadini con disabilità| Conformità livello AA delle linee guida WCAG 2.1| Test con tool automatici e navigazione con screen reader| Alta| Requisito normativo e morale essenziale per un servizio di pubblica amministrazione| 
| NFR-09| Portabilità| Sistema facilmente distribuibile per l'adozione open-source| Avvio completo (DB, Backend,Frontend) via script in meno di 15 minuti su server| Test di deployment in ambiente isolato| Media| Se l'installazione fosse complessa nessun altro comune adoterrebbe la piattaforma|
| NFR-10| Disponibilità| Alta disponibilità per inserimento segnalazioni e consultazioni| L'uptime del sito web e delle API pubbliche deve essere garantito per almeno il 99,9% del tempo ogni mese | Monitoraggio sintetico continuo| Alta| Il servizio deve essere sempre attivo, specialmente per segnalare problemi in situazioni di emergenza urbana|