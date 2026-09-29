## Arquitetura GE

                            RAW
                            │
                            ▼
                ┌──────────────────┐
                │ Data Quality     │
                │                  │
                │ GX Expectations  │
                │ FK Validation    │
                │ Business Rules   │
                └────────┬─────────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
            PASS       CRITICAL     SEVERE
                │           │           │
                │           ▼           ▼
                │      QUARANTINE     STOP
                │           │
                ▼           ▼
                ──────── STAGING ────────
                            │
                            ▼
                            dbt
                            │
                            ▼
                        ANALYTICS




## Estrutura
            gx/
            ├── suites/
            │   ├── cursos_suite.py
            │   ├── cursos_episodios_suite.py
            │   └── ...
            │
            ├── validations/
            │   ├── cursos_validation.py
            │   └── ...
            │
            ├── checkpoints/
            │   └── ...
            │
            ├── quality/
            │   └── ...
            │
            └── referential/
                ├── __init__.py
                ├── config.py
                ├── transformations.py
                ├── validator.py
                ├── quarantine.py   ← novo
                └── run.py


## Estutura Quarantine

            gx/
            ├── quarantine/
            │   ├── __init__.py
            │   ├── config.py
            │   ├── models.py
            │   ├── policy.py
            │   ├── writer.py
            │   └── manager.py
            │
            ├── quality/
            │   └── ...
            │
            └── referential/
                └── ...

e o fluxo:

                    DATA QUALITY
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
            PASS       CRITICAL      SEVERE
                │           │           │
                │           ▼           ▼
                │       QUARANTINE    STOP
                │           │
                └─────┬─────┘
                    ▼
                STAGING
                

## Responsabilidade da Quarentena
- 
            validator
                ↓
            identifica quais linhas são inválidas
                ↓
            quarantine.py
                ├── salva registros inválidos
                └── adiciona metadados da rejeição



## Troublesheet: FK COMPOSE sem integridade (Solution)

            cursos_episodios_completos
            ┌────────────────┬──────────────────────┐
            │ descSlugCurso  │ descSlugCursoEpisodio│
            ├────────────────┼──────────────────────┤
            │ carreira       │ ep-12                │
            └────────────────┴──────────────────────┘
                                │
                                │ extrair
                                ▼
                            nrEp=12
                                │
                                ▼
            cursos_episodios
            ┌────────────────┬──────┐
            │ descSlugCurso  │ nrEp │
            ├────────────────┼──────┤
            │ carreira       │ 12   │
            └────────────────┴──────┘


## Resultado Final

                                ┌── Great Expectations
                                │
            RAW ──► QUALITY ────┼── Referential Integrity
                                │
                                └── Business Rules
                                    │
                                    ▼
                            QualityCheckResult
                                    │
                            ┌──────────┼──────────┐
                            ▼          ▼          ▼
                        PASS      CRITICAL    SEVERE
                            │          │          │
                            │          ▼          ▼
                            │      QUARANTINE    STOP
                            │          │
                            └────┬─────┘
                                ▼
                            STAGING