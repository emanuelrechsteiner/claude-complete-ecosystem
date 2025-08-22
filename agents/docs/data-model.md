## Data Model

Datastores:
- File-based JSON ledgers in `ledgers/`
- Global observation ledger in `global-observation/`
- Activity and pattern recognition artifacts in `observation/`

Entities and relationships:
```mermaid
erDiagram
  AGENT ||--o{ LEDGER_TASK : updates
  LEDGER_TASK }o--|| CONTROL_AGENT : validated_by
  AGENT ||--o{ OBS_ENTRY : emits
  OBS_ENTRY }o--|| GLOBAL_LEDGER : aggregates

  AGENT {
    string name
    string role
  }
  LEDGER_TASK {
    string id
    string status
    string ownerAgent
    string[] dependencies
  }
  OBS_ENTRY {
    string type
    string taskId
    string timestamp
  }
  GLOBAL_LEDGER {
    string path
    number version
  }
```

Migration/seed notes:
- No DB migrations. Ledgers are append-only JSON edited via normal VCS.


