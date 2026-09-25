from pathlib import Path


# ============================================================
# PROJECT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# GREAT EXPECTATIONS
# ============================================================

DATA_SOURCE_NAME = "education_platform_csv"


# ============================================================
# CURSOS
# ============================================================

CURSOS_ASSET_NAME = "cursos"

CURSOS_BATCH_DEFINITION_NAME = "cursos_csv"

CURSOS_SUITE_NAME = "cursos_suite"

CURSOS_VALIDATION_NAME = "cursos_validation"

CURSOS_CHECKPOINT_NAME = "cursos_checkpoint"

# ============================================================
# CURSOS EPISODIOS
# ============================================================

CURSOS_EPISODIOS_ASSET_NAME = "cursos_episodios"

CURSOS_EPISODIOS_BATCH_DEFINITION_NAME = "cursos_episodios_csv"

CURSOS_EPISODIOS_SUITE_NAME = "cursos_episodios_suite"

CURSOS_EPISODIOS_VALIDATION_NAME = "cursos_episodios_validation"

CURSOS_EPISODIOS_CHECKPOINT_NAME = "cursos_episodios_checkpoint"