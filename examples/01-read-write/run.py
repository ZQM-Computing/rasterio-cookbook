"""Example 01: create, inspect, and write a small GeoTIFF with Rasterio.

Run from any directory with:
    python /path/to/examples/01-read-write/run.py

The example writes outputs beneath ./output in the current working directory so
it can be run safely from a disposable directory during tests.
"""
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

OUTPUT_DIR = Path("output")
SOURCE_PATH = OUTPUT_DIR / "rasterio_source.tif"
OUTPUT_PATH = OUTPUT_DIR / "rasterio_copy.tif"


def main() -> None:
    """Create a deterministic raster, inspect its metadata, and write a copy."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pixels = np.arange(100, dtype=np.uint16).reshape(10, 10)
    transform = from_origin(-80.0, 30.0, 0.01, 0.01)
    profile = {
        "driver": "GTiff",
        "height": pixels.shape[0],
        "width": pixels.shape[1],
        "count": 1,
        "dtype": pixels.dtype,
        "crs": "EPSG:4326",
        "transform": transform,
        "compress": "deflate",
    }

    with rasterio.open(SOURCE_PATH, "w", **profile) as dataset:
        dataset.write(pixels, 1)

    with rasterio.open(SOURCE_PATH) as source:
        print(f"Source: {SOURCE_PATH}")
        print(f"Dimensions: {source.width} x {source.height}")
        print(f"Bands: {source.count}")
        print(f"CRS: {source.crs}")
        print(f"Bounds: {source.bounds}")
        output_profile = source.profile.copy()
        band = source.read(1)

    with rasterio.open(OUTPUT_PATH, "w", **output_profile) as destination:
        destination.write(band, 1)

    with rasterio.open(OUTPUT_PATH) as result:
        if result.crs != rasterio.crs.CRS.from_epsg(4326):
            raise RuntimeError("Output CRS changed unexpectedly")
        if not np.array_equal(result.read(1), pixels):
            raise RuntimeError("Output pixel values differ from the source")
    print(f"Verified copy: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
