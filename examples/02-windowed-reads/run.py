"""Example 02: process a tiled raster in its native storage blocks."""
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

OUTPUT_DIR = Path("output")
RASTER_PATH = OUTPUT_DIR / "windowed_demo.tif"


def main() -> None:
    """Create a tiled raster and sum native blocks incrementally."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pixels = np.arange(512 * 512, dtype=np.uint32).reshape(512, 512)
    profile = {
        "driver": "GTiff",
        "height": 512,
        "width": 512,
        "count": 1,
        "dtype": "uint32",
        "crs": "EPSG:3857",
        "transform": from_origin(0, 512, 1, 1),
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
        "compress": "deflate",
    }
    with rasterio.open(RASTER_PATH, "w", **profile) as dataset:
        dataset.write(pixels, 1)

    total = 0
    window_count = 0
    with rasterio.open(RASTER_PATH) as dataset:
        # block_windows() aligns iteration with the GeoTIFF's physical
        # storage layout and reduces logical read calls. GDAL's block cache
        # may already avoid repeated decompression for smaller windows, so
        # wall-clock effects depend on the driver, cache, and workload.
        for _, window in dataset.block_windows(1):
            tile = dataset.read(1, window=window)
            total += int(tile.sum(dtype=np.uint64))
            window_count += 1

    expected = int(pixels.sum(dtype=np.uint64))
    if total != expected:
        raise RuntimeError(f"Block sum mismatch: got {total}, expected {expected}")
    print(f"Raster: {RASTER_PATH}")
    print(f"Native block shape: {profile['blockysize']}x{profile['blockxsize']}")
    print(f"Windows processed: {window_count}")
    print(f"Pixel sum: {total}")


if __name__ == "__main__":
    main()
