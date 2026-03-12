# SONICCLOUD - PROJECT MANAGEMENT

Vincoli: Web app + app mobili native, cloud storage e CDN, 100k utenti registrati, upload di audio da parte degli utenti e streaming on-demand. Durata progetto massima: 9 mesi (~39 settimane).

# PBS

La PBS elenca ciò che *deve esistere a fine progetto* (deliverable), **non** le attività necessarie per produrlo. Si divide in tre famiglie: Software, Infrastruttura, Documentazione.


##  Software

| ID | Deliverable |
|:---|:------------|
|S1 | Applicazione Web (UI + client)|
|S2 | App mobile Android |
|S3 | App mobile iOS |
|S4 | API Gateway / BFF |
|S5 | Autenticazione & Servizi utente |
|S6 | Tracking utilizzo |
|S7 | Interazioni social |
|S8 | Ricerca / Discovery / Recommendation|
|S9 |Servizio di notifiche |
|S10 | Admin & Moderazione |

**OPPURE** (ipotizzando di non voler fare troppo design già in questa fase iniziale)

| ID | Deliverable |
|:---|:------------|
|S1 | Applicazione Web (UI + client)|
|S2 | App mobile Android |
|S3 | App mobile iOS |
|S4 | Backend |

## Infrastruttura

| ID | Deliverable |
|:---|:------------|
|I1| Cloud account |
|I2| pipeline CI/CD & repo (git..) |
|I3| Docker k8s... (infrastruttura cloud)|
|I4| Database |
|I5| Object storage (file musicali)|
|I6| Content delivery network config|
|I7| Metriche log ecc|
|I8| Backup|

## Documentazione

| ID | Deliverable |
|:---|:------------|
|D1| Documento di visione, scopo...|
|D2 |Documento dei requisiti (elenco requisiti, user stories...)|
|D3| Architettura|
|D4| Documentazione API (Swagger)|
|D5| Strategia di test|
|D6| Manualistica di deploy / operazionale|
|D7| Istruzioni utente|
|D8| Sicurezza & Privacy  & Legale|
|D9| Pianificazione Progetto|


# WBS

La WBS trasforma i deliverable della PBS in **work package** schedulabili. Ogni WP produce output misurabili e ha confini chiari. La colonna "Output PBS" garantisce la tracciabilità.

Dove serve, i work package sono scomposti in **sottotask**.


|WBS|Work package|Sottotask|Task Gantt| Output PBS|
|:--|:---|:----|:----|:-----|
|1 |Avvio e pianificazione| | T1| (D1, D9)|
|2 | Analisi dei requisiti| | T2| (D1,  D2)|
|3| Architettura, UX, API ||T3|(D3, S4, D4)|
|4| Cloud/DevOps.... ||T4|(I1, I2, I3, I7, I8)|
|5| Sviluppo Backend | |  |I4, S4, S5, S6, S7, S8, S9, S10|
||  | 5.1 API + scheletro backend (auth, utenti) | T5|S4, S5, I4|
| | | 5.2 Backend (social, search, admin) | T6|S6, S7, S8, S9, S10|
|6| Media storage & streaming || T7|I5, I6|
|7| Implementazione web app | | T8|S1|
|8| Implementazione mobile |||S2, S3|
|| |Android|T9|S2|
|| |iOS|T10|S3
|9| System Integration & functional testing||T11|D5|
|10| Non functional validation (test di  qualità)||T12| D5 D8|
|11| Gestione dei rilasci||T13| D6 D7|
|12| Finalizzazione documenti||T14| D3, D4, D6, D7, D8, D9|



# Gantt

Finestra temporale: **9 mesi ~39 settimane**

Lo **slack** (o *float*) di un'attività è il numero di settimane di cui quell'attività può ritardare senza spostare la data di fine progetto. Se lo slack è 0, l'attività è **critica**: qualsiasi ritardo si propaga direttamente alla consegna finale. Le attività con slack > 0 hanno un margine di manovra.

