"""Build a GitHub-safe public version of the urea supply analysis.

The source package contains classroom/original materials and Korean CSV files
whose headers were already mojibake in the exported archive.  This script keeps
only derived, presentation-safe assets and rewrites them with English column
names.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat as nbf
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = PROJECT_ROOT.parent / "public_repo_work"

OUT_DATA = PROJECT_ROOT / "data" / "processed"
OUT_BOUNDARY = PROJECT_ROOT / "data" / "boundaries"
OUT_FIG = PROJECT_ROOT / "figures"
OUT_NOTEBOOK = PROJECT_ROOT / "notebooks"

PROVINCE_ORDER = ["Gyeonggi-do", "Incheon"]


def _mkdirs() -> None:
    for path in [OUT_DATA, OUT_BOUNDARY, OUT_FIG, OUT_NOTEBOOK]:
        path.mkdir(parents=True, exist_ok=True)


def _read_csv(relative_path: str) -> pd.DataFrame:
    return pd.read_csv(WORK_ROOT / relative_path)


def province_from_raw(series: pd.Series) -> pd.Series:
    """Convert mojibake province labels by their observed order.

    The source export contains two province labels.  In every derived file they
    appear in the same order: Gyeonggi-do first, Incheon second.
    """

    values = [value for value in pd.unique(series.dropna())]
    mapping = {value: PROVINCE_ORDER[i] for i, value in enumerate(values[: len(PROVINCE_ORDER)])}
    return series.map(mapping)


def build_region_balance() -> pd.DataFrame:
    raw = _read_csv("output/region_supply_balance_safety_stock.csv")
    df = pd.DataFrame(
        {
            "province": province_from_raw(raw.iloc[:, 0]),
            "annual_demand_low_l": raw.iloc[:, 1],
            "annual_demand_base_l": raw.iloc[:, 2],
            "annual_demand_high_l": raw.iloc[:, 3],
            "avg_annual_mileage_km": raw.iloc[:, 4],
            "observed_station_count": raw.iloc[:, 12],
            "observed_inventory_l": raw.iloc[:, 13],
            "avg_observed_inventory_l": raw.iloc[:, 14],
            "avg_price_krw_per_l": raw.iloc[:, 16],
            "regional_supply_priority_score": raw.iloc[:, 28],
            "daily_demand_base_l": raw.iloc[:, 31],
            "inventory_cover_days": raw.iloc[:, 32],
            "target_safety_stock_3days_l": raw.iloc[:, 33],
            "safety_stock_gap_l": raw.iloc[:, 34],
            "demand_share_pct": raw.iloc[:, 35],
            "inventory_share_pct": raw.iloc[:, 36],
            "share_gap_pp": raw.iloc[:, 37],
        }
    )
    df = df.sort_values("annual_demand_base_l", ascending=False).reset_index(drop=True)
    df.to_csv(OUT_DATA / "region_supply_balance.csv", index=False, encoding="utf-8")
    return df


def build_scenario_assumptions() -> pd.DataFrame:
    df = _read_csv("output/demand_scenario_assumptions.csv")
    out = pd.DataFrame(
        {
            "scenario": ["Low", "Base", "High"],
            "scr_adoption_rate": [0.10, 0.166, 0.25],
            "urea_use_l_per_10l_diesel": [1, 1, 1],
            "truck_fuel_efficiency_km_per_10l": [400, 350, 300],
            "meaning": [
                "Conservative demand case",
                "Planning baseline",
                "Stress case for emergency reserves",
            ],
        }
    )
    out.to_csv(OUT_DATA / "demand_scenario_assumptions.csv", index=False, encoding="utf-8")
    return out


def build_sigungu() -> pd.DataFrame:
    raw = _read_csv("output/sigungu_demand_supply_geo_result_REVISED.csv")
    df = pd.DataFrame(
        {
            "province": province_from_raw(raw.iloc[:, 0]),
            "municipality": raw.iloc[:, 4],
            "municipality_code": raw.iloc[:, 5].astype(str),
            "total_registered_vehicles": raw.iloc[:, 6],
            "estimated_diesel_trucks": raw.iloc[:, 7],
            "annual_demand_base_l": raw.iloc[:, 8],
            "demand_share": raw.iloc[:, 9],
            "observed_station_count": raw.iloc[:, 10],
            "observed_station_count_with_stock": raw.iloc[:, 11],
            "observed_inventory_l": raw.iloc[:, 12],
            "avg_price_krw_per_l": raw.iloc[:, 13],
            "municipality_priority_score": raw.iloc[:, 14],
            "daily_demand_base_l": raw.iloc[:, 19],
            "target_safety_stock_3days_l": raw.iloc[:, 20],
            "inventory_cover_days": raw.iloc[:, 21],
            "safety_stock_gap_l": raw.iloc[:, 22],
            "demand_rank_score": raw.iloc[:, 25],
            "supply_availability_score": raw.iloc[:, 26],
        }
    )
    df["province"] = df["province"].fillna("Unknown")
    df = df.sort_values("annual_demand_base_l", ascending=False).reset_index(drop=True)
    df.to_csv(OUT_DATA / "municipality_demand_supply.csv", index=False, encoding="utf-8")
    return df


def build_station_public() -> pd.DataFrame:
    raw = _read_csv("output/station_supply_priority_REVISED.csv")
    df = pd.DataFrame(
        {
            "station_public_id": [f"STN-{i:03d}" for i in range(1, len(raw) + 1)],
            "province": province_from_raw(raw.iloc[:, 3]),
            "inventory_l": raw.iloc[:, 5],
            "price_krw_per_l": raw.iloc[:, 6],
            "latitude": raw.iloc[:, 7],
            "longitude": raw.iloc[:, 8],
            "stock_status_color": raw.iloc[:, 9],
            "observed_at": raw.iloc[:, 10],
            "regional_demand_base_l": raw.iloc[:, 12],
            "station_inventory_score": raw.iloc[:, 21],
            "station_price_pressure_score": raw.iloc[:, 22],
            "station_supply_priority_score": raw.iloc[:, 23],
            "station_priority_rank": raw.iloc[:, 24],
            "municipality_supply_availability_score": raw.iloc[:, 35],
            "final_priority_score": raw.iloc[:, 36],
            "final_priority_rank": raw.iloc[:, 37],
        }
    )
    df = df.sort_values("final_priority_rank", ascending=True).reset_index(drop=True)
    df.to_csv(OUT_DATA / "station_priority_anonymized.csv", index=False, encoding="utf-8")
    return df


def build_allocation() -> pd.DataFrame:
    raw = _read_csv("output/sigungu_allocation_simulation_1million_L.csv")
    df = pd.DataFrame(
        {
            "province": province_from_raw(raw.iloc[:, 0]),
            "municipality": raw.iloc[:, 4],
            "annual_demand_base_l": raw.iloc[:, 8],
            "observed_inventory_l": raw.iloc[:, 12],
            "safety_stock_gap_l": raw.iloc[:, 21],
            "minimum_reserve_l": raw.iloc[:, 22],
            "demand_proportional_l": raw.iloc[:, 23],
            "emergency_topup_l": raw.iloc[:, 24],
            "recommended_allocation_l": raw.iloc[:, 25],
        }
    )
    df["province"] = df["province"].fillna("Unknown")
    df = df.sort_values("recommended_allocation_l", ascending=False).reset_index(drop=True)
    df.to_csv(OUT_DATA / "allocation_simulation_1million_l.csv", index=False, encoding="utf-8")
    return df


def build_boundary(sigungu: pd.DataFrame) -> None:
    source = WORK_ROOT / "data" / "skorea-municipalities-2018-geo.json"
    geo = json.loads(source.read_text(encoding="utf-8"))
    wanted_codes = set(sigungu["municipality_code"].astype(str))
    rows = sigungu.set_index("municipality_code").to_dict("index")
    features = []
    for feature in geo["features"]:
        code = str(feature.get("properties", {}).get("code", ""))
        if code not in wanted_codes:
            continue
        row = rows.get(code, {})
        feature["properties"] = {
            "province": row.get("province"),
            "municipality": row.get("municipality"),
            "municipality_code": code,
            "annual_demand_base_l": row.get("annual_demand_base_l"),
            "observed_inventory_l": row.get("observed_inventory_l"),
            "safety_stock_gap_l": row.get("safety_stock_gap_l"),
        }
        features.append(feature)
    out = {"type": "FeatureCollection", "features": features}
    (OUT_BOUNDARY / "gyeonggi_incheon_municipalities.geojson").write_text(
        json.dumps(out, ensure_ascii=False), encoding="utf-8"
    )


def make_figures(region: pd.DataFrame, sigungu: pd.DataFrame, station: pd.DataFrame, allocation: pd.DataFrame) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    region.plot(
        x="province",
        y=["annual_demand_low_l", "annual_demand_base_l", "annual_demand_high_l"],
        kind="bar",
        ax=ax,
        color=["#9ecae1", "#3182bd", "#08519c"],
    )
    ax.set_title("Annual Urea Demand Scenarios")
    ax.set_ylabel("Liters per year")
    ax.set_xlabel("")
    ax.legend(["Low", "Base", "High"])
    fig.tight_layout()
    fig.savefig(OUT_FIG / "01_region_demand_scenarios.png", dpi=180)
    plt.close(fig)

    top = sigungu.nlargest(15, "annual_demand_base_l").sort_values("annual_demand_base_l")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top["municipality"], top["annual_demand_base_l"], color="#de2d26")
    ax.set_title("Top 15 Municipalities by Estimated Demand")
    ax.set_xlabel("Annual demand, liters")
    fig.tight_layout()
    fig.savefig(OUT_FIG / "02_top_municipality_demand.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(
        station["longitude"],
        station["latitude"],
        s=(station["inventory_l"].clip(lower=0) / station["inventory_l"].max() * 220 + 20),
        c=station["final_priority_score"],
        cmap="Reds",
        alpha=0.72,
        edgecolor="white",
        linewidth=0.4,
    )
    ax.set_title("Observed Station Priority Sample")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.colorbar(scatter, ax=ax, label="Priority score")
    fig.tight_layout()
    fig.savefig(OUT_FIG / "03_station_priority_scatter.png", dpi=180)
    plt.close(fig)

    top_alloc = allocation.nlargest(15, "recommended_allocation_l").sort_values("recommended_allocation_l")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top_alloc["municipality"], top_alloc["recommended_allocation_l"], color="#756bb1")
    ax.set_title("1,000,000 L Allocation Simulation")
    ax.set_xlabel("Recommended allocation, liters")
    fig.tight_layout()
    fig.savefig(OUT_FIG / "04_allocation_simulation.png", dpi=180)
    plt.close(fig)


def make_notebook() -> None:
    nb = nbf.v4.new_notebook()
    nb["cells"] = [
        nbf.v4.new_markdown_cell(
            "# Urea Supply Map Analysis\n\n"
            "A compact, GitHub-safe analysis of the 2021 urea inventory sample, "
            "restricted to Gyeonggi-do and Incheon because the observed station sample "
            "is heavily concentrated in those two regions."
        ),
        nbf.v4.new_markdown_cell(
            "## Scope\n\n"
            "- The station sample is treated as an observed sample, not a national census.\n"
            "- Station names, street addresses, and phone numbers are excluded from the public dataset.\n"
            "- Demand estimates use explicit scenario assumptions and public aggregated vehicle/mileage tables."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n\n"
            "ROOT = Path('..')\n"
            "DATA = ROOT / 'data' / 'processed'\n"
            "FIG = ROOT / 'figures'\n\n"
            "region = pd.read_csv(DATA / 'region_supply_balance.csv')\n"
            "municipality = pd.read_csv(DATA / 'municipality_demand_supply.csv')\n"
            "station = pd.read_csv(DATA / 'station_priority_anonymized.csv')\n"
            "allocation = pd.read_csv(DATA / 'allocation_simulation_1million_l.csv')\n"
            "region"
        ),
        nbf.v4.new_code_cell(
            "cols = ['province', 'annual_demand_base_l', 'observed_inventory_l', "
            "'inventory_cover_days', 'safety_stock_gap_l']\n"
            "region[cols].sort_values('annual_demand_base_l', ascending=False)"
        ),
        nbf.v4.new_code_cell(
            "municipality[['province','municipality','annual_demand_base_l',"
            "'observed_inventory_l','safety_stock_gap_l']].head(15)"
        ),
        nbf.v4.new_code_cell(
            "fig, ax = plt.subplots(figsize=(8, 4.5))\n"
            "region.plot(x='province', y=['annual_demand_low_l','annual_demand_base_l','annual_demand_high_l'], "
            "kind='bar', ax=ax)\n"
            "ax.set_title('Annual Urea Demand Scenarios')\n"
            "ax.set_ylabel('Liters per year')\n"
            "ax.set_xlabel('')\n"
            "plt.tight_layout()"
        ),
        nbf.v4.new_code_cell(
            "top = municipality.nlargest(15, 'annual_demand_base_l').sort_values('annual_demand_base_l')\n"
            "fig, ax = plt.subplots(figsize=(8, 6))\n"
            "ax.barh(top['municipality'], top['annual_demand_base_l'], color='#de2d26')\n"
            "ax.set_title('Top 15 Municipalities by Estimated Demand')\n"
            "ax.set_xlabel('Annual demand, liters')\n"
            "plt.tight_layout()"
        ),
        nbf.v4.new_code_cell(
            "fig, ax = plt.subplots(figsize=(7,5))\n"
            "scatter = ax.scatter(station['longitude'], station['latitude'], "
            "s=(station['inventory_l'].clip(lower=0)/station['inventory_l'].max()*220+20), "
            "c=station['final_priority_score'], cmap='Reds', alpha=0.72, edgecolor='white', linewidth=0.4)\n"
            "ax.set_title('Observed Station Priority Sample')\n"
            "ax.set_xlabel('Longitude')\n"
            "ax.set_ylabel('Latitude')\n"
            "plt.colorbar(scatter, ax=ax, label='Priority score')\n"
            "plt.tight_layout()"
        ),
        nbf.v4.new_code_cell(
            "allocation[['province','municipality','minimum_reserve_l','demand_proportional_l',"
            "'emergency_topup_l','recommended_allocation_l']].head(15)"
        ),
    ]
    nbf.write(nb, OUT_NOTEBOOK / "urea_supply_map_analysis.ipynb")


def write_project_files() -> None:
    (PROJECT_ROOT / ".gitignore").write_text(
        "\n".join(
            [
                "__pycache__/",
                ".ipynb_checkpoints/",
                ".DS_Store",
                "*.pyc",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (PROJECT_ROOT / "requirements.txt").write_text(
        "pandas\nmatplotlib\njupyter\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "LICENSE").write_text(
        "MIT License\n\n"
        "Copyright (c) 2026\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy "
        "of this software and associated documentation files (the \"Software\"), to deal "
        "in the Software without restriction, including without limitation the rights "
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
        "copies of the Software, and to permit persons to whom the Software is "
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all "
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
        "SOFTWARE.\n",
        encoding="utf-8",
    )
    readme = """# Urea Supply Map Analysis

