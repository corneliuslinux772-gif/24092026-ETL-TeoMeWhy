import great_expectations as gx

from gx.config import (
    DATA_SOURCE_NAME, 
    USUARIOS_ASSET_NAME,
    USUARIOS_BATCH_DEFINITION_NAME
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
    data_asset = data_source.get_asset(USUARIOS_ASSET_NAME)
    print(f"Data Asset já existe: {USUARIOS_ASSET_NAME}")

except LookupError:
    data_asset = data_source.add_csv_asset(
        name=USUARIOS_ASSET_NAME,
        sep=";",
    )

    print(f"Data Asset criado: {USUARIOS_ASSET_NAME}")


# ---------------------------------------------------------
# Batch Definition
# ---------------------------------------------------------

try:
    batch_definition = data_asset.get_batch_definition(
        USUARIOS_BATCH_DEFINITION_NAME
    )

    print(f"Batch Definition já existe: {USUARIOS_BATCH_DEFINITION_NAME}")

except LookupError:
    batch_definition = data_asset.add_batch_definition_path(
        name=USUARIOS_BATCH_DEFINITION_NAME,
        path="usuarios_tmw.csv",
    )

    print(f"Batch Definition criado: {USUARIOS_BATCH_DEFINITION_NAME}")


# ---------------------------------------------------------
# Batch
# ---------------------------------------------------------

batch = batch_definition.get_batch()

print("\nBatch criado com sucesso!")

print("\nData:")
print(batch.head())