import logging
import os
from typing import Optional

import click
from click import Command, Group
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
    @click.argument("INFILE")
    @click.argument("OUTDIR")
    @click.option(
        "-c",
        "--check-existence",
        is_flag=True,
        default=False,
        help="Check for COG existence",
    )
    @click.option(
        "-a",
        "--antimeridian_strategy",
        type=click.Choice(["normalize", "split"], case_sensitive=False),
        default="split",
        show_default=True,
        help="Geometry strategy for antimeridian scenes",
    )
    @click.option(
        "-t",
        "--tolerance",
        type=float,
        help="Maximum acceptable error in geometry polygon (unit=geographic degree)",
    )
    def create_item_command(
        infile: str,
        outdir: str,
        check_existence: bool,
        antimeridian_strategy: str,
        tolerance: Optional[float] = None,
    ) -> None:
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Item
        """
        strategy = Strategy[antimeridian_strategy.upper()]

        item = stac.create_item(
            infile,
            check_existence=check_existence,
            antimeridian_strategy=strategy,
            geometry_tolerance=tolerance,
        )
        item_path = os.path.join(outdir, f"{item.id}.json")
        item.set_self_href(item_path)
        item.make_asset_hrefs_relative()
        item.validate()
        item.save_object()

        return None

    return hls
