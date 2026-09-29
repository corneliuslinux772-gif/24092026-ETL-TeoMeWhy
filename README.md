# DAG TeoMeWhy

Started: 24-09-2026


## Arquitetura Geral

                 ┌─────────────────────┐
                 │       KAGGLE        │
                 │ Education Dataset   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       PYTHON        │
                 │     INGESTION       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     POSTGRESQL      │
                 │                     │
                 │       RAW           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ GREAT EXPECTATIONS  │
                 │    DATA QUALITY     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │        DBT          │
                 │    TRANSFORMATION   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     POSTGRESQL      │
                 │                     │
                 │      STAGING        │
                 │         ↓           │
                 │      ANALYTICS      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ GREAT EXPECTATIONS  │
                 │ FINAL VALIDATION    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      AIRFLOW        │
                 │   ORCHESTRATION     │
                 └─────────────────────┘


## Arquitetura DAG

                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Download Kaggle │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Validate Files  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Load PostgreSQL │
                  │      RAW        │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Great           │
                  │ Expectations   │
                  └────────┬────────┘
                           │
                    ┌──────▼──────┐
                    │    PASS?    │
                    └───┬─────┬───┘
                        │     │
                       YES    NO
                        │     │
                        ▼     ▼
                  ┌────────┐  QUARANTINE / FAIL
                  │  dbt   │
                  │ staging │
                  └────┬───┘
                       │
                       ▼
                  ┌─────────────┐
                  │ dbt tests   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ dbt         │
                  │ analytics   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Final       │
                  │ validation  │
                  └──────┬──────┘
                         │
                         ▼
                       END


## Arquitetura GE

             DATA CONTRACT
                   │
                   ▼
        GREAT EXPECTATIONS
                   │
                   ▼
          QUALITY ENGINE
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
     PASS       QUARANTINE    FAIL
       │           │           │
       ▼           ▼           ▼
     DBT         QUARANTINE   AIRFLOW
       │           │          FAILED
       ▼           ▼
 ANALYTICS      AUDIT


## Arquitetura Orquestrador

                         AIRFLOW
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       Python               GX                dbt
     ingestion          validation        transformation
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                       PostgreSQL

                       
## Estrutura do projeto

education-data-platform/
│
├── docker-compose.yml
├── README.md
├── .env
├── .gitignore
│
├── airflow/
│   ├── dags/
│   │   └── education_pipeline.py
│   │
│   ├── logs/
│   └── plugins/
│
├── ingestion/
│   ├── __init__.py
│   ├── download.py
│   ├── extract.py
│   ├── load.py
│   └── utils.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dbt/
│   └── education_dw/
│       │
│       ├── dbt_project.yml
│       ├── profiles.yml
│       │
│       ├── models/
│       │   │
│       │   ├── staging/
│       │   │   ├── _sources.yml
│       │   │   ├── _staging.yml
│       │   │   ├── stg_users.sql
│       │   │   ├── stg_courses.sql
│       │   │   └── ...
│       │   │
│       │   └── marts/
│       │       ├── dimensions/
│       │       │   ├── dim_users.sql
│       │       │   ├── dim_courses.sql
│       │       │   └── dim_date.sql
│       │       │
│       │       └── facts/
│       │           ├── fact_enrollments.sql
│       │           ├── fact_payments.sql
│       │           └── fact_progress.sql
│       │
│       ├── tests/
│       ├── macros/
│       └── seeds/
│
├── great_expectations/
│   ├── expectations/
│   ├── checkpoints/
│   └── ...
│
├── sql/
│   ├── ddl/
│   └── analysis/
│
└── docs/
    ├── architecture.md
    ├── data_dictionary.md
    └── data_quality.md


## Modelo Conceitual da base de dados

                         ┌─────────────────┐
                         │     CURSOS      │
                         │─────────────────│
                         │ slug_curso      │
                         │ curso            │
                         │ descricao        │
                         │ ano              │
                         └────────┬────────┘
                                  │
                                  │ 1:N
                                  ▼
                         ┌─────────────────┐
                         │    EPISÓDIOS    │
                         │─────────────────│
                         │ slug_curso      │
                         │ nr_ep           │
                         │ episodio        │
                         │ youtube_id      │
                         └────────┬────────┘
                                  │
                                  │
                                  ▼
┌───────────────┐       ┌──────────────────────┐
│    USUÁRIO    │       │  EPISÓDIOS COMPLETOS │
│───────────────│       │──────────────────────│
│ id_usuario    │◄──────│ id_usuario           │
└───────┬───────┘       │ slug_curso           │
        │               │ slug_episodio        │
        │               │ dt_criacao           │
        │               └──────────────────────┘
        │
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
┌───────────────────┐        ┌──────────────────┐
│ HABILIDADES_USER  │        │ RECOMPENSAS_USER │
│───────────────────│        │──────────────────│
│ id_usuario        │        │ id_usuario       │
│ habilidade        │        │ recompensa       │
│ nivel             │        │ dt_recompensa    │
│ dt_criacao        │        └──────────────────┘
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│    HABILIDADES    │
│───────────────────│
│ id_habilidade     │
│ nome              │
│ descricao         │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ HABILIDADES_CARGO │
│───────────────────│
│ cargo             │
│ nivel_cargo       │
│ habilidade        │
│ nivel_habilidade  │
└───────────────────┘