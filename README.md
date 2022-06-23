# stactools-hls

[![PyPI](https://img.shields.io/pypi/v/stactools-hls)](https://pypi.org/project/stactools-hls/)

- Name: hls
- Package: `stactools.hls`
- PyPI: https://pypi.org/project/stactools-hls/
- Owner: @pjhartzell
- Dataset homepage: https://www.earthdata.nasa.gov/esds/harmonized-landsat-sentinel-2
- STAC extensions used:
  - [classification](https://github.com/stac-extensions/classification/)
  - [eo](https://github.com/stac-extensions/eo)
  - [item-assets](https://github.com/stac-extensions/item-assets)
  - [proj](https://github.com/stac-extensions/projection)
  - [raster](https://github.com/stac-extensions/raster)
  - [scientific](https://github.com/stac-extensions/scientific)
- Extra fields:
  - `hls:tile-id`: Tile identifier using the Military Grid Reference System (MGRS)

Use this repository to create STAC Items and Collections for [HLS data](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/).

## STAC Examples

None yet.

## Installation
```shell
pip install stactools-hls
```

## Command-line Usage

Forthcoming.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
$ pip install -e .
$ pip install -r requirements-dev.txt
$ pre-commit install
```

To check all files:

```shell
$ pre-commit run --all-files
```

To run the tests:

```shell
$ pytest -vv
```
