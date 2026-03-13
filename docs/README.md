# EU AI Act Compliance Pipeline

Automatically generates compliance artifacts on every push via GitHub Actions.

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── pipeline.yml        # GitHub Actions workflow
├── docs/
│   ├── model_card.txt          # Model metadata (edit this)
│   ├── bias_metrics_config.json # Fairness thresholds
│   ├── compliance_config.json  # EU AI Act settings
│   ├── generate_docs.py        # Artifact generator
│   ├── README.md               # This file
│   ├── test_model.py           # Model tests (placeholder)
│   └── train.py                # Training script (placeholder)
└── artifacts/                  # ← Generated on every CI run
    ├── technical_documentation.md
    ├── risk_log.md
    ├── model_card.md
    ├── data_card.md
    └── manifest.json           # Traceability manifest (commit SHA, timestamp)
```

## Generated Artifacts

| File | EU AI Act Requirement |
|------|----------------------|
| `technical_documentation.md` | Art. 11 – Technical documentation |
| `risk_log.md` | Art. 9 – Risk management system |
| `model_card.md` | Art. 13 – Transparency |
| `data_card.md` | Art. 10 – Data governance |
| `manifest.json` | Traceability / version hash |

## How It Works

1. **Push** any commit → GitHub Actions triggers automatically.
2. `generate_docs.py` reads the three config files in `docs/` and renders all templates.
3. Artifacts are uploaded to the **Actions run** (retained 90 days) and tagged with the commit SHA.
4. On `main` branch pushes a git tag `compliance-<date>-<sha>` is created for long-term traceability.

## Customisation

- **Model metadata** → edit `docs/model_card.txt`
- **Fairness thresholds** → edit `docs/bias_metrics_config.json`
- **Risk level / articles** → edit `docs/compliance_config.json`

## Local Test Run

```bash
pip install jinja2
python docs/generate_docs.py --commit abc1234 --run-id 0 --actor you --ref main
# Artifacts appear in ./artifacts/
```
