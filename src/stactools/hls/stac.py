from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pystac import Asset, Collection, Item, Link, Summaries
from pystac.extensions.eo import EOExtension
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.view import ViewExtension
from shapely.geometry import MultiPolygon, mapping, shape
from stactools.core.io import ReadHrefModifier
from stactools.core.utils.antimeridian import Strategy, fix_item

from stactools.hls import utils
from stactools.hls.constants import (
    CLASSIFICATION_EXTENSION_HREF,
    INSTRUMENT,
    MGRS_EXTENSION_HREF,
    PLATFORMS,
    SCIENTIFIC,
)
from stactools.hls.fragments import STACFragments
from stactools.hls.metadata import hls_metadata


def create_item(
    cog_href: str,
    read_href_modifier: Optional[ReadHrefModifier] = None,
    check_existence: bool = False,
    antimeridian_strategy: Strategy = Strategy.SPLIT,
) -> Item:
    """Creates a STAC Item for an HLS granule.

    Args:
        cog_href (str): HREF to one of the EO COG files in the granule.
        read_href_modifier (ReadHrefModifier, optional): An optional
            function to modify the href (e.g. to add a token to a url)
        check_existence (bool, optional): Flag to check that COGs exist for all
                granule assets. Defaults to False.
        antimeridian_strategy (Strategy, optional):Choice of 'normalize' or
            'split' to either split the Item geometry on -180 longitude or
            normalize the Item geometry so all longitudes are either positive or
            negative. Default is 'split'.

    Returns:
        Item: An HLS STAC Item.
    """
    metadata = hls_metadata(cog_href, read_href_modifier)
    fragments = STACFragments()

    id = utils.id_from_href(cog_href)
    product = utils.product_from_href(cog_href)
    polygon = metadata.geometry

    item = Item(
        id=id,
        geometry=mapping(polygon),
        bbox=polygon.bounds,
        datetime=metadata.acquisition_datetime,
        properties={
            "sci:doi": SCIENTIFIC[product]["doi"],
            "hls:product": f"HLS{product}",
        },
    )

    cog_hrefs = utils.create_cog_hrefs(
        cog_href,
        product,
        check_existence,
        read_href_modifier,
    )
    for href in cog_hrefs:
        asset_key, asset_dict = fragments.asset(href)
        item.add_asset(asset_key, Asset.from_dict(asset_dict))

    if metadata.start_end_datetime:
        item.properties.update(**metadata.start_end_datetime)
    item.common_metadata.created = datetime.now(tz=timezone.utc)
    item.common_metadata.platform = metadata.platform
    item.common_metadata.instruments = INSTRUMENT[product]

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

    ScientificExtension.add_to(item)
    item.links.append(Link(**SCIENTIFIC[product]["cite-as"]))

    item.stac_extensions.append(CLASSIFICATION_EXTENSION_HREF)

    item.stac_extensions.sort()

    if isinstance(shape(item.geometry), MultiPolygon):
        item = utils.merge_multipolygon(item)
    fix_item(item, antimeridian_strategy)

    return item


def create_collection() -> Collection:
    """Returns an HLS Collection."""
    fragments = STACFragments()

    summaries: Dict[str, Any] = {
        "instruments": [val for values in INSTRUMENT.values() for val in values],
        "platform": PLATFORMS,
        "sci:doi": [value["doi"] for value in SCIENTIFIC.values()],
        "eo:bands": fragments.collection_eo_bands_summary(),
    }

    collection_fragments = fragments.collection_dict()
    collection = Collection(
        id=collection_fragments["id"],
        title=collection_fragments["title"],
        description=collection_fragments["description"],
        license=collection_fragments["license"],
        keywords=collection_fragments["keywords"],
        providers=collection_fragments["providers"],
        extent=collection_fragments["extent"],
        summaries=Summaries(summaries),
    )
    collection.add_links(collection_fragments["links"])

    item_assets_dict = fragments.assets
    item_assets = {k: AssetDefinition(v) for k, v in item_assets_dict.items()}
    item_assets_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets_ext.item_assets = item_assets

    RasterExtension.add_to(collection)

    EOExtension.add_to(collection)

    ScientificExtension.add_to(collection)
    collection.extra_fields["sci:publications"] = collection_fragments[
        "sci:publications"
    ]
    collection.add_links([Link(**value["cite-as"]) for value in SCIENTIFIC.values()])

    collection.stac_extensions.extend([CLASSIFICATION_EXTENSION_HREF])

    collection.stac_extensions = sorted(collection.stac_extensions)

    return collection
