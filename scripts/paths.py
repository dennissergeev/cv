# -*- coding: utf-8 -*-
"""Common paths."""
from pathlib import Path

# Absolute path to the top level of the repository
root = Path(__file__).resolve().parents[1].absolute()

# Data directory
data = root / "data"
bibcodes_file = data / "bibcodes.json"
metrics_file = data / "metrics.json"

# Images directory
images = root / "images"
