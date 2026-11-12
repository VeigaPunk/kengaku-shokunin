# Kengaku: report the Brier scale

[Brier 1950](https://www.u-cursos.cl/ingenieria/2025/1/CI71C/1/material_docente/bajar?bajar=1&id=8745481), January issue, issued April 15, defines a probability score over exclusive, exhaustive categories; its range is zero to two, including binary forecasts.

[Scikit-learn 1.7.2](https://scikit-learn.org/1.7/modules/generated/sklearn.metrics.brier_score_loss.html) documents scale_by_half, added in 1.7. Its default auto halves binary scores into zero to one but leaves multiclass scores on zero to two. Explicit True halves either.

A smaller reported value can therefore reflect normalization rather than improved forecasts. Record library version, class structure and scaling before comparing reports. Matching ranges alone does not establish comparable prediction tasks.

This supplements existing decomposition readings with a reporting convention, not a new estimator or universal best method. Unassimilated. No execution.

Original commentary only. Brier copy: reuse uncleared. Documentation: BSD notice; conditions apply.

Reviewed 2026-11-09. Space hold.

Destination: https://github.com/VeigaPunk/kengaku-shokunin, considerthese/2026-11-09-brier-reporting-scale.md.
