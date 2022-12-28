#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get NASA ADS metrics."""
import json
import os
import sys

import ads
import requests

from paths import bibcodes_file, metrics_file

ads.config.token = os.getenv("ADS_API_KEY")
MET_URL = "https://api.adsabs.harvard.edu/v1/metrics"


def fetch(clobber=False):
    """Fetch metrics from the NASA ADS private library."""
    if clobber:
        print("Fetching metrics from ADS.")
        with bibcodes_file.open("r") as f_json:
            bibcodes = json.load(f_json)["documents"]

        # Get metrics for the list of bibcodes
        req = requests.post(
            MET_URL,
            headers={
                "Authorization": f"Bearer {ads.config.token}",
                "Content-type": "application/json",
            },
            data=json.dumps({"bibcodes": bibcodes}),
        )
        with metrics_file.open("w") as f_json:
            json.dump(req.json(), f_json)
    else:
        print("Using cached metrics.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    fetch(clobber=clobber)
