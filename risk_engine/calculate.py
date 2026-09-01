"""Command-line entry point for the reusable risk engine."""

import json
from pathlib import Path

from .eal import calculate_asset_risks


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "generated"


def load_json(filename: str) -> list[dict]:
    with (DATA_DIR / filename).open(encoding="utf-8") as data_file:
        return json.load(data_file)


def main() -> None:
    risks = calculate_asset_risks(
        load_json("assets.json"),
        load_json("vulnerabilities.json"),
        load_json("threats.json"),
    )
    total_eal = sum(risk["annualized_loss_inr"] for risk in risks)
    print(f"Open vulnerability risks: {len(risks)}")
    print(f"Enterprise EAL: INR {total_eal:,.2f}")
    print("Top 5 risk contributors:")
    for risk in risks[:5]:
        print(
            f"- {risk['asset_name']}: INR {risk['annualized_loss_inr']:,.2f} "
            f"(score {risk['risk_score']})"
        )


if __name__ == "__main__":
    main()