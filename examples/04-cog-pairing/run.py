"""Example 04: write a COG-layout GeoTIFF and check its layout.

Design-only pattern (gate 1 target): this script is written, not yet
executed against a fleet Rasterio environment, and not covered by
tests/test_examples.py (which covers examples 01-03 only). Do not
describe it as validated or as full COG conformance.

What it does, when run:
1. Creates a deterministic 256x256 uint16 raster (values 0..65535,
   mean 32767.5) in EPSG:4326.
2. Writes it as a COG-layout GeoTIFF: tiled 128x128 blocks, deflate
   compression, overviews at factors 2 and 4.
3. Reopens the file and asserts the layout: tiled flag, block sizes,
   overview factors, compression, CRS, and a windowed pixel check.
4. Runs the same layout check against an untiled control file and
   shows the findings it reports there.
5. Prints the TiTiler URL shape for serving the file. The TiTiler
   host and port are placeholders: the endpoint spelling and port are
   to confirm at validation against titiler-cookbook, and are not
   asserted here.

Layout checks are NOT full COG conformance. Full conformance is
`rio cogeo validate` (rio-cogeo), a separate validation step that this
pattern deliberately does not claim.

Run from any directory with:
    python /path/to/examples/04-cog-pairing/run.py
On fleet nodes use the geo-environment Python by full path, for
example C:\\geo-tools\\python-venv\\Scripts\\python.exe (bare `python`
on Node-1 is the hermes-agent venv and must not be used). Outputs land
beneath ./output in the current working directory.
"""
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.windows import Window

OUTPUT_DIR = Path("output")
COG_PATH = OUTPUT_DIR / "cog_layout.tif"
PLAIN_PATH = OUTPUT_DIR / "plain_control.tif"
WIDTH, HEIGHT = 256, 256
BLOCK = 128
OVERVIEWS = [2, 4]


def make_pixels():
    return np.arange(WIDTH * HEIGHT, dtype=np.uint16).reshape(HEIGHT, WIDTH)


def check_cog_layout(path):
    """Return a list of layout findings; empty means COG-layout clean."""
    findings = []
    with rasterio.open(path) as dataset:
        profile = dataset.profile
        if not profile.get("tiled"):
            findings.append("not tiled")
        if profile.get("blockxsize", 0) >= WIDTH or profile.get("blockysize", 0) >= HEIGHT:
            findings.append("blocks span the full raster")
        if not dataset.overviews(1):
            findings.append("no overviews")
        if not profile.get("compress"):
            findings.append("no compression")
    return findings


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pixels = make_pixels()
    transform = from_origin(-80.0, 30.0, 0.001, 0.001)
    profile = {
        "driver": "GTiff",
        "height": HEIGHT,
        "width": WIDTH,
        "count": 1,
        "dtype": pixels.dtype,
        "crs": "EPSG:4326",
        "transform": transform,
        "tiled": True,
        "blockxsize": BLOCK,
        "blockysize": BLOCK,
        "compress": "deflate",
    }
    with rasterio.open(COG_PATH, "w", **profile) as dataset:
        dataset.write(pixels, 1)
        dataset.build_overviews(OVERVIEWS, Resampling.average)

    with rasterio.open(COG_PATH) as result:
        assert result.profile.get("tiled") is True
        assert result.profile.get("blockxsize") == BLOCK
        assert result.profile.get("blockysize") == BLOCK
        assert result.overviews(1) == OVERVIEWS
        assert result.profile.get("compress") == "deflate"
        assert result.crs == rasterio.crs.CRS.from_epsg(4326)
        window = result.read(1, window=Window(0, 0, BLOCK, BLOCK))
        if not np.array_equal(window, pixels[0:BLOCK, 0:BLOCK]):
            raise RuntimeError("Windowed pixels differ from the source")
    findings = check_cog_layout(COG_PATH)
    if findings:
        raise RuntimeError(f"COG layout findings on {COG_PATH}: {findings}")
    print(f"COG layout verified: {COG_PATH}")

    plain_profile = {k: v for k, v in profile.items()
                     if k not in ("tiled", "blockxsize", "blockysize", "compress")}
    with rasterio.open(PLAIN_PATH, "w", **plain_profile) as dataset:
        dataset.write(pixels, 1)
    control = check_cog_layout(PLAIN_PATH)
    print(f"Control file findings (expected, not clean): {control}")
    assert "not tiled" in control and "no overviews" in control

    print("TiTiler serving shape (host/port to confirm at validation):")
    print(f"  {{TITILER_HOST}}/cog/tiles/{{z}}/{{x}}/{{y}}.png?url={COG_PATH.name}")


if __name__ == "__main__":
    main()
