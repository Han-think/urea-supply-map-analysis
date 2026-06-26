# Evaluation Reflection

This note is a self-review of the urea supply mini-project. It focuses on what should be improved in future data projects, not on ranking or criticizing other teams.

## 1. Evaluation criteria understood after review

The project should be evaluated less as a simple analysis notebook and more as a practical decision-support report.

| Criterion | Meaning for future projects |
|---|---|
| SCQA | Define the data-analysis problem as a decision problem. |
| MECE / pyramid logic | Organize evidence without overlap or gaps. |
| Statistical evidence | Use tests or models to support specific claims, not as decoration. |
| Visualization | Show charts that help the audience make a decision quickly. |
| Action Plan / So What | End with who should do what, when, and how success will be measured. |
| Slide limit | Compress the main story and move details to appendix. |

## 2. What worked in this project

### 2.1 Scope correction

The original classroom dataset looked like a national urea inventory dataset at first glance, but the usable station observations were concentrated in Gyeonggi-do and Incheon. The final public version avoided overclaiming national coverage and reframed the project as a regional supply-planning analysis.

### 2.2 Public-release hygiene

The public repository removed materials that should not be published, including instructor materials, raw station names, street addresses, phone numbers, and broken intermediate exports. The released station-level data uses anonymized station IDs and English column names.

### 2.3 Operational metric

The project moved from simple inventory comparison to an operating metric: inventory cover days against estimated daily demand. This was supported by a 3-day safety-stock target and an allocation simulation.

### 2.4 Reproducible package

The repository contains processed CSV files, a compact notebook, summary figures, map imagery, and an asset-preparation script. This makes the project easier to reopen, review, and reuse later.

## 3. What was weak

### 3.1 The decision-maker was not visible enough

The analysis should have stated earlier that the intended audience was a urea supplier or dispatch manager. Without a clear decision-maker, the analysis can look like a collection of useful charts rather than a decision-support system.

Improved framing:

> This project supports a urea supplier's dispatch manager who must decide every evening which stations should receive priority replenishment.

### 3.2 SCQA was not explicit enough

The project had a reasonable problem structure, but it was not presented as a clear SCQA story.

Improved SCQA:

| SCQA | Project version |
|---|---|
| Situation | Urea inventory and demand-related data are available, but observed station inventory is concentrated in Gyeonggi-do and Incheon. |
| Complication | If the data is treated as a national inventory dataset, the analysis may create misleading priorities and miss regional shortage risks. |
| Question | Which municipalities and stations in Gyeonggi-do and Incheon should receive urea replenishment first? |
| Answer | Combine estimated regional demand with station-level inventory cover days, classify stations into priority groups, and replenish high-risk stations first. |

### 3.3 MECE framework should have been shown as a table

The project used several useful concepts, but the evidence structure should have been shown more directly.

Improved MECE framework:

| Evidence axis | Question answered | Output |
|---|---|---|
| Demand pressure | Where is urea likely to be needed most? | Municipality-level estimated demand |
| Inventory shortage | How long can current inventory cover expected demand? | `inventory_cover_days` |
| Safety-stock gap | Which areas fall below the target reserve? | 3-day safety-stock gap |
| Observation reliability | Which areas can be interpreted safely from observed data? | Regional scope limitation |
| Dispatch feasibility | How should limited replenishment volume be allocated? | Priority group and allocation simulation |

### 3.4 Statistical analysis should be tied to claims

Statistical methods should not be added just to satisfy a checklist. Each method should support a claim.

Candidate validation plan:

| Claim | Possible validation |
|---|---|
| High-demand areas require differentiated replenishment. | Compare inventory cover days between high-demand and low-demand municipalities. |
| Price alone is not enough to identify shortage risk. | Check correlation between price and inventory cover days or safety-stock gap. |
| Safety-stock gaps differ by municipality group. | Use ANOVA or a non-parametric alternative if assumptions are not met. |
| Priority score is explainable. | Check how demand, inventory, and safety-stock gap contribute to the priority score. |

### 3.5 Action Plan should have been the final slide

The project included an allocation simulation, but the final message should have been converted into a concrete operating procedure.

Improved Action Plan:

1. Update station inventory data every day at 18:00.
2. Estimate municipality-level demand pressure.
3. Calculate station-level inventory cover days.
4. Classify stations into A/B/C priority groups.
5. Replenish A-priority stations the same night.
6. Replenish B-priority stations the next morning.
7. Keep C-priority stations on regular delivery.
8. Review next-day shortage events and safety-stock achievement rate.

## 4. Future project rule

Before opening the dataset or writing code, fill out this table first.

| Item | Required answer |
|---|---|
| Decision-maker | Who will use the result? |
| Decision timing | When will they use it? |
| Decision | What must they decide? |
| Situation | What is happening now? |
| Complication | What goes wrong if nothing changes? |
| Question | What question must the analysis answer? |
| Answer | What action should be taken? |
| MECE axes | What non-overlapping evidence supports the answer? |
| Validation | Which tests, models, or comparisons support the claims? |
| Visualization | Which charts directly support the decision? |
| Action Plan | Who does what, when, and how? |
| KPI | How will success be measured? |

## 5. Personal takeaway

The main lesson is that data analysis is not just about making charts or building a model. A stronger project should change a decision.

Future structure:

```text
Decision-maker
-> Problem
-> SCQA
-> MECE evidence structure
-> Analysis and validation
-> Top message
-> Action Plan
-> KPI
```

The next project should start from the decision-maker, not from the CSV file.
