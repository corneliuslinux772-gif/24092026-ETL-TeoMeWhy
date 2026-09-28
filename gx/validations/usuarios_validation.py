import great_expectations as gx

from gx.config import (
    DATA_SOURCE_NAME, USUARIOS_ASSET_NAME,
    USUARIOS_SUITE_NAME, USUARIOS_BATCH_DEFINITION_NAME,
    USUARIOS_SUITE_NAME, USUARIOS_VALIDATION_NAME
)

context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Data Source
# ---------------------------------------------------------

data_source = context.data_sources.get(DATA_SOURCE_NAME)


# ---------------------------------------------------------
# Data Asset
# ---------------------------------------------------------

data_asset = data_source.get_asset(USUARIOS_ASSET_NAME)


# ---------------------------------------------------------
# Batch Definition
# ---------------------------------------------------------

batch_definition = data_asset.get_batch_definition(
    USUARIOS_BATCH_DEFINITION_NAME
)


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

suite = context.suites.get(USUARIOS_SUITE_NAME)


# ---------------------------------------------------------
# Validation Definition
# ---------------------------------------------------------

try:
    validation_definition = context.validation_definitions.get(
        USUARIOS_VALIDATION_NAME
    )

    print(
        f"Validation Definition já existe: "
        f"{USUARIOS_VALIDATION_NAME}"
    )

except Exception:
    validation_definition = gx.ValidationDefinition(
        name=USUARIOS_VALIDATION_NAME,
        data=batch_definition,
        suite=suite,
    )

    context.validation_definitions.add(
        validation_definition
    )

    print(
        f"Validation Definition criada: "
        f"{USUARIOS_VALIDATION_NAME}"
    )


print("\nValidation Definition:")
print(validation_definition)


# ---------------------------------------------------------
# Run Validation
# ---------------------------------------------------------

print("\nExecutando validação...")

result = validation_definition.run()

print("\nResultado da validação:")
print(result)