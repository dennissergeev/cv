#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get NASA ADS metrics."""
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


def get_metrics(clobber=False):
    """Fetch metrics from a NASA ADS private library."""
    if clobber:
        print("Fetching metrics from ADS.")
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
        bibcodes = req.json()["documents"]

        # Get metrics for the list of bibcodes
        req = requests.post(
            MET_URL,
            headers={
                "Authorization": f"Bearer {ads.config.token}",
                "Content-type": "application/json",
            },
            data=json.dumps({"bibcodes": bibcodes}),
        )
        DATA.mkdir(exist_ok=True)
        with (DATA / "metrics.json").open("w") as f_json:
            json.dump(req.json(), f_json)
    else:
        print("Using cached metrics.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    get_metrics(clobber=clobber)
