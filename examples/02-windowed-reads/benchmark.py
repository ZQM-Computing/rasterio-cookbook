"""Compare native GeoTIFF block reads with configurable logical windows.

This is an observational benchmark, not a claim that one window size is always
faster. It uses the same compressed synthetic raster and validates the sum for
every strategy before reporting timings.
"""
from __future__ import annotations

import argparse
import statistics
import tempfile
import time
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.windows import Window


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=8192)
    parser.add_argument("--height", type=int, default=8192)
    parser.add_argument("--block-size", type=int, default=256)
    parser.add_argument("--window-sizes", type=int, nargs="+", default=[64, 128, 256, 512, 1024])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--cache-mb", type=int, default=256)
    args = parser.parse_args()
    for name in ("width", "height", "block_size", "repeats", "cache_mb"):
        if getattr(args, name) <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if args.block_size % 16:
        parser.error("--block-size must be a multiple of 16 for tiled GeoTIFF")
    if any(size <= 0 for size in args.window_sizes):
        parser.error("--window-sizes values must be positive")
    return args


def logical_windows(width: int, height: int, size: int):
    for row in range(0, height, size):
        for col in range(0, width, size):
            yield Window(col, row, min(size, width - col), min(size, height - row))


def sum_windows(path: Path, strategy: str, size: int | None, cache_mb: int) -> tuple[int, int]:
    total = 0
    count = 0
    with rasterio.Env(GDAL_CACHEMAX=cache_mb):
        with rasterio.open(path) as dataset:
            windows = (
                (window for _, window in dataset.block_windows(1))
                if strategy == "native"
                else logical_windows(dataset.width, dataset.height, int(size))
            )
            for window in windows:
                values = dataset.read(1, window=window)
                total += int(values.sum(dtype=np.uint64))
                count += 1
    return total, count


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(20261031)
    pixels = rng.integers(0, 65536, size=(args.height, args.width), dtype=np.uint16)
    expected = int(pixels.sum(dtype=np.uint64))

    with tempfile.TemporaryDirectory(prefix="rasterio-window-bench-") as directory:
        raster_path = Path(directory) / "benchmark.tif"
        profile = {
            "driver": "GTiff",
            "height": args.height,
            "width": args.width,
            "count": 1,
            "dtype": "uint16",
            "crs": "EPSG:3857",
            "transform": from_origin(0, args.height, 1, 1),
            "tiled": True,
            "blockxsize": args.block_size,
            "blockysize": args.block_size,
            "compress": "deflate",
        }
        with rasterio.open(raster_path, "w", **profile) as dataset:
            dataset.write(pixels, 1)
        del pixels

        strategies = [("native", None)] + [("logical", size) for size in args.window_sizes]
        print(f"Raster: {args.width}x{args.height}, uint16, DEFLATE")
        print(f"Native block: {args.block_size}x{args.block_size}; GDAL cache: {args.cache_mb} MiB")
        print(f"Repeats: {args.repeats}; expected sum: {expected}")
        print("strategy,window_size,windows,median_ms,min_ms,max_ms")
        for strategy, size in strategies:
            elapsed = []
            count = 0
            for _ in range(args.repeats):
                started = time.perf_counter()
                total, count = sum_windows(raster_path, strategy, size, args.cache_mb)
                elapsed.append((time.perf_counter() - started) * 1000)
                if total != expected:
                    raise RuntimeError(
                        f"{strategy} size={size}: sum {total} != expected {expected}"
                    )
            label = "native" if size is None else str(size)
            print(
                f"{strategy},{label},{count},"
                f"{statistics.median(elapsed):.3f},{min(elapsed):.3f},{max(elapsed):.3f}"
            )


if __name__ == "__main__":
    main()
