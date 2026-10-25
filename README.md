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

**Status:** Active, public — seeding. Pattern passes land in follow-up work from fleet-verified setups; the tables below list what is planned, not what is already written.

**What this repository is:** rasterio patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Python geospatial developers who read and write rasters programmatically.

## Prerequisites

- rasterio in the fleet Python geo environment
- Python 3.11+
- A GeoTIFF or COG to work with

## Patterns (planned)

| # | Example | What it will demonstrate |
|---|---------|--------------------------|
| 01 | `01-read-write` | Reading raster metadata, bands, and profiles; writing outputs |
| 02 | `02-windowed-reads` | Windowed reads for large rasters without loading them whole |
| 03 | `03-reproject` | Reprojecting rasters and warping between CRSs |
| 04 | `04-cog-pairing` | Pairing rasterio writes with COG validation and TiTiler serving |

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

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [cog-cookbook](https://github.com/ZQM-Computing/cog-cookbook) — Cloud Optimized GeoTIFF creation, validation, TiTiler serving
- [gdal-cookbook](https://github.com/ZQM-Computing/gdal-cookbook) — GDAL/OGR conversion, reprojection, and raster/vector utilities
- [titiler-cookbook](https://github.com/ZQM-Computing/titiler-cookbook) — Dynamic map tiles, STAC endpoints, cloud-native raster serving
