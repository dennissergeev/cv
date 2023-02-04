#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get bibcodes from NASA ADS."""
import json
import os
import sys

import requests

from paths import bibcodes_file


token = os.getenv("ADS_API_KEY")
LIB_URL = "https://api.adsabs.harvard.edu/v1/biblib/libraries"
LIBRARY_ID = "2IT653szTA-gYw3vyA-9Sw"


def fetch(clobber=False, library_id=LIBRARY_ID):
    """Fetch bibcodes from the NASA ADS private library."""
    if clobber:
        print("Fetching bibcodes from ADS.")
        # Get library id
        # req = requests.get(
        #     LIB_URL,
        #     headers={"Authorization": f"Bearer {token}"},
        # )
        # library_id = req.json()["libraries"][0]["id"]

        # Get the list of bibcodes in the library
        req = requests.get(
            f"{LIB_URL}/{library_id}",
            headers={"Authorization": f"Bearer {token}"},
            params={"rows": 1000},
        )
        with bibcodes_file.open("w") as f_json:
            json.dump(req.json(), f_json)
    else:
        print("Using cached bibcodes.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    fetch(clobber=clobber)
