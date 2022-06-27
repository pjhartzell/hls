import logging

import click
from click import Command, Group

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
    @click.argument("source")
    @click.argument("destination")
    def create_item_command(source: str, destination: str) -> None:
        """Creates a STAC Item

        Args:
            source (str): HREF of the Asset associated with the Item
            destination (str): An HREF for the STAC Item
        """
        item = stac.create_item(source)

        item.save_object(dest_href=destination)

        return None

    return hls
