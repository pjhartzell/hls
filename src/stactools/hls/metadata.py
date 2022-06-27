import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import rasterio
import shapely.geometry
from dateutil.parser import parse
from pystac.utils import datetime_to_str
from shapely.geometry import box, mapping, shape
from stactools.core.io import ReadHrefModifier
from stactools.core.projection import reproject_geom

from stactools.hls import constants
from stactools.hls.utils import modify_href


@dataclass
class Metadata:
    id: str
    product: str
    version: str
    acquisition_datetime: datetime
    start_end_datetime: Optional[Dict[str, datetime]]
    platform: str
    instrument: List[str]
    processing_datetime: str
    cloud_cover: Optional[int]
    sun_azimuth: float
    azimuth: float
    tile_id: str
    shape: List[int]
    transform: List[float]
    epsg: int
    geometry: Dict[str, Any]

    @classmethod
    def from_cog(
        cls,
        cog_href: str,
        read_href_modifier: Optional[ReadHrefModifier] = None,
        geometry_tolerance: Optional[float] = None,
    ) -> "Metadata":
        read_h5_href = modify_href(cog_href, read_href_modifier)
        with rasterio.open(read_h5_href) as dataset:
            transform = dataset.transform
            shape = dataset.shape
            epsg = dataset.crs.to_epsg()
            tags = dataset.tags()
            bbox = list(dataset.bounds)

        geometry = reproject_geom(f"EPSG:{epsg}", "EPSG:4326", mapping(box(*bbox)))

        cloud_cover = int(tags["cloud_coverage"])
        sun_azimuth = float(tags["MEAN_SUN_AZIMUTH_ANGLE"])
        azimuth = float(tags["MEAN_VIEW_AZIMUTH_ANGLE"])

        processing_datetime = parse(tags["HLS_PROCESSING_TIME"])
        sensing_time = [parse(dt) for dt in tags["SENSING_TIME"].split(";")]
        acquisition_datetime = min(sensing_time)
        start_end_datetime = None
        if len(sensing_time) > 1:
            start_end_datetime = {
                "start_datetime": datetime_to_str(min(sensing_time)),
                "end_datetime": datetime_to_str(max(sensing_time)),
            }

        fileparts = os.path.splitext(os.path.basename(cog_href))[0].split(".")
        id = ".".join(fileparts[:-1])
        version = ".".join(fileparts[4:6])
        product = fileparts[1]
        tile_id = fileparts[2]

        instrument = constants.INSTRUMENT[product]

        if product == "S30":
            platform = "sentinel-2a"
            if tags["DATASTRIP_ID"][2] == "B":
                platform = "sentinel-2b"
        else:
            # https://lpdaac.usgs.gov/news/hls-to-include-landsat-9-observations/
            platforms = set()
            for product_id in tags["LANDSAT_PRODUCT_ID"].split(";"):
                platforms.add(f"landsat-{product_id.strip()[3]}")
            platform = ", ".join(platforms)

        return Metadata(
            id=id,
            product=product,
            version=version,
            acquisition_datetime=acquisition_datetime,
            start_end_datetime=start_end_datetime,
            platform=platform,
            instrument=instrument,
            processing_datetime=processing_datetime,
            cloud_cover=cloud_cover,
            sun_azimuth=sun_azimuth,
            azimuth=azimuth,
            tile_id=tile_id,
            shape=list(shape),
            transform=list(transform),
            epsg=epsg,
            geometry=geometry,
        )
