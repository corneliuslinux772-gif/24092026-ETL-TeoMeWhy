import great_expectations as gx

from gx.config import (
    CURSOS_EPISODIOS_CHECKPOINT_NAME,
    CURSOS_EPISODIOS_VALIDATION_NAME
)


context = gx.get_context(mode="file")


# ============================================================
# GET VALIDATION DEFINITION
# ============================================================

validation_definition = context.validation_definitions.get(
    CURSOS_EPISODIOS_VALIDATION_NAME
)


# ============================================================
# CREATE CHECKPOINT
# ============================================================

try:
    checkpoint = context.checkpoints.get(
        CURSOS_EPISODIOS_CHECKPOINT_NAME
    )

    print(
        f"Checkpoint já existe: {CURSOS_EPISODIOS_CHECKPOINT_NAME}"
    )

except Exception:

    checkpoint = gx.Checkpoint(
        name=CURSOS_EPISODIOS_CHECKPOINT_NAME,
        validation_definitions=[
            validation_definition
        ]
    )

    checkpoint = context.checkpoints.add(
        checkpoint
    )

    print(
        f"Checkpoint criado: {CURSOS_EPISODIOS_CHECKPOINT_NAME}"
    )


# ============================================================
# RUN CHECKPOINT
# ============================================================

print("\nExecutando Checkpoint...\n")

result = checkpoint.run()


# ============================================================
# RESULT
# ============================================================

print(result.describe())