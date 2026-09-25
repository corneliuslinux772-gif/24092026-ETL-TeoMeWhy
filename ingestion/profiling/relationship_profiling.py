from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")


def load(name):

    return pd.read_csv(
        DATA_DIR / name,
        encoding="utf-8",
        low_memory=False,
        sep=";"
    )


def check_relationship(
    child,
    parent,
    child_key,
    parent_key
):

    child_values = set(
        child[child_key]
        .dropna()
        .unique()
    )

    parent_values = set(
        parent[parent_key]
        .dropna()
        .unique()
    )

    orphan_values = (
        child_values - parent_values
    )

    print("\n" + "=" * 80)

    print(
        f"{child_key} -> {parent_key}"
    )

    print("=" * 80)

    print(
        f"Child distinct: "
        f"{len(child_values):,}"
    )

    print(
        f"Parent distinct: "
        f"{len(parent_values):,}"
    )

    print(
        f"Orphans: "
        f"{len(orphan_values):,}"
    )

    if orphan_values:

        print("\nExample orphans:")

        for value in list(
            orphan_values
        )[:20]:

            print(
                f"  {value}"
            )


def main():

    cursos = load(
        "cursos.csv"
    )

    cursos_episodios = load(
        "cursos_episodios.csv"
    )

    cursos_completos = load(
        "cursos_episodios_completos.csv"
    )

    habilidades = load(
        "habilidades.csv"
    )

    habilidades_usuarios = load(
        "habilidades_usuarios.csv"
    )

    # Curso -> episódios
    check_relationship(
        child=cursos_episodios,
        parent=cursos,
        child_key="descSlugCurso",
        parent_key="descSlugCurso"
    )

    # Curso -> conclusões
    check_relationship(
        child=cursos_completos,
        parent=cursos,
        child_key="descSlugCurso",
        parent_key="descSlugCurso"
    )

    # Habilidade -> usuários
    check_relationship(
        child=habilidades_usuarios,
        parent=habilidades,
        child_key="descNomeHabilidade",
        parent_key="descNomeHabilidade"
    )


if __name__ == "__main__":
    main()