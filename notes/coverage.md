## Comandi
Ci spostiamo nella cartella src\backend e attivare l'ambiente
```bash
cd .\src\backend\

.\.venv\Scripts\Activate.ps1
```
e per lanciare pytest e generare html per la coverage con tutti i test:
```bash
python -m pytest --cov=participium --cov-report=html

(windows)   start .\reports\coverage\html\index.html 
(macOs)     open  .\reports\coverage\html\index.html 
```
oppure per lanciare i test di cartelle specifiche:
```bash
python -m pytest --cov=participium --cov-report=html tests/unit

python -m pytest --cov=participium --cov-report=html tests/whitebox

python -m pytest --cov=participium --cov-report=html tests/unit tests/whitebox
```
ma in questo modo ogni volta che si lancia un comando il report HTML viene sovrascritto, 
se si vogliono lanciare i test separatamente e avere i risultati della coverage che si sommino invece di sovrascriversi
aggiungere il flag `--cov-append` nei successivi comandi:
```bash
python -m pytest --cov=participium --cov-report=html tests/unit

python -m pytest --cov=participium --cov-append --cov-report=html tests/integration

```


### Metodi da non fare in unit test per non duplicare i test
Questi metodi sono già oggetto di test white/black box quindi per evitare duplicazione di codice non andrebbero messi tra gli unit test da aggiungere per la coverage:

- services:
    - auth_service
      - AuthService.authenticate **BB**
  
    - report_service
      - ReportService.create_report **BB/WB**
      - ReportService.update_status **BB**
      - ReportService.list_public_reports **BB**
  
    - messaging_service
      - MessagingService.send_message **BB**
      - MessagingService._resolve_recipient **WB**

    - notification_service
      - NotificationService.create_notification **BB**
      - NotificationService.notify_status_change **WB**
      - NotificationService.count_unread_message_notifications_by_report **WB**
  
    - user_service
      - UserService.update_profile **BB**
      - UserService.update_user **WB**


- core:
    - utils
      - parse_date **BB**
  
    - status_flow
      - ensure_transition_allowed **BB**
  
    - security
      - verify_password **BB**
  
