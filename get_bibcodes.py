#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get bibcodes from NASA ADS."""
import json
from pathlib import Path
import os
import sys

import ads
import requests


ads.config.token = os.getenv("ADS_API_KEY")
LIB_URL = "https://api.adsabs.harvard.edu/v1/biblib/libraries"
MET_URL = "https://api.adsabs.harvard.edu/v1/metrics"
DATA = Path("data")


def fetch(clobber=False):
    """Fetch bibcodes from the NASA ADS private library."""
    if clobber:
        print("Fetching bibcodes from ADS.")
        # Get library id
        req = requests.get(
            LIB_URL,
            headers={"Authorization": f"Bearer {ads.config.token}"},
        )
        library_id = req.json()["libraries"][0]["id"]

        # Get the list of bibcodes in the library
        req = requests.get(
            f"{LIB_URL}/{library_id}",
            headers={"Authorization": f"Bearer {ads.config.token}"},
        )
        DATA.mkdir(exist_ok=True)
        with (DATA / "bibcodes.json").open("w") as f_json:
            json.dump(req.json(), f_json)
    else:
        print("Using cached bibcodes.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    fetch(clobber=clobber)
