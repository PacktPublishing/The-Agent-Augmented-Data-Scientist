---
name: cg-ds-standards
description: >
  Shared analytical standards for Cascade Goods.
  Read when planning, checking, or communicating analytical work.
owner: Maya S, Senior Data Scientist
status: draft
last_reviewed: 2026-09-27
---

# Cascade Goods DS Standards

Shared conventions for analytical work at Cascade Goods. Follow these defaults. If a task calls for a different convention, surface the difference and agree the exception with the responsible data scientist before applying it. Record the reason and continue to follow the applicable data-handling and review requirements.

## Shared analytical standards

- Use the metric registry and data dictionary for shared definitions. Surface conflicting definitions before using them.
- Support conclusions with evidence. Distinguish observations, assumptions, and interpretation.
- Preserve source references, code, parameters, and random seeds needed to reproduce results.

## Code and notebook hygiene

- Use `snake_case` for Python variables, functions, SQL aliases, and filenames.
- Use four-space indentation in Python and SQL.
- Write SQL keywords in uppercase and list selected columns explicitly.
- Use descriptive names; avoid unexplained abbreviations.
- Extract repeated logic into functions when it improves readability.
- Give reusable functions short docstrings covering purpose, inputs, and outputs.
- Comment on business logic and non-obvious choices.
- Organize notebooks into: Question, Inputs, Analysis, Findings, and Limitations.
- Introduce each major notebook section with a short Markdown explanation.
- Before sharing, restart the kernel and run all cells in order.
- Use random seed `42` for stochastic steps and record it.

## Visualization

- Use `matplotlib` for static charts.
- Use a white background and DejaVu Sans font.
- Default figure size: 8 × 5 inches.
- Font sizes: title 14 pt; axis labels 11 pt; ticks, legends, and captions 10 pt.
- Use navy `#17324D` for text and teal `#147D92` for a single data series.
- For multiple categories, use this order: blue `#0072B2`, orange `#E69F00`, green `#009E73`, purple `#CC79A7`, vermilion `#D55E00`.
- Keep category colors consistent across charts within an analysis.
- Use gray `#9AA0A6` for background or comparison groups.
- Pair color with labels, markers, or line styles when distinction matters.
- Use horizontal gridlines in `#E5E7EB`; remove top and right borders.
- Give every chart a clear title, units, and reporting period.
- Use legends only when multiple series require identification.
- Add a one- or two-sentence caption explaining the finding and a material caveat, if applicable.
- Start bar-chart value axes at zero. Clearly indicate any restricted range on other charts.
- Export charts as PNG at 300 DPI and SVG, with tight bounding boxes.

## Numbers and dates

- Metric-specific display rules take precedence over these defaults.
- Counts: whole numbers with thousands separators, such as `12,345`.
- Currency: currency code and two decimal places, such as `USD 1,234.56`.
- Percentages: one decimal place, such as `12.3%`.
- Percentage-point changes: signed values with one decimal place, such as `+2.1 pp`.
- Other decimal measures: two decimal places.
- Show additional precision when rounding would hide a meaningful difference.
- Display missing or undefined values as `N/A`, never as zero.
- Round for display only; retain calculation precision.
- Store dates as `YYYY-MM-DD` and timestamps in UTC.
- Use `Jan 2025` for monthly chart labels.

## Files and exports

- Export flat tables as UTF-8 CSV without a dataframe index.
- Save generated work under `outputs/<analysis_name>/<run_id>/`.
- Use UTC run IDs in `YYYYMMDDTHHMMSSZ` format.
- Use lowercase, descriptive filenames, such as `monthly_net_aov.csv`.
- Preserve source files; save transformed data separately.
- Export scikit-learn models with `joblib`; load artifacts only from trusted sources.
- Save model features, parameters, and dependency versions alongside the model.

## Tech stack

- Python baseline: 3.11.
- SQL dialect: SQLite for the local companion data.
- Data manipulation: `pandas` and `numpy`.
- Static visualization: `matplotlib`.
- Statistical analysis: `scipy` and `statsmodels`.
- Machine learning: `scikit-learn`.
- Model serialization: `joblib`.
- Keep the existing purchase-metrics runner standard-library-only.
- Use a project virtual environment; pin exact dependencies in `requirements.txt` when configuring it.
- Record the Python and SQLite runtime versions used for each analysis.
- Use parameterized SQL for input values.
- Select only required columns and filter the relevant period where this preserves the calculation.
- Propose additional dependencies before adding them.

## Communication, data handling, and review

- Lead with the answer, then evidence and material limitations.
- Use short paragraphs and direct language; avoid filler and em dashes.
- Follow the data-handling requirements in Team Context.
- Share aggregate results by default; include customer-level details only when required and permitted.
- Never include credentials in code, notebooks, or exported artifacts.
- Show proposed changes to the requester before committing.
- PR descriptions must include: Why, Changes, Validation, and Limitations.
- Obtain the required review before merging.

## Supporting references and upkeep

- [Business context](../context/business_context.md): company and purchasing concepts.
- [Team context](../context/team_context.md): responsibilities, working norms, and review arrangements.
- [Data documentation](../data/README.md): fields, grain, conventions, and relationships.
- [Metric registry](../context/metric_registry.md): shared metric definitions, calculations, and calculation tests.

When a failure exposes a reusable gap, propose an update to the relevant context, standard, or playbook. The file owner reviews changes.
