"""Simple training entry point for the explainable CyberQuant risk model."""

from pathlib import Path

from ml.risk_model import RiskModel, load_enterprise_dataset


def main() -> None:
    dataset = load_enterprise_dataset(Path(__file__).resolve().parents[1] / "data" / "generated")
    model = RiskModel().train(dataset)
    enterprise = model.predict_enterprise_risk(dataset)
    print(f"Trained model: {model.training_summary}")
    print(f"Enterprise risk score: {enterprise['enterprise_risk_score']}")
    print(f"Total EAL: ₹{enterprise['total_expected_annual_loss_inr']:,.2f}")


if __name__ == "__main__":
    main()
