from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main():
    completions_file = RAW_DATA_DIR / "cursos_episodios_completos.csv"
    users_file = RAW_DATA_DIR / "usuarios_tmw.csv"

    completions = pd.read_csv(
        completions_file,
        sep=";",
        low_memory=False,
    )

    users = pd.read_csv(
        users_file,
        sep=";",
        low_memory=False,
    )

    completion_users = set(
        completions["idUsuario"].dropna()
    )

    known_users = set(
        users["idUsuario"].dropna()
    )

    matched_users = completion_users & known_users
    orphan_users = completion_users - known_users

    print("=" * 70)
    print("INVESTIGATION: cursos_episodios_completos.idUsuario")
    print("=" * 70)

    print(f"\nCompletion rows: {len(completions)}")
    print(f"Distinct completion users: {len(completion_users)}")

    print(f"\nUsers in usuarios_tmw: {len(known_users)}")

    print(f"\nMatched users: {len(matched_users)}")
    print(f"Orphan users: {len(orphan_users)}")

    print(
        f"\nMatch rate: "
        f"{len(matched_users) / len(completion_users):.2%}"
    )

    print(
        f"Orphan rate: "
        f"{len(orphan_users) / len(completion_users):.2%}"
    )

    print("\nSample orphan IDs:")

    for user_id in sorted(orphan_users)[:20]:
        print(f"  - {user_id}")


if __name__ == "__main__":
    main()