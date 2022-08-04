from typing import Any, Dict

FOOTPRINT_DENSIFICATION_FACTOR = 10
FOOTPRINT_SIMPLIFICATION_TOLERANCE = 0.0006  # degrees; approximately 60m

CLASSIFICATION_EXTENSION_HREF = (
    "https://stac-extensions.github.io/classification/v1.1.0/schema.json"
)
MGRS_EXTENSION_HREF = "https://stac-extensions.github.io/mgrs/v1.0.0/schema.json"

INSTRUMENT = {"L30": ["oli", "tiirs"], "S30": ["msi"]}
PLATFORMS = ["landsat-8", "landsat-9", "sentinel-2a", "sentinel-2b"]

BANDS: Dict[str, Any] = {
    "L30": {
        "B01": {"common_name": "coastal_aerosol", "gsd": 30},
        "B02": {"common_name": "blue", "gsd": 30},
        "B03": {"common_name": "green", "gsd": 30},
        "B04": {"common_name": "red", "gsd": 30},
        "B05": {"common_name": "nir_narrow", "gsd": 30},
        "B06": {"common_name": "swir_1", "gsd": 30},
        "B07": {"common_name": "swir_2", "gsd": 30},
        "B09": {"common_name": "cirrus", "gsd": 30},
        "B10": {"common_name": "thermal_infrared_1", "gsd": 100},
        "B11": {"common_name": "thermal_infrared_2", "gsd": 100},
    },
    "S30": {
        "B01": {"common_name": "coastal_aerosol", "gsd": 60},
        "B02": {"common_name": "blue", "gsd": 10},
        "B03": {"common_name": "green", "gsd": 10},
        "B04": {"common_name": "red", "gsd": 10},
        "B05": {"common_name": "red_edge_1", "gsd": 20},
        "B06": {"common_name": "red_edge_2", "gsd": 20},
        "B07": {"common_name": "red_edge_3", "gsd": 20},
        "B08": {"common_name": "nir_broad", "gsd": 10},
        "B8A": {"common_name": "nir_narrow", "gsd": 20},
        "B09": {"common_name": "water_vapor", "gsd": 60},
        "B10": {"common_name": "cirrus", "gsd": 60},
        "B11": {"common_name": "swir_1", "gsd": 20},
        "B12": {"common_name": "swir_2", "gsd": 20},
    },
    "common": {
        "Fmask": "fmask",
        "SAA": "saa",
        "SZA": "sza",
        "VAA": "vaa",
        "VZA": "vza",
    },
}

SCIENTIFIC: Dict[str, Any] = {
    "L30": {
        "doi": "10.5067/HLS/HLSL30.002",
        "cite-as": {
            "rel": "cite-as",
            "target": "https://doi.org/10.5067/HLS/HLSL30.002",
            "media_type": "text/html",
            "title": "LP DAAC - HLSL30 v002",
        },
    },
    "S30": {
        "doi": "10.5067/HLS/HLSS30.002",
        "cite-as": {
            "rel": "cite-as",
            "target": "https://doi.org/10.5067/HLS/HLSS30.002",
            "media_type": "text/html",
            "title": "LP DAAC - HLSS30 v002",
        },
    },
}
