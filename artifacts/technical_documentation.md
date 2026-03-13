# Technical Documentation
**Generated:** 2026-03-13 08:32 UTC
**Commit:** `abc1234def`
**Branch/Ref:** main
**Run ID:** 42
**Triggered by:** testuser

---

## 1  System Overview
**Model name:** MyEUComplianceModel
**Version:** 1.0.0
**Type:** classification
**Framework:** scikit-learn

## 2  Intended Use
Automated document classification for internal compliance workflows

### Out-of-scope uses
- Medical diagnosis
- Law enforcement decisions
- Credit scoring

## 3  Risk Classification (EU AI Act)
**Risk level:** limited
**Applicable articles:** Art. 13 – Transparency, Art. 14 – Human Oversight, Art. 52 – Transparency obligations

## 4  Training Data
Internal labeled dataset, 50 000 samples, 2022–2024

## 5  Bias & Fairness Metrics
Protected attributes: gender, age_group, nationality

| Metric | Threshold |
|--------|-----------|
| demographic_parity_difference | 0.05 |
| equalized_odds_difference | 0.05 |
| accuracy_gap | 0.03 |

## 6  Conformity Assessment
Method: self-assessment
Post-market monitoring: True
Incident contact: compliance@example.com

## 7  Traceability
This document is automatically generated and versioned by the CI/CD pipeline.
Each build produces a uniquely identified artifact bundle tagged with the commit SHA.
