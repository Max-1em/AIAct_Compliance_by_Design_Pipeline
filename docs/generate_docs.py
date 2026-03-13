"""
generate_docs.py
Generates EU AI Act compliance artifacts on every CI run.
Usage:
    python docs/generate_docs.py \
        --commit <sha> --run-id <id> --actor <user> --ref <branch>
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Templates (inline – no extra files needed)
# ---------------------------------------------------------------------------

TECH_DOC_TEMPLATE = """\
# Technical Documentation
**Generated:** {timestamp}
**Commit:** `{commit}`
**Branch/Ref:** {ref}
**Run ID:** {run_id}
**Triggered by:** {actor}

---

## 1  System Overview
**Model name:** {model_name}
**Version:** {model_version}
**Type:** {model_type}
**Framework:** {framework}

## 2  Intended Use
{intended_use}

### Out-of-scope uses
{out_of_scope}

## 3  Risk Classification (EU AI Act)
**Risk level:** {risk_level}
**Applicable articles:** {articles}

## 4  Training Data
{training_data}

## 5  Bias & Fairness Metrics
Protected attributes: {protected_attributes}

| Metric | Threshold |
|--------|-----------|
{bias_table}

## 6  Conformity Assessment
Method: {conformity_assessment}
Post-market monitoring: {post_market_monitoring}
Incident contact: {incident_contact}

## 7  Traceability
This document is automatically generated and versioned by the CI/CD pipeline.
Each build produces a uniquely identified artifact bundle tagged with the commit SHA.
"""

RISK_LOG_TEMPLATE = """\
# Risk Log
**Generated:** {timestamp}
**Commit:** `{commit}`
**Model:** {model_name} v{model_version}

---

| # | Risk Description | Likelihood | Impact | Mitigation | Status |
|---|-----------------|-----------|--------|-----------|--------|
| 1 | Model produces biased outputs for protected groups | Medium | High | Bias metrics enforced via CI (see bias_metrics_config.json) | Open |
| 2 | Model used outside intended scope | Low | High | Documented out-of-scope list; user-facing warnings | Open |
| 3 | Data drift degrades model performance | Medium | Medium | Post-market monitoring enabled; review every {review_cycle_days} days | Open |
| 4 | Insufficient human oversight in automated pipeline | Low | High | Human-in-the-loop required for high-stakes decisions (Art. 14) | Open |
| 5 | Incomplete incident reporting | Low | Medium | Contact: {incident_contact} | Open |

---
*Review cycle: every {review_cycle_days} days or after any significant model update.*
"""

MODEL_CARD_TEMPLATE = """\
# Model Card – {model_name}
**Generated:** {timestamp}
**Commit:** `{commit}`

---

## Model Details
| Field | Value |
|-------|-------|
| Name | {model_name} |
| Version | {model_version} |
| Type | {model_type} |
| Framework | {framework} |
| License | {license} |
| Contact | {contact} |

## Intended Use
{intended_use}

## Out-of-Scope Uses
{out_of_scope}

## Training Data
{training_data}

## Bias Evaluation
Protected attributes considered: {protected_attributes}

## EU AI Act Risk Category
**{risk_level}** – {articles}

## Caveats & Recommendations
- Always keep a human in the loop for consequential decisions.
- Re-evaluate bias metrics after every significant data or model update.
- Report incidents to: {incident_contact}
"""

DATA_CARD_TEMPLATE = """\
# Data Card
**Generated:** {timestamp}
**Commit:** `{commit}`
**Model:** {model_name} v{model_version}

---

## Dataset Summary
| Field | Value |
|-------|-------|
| Description | {training_data} |
| Protected attributes | {protected_attributes} |
| Evaluation set | {evaluation_dataset} |

## Collection & Consent
- Data collected under internal data governance policy.
- Personal data processed in compliance with GDPR.
- No sensitive special-category data included.

## Known Limitations
- Dataset covers 2022–2024; performance on more recent distributions is unverified.
- Class balance may not reflect real-world deployment distribution.

## Bias Evaluation Configuration
See `docs/bias_metrics_config.json` for full metric definitions and thresholds.
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_bias_table(metrics: list) -> str:
    rows = [f"| {m['name']} | {m['threshold']} |" for m in metrics]
    return "\n".join(rows)


def write_artifact(output_dir: Path, filename: str, content: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(content, encoding="utf-8")
    print(f"  ✓  {output_dir / filename}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", default="local")
    parser.add_argument("--run-id", default="local")
    parser.add_argument("--actor", default="local")
    parser.add_argument("--ref", default="local")
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    docs_dir = root / "docs"
    output_dir = root / "artifacts"

    # Load configs
    model_cfg = json.loads((docs_dir / "model_card.txt").read_text())
    bias_cfg = load_json(docs_dir / "bias_metrics_config.json")
    compliance_cfg = load_json(docs_dir / "compliance_config.json")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    eu = compliance_cfg["eu_ai_act"]
    doc_reqs = compliance_cfg["documentation_requirements"]

    ctx = {
        "timestamp": timestamp,
        "commit": args.commit,
        "run_id": args.run_id,
        "actor": args.actor,
        "ref": args.ref,
        # model
        "model_name": model_cfg["model_name"],
        "model_version": model_cfg["version"],
        "model_type": model_cfg["model_type"],
        "framework": model_cfg["framework"],
        "license": model_cfg["license"],
        "contact": model_cfg["contact"],
        "intended_use": model_cfg["intended_use"],
        "out_of_scope": "\n".join(f"- {u}" for u in model_cfg["out_of_scope"]),
        "training_data": model_cfg["training_data"],
        # bias
        "protected_attributes": ", ".join(bias_cfg["protected_attributes"]),
        "bias_table": build_bias_table(bias_cfg["metrics"]),
        "evaluation_dataset": bias_cfg["evaluation_dataset"],
        # compliance
        "risk_level": eu["risk_level"],
        "articles": ", ".join(eu["articles_applicable"]),
        "conformity_assessment": eu["conformity_assessment"],
        "post_market_monitoring": eu["post_market_monitoring"],
        "incident_contact": eu["incident_reporting_contact"],
        "review_cycle_days": compliance_cfg["review_cycle_days"],
    }

    print("\n🚀 Generating EU AI Act compliance artifacts...\n")

    if doc_reqs.get("technical_documentation"):
        write_artifact(output_dir, "technical_documentation.md",
                       TECH_DOC_TEMPLATE.format(**ctx))

    if doc_reqs.get("risk_log"):
        write_artifact(output_dir, "risk_log.md",
                       RISK_LOG_TEMPLATE.format(**ctx))

    if doc_reqs.get("model_card"):
        write_artifact(output_dir, "model_card.md",
                       MODEL_CARD_TEMPLATE.format(**ctx))

    if doc_reqs.get("data_card"):
        write_artifact(output_dir, "data_card.md",
                       DATA_CARD_TEMPLATE.format(**ctx))

    # Write a manifest with commit hash for traceability
    manifest = {
        "generated_at": timestamp,
        "commit": args.commit,
        "run_id": args.run_id,
        "actor": args.actor,
        "ref": args.ref,
        "artifacts": [f.name for f in output_dir.glob("*.md")],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"  ✓  {output_dir / 'manifest.json'}")
    print("\n✅ All artifacts generated successfully.\n")


if __name__ == "__main__":
    main()
