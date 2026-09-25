# Data Contract — TeoMeWhy Education Platform

## 1. Objetivo

Este documento define o contrato de dados identificado a partir da fase de profiling exploratório do dataset **TeoMeWhy Education Platform**.

O contrato documenta:

* estrutura dos datasets;
* granularidade das tabelas;
* chaves primárias;
* chaves de negócio;
* relacionamentos;
* regras de unicidade;
* nulabilidade;
* domínios conhecidos;
* regras de integridade referencial;
* anomalias identificadas durante o profiling.

Este documento será utilizado como referência para:

* validações de qualidade com Great Expectations;
* modelagem do PostgreSQL;
* transformações com dbt;
* testes automatizados;
* orquestração do pipeline com Airflow.

---

# 2. Princípios

O contrato diferencia **características observadas nos dados** de **regras que serão impostas pelo pipeline**.

Uma característica observada durante o profiling não deve ser automaticamente considerada uma regra de negócio.

Exemplo:

> Atualmente existem 32 cursos.

Isso não significa que o pipeline deva exigir exatamente 32 cursos.

A regra apropriada é:

> `descSlugCurso` deve ser único e não nulo.

Dessa forma, novos cursos podem ser adicionados sem quebrar o pipeline.

---

# 3. Visão geral dos datasets

| Dataset                          | Registros | Granularidade                                     |
| -------------------------------- | --------: | ------------------------------------------------- |
| `cursos.csv`                     |        32 | Um registro por curso                             |
| `cursos_episodios.csv`           |       375 | Um registro por episódio de curso                 |
| `cursos_episodios_completos.csv` |    43.085 | Um registro por conclusão de episódio por usuário |
| `habilidades.csv`                |        25 | Uma habilidade                                    |
| `habilidades_cargos.csv`         |       275 | Uma habilidade associada a um cargo/nível         |
| `habilidades_usuarios.csv`       |    58.483 | Uma habilidade associada a um usuário             |
| `recompensas_usuarios.csv`       |       665 | Uma recompensa concedida a um usuário             |
| `usuarios_tmw.csv`               |     2.497 | Um usuário e seu identificador TMW                |

---

# 4. `cursos`

## Granularidade

Um registro representa um curso.

## Chave primária

```text
descSlugCurso
```

## Regras

| Campo           | Regra    |
| --------------- | -------- |
| `descSlugCurso` | NOT NULL |
| `descSlugCurso` | UNIQUE   |
| `descCurso`     | NOT NULL |
| `descDescricao` | NOT NULL |
| `nrAno`         | NOT NULL |

## Observações

O profiling identificou:

* 32 registros;
* nenhuma duplicidade;
* `descSlugCurso` com 32 valores únicos;
* `descCurso` com apenas 29 valores únicos.

Portanto, `descCurso` não deve ser utilizado como identificador do curso.

`descSlugCurso` é a chave de identificação adotada.

## Domínio observado

`nrAno` apresentou valores entre 2020 e 2026.

A faixa observada não será utilizada como regra rígida de quantidade de anos.

---

# 5. `cursos_episodios`

## Granularidade

Um registro representa um episódio pertencente a um curso.

## Chave

```text
(descSlugCurso, nrEp)
```

## Regras

| Campo/regra             | Validação                      |
| ----------------------- | ------------------------------ |
| `descSlugCurso`         | NOT NULL                       |
| `nrEp`                  | NOT NULL                       |
| `descEpisodio`          | NOT NULL                       |
| `descYoutubeID`         | NOT NULL                       |
| `(descSlugCurso, nrEp)` | UNIQUE                         |
| `descYoutubeID`         | UNIQUE                         |
| `descSlugCurso`         | FK para `cursos.descSlugCurso` |

## Resultado do profiling

Foram encontrados:

```text
375 registros
0 combinações duplicadas
0 cursos órfãos
```

Portanto:

```text
(descSlugCurso, nrEp)
```

é uma chave composta válida.

---

# 6. `cursos_episodios_completos`

## Granularidade

Um registro representa a conclusão de um episódio por um usuário.

## Chave primária

```text
idCursoEpisodioCompleto
```

## Relacionamentos

### Usuário

```text
idUsuario
    ↓
usuarios_tmw.idUsuario
```

### Episódio

O episódio pode ser identificado através da combinação:

```text
descSlugCurso
+
nrEp
```

onde `nrEp` é extraído de `descSlugCursoEpisodio`.

Relacionamento:

```text
(descSlugCurso, nrEp)
    ↓
cursos_episodios
```

## Regras

| Campo/regra               | Validação                        |
| ------------------------- | -------------------------------- |
| `idCursoEpisodioCompleto` | UNIQUE                           |
| `idUsuario`               | FK para `usuarios_tmw.idUsuario` |
| `descSlugCurso`           | FK composta                      |
| `descSlugCursoEpisodio`   | deve permitir extração de `nrEp` |

