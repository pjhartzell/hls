import pytest
import shapely.geometry
from stactools.core.utils.antimeridian import Strategy

from stactools.hls import stac
from tests import L30, test_data


def test_create_l30_item() -> None:
    for filename in L30:
        test_data.get_external_data(filename)
    href = test_data.get_external_data("HLS.L30.T19LDD.2022165T144027.v2.0.B01.tif")
    item = stac.create_item(href, check_existence=True)
    assert item.id == "HLS.L30.T19LDD.2022165T144027.v2.0"
    asset_dict = item.assets
    assert "fmask" in asset_dict  # common asset
    assert "thermal_infrared_1" in asset_dict  # eo asset specific to landsat
    assert asset_dict["blue"].to_dict()["gsd"] == 30
    item.validate()


def test_create_s30_item() -> None:
    href = test_data.get_external_data("HLS.S30.T19LDD.2022166T144741.v2.0.B01.tif")
    test_data.get_external_data("HLS.S30.T19LDD.2022166T144741.v2.0.cmr.xml")
    item = stac.create_item(href, check_existence=False)
    assert item.id == "HLS.S30.T19LDD.2022166T144741.v2.0"
    asset_dict = item.assets
    assert "fmask" in asset_dict  # common asset
    assert "red_edge_1" in asset_dict  # eo asset specific to sentinel
    assert asset_dict["blue"].to_dict()["gsd"] == 10
    item.validate()


def test_parse_old_wkt() -> None:
    href = test_data.get_external_data("HLS.S30.T19LCD.2022034T145719.v2.0.B01.tif")
    test_data.get_external_data("HLS.S30.T19LCD.2022034T145719.v2.0.cmr.xml")
    item = stac.create_item(href)
    assert item.properties["proj:epsg"] == 32619
    item.validate()


def test_read_href_modifier() -> None:
    href = test_data.get_external_data("HLS.S30.T19LDD.2022166T144741.v2.0.B01.tif")
    test_data.get_external_data("HLS.S30.T19LDD.2022166T144741.v2.0.cmr.xml")

    did_it = False

    def read_href_modifier(href: str) -> str:
        nonlocal did_it
        did_it = True
        return href

    _ = stac.create_item(href, read_href_modifier=read_href_modifier)
    assert did_it


def test_antimeridian_normalize() -> None:
    href = test_data.get_external_data("HLS.S30.T60VXR.2022178T233701.v2.0.B01.tif")
    test_data.get_external_data("HLS.S30.T60VXR.2022178T233701.v2.0.cmr.xml")

    item = stac.create_item(href, antimeridian_strategy=Strategy.NORMALIZE)
    bounds = shapely.geometry.shape(item.geometry).bounds
    assert bounds[0] == pytest.approx(-181.02364614436414)
    assert bounds[2] == pytest.approx(-178.71375591092647)
    item.validate()


def test_antimeridian_split() -> None:
    href = test_data.get_external_data("HLS.S30.T60VXR.2022178T233701.v2.0.B01.tif")
    test_data.get_external_data("HLS.S30.T60VXR.2022178T233701.v2.0.cmr.xml")
    item = stac.create_item(href, antimeridian_strategy=Strategy.SPLIT)
    item_dict = item.to_dict()
    assert len(item_dict["geometry"]["coordinates"]) == 2
    item.validate()


def test_create_collection() -> None:
    collection = stac.create_collection()
    assert collection.id == "hls"
    collection_dict = collection.to_dict()
    assert "eo:bands" in collection_dict["summaries"]
    assert len(collection_dict["item_assets"]) == 20
