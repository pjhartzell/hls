from typing import Any, Dict

from stactools.testing.test_data import TestData

L30 = [
    "HLS.L30.T19LDD.2022165T144027.v2.0.B01.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B02.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B03.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B04.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B05.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B06.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B07.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B09.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B10.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.B11.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.Fmask.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.SAA.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.SZA.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.VAA.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.VZA.tif",
    "HLS.L30.T19LDD.2022165T144027.v2.0.cmr.xml",
]

S30 = [
    "HLS.S30.T19LCD.2022034T145719.v2.0.B01.tif",
    "HLS.S30.T19LCD.2022034T145719.v2.0.cmr.xml",
    "HLS.S30.T19LDD.2022166T144741.v2.0.B01.tif",
    "HLS.S30.T19LDD.2022166T144741.v2.0.cmr.xml",
    "HLS.S30.T60VXR.2022178T233701.v2.0.B01.tif",
    "HLS.S30.T60VXR.2022178T233701.v2.0.cmr.xml",
]


def create_external_data_dict() -> Dict[str, Dict[str, Any]]:
    external_data: Dict[str, Dict[str, Any]] = {}
    for filename in L30:
        external_data[filename] = {
            "url": "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/l30"
            f"/{filename}"
        }
    for filename in S30:
        external_data[filename] = {
            "url": "https://ai4epublictestdata.blob.core.windows.net/stactools/hls/s30"
            f"/{filename}"
        }
    return external_data


external_data = create_external_data_dict()

test_data = TestData(__file__, external_data=external_data)
