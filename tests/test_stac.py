import pytest
import shapely.geometry
from stactools.core.utils.antimeridian import Strategy

from stactools.hls import stac


def test_create_l30_item() -> None:
    href = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/l30/HLS.L30.T19LDD.2022165T144027.v2.0.B01.tif"  # noqa
    item = stac.create_item(href, check_existence=True)
    assert item.id == "HLS.L30.T19LDD.2022165T144027.v2.0"
    asset_dict = item.assets
    assert "fmask" in asset_dict  # common asset
    assert "thermal_infrared_1" in asset_dict  # eo asset specific to landsat
    item.validate()


def test_create_s30_item() -> None:
    href = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/s30/HLS.S30.T19LDD.2022166T144741.v2.0.B01.tif"  # noqa
    item = stac.create_item(href, check_existence=True)
    assert item.id == "HLS.S30.T19LDD.2022166T144741.v2.0"
    asset_dict = item.assets
    assert "fmask" in asset_dict  # common asset
    assert "red_edge_1" in asset_dict  # eo asset specific to sentinel
    item.validate()


def test_read_href_modifier() -> None:
    href = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/s30/HLS.S30.T19LDD.2022166T144741.v2.0.B01.tif"  # noqa

    did_it = False

    def read_href_modifier(href: str) -> str:
        nonlocal did_it
        did_it = True
        return href

    _ = stac.create_item(href, read_href_modifier=read_href_modifier)
    assert did_it


def test_antimeridian_normalize() -> None:
    href = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/s30/HLS.S30.T60VXR.2022178T233701.v2.0.B01.tif"  # noqa
    item = stac.create_item(href, antimeridian_strategy=Strategy.NORMALIZE)
    bounds = shapely.geometry.shape(item.geometry).bounds
    assert bounds[0] == pytest.approx(-181.02364614436414)
    assert bounds[2] == pytest.approx(-178.71375591092647)
    item.validate()


def test_antimeridian_split() -> None:
    href = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/s30/HLS.S30.T60VXR.2022178T233701.v2.0.B01.tif"  # noqa
    item = stac.create_item(href, antimeridian_strategy=Strategy.SPLIT)
    item_dict = item.to_dict()
    assert len(item_dict["geometry"]["coordinates"]) == 2
    item.validate()