Lightweight public analysis of a 2021 urea inventory sample for emergency supply planning.

## Why the scope is limited

The original classroom dataset is described as nationwide, but the observed station inventory sample is not suitable for a nationwide supply ranking. Most usable station observations are concentrated in **Gyeonggi-do** and **Incheon**, so this public version treats the data as a regional sample and avoids filling missing regions with artificial inventory or price values.

## What is included

- Demand estimates by province and municipality
- Safety-stock gap estimates using daily demand and a 3-day reserve target
- An anonymized station priority table
- A 1,000,000 L allocation simulation with:
  - 20% minimum regional reserve
  - 70% demand-proportional allocation
  - 10% emergency top-up for safety-stock gaps
- English charts and a compact Jupyter notebook

## What is excluded

For public safety and copyright hygiene, this repository excludes:

- instructor PDF materials
- original classroom notebooks
- raw station names, street addresses, and phone numbers
- broken/mojibake intermediate exports
- nationwide supply rankings that would overstate sample coverage

## Repository structure

```text
data/
  processed/      English-column CSV files used by the notebook
  boundaries/     Filtered Gyeonggi/Incheon municipality GeoJSON
figures/          English summary charts
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
"""
    (PROJECT_ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    _mkdirs()
    region = build_region_balance()
    build_scenario_assumptions()
    sigungu = build_sigungu()
    station = build_station_public()
    allocation = build_allocation()
    build_boundary(sigungu)
    make_figures(region, sigungu, station, allocation)
    make_notebook()
    write_project_files()


if __name__ == "__main__":
    main()
