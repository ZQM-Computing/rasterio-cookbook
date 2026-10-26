# rasterio Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **rasterio cookbook** for raster reads, windows, reprojection, and COG pairing in Python. Patterns are drawn from the ZQM fleet's Python geo environments, where rasterio backs the raster workflows behind the COG and TiTiler passes. It is intended for Python geospatial developers who read and write rasters programmatically. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public — first executable patterns implemented. Examples are synthetic and self-contained; CI smoke-tests their outputs, but this does not establish production readiness.

**What this repository is:** rasterio patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Python geospatial developers who read and write rasters programmatically.

## Prerequisites

- rasterio in the fleet Python geo environment
- Python 3.11+
- A GeoTIFF or COG to work with

## Patterns

| # | Example | What it will demonstrate |
|---|---------|--------------------------|
| 01 | [`01-read-write`](examples/01-read-write/run.py) | Create a GeoTIFF, inspect dimensions/CRS/bounds, copy pixels, and verify output |
| 02 | [`02-windowed-reads`](examples/02-windowed-reads/run.py) | Iterate through raster windows and validate an incremental pixel sum |
| 03 | `03-reproject` | Planned: reprojection and warping between CRSs |
| 04 | `04-cog-pairing` | Planned: pair Rasterio output with COG validation and TiTiler serving |

## Repository layout

```text
rasterio-cookbook/
├── examples/          # pattern passes, landing in follow-up work
├── README.md
└── LICENSE
```

## Roadmap

- First pattern pass: the first two table rows
- Second pass: the remaining rows, from fleet-verified setups

## Contributing

Contributions should include reproducible examples and tests that validate output data, CRS, dimensions, and failure behavior. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [cog-cookbook](https://github.com/ZQM-Computing/cog-cookbook) — Cloud Optimized GeoTIFF creation, validation, TiTiler serving
- [gdal-cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR conversion, reprojection, and raster/vector utilities
- [titiler-cookbook](https://github.com/ZQM-Computing/titiler-cookbook) — Dynamic map tiles, STAC endpoints, cloud-native raster serving
