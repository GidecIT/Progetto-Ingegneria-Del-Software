# PBS - Product Breakdown structure

## Software
I prodotti software identificati sono:
- S1 Applicazione Web (UI + Client)
- S2 App mobile Android
- S3 App mobile IOS
- S4 API Gateway / BFF
- S5 Autenticazione & Servizi Utente
- S6 Tracking
- S7 Iterazioni Social
- S8 Ricerca / Discovery / Reccomendation
- S9 Srvizio di notifiche
- S10 Admin & Moderazione

## Infrastruttura
- I1 Cloud Account
- I2 Pipeline CI / CD & repo (git...)
- I3 Docker kuberneves ... (infrastruttura clous)
- I4 Servizio di Database
- I5 Object Storage (file musicali)
- I6 Content Delivery Network config
- I7 Metriche log ecc
- I8 Backup

## Documentazione
- D1 Documento di visione, scopo ...
- D2 Documento dei requisiti (elenco dei requisiti, user storage...)
- D3 Architettura
- D4 Documentazione API (Swagger)
- D5 Strategia di tesi
- D6 Manualistica di Deploy / Utilizzo
- D7 istruzioni Utente
- D8 Sicurezza & Privacy & Legale
- D9 Pianificazione Progetto

# WBS - Work Breakdown Structure
1) Project Managment (D1,D9)
2) Requirement Elicitation (D1,D2)
3) Architettura, User Experience, API ... ( S4,D3,D4)
4) Cloud Develops (I1,I2,I3,I8)
5) Sviluppo Backend (I4,S10,S4,S5,S6,S7,S8,S9)
6) Media Storage (I5,I6,I7)
7) Implementazione WebApp (S1)
8) Implementazione mobile (S2,S3) 
    - 8.1 Android
    - 8.2 IOS
9) System Integration & functional testing (D5)
10) Non functionalValidation (D5,D8)
11) gestione del rilascio (D6,D7)
12) Finalizzazione documenti ( D3,D4,D6,D7,D8,D9)

## GANTT
|: | ID | Nome attività | Durata | Dipendenze | Inizio | Fine | Critica |
|:--||:--||:--||:--||:--|