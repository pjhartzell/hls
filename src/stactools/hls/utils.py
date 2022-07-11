import os
from typing import List, Optional

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


def create_cog_hrefs(
    href: str,
    product: str,
    check_existence: bool,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> List[str]:
    """Creates a list of all COG hrefs for a granule from a single COG href and
    optionally checks that all created hrefs exist.

    Args:
        href (str): A COG href belonging to an HLS granule.
        product (str): The HLS product, either 'L30' or 'S30'.
        check_existence (bool): If True, checks that each created COG href
            exists.
        read_href_modifier (Optional[ReadHrefModifier], optional): An optional
            function to modify the href (e.g. to add a token to a url) for use
            in checking href existence.

    Returns:
        List[str]: List of granule COG hrefs.
    """
    base_href, filename = os.path.split(href)
    base_filename = ".".join(filename.split(".")[:-2])

    cog_hrefs = []
    for band in constants.BANDS[product]:
        cog_hrefs.append(f"{base_href}/{base_filename}.{band}.tif")
    for common_band in constants.BANDS["common"]:
        cog_hrefs.append(f"{base_href}/{base_filename}.{common_band}.tif")

    if check_existence:
        for cog_href in cog_hrefs:
            read_href = modify_href(cog_href, read_href_modifier=read_href_modifier)
            if not href_exists(read_href):
                raise ValueError(f"File not found: {cog_href}")

    return cog_hrefs


def filename_parts(href: str) -> List[str]:
    """Splits the filename from an HLS COG file HREF into a list of its parts."""
    return os.path.splitext(os.path.basename(href))[0].split(".")


def id_from_href(href: str) -> str:
    """Extracts the HLS granule id from an HLS COG file HREF."""
    return ".".join(filename_parts(href)[:-1])


def product_from_href(href: str) -> str:
    """Extracts the HLS product (L30 or S30) from an HLS COG file HREF."""
    return filename_parts(href)[1]


def tile_id_from_href(href: str) -> str:
    """Extracts the HLS tile ID from an HLS COG file HREF."""
    return filename_parts(href)[2]


def version_from_href(href: str) -> str:
    """Extracts the HLS version from an HLS COG file HREF."""
    return ".".join(filename_parts(href)[4:6])


def band_name_from_href(href: str) -> str:
    """Extracts the band name from an HLS COG file HREF."""
    return filename_parts(href)[-1]
