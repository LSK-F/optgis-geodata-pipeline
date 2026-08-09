# 🌍 OPTGIS Geodata Pipeline

A hybrid geospatial data engineering pipeline, developed with Python and R, for the preparation, geocoding, and spatial analysis of urban datasets.

This repository documents computational routines developed as part of a research project at the Laboratory of Optimization and Geographic Information Systems (OPTGIS), COPPE/UFRJ, within the context of a broader study on spatial indicators and transportation planning in the Rio de Janeiro Metropolitan Area, Brazil.

---

## Project context

The work was developed within the research activities of the OPTGIS laboratory, contributing to the GeoData Science component of a project focused on the synthesis of spatial indicators to support the analysis and planning of transportation systems.

The pipeline was designed to support the processing of large urban datasets.

Its main computational tasks include:

- Data cleaning and preprocessing;
- Address standardization;
- Large-scale address geocoding;
- Spatial data processing;
- Dasymetric interpolation;
- Spatial aggregation using the **H3** indexing system;
- Generation of cartographic visualizations.


> This work was developed during an Undergraduate Technological Research (ITI-A/CNPq) scholarship at the OPTGIS laboratory, COPPE/UFRJ.
> 
> The research involved a multidisciplinary team and was supervised by researchers from the laboratory. The routines documented in this repository represent the computational work developed within the project's GeoData Science activities.

---

## Research application

The methodology was developed to support the analysis of urban and transportation-related spatial patterns in the Rio de Janeiro Metropolitan Area.

In particular, the project contributed to the processing and synthesis of spatial information that could be incorporated into discussions concerning transportation infrastructure and route planning.

The spatial analysis employed H3, a hierarchical spatial indexing system developed by Uber, to aggregate observations into a regular hexagonal spatial grid.

This representation provides a consistent spatial framework for exploratory analysis and the construction of spatial indicators.

---

## Technologies

The project uses a hybrid architecture combining tools from the Python and R ecosystems.

### Python

Python is used for data preparation, spatial processing, H3 aggregation, and visualization.

Main libraries:

- `pandas`
- `geopandas`
- `shapely`
- `h3`
- `mapclassify`
- `matplotlib`
- `folium`
- `ipykernel`

### R

R is primarily used for address geocoding and geospatial data processing.

Main packages:

- `geocodebr`
- `sf`

## Reproducibility

### Requirements

The following software is required to reproduce the computational environment:

- Python 3.14+
- R 4.6+
- [uv](https://docs.astral.sh/uv/)

---

### 1. Clone the repository

```bash
git clone https://github.com/LSK-F/optgis-geodata-pipeline.git
cd optgis-geodata-pipeline
```

---

### 2. Install Python dependencies

From the project root:

```bash
uv sync
```

This command uses `uv.lock` to install the pinned Python dependencies and creates the virtual environment:

```text
.venv/
```

---

### 3. Install R dependencies

Run the provided installation script:

```bash
Rscript src/install_r_dependencies.R
```

Or open your R environment, ensure your working directory is set to the project root, and execute:

```R
source("src/install_r_dependencies.R")
```

---

## Running the pipeline

The computational workflow is organized into three main stages.

### 1. Data ETL

Place the raw datasets in:

```text
data/raw/
```

Then run:

```bash
python src/etl/01_etl_censo_escolar.py
```

This stage performs the initial preparation of the source data, including cleaning, filtering, and standardization of the variables required for subsequent processing.

---

### 2. Geocoding

After the address data has been prepared, run the R-based geocoding engine:

```bash
Rscript src/geocoding/02_geocode_r_engine.R
```
Or
```R
source("src/geocoding/02_geocode_r_engine.R")
```

This stage processes the standardized addresses and generates geographic coordinates for the records.

The resulting geospatial dataset is stored as a GeoPackage:

```text
data/processed/censo_escolar_geocodificado.gpkg
```

---

### 3. Spatial analysis and visualization

Open the Jupyter notebook:

```text
notebooks/03_analise_censo.ipynb
```

Select the Python environment created by `uv` as the notebook kernel and execute the analysis.

This stage includes:

- Loading the georeferenced data;
- Assigning H3 spatial indexes;
- Aggregating observations spatially;
- Analyzing the resulting spatial distribution;
- Generating cartographic visualizations;
- Exporting the interactive map.

Visualization utilities are implemented in:

```text
src/visualization/
```

The final interactive map is exported to:

```text
data/processed/map_censo_interactive.html
```

---

## Project structure

```text
optgis-geodata-pipeline/
│
├── data/
│   ├── raw/
│   │   ├── dicionário_dados_educação_básica.xlsx
│   │   └── microdados_ed_basica_2024.csv
│   │
│   └── processed/
│       ├── censo_escolar_2024_RJ_Endereços&Matrículas.csv
│       ├── censo_escolar_geocodificado.gpkg
│       └── map_censo_interactive.html
│
├── notebooks/
│   └── 03_analise_censo.ipynb
│
├── src/
│   ├── etl/
│   │   ├── __init__.py
│   │   └── 01_etl_censo_escolar.py
│   │
│   ├── geocoding/
│   │   └── 02_geocode_r_engine.R
│   │
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── hexbin_maps.py
│   │
│   ├── __init__.py
│   └── install_r_dependencies.R
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```
Note: Raw datasets and large processed files (.csv, .gpkg) are ignored in version control via .gitignore to keep the repository lightweight. They are generated locally when running the pipeline.