| ID | Nome attività | Durata (sett.)| Dipendenze | Inizio | Fine | Slack | Critica |
|:---|:--------------|:-------|:-----------|:-------|:-----|:------|:--------|
| T1  | Avvio e pianificazione  | 2  |  —  |  W1  |  W2  | 0 | **Sì** |
| T2  | Analisi dei requisiti | 4  |  T1  |  W3  |  W6  | 0 | **Sì** |
| T3  | Architettura, UX, API | 4  |  T2  |  W7  |  W10  | 0 | **Sì** |
| T4  | Cloud/DevOps | 4  |  T2  |  W7  |  W10  | 0 | **Sì** |
| T5  | API + scheletro backend (auth, utenti) | 4  |  T3, T4  |  W11  |  W14  | 0 | **Sì** |
| T6  | Backend (social, search, admin) | 8  |  T5  |  W15  |  W22  | 2 | No |
| T7  | Media storage & streaming | 8  |  T3, T4  |  W11  |  W18  | 6 | No |
| T8  | Implementazione web app | 10  |  T3, T5  |  W15  |  W24  | 0 | **Sì** |
| T9  | Implementazione mobile Android | 10  |  T3, T5  |  W15  |  W24  | 0 | **Sì** |
| T10  | Implementazione mobile iOS | 10  |  T3, T5  |  W15  |  W24  | 0 | **Sì** |
| T11  | System Integration & functional testing | 4  |  T6, T7, T8, T9, T10  |  W25  |  W28  | 0 | **Sì** |
| T12  | Non functional validation (test di qualità) | 4  |  T11  |  W29  |  W32  | 0 | **Sì** |
| T13  | Gestione dei rilasci | 3  |  T11, T12  |  W33  |  W35  | 0 | **Sì** |
| T14  | Finalizzazione documenti | 2  |  T13  |  W36  |  W37  | 0 | **Sì** |

### Diagramma di Gantt

```
                                          M1  M2  M3  M4  M5  M6  M7  M8  M9
                                          │   │   │   │   │   │   │   │   │
                                          1···5····10···15···20···25···30···35·37
                                          ─────────────────────────────────────
T1  Avvio e pianificazione                ██
T2  Analisi dei requisiti                   ████
T3  Architettura, UX, API                       ████
T4  Cloud/DevOps                                ████
T5  API + skeleton backend                          ████
T7  Media storage & streaming                       ░░░░░░░░
T6  Backend (social, search, admin)                     ░░░░░░░░
T8  Implementazione web app                             ██████████
T9  Implementazione mobile Android                      ██████████
T10 Implementazione mobile iOS                          ██████████
T11 System Integration & test                                     ████
T12 Non functional validation                                         ████
T13 Gestione dei rilasci                                                  ███
T14 Finalizzazione documenti                                                 ██

                                          █ = percorso critico   ░ = non critica
```

### Percorso critico

```
T1 → T2 → (T3 ‖ T4) → T5 → (T8 ‖ T9 ‖ T10) → T11 → T12 → T13 → T14
```

Durata baseline: **37 settimane** — buffer residuo ~2 settimane sul vincolo di 9 mesi.

### Grafo delle dipendenze (percorso critico evidenziato)

```
                      ┌──────── T7 [8w] ░ ──────────────────────┐
                      │                                          │
T1 ━━► T2 ━━►┬━ T3 ━━┿━━► T5 ━━►┬━ T6  [8w] ░ ───────────────┤
              │       │          ├━ T8  [10w] █ ━━━━━━━━━━━━━━━━┤
              └━ T4 ━━┘          ├━ T9  [10w] █ ━━━━━━━━━━━━━━━━┤
                                 └━ T10 [10w] █ ━━━━━━━━━━━━━━━━┤
                                                                │
                                             T11 ◄━━━━━━━━━━━━━━┘
                                              ┃
                                             T12
                                              ┃
                                             T13
                                              ┃
                                             T14

━━ percorso critico (slack = 0)     ── non critico (T6: slack 2, T7: slack 6)
```

Note: T3 e T4 sono *entrambi* critici (stesso predecessore T2, stessa durata, entrambi predecessori di T5). Le tre implementazioni (T8, T9, T10) corrono in parallelo e sono tutte critiche perché guidano la data di inizio di T11.


#ANALISI DEI RISCHI

Scala Probabilità (P): 1 -> raro ... 5 -> quasi certo

Scala Impatto (I): 1 -> minimo ... 5 -> critico

Esposizione = P x I

| ID | Rischio | Categoria | P | I | Esposizione | Livello | Strategia di mitigazione |
|:---|:---|:---|:---|:---|:---|:---|:---|
|R1| Scalabilità (latenza streaming sotto carico)| Tecnico| 3 |5|15|Alto|Stress test, analisi log di carico| 
|R2| Gestione copyright / moderazione | Legale | 4 | 4| 16 | Molto alto | Policy, moderazione, log|
|R3| Requisiti non stabili| Progetto (scope) | 3| 4 |12| Alto| MVP chiaro, roadmap definita|
|R4|Costi cloud superiori alle attese| Economico| 3|4|12|Alto|Limiti di fatturazione, test|
|R5| Vulnerabilità e data breach | Sicurezza Privacy|2|5|10|Medio| test, log, incident response|
|R6| Frammentazione device| Esterno |2|3|6|Medio|GUI test, seguire linee guida store|





