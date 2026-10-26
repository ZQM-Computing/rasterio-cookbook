"""Example 03: reproject a synthetic raster with explicit grid and NoData checks."""

from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.warp import calculate_default_transform, reproject

OUTPUT_DIR = Path("output")
SOURCE_PATH = OUTPUT_DIR / "reprojection_source.tif"
DESTINATION_PATH = OUTPUT_DIR / "reprojected_3857.tif"
SOURCE_CRS = "EPSG:4326"
DESTINATION_CRS = "EPSG:3857"
NODATA = -9999.0


def main() -> None:
    """Create a small source raster, reproject it, and verify the output grid."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pixels = np.arange(400, dtype=np.float32).reshape(20, 20)
    pixels[0, 0] = NODATA
    source_transform = from_origin(-80.95, 29.05, 0.001, 0.001)
    source_profile = {
        "driver": "GTiff",
        "height": pixels.shape[0],
        "width": pixels.shape[1],
        "count": 1,
        "dtype": "float32",
        "crs": SOURCE_CRS,
        "transform": source_transform,
        "nodata": NODATA,
        "compress": "deflate",
    }

    with rasterio.open(SOURCE_PATH, "w", **source_profile) as source:
        source.write(pixels, 1)

    with rasterio.open(SOURCE_PATH) as source:
        destination_transform, width, height = calculate_default_transform(
            source.crs,
            DESTINATION_CRS,
            source.width,
            source.height,
            *source.bounds,
        )
        if width <= 0 or height <= 0:
            raise RuntimeError(f"Invalid destination dimensions: {width} x {height}")
        destination = np.full((height, width), NODATA, dtype=np.float32)
        reproject(
            source=rasterio.band(source, 1),
            destination=destination,
            src_transform=source.transform,
            src_crs=source.crs,
            src_nodata=source.nodata,
            dst_transform=destination_transform,
            dst_crs=DESTINATION_CRS,
            dst_nodata=NODATA,
            resampling=Resampling.nearest,
            init_dest_nodata=True,
        )

    destination_profile = {
        **source_profile,
        "height": height,
        "width": width,
        "crs": DESTINATION_CRS,
        "transform": destination_transform,
        "nodata": NODATA,
    }
    with rasterio.open(DESTINATION_PATH, "w", **destination_profile) as result:
        result.write(destination, 1)

    with rasterio.open(DESTINATION_PATH) as result:
        actual = result.read(1)
        if result.crs != rasterio.crs.CRS.from_epsg(3857):
            raise RuntimeError(f"Unexpected destination CRS: {result.crs}")
        if result.width != width or result.height != height:
            raise RuntimeError("Saved raster dimensions do not match the calculated destination grid")
        if not np.isfinite(result.transform.a) or not np.isfinite(result.transform.e):
            raise RuntimeError("Destination affine transform is not finite")
        valid = actual != NODATA
        if not valid.any():
            raise RuntimeError("Reprojection produced no valid pixels")
        if not np.isfinite(actual[valid]).all():
            raise RuntimeError("Reprojected valid pixels contain non-finite values")

    print(f"Source CRS: {SOURCE_CRS}")
    print(f"Destination CRS: {DESTINATION_CRS}")
    print(f"Destination dimensions: {width} x {height}")
    print(f"Valid pixels: {int(valid.sum())}")
    print(f"NoData pixels: {int((~valid).sum())}")
    print(f"Reprojection verified: {DESTINATION_PATH}")


if __name__ == "__main__":
    main()
