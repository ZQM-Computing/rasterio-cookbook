"""End-to-end tests for the cookbook's self-contained Rasterio examples."""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = (
    ("01-read-write", "Verified copy: output/rasterio_copy.tif"),
    ("02-windowed-reads", "Windows processed: 4"),
    ("03-reprojection", "Reprojection verified: output/reprojected_3857.tif"),
)


def test_example_scripts_have_valid_python_syntax():
    for name, _ in EXAMPLES:
        script = ROOT / "examples" / name / "run.py"
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


def test_examples_run_and_write_valid_rasters(tmp_path):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for name, marker in EXAMPLES:
        script = ROOT / "examples" / name / "run.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, (
            f"{name} failed ({result.returncode}).\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
        assert marker in result.stdout
    with rasterio.open(tmp_path / "output" / "rasterio_copy.tif") as dataset:
        assert dataset.width == 10 and dataset.height == 10 and dataset.count == 1
        assert dataset.crs == rasterio.crs.CRS.from_epsg(4326)
        assert np.array_equal(dataset.read(1), np.arange(100, dtype=np.uint16).reshape(10, 10))
    with rasterio.open(tmp_path / "output" / "windowed_demo.tif") as dataset:
        assert dataset.width == 512 and dataset.height == 512
        assert dataset.crs == rasterio.crs.CRS.from_epsg(3857)
        assert dataset.block_shapes == [(256, 256)]
    with rasterio.open(tmp_path / "output" / "reprojected_3857.tif") as dataset:
        assert dataset.width > 0 and dataset.height > 0
        assert dataset.crs == rasterio.crs.CRS.from_epsg(3857)
        assert dataset.nodata == -9999.0
        assert dataset.transform.a > 0 and dataset.transform.e < 0
        values = dataset.read(1)
        valid = values != dataset.nodata
        assert valid.any()
        assert np.isfinite(values[valid]).all()
