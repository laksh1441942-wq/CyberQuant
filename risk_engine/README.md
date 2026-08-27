# Risk Engine

This is the first deterministic prototype of CyberQuant's risk quantification
engine. It converts the synthetic asset, vulnerability, and threat data into
financial exposure.

## Model

```text
Likelihood = threat likelihood × CVSS × exposure × exploit × age
             × (1 - control effectiveness)

Impact = asset value + 24-hour downtime cost + 25% recovery/regulatory cost

EAL = likelihood × impact
```

The values are synthetic assumptions for the prototype. They are estimates,
not observed enterprise losses or financial advice.

## Run

From the project root:

```bash
python -m risk_engine.calculate
```