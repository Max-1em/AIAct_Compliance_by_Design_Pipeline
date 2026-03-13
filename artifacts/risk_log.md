# Risk Log
**Generated:** 2026-03-13 08:32 UTC
**Commit:** `abc1234def`
**Model:** MyEUComplianceModel v1.0.0

---

| # | Risk Description | Likelihood | Impact | Mitigation | Status |
|---|-----------------|-----------|--------|-----------|--------|
| 1 | Model produces biased outputs for protected groups | Medium | High | Bias metrics enforced via CI (see bias_metrics_config.json) | Open |
| 2 | Model used outside intended scope | Low | High | Documented out-of-scope list; user-facing warnings | Open |
| 3 | Data drift degrades model performance | Medium | Medium | Post-market monitoring enabled; review every 180 days | Open |
| 4 | Insufficient human oversight in automated pipeline | Low | High | Human-in-the-loop required for high-stakes decisions (Art. 14) | Open |
| 5 | Incomplete incident reporting | Low | Medium | Contact: compliance@example.com | Open |

---
*Review cycle: every 180 days or after any significant model update.*