## Resultado do profiling

Foram encontrados:

```text
43.085 completions
43.085 matches com episódios
0 órfãos
```

Também foram encontrados 0 registros sem número de episódio identificável.

---

# 7. `habilidades`

## Granularidade

Um registro representa uma habilidade.

## Chave primária

```text
idHabilidade
```

## Regras

| Campo                     | Regra    |
| ------------------------- | -------- |
| `idHabilidade`            | NOT NULL |
| `idHabilidade`            | UNIQUE   |
| `descNomeHabilidade`      | NOT NULL |
| `descNomeHabilidade`      | UNIQUE   |
| `descDescricaoHabilidade` | NOT NULL |

## Resultado do profiling

Foram encontrados:

```text
25 habilidades
0 duplicidades
```

---

# 8. `habilidades_cargos`

## Granularidade

Um registro representa uma habilidade associada a um cargo e nível profissional.

## Chave primária

```text
idHabilidadeCargo
```

## Regras

| Campo/regra           | Validação                                |
| --------------------- | ---------------------------------------- |
| `idHabilidadeCargo`   | UNIQUE                                   |
| `descNomeCargo`       | NOT NULL                                 |
| `descNivelCargo`      | NOT NULL                                 |
| `descNomeHabilidade`  | NOT NULL                                 |
| `descNivelHabilidade` | NOT NULL                                 |
| `descNomeHabilidade`  | FK para `habilidades.descNomeHabilidade` |

## Domínios observados

### Cargo

Foram encontrados 3 cargos:

```text
Data Analyst
Data Engineer
Data Scientist
```

### Níveis de cargo

Foram observados:

```text
Jr.
Pl.
Sr.
Staff
Principal
```

### Níveis de habilidade

Foram observados:

```text
00. Não esperada
01. Aprendiz
02. Iniciante
03. Profissional
04. Expert
05. Professor
```

## Resultado do profiling

```text
275 registros
0 duplicidades
0 habilidades órfãs
```

---

# 9. `habilidades_usuarios`

## Granularidade

Um registro representa uma habilidade associada a um usuário.

## Chave primária

```text
idHabilidadeusuario
```

## Chave de negócio

```text
(idUsuario, descNomeHabilidade)
```

Essa combinação não apresentou duplicidades.

## Relacionamentos

```text
idUsuario
    ↓
usuarios_tmw.idUsuario
```

```text
descNomeHabilidade
    ↓
habilidades.descNomeHabilidade
```

## Regras

| Campo/regra                       | Validação     |
| --------------------------------- | ------------- |
| `idHabilidadeusuario`             | UNIQUE        |
| `idUsuario`                       | FK            |
| `descNomeHabilidade`              | FK            |
| `(idUsuario, descNomeHabilidade)` | UNIQUE        |
| `descNivelHabilidade`             | pode ser NULL |
| `dtCriacao`                       | NOT NULL      |

## Nulabilidade

`descNivelHabilidade` apresentou:

```text
1.869 NULL
3,20%
```

Portanto, NULL é permitido nesta coluna.

## Resultado do profiling

```text
58.483 registros
0 duplicidades de usuário + habilidade
0 habilidades órfãs
```

---

# 10. `recompensas_usuarios`

## Granularidade

Um registro representa uma recompensa associada a um usuário.

## Chave de negócio candidata

```text
(idUsuario, idRecompensa)
```

Essa combinação apresentou:

```text
665 registros
0 duplicidades
```

## Relacionamento

```text
idUsuario
    ↓
usuarios_tmw.idUsuario
```

## Regras

| Campo/regra                 | Validação                        |
| --------------------------- | -------------------------------- |
| `idUsuario`                 | FK para `usuarios_tmw.idUsuario` |
| `idRecompensa`              | NOT NULL                         |
| `(idUsuario, idRecompensa)` | UNIQUE                           |
| `dtRecompensa`              | NOT NULL                         |

## Anomalia identificada

Foram encontrados 2 `idUsuario` sem correspondência em `usuarios_tmw`:

```text
8f7b75ff-d17c-44a0-a696-de03a19a653b
d28b2f3f-a651-4c6c-b5aa-f3a81aad566a
```

Esses registros **não devem ser automaticamente excluídos**.

A decisão de tratamento deverá ser definida na camada de qualidade/ingestão.

---

# 11. `usuarios_tmw`

## Granularidade

Um registro representa um usuário e seu identificador de cliente TMW.

## Chaves

```text
idUsuario
idTMWCliente
```

Ambas apresentaram unicidade.

## Regras

| Campo          | Regra    |
| -------------- | -------- |
| `idUsuario`    | NOT NULL |
| `idUsuario`    | UNIQUE   |
| `idTMWCliente` | NOT NULL |
| `idTMWCliente` | UNIQUE   |

