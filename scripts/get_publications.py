#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get publication metadata from NASA ADS."""
import json
import os
import sys

import requests

from paths import bibcodes_file, publications_file

token = os.getenv("ADS_API_KEY")
BQ_URL = "https://api.adsabs.harvard.edu/v1/search/bigquery"


def fetch(clobber=False):
    """Fetch entries from NASA ADS."""
    if clobber:
        # Load bibcodes from another JSON file
        with bibcodes_file.open("r") as f_json:
            bibcodes = json.load(f_json)["documents"]
        # Get metrics for the list of bibcodes
        print("Fetching publications from ADS.")
        req = requests.post(
            BQ_URL,
            params={
                "q": "*:*",
                "fl": [
                    "title",
                    "author",
                    "doi",
                    "year",
                    "pubdate",
                    "pub",
                    "volume",
                    "page",
                    "doctype",
                    "citation_count",
                    "bibcode",
                ],
                "rows": 1000,
            },
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "big-query/csv",
            },
            data="bibcode\n" + "\n".join(bibcodes),
        )
        with publications_file.open("w") as f_json:
            json.dump(req.json()["response"], f_json)
    else:
        print("Using cached data.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    fetch(clobber=clobber)
