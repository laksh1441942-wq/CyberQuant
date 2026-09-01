import json
from pathlib import Path

from ml.risk_model import RiskModel, load_enterprise_dataset


def test_load_enterprise_dataset_reads_generated_json():
    dataset = load_enterprise_dataset(Path("data/generated"))
    assert dataset["assets"]
    assert dataset["vulnerabilities"]
    assert dataset["threats"]


def test_risk_model_predicts_modest_ranges():
    dataset = load_enterprise_dataset(Path("data/generated"))
    model = RiskModel()
    model.train(dataset)

    result = model.predict_asset_risk(
        dataset["assets"][0],
        dataset["vulnerabilities"],
        dataset["threats"],
    )

    assert 0.0 <= result["risk_probability"] <= 1.0
    assert result["expected_annual_loss_inr"] >= 0
    assert result["risk_band"] in {"Low", "Medium", "High", "Critical"}
    assert "top_drivers" in result
