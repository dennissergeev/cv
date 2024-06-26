# -*- coding: utf-8 -*-
"""Common paths."""
from pathlib import Path

# Absolute path to the top level of the repository
root = Path(__file__).resolve().parents[1].absolute()

# Data directory
data = root / "data"
bibcodes_file = data / "bibcodes.json"
metrics_file = data / "metrics.json"
publications_file = data / "publications.json"

# Other static data
static = root / "static"
journal_abbr_file = static / "journal_abbr.json"

# Images directory
images = root / "images"

# TeX files
stats_file = root / "stats.tex"
pubs_formatted = root / "pubs.tex"
pubs_formatted_short = root / "pubs_short.tex"
