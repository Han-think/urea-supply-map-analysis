# Urea Supply Map Analysis

Public-safe regional analysis of a 2021 urea inventory sample for emergency supply planning.

![Municipality demand and supply map](figures/05_municipality_demand_supply_map.png)

## Executive summary

The original classroom dataset was described as nationwide, but the observed station sample was not suitable for a nationwide supply ranking. Most usable station records were concentrated in **Gyeonggi-do** and **Incheon**.

This project therefore reframes the problem:

- estimate regional urea demand;
- compare observed inventory with estimated daily demand;
- calculate inventory cover days and 3-day safety-stock gaps;
- anonymize station-level records for public release;
- simulate a 1,000,000 L allocation plan.

## Evaluation-oriented summary

This project was later reviewed against practical mini-project criteria:

- SCQA problem definition;
- MECE evidence structure;
- claim-based statistical validation;
- decision-oriented visualization;
- Action Plan / So What;
- public-safe GitHub packaging.

The main improvement lesson is that a stronger data project should start from the decision-maker, not from the CSV file.

## Quick links

| Item | Link |
|---|---|
| Notebook | [notebooks/urea_supply_map_analysis.ipynb](notebooks/urea_supply_map_analysis.ipynb) |
| Processed data | [data/processed/](data/processed/) |
| Boundary GeoJSON | [data/boundaries/gyeonggi_incheon_municipalities.geojson](data/boundaries/gyeonggi_incheon_municipalities.geojson) |
| Figures | [figures/](figures/) |
| Asset builder | [src/prepare_public_assets.py](src/prepare_public_assets.py) |
| Experience note | [../docs/project_experience.md](../docs/project_experience.md) |
| Evaluation reflection | [../docs/evaluation_reflection.md](../docs/evaluation_reflection.md) |

## Key numbers

| Metric | Value |
|---|---:|
| Provinces analyzed | 2 |
| Municipalities analyzed | 41 |
| Public-safe station records | 178 |
| Allocation simulation volume | 1,000,000 L |
| Safety-stock target | 3 days |

## Visual summary

### Demand scenarios

![Annual urea demand scenarios](figures/01_region_demand_scenarios.png)

### Top municipalities by estimated demand

![Top municipality demand](figures/02_top_municipality_demand.png)

### Observed station priority sample

![Station priority scatter](figures/03_station_priority_scatter.png)

### Allocation simulation

![Allocation simulation](figures/04_allocation_simulation.png)

## Data files

| File | Description |
|---|---|
| [region_supply_balance.csv](data/processed/region_supply_balance.csv) | Province-level demand, observed inventory, inventory cover days, and 3-day safety-stock gap |
| [municipality_demand_supply.csv](data/processed/municipality_demand_supply.csv) | Municipality-level estimated demand and observed supply indicators |
| [station_priority_anonymized.csv](data/processed/station_priority_anonymized.csv) | Public-safe station priority sample without station names, street addresses, or phone numbers |
| [allocation_simulation_1million_l.csv](data/processed/allocation_simulation_1million_l.csv) | 1,000,000 L allocation simulation using minimum reserve, demand share, and emergency top-up |
| [demand_scenario_assumptions.csv](data/processed/demand_scenario_assumptions.csv) | Low, base, and high scenario assumptions |

## What is included

- Demand estimates by province and municipality
- Safety-stock gap estimates using daily demand and a 3-day reserve target
- An anonymized station priority table
- A 1,000,000 L allocation simulation with:
  - 20% minimum reserve;
  - 70% demand-proportional allocation;
  - 10% emergency top-up for safety-stock gaps.
- English charts and a compact Jupyter notebook

## What is excluded

For public safety and copyright hygiene, this repository excludes:

- instructor PDF materials;
- original classroom notebooks;
- raw station names, street addresses, and phone numbers;
- broken/mojibake intermediate exports;
- nationwide supply rankings that would overstate sample coverage.

## Repository structure

```text
data/
  processed/      English-column CSV files used by the notebook
  boundaries/     Filtered Gyeonggi/Incheon municipality GeoJSON
figures/          English summary charts and map imagery
notebooks/        Reproducible analysis notebook
src/              Asset preparation script
```

## Quick start

```bash
pip install -r requirements.txt
jupyter notebook notebooks/urea_supply_map_analysis.ipynb
```

## Key interpretation

Inventory is compared with estimated **daily demand**, not directly with annual demand. The main operational metric is `inventory_cover_days`, supported by a 3-day safety-stock target.

## Data note

The public CSV files are derived from aggregated vehicle, mileage, and observed station inventory tables. Station-level records are anonymized before publication.
