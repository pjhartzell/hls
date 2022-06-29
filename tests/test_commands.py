import os.path
from tempfile import TemporaryDirectory
from typing import Callable, List

import pystac
from click import Command, Group
from stactools.testing.cli_test import CliTestCase

from stactools.hls.commands import create_hls_command
from stactools.hls.utils import id_from_href


class CommandsTest(CliTestCase):
    def create_subcommand_functions(self) -> List[Callable[[Group], Command]]:
        return [create_hls_command]

    def test_create_item(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            infile = "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/l30/HLS.L30.T19LDD.2022165T144027.v2.0.B01.tif"  # noqa
            result = self.run_command(f"hls create-item {infile} {tmp_dir}")
            assert result.exit_code == 0, "\n{}".format(result.output)

            item_id = id_from_href(infile)
            item_path = os.path.join(tmp_dir, f"{item_id}.json")
            item = pystac.read_file(item_path)
            assert item.id == "HLS.L30.T19LDD.2022165T144027.v2.0"
            item.validate()
