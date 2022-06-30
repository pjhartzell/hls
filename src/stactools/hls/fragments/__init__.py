import json
from typing import Any, Dict, Tuple

import pkg_resources
from pystac import Extent, Link, MediaType, Provider
from pystac.utils import make_absolute_href

from stactools.hls.constants import BANDS
from stactools.hls.utils import band_name_from_href, product_from_href


class STACFragments:
    """Class for accessing collection and asset data."""

    def __init__(self) -> None:
        self.assets = self._load("assets.json")
        for key in self.assets.keys():
            self.assets[key]["type"] = MediaType.COG

    def asset(self, href: str) -> Tuple[str, Dict[str, Any]]:
        """Returns an Asset dictionary for a given COG HREF.

        Args:
            href (str): HREF to an asset COG file

        Returns:
            Dict[str, Any]: Asset dictionary
        """
        band_name = band_name_from_href(href)
        if band_name in BANDS["common"]:
            asset_key = BANDS["common"][band_name]
            asset = self.assets[asset_key]
        else:
            product = product_from_href(href)
            asset_key = BANDS[product][band_name]
            asset = self.assets[asset_key]
            asset["eo:bands"][0]["name"] = band_name
        asset["href"] = make_absolute_href(href)
        return (asset_key, asset)

    def collection_dict(self) -> Dict[str, Any]:
        """Returns a dictionary of Collection fields.

        Returns:
            Dict[str, Any]: Dictionary of Collection fields
        """
        collection: Dict[str, Any] = self._load("collection.json")
        collection["extent"] = Extent.from_dict(collection["extent"])
        collection["providers"] = [
            Provider.from_dict(provider) for provider in collection["providers"]
        ]
        collection["links"] = [Link.from_dict(link) for link in collection["links"]]
        return collection

    def _load(self, file_name: str) -> Any:
        try:
            with pkg_resources.resource_stream(
                "stactools.hls.fragments", f"./{file_name}"
            ) as stream:
                return json.load(stream)
        except FileNotFoundError as e:
            raise e
