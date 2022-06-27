import os
from typing import Any, Dict, List, Optional

from pystac.extensions.eo import EOExtension
from pystac.extensions.raster import RasterExtension
from stactools.core.io import ReadHrefModifier
from stactools.core.utils import href_exists

from stactools.hls import constants


class UnsupportedProduct(Exception):
    """Product is not supported by this stactools package"""


def modify_href(
    href: str, read_href_modifier: Optional[ReadHrefModifier] = None
) -> str:
    """Generate a modified href, e.g., add a token to a url.

    Args:
        href (str): The HREF to be modified
        read_href_modifier (ReadHrefModifier): function that modifies an HREF

    Returns:
        str: Modified HREF
    """
    if read_href_modifier:
        read_href = read_href_modifier(href)
        return read_href
    else:
        return href


def find_extensions(assets: Dict[str, Any]) -> List[str]:
    """Adds extensions to the Item extension list if they exist on the Item assets.

    NOTE: This package does not nest the classification extension inside
    'raster:bands', so we do not check for its existence there.

    Args:
        item (Item): The Item being modified

    Returns:
        List[str]: List of stac extension URIs
    """
    extensions = set()
    for asset in assets.values():
        if "classification:classes" in asset or "classification:bitfields" in asset:
            extensions.add(constants.CLASSIFICATION_EXTENSION_HREF)
        if "eo:bands" in asset:
            extensions.add(EOExtension.get_schema_uri())
        if "raster:bands" in asset:
            extensions.add(RasterExtension.get_schema_uri())

    return list(extensions)


def create_cog_hrefs(
    href: str,
    product: str,
    check_existence: bool,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> List[str]:
    base_href, filename = os.path.split(href)
    base_filename = ".".join(filename.split(".")[:-2])

    cog_hrefs = []
    for asset_key in constants.ASSET_KEYS[product]:
        cog_hrefs.append(f"{base_href}/{base_filename}.{asset_key}.tif")

    if check_existence:
        for cog_href in cog_hrefs:
            read_href = modify_href(cog_href, read_href_modifier=read_href_modifier)
            if not href_exists(read_href):
                raise ValueError(f"File not found: {cog_href}")

    return cog_hrefs
