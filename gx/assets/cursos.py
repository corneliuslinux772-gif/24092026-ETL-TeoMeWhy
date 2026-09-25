import great_expectations as gx

from gx.config import (
    DATA_SOURCE_NAME, CURSOS_ASSET_NAME, 
    CURSOS_BATCH_DEFINITION_NAME
)

context = gx.get_context(mode="file")

# ---------------------------------------------------------
# Data Source
# ---------------------------------------------------------

data_source = context.data_sources.get(DATA_SOURCE_NAME)


# ---------------------------------------------------------
# Data Asset
# ---------------------------------------------------------

try:
    data_asset = data_source.get_asset(CURSOS_ASSET_NAME)
    print(f"Data Asset já existe: {CURSOS_ASSET_NAME}")

except LookupError:
    data_asset = data_source.add_csv_asset(
        name=CURSOS_ASSET_NAME,
        sep=";",
    )

    print(f"Data Asset criado: {CURSOS_ASSET_NAME}")


# ---------------------------------------------------------
# Batch Definition
# ---------------------------------------------------------

try:
    batch_definition = data_asset.get_batch_definition(
        CURSOS_BATCH_DEFINITION_NAME
    )

    print(f"Batch Definition já existe: {CURSOS_BATCH_DEFINITION_NAME}")

except LookupError:
    batch_definition = data_asset.add_batch_definition_path(
        name=CURSOS_BATCH_DEFINITION_NAME,
        path="cursos.csv",
    )

    print(f"Batch Definition criado: {CURSOS_BATCH_DEFINITION_NAME}")


# ---------------------------------------------------------
# Batch
# ---------------------------------------------------------

batch = batch_definition.get_batch()

print("\nBatch criado com sucesso!")

print("\nData:")
print(batch.head())