from pathlib import Path
import pandas as pd
import re


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"


def load_csv(filename):
    path = DATA_DIR / filename

    for encoding in ["utf-8", "utf-8-sig", "latin1"]:
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False, sep=";")
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Não foi possível ler o arquivo: {filename}")


# ============================================================
# HELPERS
# ============================================================

def print_header(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def check_fk(child_df, parent_df, child_col, parent_col):
    """
    Verifica valores do filho que não existem no pai.
    """

    child_values = set(child_df[child_col].dropna().unique())
    parent_values = set(parent_df[parent_col].dropna().unique())

    orphans = sorted(child_values - parent_values)

    print(f"Child distinct : {len(child_values):,}")
    print(f"Parent distinct: {len(parent_values):,}")
    print(f"Orphans        : {len(orphans):,}")

    if orphans:
        print("\nValores órfãos:")
        for value in orphans:
            print(f"  {value}")

    return orphans


def check_composite_uniqueness(df, columns):
    """
    Verifica se uma combinação de colunas é única.
    """

    duplicates = df.duplicated(subset=columns, keep=False)
    duplicate_count = duplicates.sum()

    print(f"Columns: {columns}")
    print(f"Rows: {len(df):,}")
    print(f"Duplicated combinations: {duplicate_count:,}")

    if duplicate_count > 0:
        print("\nExemplos de combinações duplicadas:")

        duplicated_rows = (
            df.loc[duplicates, columns]
            .value_counts()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(20)
        )

        print(duplicated_rows.to_string(index=False))

    return duplicate_count


# ============================================================
# LOAD DATA
# ============================================================

cursos = load_csv("cursos.csv")
cursos_episodios = load_csv("cursos_episodios.csv")
completos = load_csv("cursos_episodios_completos.csv")
habilidades = load_csv("habilidades.csv")
habilidades_cargos = load_csv("habilidades_cargos.csv")
habilidades_usuarios = load_csv("habilidades_usuarios.csv")
recompensas = load_csv("recompensas_usuarios.csv")
usuarios_tmw = load_csv("usuarios_tmw.csv")


# ============================================================
# 1. HABILIDADES_CARGOS -> HABILIDADES
# ============================================================

print_header(
    "1. FK: habilidades_cargos.descNomeHabilidade "
    "-> habilidades.descNomeHabilidade"
)

check_fk(
    habilidades_cargos,
    habilidades,
    "descNomeHabilidade",
    "descNomeHabilidade",
)


# ============================================================
# 2. HABILIDADES_USUARIOS -> HABILIDADES
# ============================================================

print_header(
    "2. FK: habilidades_usuarios.descNomeHabilidade "
    "-> habilidades.descNomeHabilidade"
)

check_fk(
    habilidades_usuarios,
    habilidades,
    "descNomeHabilidade",
    "descNomeHabilidade",
)


# ============================================================
# 3. CHAVE DE CURSO + EPISÓDIO
# ============================================================

print_header(
    "3. UNIQUE: cursos_episodios(descSlugCurso, nrEp)"
)

check_composite_uniqueness(
    cursos_episodios,
    ["descSlugCurso", "nrEp"],
)


# ============================================================
# 4. PADRÃO DO descSlugCursoEpisodio
# ============================================================

print_header(
    "4. PROFILE: cursos_episodios_completos.descSlugCursoEpisodio"
)

print("Valores distintos:")
print(
    completos["descSlugCursoEpisodio"]
    .dropna()
    .value_counts()
    .sort_index()
    .to_string()
)


# ============================================================
# 5. TENTATIVA DE EXTRAÇÃO DO NÚMERO DO EPISÓDIO
# ============================================================

print_header(
    "5. EXTRAÇÃO DE nrEp A PARTIR DE descSlugCursoEpisodio"
)


def extract_episode_number(value):
    """
    Tenta extrair um número de strings como:

        ep-01
        ep-02
        episodio-03
        episode-04

    Se não encontrar número, retorna None.
    """

    if pd.isna(value):
        return None

    match = re.search(r"(\d+)", str(value))

    if match:
        return int(match.group(1))

    return None


completos["_nrEp_extraido"] = (
    completos["descSlugCursoEpisodio"]
    .apply(extract_episode_number)
)

missing_episode_number = completos["_nrEp_extraido"].isna().sum()

print(
    f"Registros sem número de episódio identificável: "
    f"{missing_episode_number:,}"
)

print("\nDistribuição dos números extraídos:")
print(
    completos["_nrEp_extraido"]
    .value_counts()
    .sort_index()
    .to_string()
)


# ============================================================
# 6. VALIDAR CURSO + EPISÓDIO CONTRA cursos_episodios
# ============================================================

print_header(
    "6. FK COMPOSTA: curso + nrEp "
    "completos -> cursos_episodios"
)

episodes_parent = (
    cursos_episodios[
        ["descSlugCurso", "nrEp"]
    ]
    .drop_duplicates()
    .copy()
)

episodes_parent["_exists"] = True


completos_check = completos[
    ["idCursoEpisodioCompleto", "descSlugCurso", "_nrEp_extraido"]
].copy()

completos_check = completos_check.rename(
    columns={"_nrEp_extraido": "nrEp"}
)

completos_check = completos_check.merge(
    episodes_parent,
    on=["descSlugCurso", "nrEp"],
    how="left",
)

orphans = completos_check["_exists"].isna()

print(f"Total de completions : {len(completos_check):,}")
print(f"Matches              : {(~orphans).sum():,}")
print(f"Orphans              : {orphans.sum():,}")


if orphans.any():
    print("\nExemplos de combinações órfãs:")

    print(
        completos_check.loc[
            orphans,
            [
                "idCursoEpisodioCompleto",
                "descSlugCurso",
                "nrEp",
            ],
        ]
        .drop_duplicates()
        .head(30)
        .to_string(index=False)
    )


# ============================================================
# 7. RECOMPENSAS: CHAVE (USUARIO, RECOMPENSA)
# ============================================================

print_header(
    "7. UNIQUE: recompensas_usuarios(idUsuario, idRecompensa)"
)

check_composite_uniqueness(
    recompensas,
    ["idUsuario", "idRecompensa"],
)


# ============================================================
# 8. RECOMPENSAS: USUARIO + RECOMPENSA + DATA
# ============================================================

print_header(
    "8. UNIQUE: recompensas_usuarios("
    "idUsuario, idRecompensa, dtRecompensa)"
)

check_composite_uniqueness(
    recompensas,
    ["idUsuario", "idRecompensa", "dtRecompensa"],
)


# ============================================================
# 9. USUÁRIOS: COMPLETIONS -> usuarios_tmw
# ============================================================

print_header(
    "9. FK: completions.idUsuario -> usuarios_tmw.idUsuario"
)

check_fk(
    completos,
    usuarios_tmw,
    "idUsuario",
    "idUsuario",
)


# ============================================================
# 10. USUÁRIOS: HABILIDADES -> usuarios_tmw
# ============================================================

print_header(
    "10. FK: habilidades_usuarios.idUsuario -> usuarios_tmw.idUsuario"
)

check_fk(
    habilidades_usuarios,
    usuarios_tmw,
    "idUsuario",
    "idUsuario",
)


# ============================================================
# 11. USUÁRIOS: RECOMPENSAS -> usuarios_tmw
# ============================================================

print_header(
    "11. FK: recompensas_usuarios.idUsuario -> usuarios_tmw.idUsuario"
)

check_fk(
    recompensas,
    usuarios_tmw,
    "idUsuario",
    "idUsuario",
)


# ============================================================
# 12. USUÁRIOS_TMW: ONE-TO-ONE
# ============================================================

print_header(
    "12. usuarios_tmw: relação idUsuario <-> idTMWCliente"
)

print(f"Rows: {len(usuarios_tmw):,}")

print(
    f"idUsuario unique: "
    f"{usuarios_tmw['idUsuario'].nunique() == len(usuarios_tmw)}"
)

print(
    f"idTMWCliente unique: "
    f"{usuarios_tmw['idTMWCliente'].nunique() == len(usuarios_tmw)}"
)


# ============================================================
# 13. HABILIDADES_USUARIOS: USUARIO + HABILIDADE
# ============================================================

print_header(
    "13. UNIQUE: habilidades_usuarios(idUsuario, descNomeHabilidade)"
)

check_composite_uniqueness(
    habilidades_usuarios,
    ["idUsuario", "descNomeHabilidade"],
)


# ============================================================
# 14. DISTRIBUIÇÃO DE HABILIDADES POR USUÁRIO
# ============================================================

print_header(
    "14. HABILIDADES POR USUÁRIO"
)

skills_per_user = (
    habilidades_usuarios
    .groupby("idUsuario")
    .size()
)

print(f"Usuários com habilidades: {skills_per_user.shape[0]:,}")
print(f"Mínimo de habilidades: {skills_per_user.min()}")
print(f"Máximo de habilidades: {skills_per_user.max()}")
print(f"Média de habilidades: {skills_per_user.mean():.2f}")
print(f"Mediana de habilidades: {skills_per_user.median():.2f}")


# ============================================================
# 15. EPISÓDIOS POR CURSO
# ============================================================

print_header(
    "15. EPISÓDIOS POR CURSO"
)

episodes_per_course = (
    cursos_episodios
    .groupby("descSlugCurso")
    .size()
    .sort_values(ascending=False)
)

print(episodes_per_course.to_string())


# ============================================================
# 16. CONCLUSÕES POR CURSO
# ============================================================

print_header(
    "16. CONCLUSÕES POR CURSO"
)

completions_per_course = (
    completos
    .groupby("descSlugCurso")
    .size()
    .sort_values(ascending=False)
)

print(completions_per_course.to_string())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 100)
print("RELATIONSHIP DEEP PROFILING FINALIZADO")
print("=" * 100)
