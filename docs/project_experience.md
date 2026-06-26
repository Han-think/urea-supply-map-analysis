# Project Experience Note

## Context

This project started as a classroom-style urea supply analysis. The first version looked usable as a nationwide supply strategy, but the data quality checks showed that the observed station inventory sample was not evenly distributed across the country.

The important lesson was simple: a polished chart is not enough if the data scope is wrong.

## What changed during the work

### 1. Scope was corrected

The station inventory data was treated as an observed sample rather than a complete national inventory dataset.

Because most usable observations were concentrated in Gyeonggi-do and Incheon, the final public version limits the supply-side interpretation to those two regions.

### 2. Demand and supply were separated

Demand estimation and observed inventory analysis were handled as different layers:

- demand is estimated from vehicle and mileage assumptions;
- supply is based only on observed station inventory records;
- missing regions are not filled with artificial inventory, price, or priority scores.

### 3. The operating metric was reframed

Annual demand and one-time inventory are not directly comparable. The final version compares inventory with estimated daily demand and uses:

- inventory cover days;
- 3-day safety-stock target;
- safety-stock gap;
- allocation simulation.

### 4. Public release hygiene was improved

The public GitHub version removes materials that should not be published:

- instructor PDF files;
- original classroom notebooks;
- raw station names;
- street addresses;
- phone numbers;
- broken intermediate exports.

The released station dataset uses anonymized station IDs and English column names.

## Final public package

The repository now contains:

- a compact analysis notebook;
- processed CSV files with English column names;
- summary charts;
- a municipality-level map image;
- a reproducible asset preparation script;
- README pages with direct links and visual previews.

## What I learned

This project was less about making one more chart and more about learning how to protect analysis credibility.

The biggest decisions were:

- do not overclaim national coverage;
- do not treat unobserved regions as zero inventory;
- do not publish raw location/contact details unnecessarily;
- make the analysis reproducible and readable for someone opening the repository later.

That turned the project from a rough classroom artifact into a cleaner portfolio-style data analysis package.
