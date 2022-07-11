import logging
import os

import click
from click import Command, Group
from pystac import CatalogType
from stactools.core.utils.antimeridian import Strategy

from stactools.hls import stac

logger = logging.getLogger(__name__)


def create_hls_command(cli: Group) -> Command:
    """Creates the stactools-hls command line utility."""

    @cli.group(
        "hls",
        short_help=("Commands for working with stactools-hls"),
    )
    def hls() -> None:
        pass

    @hls.command("create-item", short_help="Create a STAC item")
    @click.argument("SOURCE")
    @click.argument("OUTDIR")
    @click.option(
        "-c",
        "--check-existence",
        is_flag=True,
        default=False,
        help="Check that all granule asset COGs exist",
    )
    @click.option(
        "-a",
        "--antimeridian_strategy",
        type=click.Choice(["normalize", "split"], case_sensitive=False),
        default="split",
        show_default=True,
        help="Geometry strategy for antimeridian scenes",
    )
    def create_item_command(
        source: str,
        outdir: str,
        check_existence: bool,
        antimeridian_strategy: str,
    ) -> None:
        """Creates a STAC Item for an HLS L30 or S30 granule.

        Args:
            source (str): HREF to a single COG asset of an HLS granule.
            outdir (str): Directory that will contain the STAC Item.
            check_existence (bool): Flag to check that COGs exist for all
                granule assets. Default is False.
            antimeridian_strategy (str, optional): Choice of 'normalize' or
                'split' to either split the Item geometry on -180 longitude or
                normalize the Item geometry so all longitudes are either
                positive or negative. Default is 'split'.
        """
        strategy = Strategy[antimeridian_strategy.upper()]

        item = stac.create_item(
            source,
            check_existence=check_existence,
            antimeridian_strategy=strategy,
        )
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object(include_self_link=False)

        return None

    @hls.command("create-collection", short_help="Create a STAC Collection")
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option(
        "-a",
        "--antimeridian-strategy",
        type=click.Choice(["normalize", "split"], case_sensitive=False),
        default="split",
        show_default=True,
        help="Geometry strategy for antimeridian scenes",
    )
    def create_collection_command(
        infile: str, outdir: str, antimeridian_strategy: str
    ) -> None:
        """Creates a STAC Collection with Items created from granule asset HREFs
        listed in INFILE. Only one asset HREF for each granule should be listed.

        \b
        Args:
            infile (str): Text file containing one HREF per line. The HREFs
                should point to a single HLS or L30 granule COG file. Do not
                list multiple COG file HREFs for the same granule.
            outdir (str): Directory that will contain the collection.
            antimeridian_strategy (str, optional): Choice of 'normalize' or
                'split' to either split the Item geometry on -180 longitude or
                normalize the Item geometry so all longitudes are either
                positive or negative. Default is 'split'.
        """
        strategy = Strategy[antimeridian_strategy.upper()]

        with open(infile) as f:
            hrefs = [os.path.abspath(line.strip()) for line in f.readlines()]

        collection = stac.create_collection()

        for href in hrefs:
            item = stac.create_item(href, antimeridian_strategy=strategy)
            collection.add_item(item)

        collection.set_self_href(os.path.join(outdir, "collection.json"))
        collection.catalog_type = CatalogType.SELF_CONTAINED
        collection.validate_all()
        collection.save()

        return None

    return hls
