import great_expectations as gx

from gx.config import (
    DATA_SOURCE_NAME, 
    RECOMPENSAS_ASSET_NAME,
    RECOMPENSAS_BATCH_DEFINITION_NAME
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
    data_asset = data_source.get_asset(RECOMPENSAS_ASSET_NAME)
    print(f"Data Asset já existe: {RECOMPENSAS_ASSET_NAME}")

except LookupError:
    data_asset = data_source.add_csv_asset(
        name=RECOMPENSAS_ASSET_NAME,
        sep=";",
    )

    print(f"Data Asset criado: {RECOMPENSAS_ASSET_NAME}")


# ---------------------------------------------------------
# Batch Definition
# ---------------------------------------------------------

try:
    batch_definition = data_asset.get_batch_definition(
        RECOMPENSAS_BATCH_DEFINITION_NAME
    )

    print(f"Batch Definition já existe: {RECOMPENSAS_BATCH_DEFINITION_NAME}")

except LookupError:
    batch_definition = data_asset.add_batch_definition_path(
        name=RECOMPENSAS_BATCH_DEFINITION_NAME,
        path="recompensas_usuarios.csv",
    )

    print(f"Batch Definition criado: {RECOMPENSAS_BATCH_DEFINITION_NAME}")


# ---------------------------------------------------------
# Batch
# ---------------------------------------------------------

batch = batch_definition.get_batch()

print("\nBatch criado com sucesso!")

print("\nData:")
print(batch.head())