import geopandas as gpd
import h3
from shapely.geometry import Polygon

def plot_hexbin_map(gdf: gpd.GeoDataFrame, hex_resolution: int = 8, weight_col: str = None):
    """
    Generates an interactive map grouping points into H3 system hexagons.
    """

    # Removes null values and empty geometries
    gdf_clean = gdf[gdf.geometry.notnull() & (~gdf.geometry.is_empty) & (gdf.is_valid)].copy()
    
    if gdf_clean.crs != "EPSG:4326":
        gdf_clean = gdf_clean.to_crs("EPSG:4326")


    # Extracts coordinates
    gdf_clean["lon"] = gdf_clean.geometry.x
    gdf_clean["lat"] = gdf_clean.geometry.y

    # Creates the H3 cell for each point
    gdf_clean["h3_index"] = gdf_clean.apply(
        lambda row: h3.latlng_to_cell(row["lat"], row["lon"], hex_resolution), axis=1
    ) 


    # Aggregation
    if weight_col:
        agg = gdf_clean.groupby("h3_index")[weight_col].sum().reset_index(name="weight")
    else:
        agg = gdf_clean.groupby("h3_index").size().reset_index(name="weight")


    # Converts H3 indices back to spatial polygons
    polygons = [
        Polygon([(lng, lat) for lat, lng in h3.cell_to_boundary(row["h3_index"])]) 
        for _, row in agg.iterrows()
    ]
    hex_gdf = gpd.GeoDataFrame(agg, geometry=polygons, crs="EPSG:4326")


    # Renders the Folium map
    return hex_gdf.explore(
        column="weight",
        tiles="CartoDB positron",
        cmap="viridis",
        scheme="HeadTailBreaks",
        legend=True,
        tooltip=["weight"]
    )