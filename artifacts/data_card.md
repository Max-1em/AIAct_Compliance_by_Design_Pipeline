# Data Card
**Generated:** 2026-03-13 08:32 UTC
**Commit:** `abc1234def`
**Model:** MyEUComplianceModel v1.0.0

---

## Dataset Summary
| Field | Value |
|-------|-------|
| Description | Internal labeled dataset, 50 000 samples, 2022–2024 |
| Protected attributes | gender, age_group, nationality |
| Evaluation set | data/bias_eval_set.csv |

## Collection & Consent
- Data collected under internal data governance policy.
- Personal data processed in compliance with GDPR.
- No sensitive special-category data included.

## Known Limitations
- Dataset covers 2022–2024; performance on more recent distributions is unverified.
- Class balance may not reflect real-world deployment distribution.

## Bias Evaluation Configuration
See `docs/bias_metrics_config.json` for full metric definitions and thresholds.
