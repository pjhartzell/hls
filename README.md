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
  - [mgrs](https://github.com/stac-extensions/mgrs)
  - [proj](https://github.com/stac-extensions/projection)
  - [raster](https://github.com/stac-extensions/raster)
  - [scientific](https://github.com/stac-extensions/scientific)
  - [view](https://github.com/stac-extensions/view)
- Extra fields:
  - `hls:product`: "HLSL30" (Landsat) or "HLSS30" (Sentinel) product

Use this repository to create STAC Items and Collections for [HLS](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/harmonized-landsat-sentinel-2-hls-overview/) data.

## STAC Examples

- [Collection](examples/collection.json)
- HLSL30 [Item](examples/HLS.L30.T19LDD.2022165T144027.v2.0/HLS.L30.T19LDD.2022165T144027.v2.0.json) (Landsat)
- HLSS30 [Item](examples/HLS.S30.T19LDD.2022166T144741.v2.0/HLS.S30.T19LDD.2022166T144741.v2.0.json)  (Sentinel)

## Installation
```shell
$ pip install stactools-hls
```

## Command-line Usage

To create a single STAC Item from a HLS COG file:

```shell
$ stac hls create-item <COG file path> <output directory>
```

Only a single COG file from the set comprising an HLS granule needs to be passed. However, the COG must be for one of the electro-optical (EO) bands.

To create a STAC Collection, enter COG file paths into a text file with one file path per line. Each file must be from a distinct HLS granule. Then pass the text file to the `create-collection` command:

```shell
$ stac hls create-collection <text file path> <output directory>
```

To create the files in the `examples` directory:
```shell
$ stac hls create-collection examples/file-list.txt examples
```

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
