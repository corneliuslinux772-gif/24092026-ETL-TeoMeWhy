
# ============================================================
# FK DICTIONARY
# ============================================================

FOREIGN_KEYS = [
    {
        "name": "cursos_episodios_curso",
        "child_dataset": "cursos_episodios",
        "child_column": "descSlugCurso",
        "parent_dataset": "cursos",
        "parent_column": "descSlugCurso",
    },

    {
        "name": "cursos_episodios_completos_curso",
        "child_dataset": "cursos_episodios_completos",
        "child_column": "descSlugCurso",
        "parent_dataset": "cursos",
        "parent_column": "descSlugCurso",
    },

    {
        "name": "cursos_episodios_completos_usuario",
        "child_dataset": "cursos_episodios_completos",
        "child_column": "idUsuario",
        "parent_dataset": "usuarios_tmw",
        "parent_column": "idUsuario",
    },

    {
        "name": "habilidades_cargos_habilidade",
        "child_dataset": "habilidades_cargos",
        "child_column": "descNomeHabilidade",
        "parent_dataset": "habilidades",
        "parent_column": "descNomeHabilidade",
    },

    {
        "name": "habilidades_usuarios_habilidade",
        "child_dataset": "habilidades_usuarios",
        "child_column": "descNomeHabilidade",
        "parent_dataset": "habilidades",
        "parent_column": "descNomeHabilidade",
    },

    {
        "name": "recompensas_usuarios_usuario",
        "child_dataset": "recompensas_usuarios",
        "child_column": "idUsuario",
        "parent_dataset": "usuarios_tmw",
        "parent_column": "idUsuario",
    },
]


# ============================================================
# FK COMPOUNDED DICTIONARY
# ============================================================

COMPOUND_FOREIGN_KEYS = [
    {
        "name": "cursos_episodios_completos_episodio",
        "child_dataset": "cursos_episodios_completos",
        "child_columns": [
            "descSlugCurso",
            "descSlugCursoEpisodio",
        ],
        "parent_dataset": "cursos_episodios",
        "parent_columns": [
            "descSlugCurso",
            "nrEp",
        ],
        "transform": "extract_nr_ep",
    },
]


# ============================================================
# DATASET PATH
# ============================================================

DATASET_FILES = {
    "cursos": "cursos.csv",
    "cursos_episodios": "cursos_episodios.csv",
    "cursos_episodios_completos": "cursos_episodios_completos.csv",
    "habilidades": "habilidades.csv",
    "habilidades_cargos": "habilidades_cargos.csv",
    "habilidades_usuarios": "habilidades_usuarios.csv",
    "recompensas_usuarios": "recompensas_usuarios.csv",
    "usuarios_tmw": "usuarios_tmw.csv",
}
