from stactools.hls import stac


def test_create_item() -> None:
    # Write tests for each for the creation of STAC Items
    # Create the STAC Item...
    item = stac.create_item("/path/to/asset.tif")

    # Check that it has some required attributes
    assert item.id == "my-item-id"
    # self.assertEqual(item.other_attr...

    # Validate
    item.validate()
