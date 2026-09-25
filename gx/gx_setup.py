import great_expectations as gx
from pathlib import Path

# Create a new project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# Data Context
# ---------------------------------------------------------

context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Data Source
# ---------------------------------------------------------

DATA_SOURCE_NAME = "education_platform_csv"

if DATA_SOURCE_NAME in context.data_sources.all():
    data_source = context.data_sources.get(DATA_SOURCE_NAME)
    print(f"Data source '{DATA_SOURCE_NAME}' already exists.")
else:
    data_source = context.data_sources.add_pandas_filesystem(
        name=DATA_SOURCE_NAME,
        base_directory=DATA_RAW,
    )
    print(f"Data source created: {DATA_SOURCE_NAME}")

print("\nData Source: ")
print(data_source)
