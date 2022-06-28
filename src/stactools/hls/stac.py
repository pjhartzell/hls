import logging
import os
from datetime import datetime, timezone
from typing import Optional

import shapely.geometry
from pystac import Asset, Item
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from pystac.extensions.view import ViewExtension
from pystac.utils import make_absolute_href
from stactools.core.io import ReadHrefModifier
from stactools.core.utils.antimeridian import Strategy, fix_item

from stactools.hls.constants import CLASSIFICATION_EXTENSION_HREF, MGRS_EXTENSION_HREF
from stactools.hls.fragments import STACFragments
from stactools.hls.metadata import Metadata
from stactools.hls.utils import create_cog_hrefs

logger = logging.getLogger(__name__)


def create_item(
    cog_href: str,
    read_href_modifier: Optional[ReadHrefModifier] = None,
    check_existence: bool = False,
    antimeridian_strategy: Strategy = Strategy.SPLIT,
    geometry_tolerance: Optional[float] = None,
) -> Item:

    metadata = Metadata.from_cog(
        cog_href,
        read_href_modifier,
        geometry_tolerance,
    )
    fragments = STACFragments(metadata.product)

    item = Item(
        id=metadata.id,
        geometry=metadata.geometry,
        bbox=list(shapely.geometry.shape(metadata.geometry).bounds),
        datetime=metadata.acquisition_datetime,
        properties={},
    )

    if metadata.start_end_datetime:
        item.properties.update(**metadata.start_end_datetime)
    item.common_metadata.created = datetime.now(tz=timezone.utc)

    item.common_metadata.platform = metadata.platform
    item.common_metadata.instruments = metadata.instrument

    cog_hrefs = create_cog_hrefs(
        cog_href,
        metadata.product,
        check_existence,
        read_href_modifier,
    )
    for href in cog_hrefs:
        asset_key = os.path.basename(href).split(".")[-2]
        asset_dict = fragments.asset_dict(asset_key)
        asset_dict["href"] = make_absolute_href(href)
        item.add_asset(asset_key, Asset.from_dict(asset_dict))

    eo = EOExtension.ext(item, add_if_missing=True)
    eo.cloud_cover = metadata.cloud_cover

    view = ViewExtension.ext(item, add_if_missing=True)
    view.azimuth = metadata.azimuth
    view.sun_azimuth = metadata.sun_azimuth

    proj = ProjectionExtension.ext(item, add_if_missing=True)
    proj.epsg = metadata.epsg
    proj.shape = metadata.shape
    proj.transform = metadata.transform

    item.stac_extensions.append(MGRS_EXTENSION_HREF)
    item.properties.update(**metadata.mgrs)

    RasterExtension.add_to(item)
    item.stac_extensions.append(CLASSIFICATION_EXTENSION_HREF)

    fix_item(item, antimeridian_strategy)

    return item


# href = "/Users/pjh/dev/hls/tests/data-files/external/HLS.S30.T19LDD.2022166T144741.v2.0.B09.tif"
href = "/Users/pjh/dev/hls/tests/data-files/external/HLS.L30.T19LDD.2022165T144027.v2.0.B09.tif"
create_item(href)
