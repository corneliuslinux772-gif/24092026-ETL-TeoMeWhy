from pathlib import Path

from gx.referential.config import (
    FOREIGN_KEYS, DATASET_FILES, COMPOUND_FOREIGN_KEYS,
)
from gx.referential.validator import (
    validate_foreign_key,
    validate_compound_foreign_key
)
from gx.referential.transformations import (
    extract_nr_ep
)


TRANSFORMS = {
    "extract_nr_ep": extract_nr_ep,
}


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def validate_simple_foreign_keys():
    results = []

    for foreign_key in FOREIGN_KEYS:
        child_dataset = foreign_key["child_dataset"]
        parent_dataset = foreign_key["parent_dataset"]

        child_file = RAW_DATA_DIR / DATASET_FILES[child_dataset]
        parent_file = RAW_DATA_DIR / DATASET_FILES[parent_dataset]

        result = validate_foreign_key(
            child_file=child_file,
            child_column=foreign_key["child_column"],
            parent_file=parent_file,
            parent_column=foreign_key["parent_column"],
        )

        result["name"] = foreign_key["name"]

        results.append(result)

    return results



def validate_compound_foreign_keys():
    results = []

    for foreign_key in COMPOUND_FOREIGN_KEYS:
        child_dataset = foreign_key["child_dataset"]
        parent_dataset = foreign_key["parent_dataset"]

        child_file = RAW_DATA_DIR / DATASET_FILES[child_dataset]
        parent_file = RAW_DATA_DIR / DATASET_FILES[parent_dataset]

        transform_name = foreign_key.get("transform")
        transform = TRANSFORMS.get(transform_name)

        if transform_name and transform is None:
            raise ValueError(
                f"Unknown transformation: {transform_name}"
            )

        result = validate_compound_foreign_key(
            child_file=child_file,
            child_columns=foreign_key["child_columns"],
            parent_file=parent_file,
            parent_columns=foreign_key["parent_columns"],
            transform=transform,
        )

        result["name"] = foreign_key["name"]

        results.append(result)

    return results


def print_simple_result(result):
    status = "PASS" if result["success"] else "FAIL"

    print(f"\n[{status}] {result['name']}")
    print(
        f"  {result['child_file']}."
        f"{result['child_column']}"
        f" -> "
        f"{result['parent_file']}."
        f"{result['parent_column']}"
    )
    print(f"  Child rows: {result['child_rows']}")
    print(
        f"  Distinct child values: "
        f"{result['distinct_child_values']}"
    )
    print(f"  Parent rows: {result['parent_rows']}")
    print(
        f"  Distinct parent values: "
        f"{result['distinct_parent_values']}"
    )
    print(f"  Orphans: {result['orphan_count']}")

    if result["orphan_values"]:
        print("  Orphan values (sample of 5):")

        for value in result["orphan_values"][:5]:
            print(f"    - {value}")



def print_compound_result(result):
    status = "PASS" if result["success"] else "FAIL"

    print(f"\n[{status}] {result['name']}")
    print(
        f"  {result['child_file']}."
        f"{tuple(result['child_columns'])}"
        f" -> "
        f"{result['parent_file']}."
        f"{tuple(result['parent_columns'])}"
    )
    print(f"  Child rows: {result['child_rows']}")
    print(
        f"  Distinct child keys: "
        f"{result['distinct_child_keys']}"
    )
    print(f"  Parent rows: {result['parent_rows']}")
    print(
        f"  Distinct parent keys: "
        f"{result['distinct_parent_keys']}"
    )
    print(f"  Orphans: {result['orphan_count']}")

    if result["orphan_values"]:
        print("  Orphan keys:")

        for value in result["orphan_values"]:
            print(f"    - {value}")


def main():
    simple_results = validate_simple_foreign_keys()
    compound_results = validate_compound_foreign_keys()

    results = simple_results + compound_results

    print("\n" + "=" * 70)
    print("REFERENTIAL INTEGRITY VALIDATION")
    print("=" * 70)

    for result in simple_results:
        print_simple_result(result)

    for result in compound_results:
        print_compound_result(result)

    failed = [
        result
        for result in results
        if not result["success"]
    ]

    passed = len(results) - len(failed)

    print("\n" + "=" * 70)
    print(
        f"SUMMARY: {passed}/{len(results)} "
        "relationships passed"
    )
    print("=" * 70)

    if failed:
        raise SystemExit(1)

    
if __name__ == "__main__":
    main()