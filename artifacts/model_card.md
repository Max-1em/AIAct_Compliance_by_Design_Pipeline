# Model Card – MyEUComplianceModel
**Generated:** 2026-03-13 08:32 UTC
**Commit:** `abc1234def`

---

## Model Details
| Field | Value |
|-------|-------|
| Name | MyEUComplianceModel |
| Version | 1.0.0 |
| Type | classification |
| Framework | scikit-learn |
| License | Proprietary |
| Contact | ai-team@example.com |

## Intended Use
Automated document classification for internal compliance workflows

## Out-of-Scope Uses
- Medical diagnosis
- Law enforcement decisions
- Credit scoring

## Training Data
Internal labeled dataset, 50 000 samples, 2022–2024

## Bias Evaluation
Protected attributes considered: gender, age_group, nationality

## EU AI Act Risk Category
**limited** – Art. 13 – Transparency, Art. 14 – Human Oversight, Art. 52 – Transparency obligations

## Caveats & Recommendations
- Always keep a human in the loop for consequential decisions.
- Re-evaluate bias metrics after every significant data or model update.
- Report incidents to: compliance@example.com
