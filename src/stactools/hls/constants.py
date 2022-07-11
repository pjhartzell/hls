from typing import Any, Dict

CLASSIFICATION_EXTENSION_HREF = (
    "https://stac-extensions.github.io/classification/v1.0.0/schema.json"
)
MGRS_EXTENSION_HREF = "https://stac-extensions.github.io/mgrs/v1.0.0/schema.json"

INSTRUMENT = {"L30": ["oli", "tiirs"], "S30": ["msi"]}
PLATFORMS = ["landsat-8", "landsat-9", "sentinel-2a", "sentinel-2b"]

BANDS = {
    "L30": {
        "B01": "coastal_aerosol",
        "B02": "blue",
        "B03": "green",
        "B04": "red",
        "B05": "nir_narrow",
        "B06": "swir_1",
        "B07": "swir_2",
        "B09": "cirrus",
        "B10": "thermal_infrared_1",
        "B11": "thermal_infrared_2",
    },
    "S30": {
        "B01": "coastal_aerosol",
        "B02": "blue",
        "B03": "green",
        "B04": "red",
        "B05": "red_edge_1",
        "B06": "red_edge_2",
        "B07": "red_edge_3",
        "B08": "nir_broad",
        "B8A": "nir_narrow",
        "B09": "swir_1",
        "B10": "swir_2",
        "B11": "water_vapor",
        "B12": "cirrus",
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
