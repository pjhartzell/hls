import json
from typing import Any, Dict, Optional

import pkg_resources
from pystac import Extent, Link, MediaType, Provider


class STACFragments:
    """Class for accessing collection and asset data."""

    def __init__(self, product: str) -> None:
        self.product = product
        self.assets = self._load("assets.json")

    def assets_dict(self) -> Dict[str, Any]:
        """Returns a dictionary of Asset dictionaries (less the 'href' field)
        for the VIIRS product used to create the class instance.

        Returns:
            Dict[str, Any]: Dictionary of Asset dictionaries
        """
        assets: Dict[str, Any] = self.assets
        for key in assets.keys():
            assets[key]["type"] = MediaType.COG
        return assets

    def asset_dict(self, asset_name: str) -> Dict[str, Any]:
        """Returns a dictionary for a STAC Asset (less the 'href' field) for the
        given product asset name.

        Args:
            asset (str): Asset name

        Returns:
            Dict[str, Any]: Asset dictionary
        """
        asset: Dict[str, Any] = self.assets[asset_name]
        asset["type"] = MediaType.COG
        return asset

    def collection_dict(self) -> Dict[str, Any]:
        """Returns a dictionary of Collection fields (not exhaustive) for the
        VIIRS product used to create the class instance.

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
                "stactools.hls.fragments", f"fragments/{self.product}/{file_name}"
            ) as stream:
                return json.load(stream)
        except FileNotFoundError as e:
            raise e