## Cardinalidade

O profiling indica uma relação 1:1:

```text
idUsuario ↔ idTMWCliente
```

## Resultado

```text
2.497 registros
idUsuario unique = True
idTMWCliente unique = True
```

---

# 12. Mapa de relacionamentos

```text
                         cursos
                           │
                           │ descSlugCurso
                           ▼
                    cursos_episodios
                           │
                    ┌──────┴──────┐
                    │             │
                    │             │
              curso + nrEp       │
                    │             │
                    ▼             │
          cursos_episodios_completos
                    │
                    │ idUsuario
                    ▼
                usuarios_tmw
                    ▲
                    │
              ┌─────┴─────┐
              │           │
              │           │
    habilidades_usuarios  recompensas_usuarios
              │
              │ descNomeHabilidade
              ▼
          habilidades
              ▲
              │
              │ descNomeHabilidade
              │
     habilidades_cargos
```

---

# 13. Regras de integridade identificadas

## Integridade referencial

Devem ser validadas:

```text
cursos_episodios.descSlugCurso
    → cursos.descSlugCurso
```

```text
cursos_episodios_completos.idUsuario
    → usuarios_tmw.idUsuario
```

```text
cursos_episodios_completos.(descSlugCurso, nrEp)
    → cursos_episodios.(descSlugCurso, nrEp)
```

```text
habilidades_cargos.descNomeHabilidade
    → habilidades.descNomeHabilidade
```

```text
habilidades_usuarios.idUsuario
    → usuarios_tmw.idUsuario
```

```text
habilidades_usuarios.descNomeHabilidade
    → habilidades.descNomeHabilidade
```

```text
recompensas_usuarios.idUsuario
    → usuarios_tmw.idUsuario
```

## Unicidade

Devem ser validadas:

```text
cursos.descSlugCurso
cursos_episodios.(descSlugCurso, nrEp)
cursos_episodios.descYoutubeID
cursos_episodios_completos.idCursoEpisodioCompleto
habilidades.idHabilidade
habilidades.descNomeHabilidade
habilidades_cargos.idHabilidadeCargo
habilidades_usuarios.idHabilidadeusuario
habilidades_usuarios.(idUsuario, descNomeHabilidade)
recompensas_usuarios.(idUsuario, idRecompensa)
usuarios_tmw.idUsuario
usuarios_tmw.idTMWCliente
```

---

# 14. Anomalias conhecidas

| Dataset                | Anomalia                                          |                               Quantidade | Tratamento                  |
| ---------------------- | ------------------------------------------------- | ---------------------------------------: | --------------------------- |
| `recompensas_usuarios` | `idUsuario` sem correspondência em `usuarios_tmw` |                                        2 | Investigar antes de excluir |
| `habilidades_usuarios` | `descNivelHabilidade` NULL                        |                                    1.869 | Permitido                   |
| `cursos`               | `descCurso` não é único                           | 3 repetições em relação aos 32 registros | Não utilizar como chave     |

---

# 15. O que NÃO será transformado em regra rígida

Os valores abaixo foram observados durante o profiling, mas não devem ser tratados como regras fixas:

* quantidade atual de cursos;
* quantidade atual de usuários;
* quantidade atual de episódios;
* quantidade atual de habilidades;
* quantidade atual de completions;
* quantidade atual de recompensas;
* quantidade atual de cursos por ano;
* quantidade atual de episódios por curso.

Por exemplo, o fato de existirem atualmente 32 cursos não significa que um próximo carregamento contendo 33 cursos seja inválido.

As validações devem priorizar **invariantes estruturais e de negócio**, e não números acidentais do dataset atual.

---

# 16. Regras ainda pendentes

Antes da implementação definitiva das validações, ainda precisam ser definidos:

1. Tratamento dos 2 usuários órfãos em `recompensas_usuarios`.
2. Regras de domínio para datas.
3. Regras de domínio para `nrAno`.
4. Regras para valores de `nrEp`.
5. Tratamento de registros inválidos durante a ingestão.
6. Estratégia para registros rejeitados pelas validações.
7. Severidade de cada regra:

   * `ERROR`
   * `WARNING`

Essas decisões serão incorporadas posteriormente às validações do Great Expectations e ao comportamento do pipeline Airflow.

---

# 17. Próxima etapa

Com o profiling concluído e o contrato inicial definido, a próxima etapa é implementar a camada de **Data Quality**.

Fluxo planejado:

```text
CSV
 ↓
Ingestion
 ↓
RAW PostgreSQL
 ↓
Great Expectations
 ↓
STAGING
 ↓
dbt tests
 ↓
Analytics
```

O `data_contract.md` será a fonte de referência para transformar as descobertas do profiling em validações automatizadas.
