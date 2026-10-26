# Rasterio Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A practical **Rasterio cookbook** for Python raster workflows. The repository currently contains three executable, synthetic-data examples for GeoTIFF read/write and windowed reads. Reprojection and Cloud Optimized GeoTIFF (COG) integration remain planned. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public. The first two executable patterns and automated tests are implemented.

**Scope:** Rasterio examples and regression tests. This repository is part of the [ZQM Computing geospatial cookbook series](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Evidence boundary:** The examples use generated synthetic rasters. CI runs the repository's configured tests; passing those tests does not establish production readiness, COG conformance, performance at scale, or suitability for every dataset.

## Who this is for

Python geospatial developers who need reproducible examples for reading, writing, and processing raster data.

## Prerequisites

- Python 3.11 or newer
- Rasterio and its compatible GDAL runtime
- NumPy

For local testing, install the test dependencies:

```bash
python -m pip install -r requirements-test.txt
python -m pytest -q
```

The examples create their own synthetic input data; no external raster download is required.

## Implemented patterns

| # | Example | What it demonstrates |
|---|---|---|
| 01 | [examples/01-read-write/run.py](examples/01-read-write/run.py) | Create a deterministic GeoTIFF, inspect metadata, write a pixel copy, and verify CRS and pixel equality. |
| 02 | [examples/02-windowed-reads/run.py](examples/02-windowed-reads/run.py) | Create a tiled 512 × 512 GeoTIFF, read 128 × 128 windows, accumulate values, and compare the result with the expected total. |
| 03 | [examples/03-reprojection/run.py](examples/03-reprojection/run.py) | Reproject a synthetic EPSG:4326 raster to EPSG:3857 with an explicit destination grid and NoData preservation checks. |

Run an example from the repository root:

```bash
python examples/01-read-write/run.py
python examples/02-windowed-reads/run.py
python examples/03-reprojection/run.py
```

Each example writes outputs in its current working directory. To keep the repository checkout clean, run it from a temporary directory, for example:

```bash
mkdir -p /tmp/rasterio-cookbook-run
cd /tmp/rasterio-cookbook-run
python /path/to/rasterio-cookbook/examples/01-read-write/run.py
python /path/to/rasterio-cookbook/examples/02-windowed-reads/run.py
```

Replace `/path/to/rasterio-cookbook` with the absolute path to your checkout.

## Tests and continuous integration

- [tests/test_examples.py](tests/test_examples.py) checks Python syntax and executes all three examples in temporary directories.
- [requirements-test.txt](requirements-test.txt) declares the test dependencies.
- [.github/workflows/tests.yml](.github/workflows/tests.yml) runs the test suite on pull requests and pushes to the default branch.

The tests verify selected behavior for these three examples. They do not yet test reprojection, COG conformance, remote range requests, large-raster performance, or a broad Rasterio/GDAL version matrix.

## Roadmap

1. Add a COG creation/validation example that checks the produced layout and documents the distinction between metadata checks and full conformance.
2. Expand tests across supported Rasterio/GDAL environments and add failure-path coverage where it provides meaningful assurance.

## Contributing

Contributions should include reproducible examples and tests that validate output data, CRS, dimensions, and failure behavior. Document runtime assumptions and avoid describing an example as production-ready without corresponding evidence.

Report security issues to <zqmcomputing@gmail.com>; please do not open a public issue for them.

## Related cookbooks

- [COG Cookbook](https://github.com/ZQM-Computing/cog-cookbook) — Cloud Optimized GeoTIFF creation and validation.
- [GDAL Cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR conversion, reprojection, and raster/vector utilities.
- [TiTiler Cookbook](https://github.com/ZQM-Computing/titiler-cookbook) — Dynamic map tiles and cloud-native raster serving.
