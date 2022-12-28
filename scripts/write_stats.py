#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Write NASA ADS stats as TeX table."""
import json

from paths import metrics_file, publications_file, stats_file


def main(last_name):
    """Load data from existing JSON files and write it as TeX table."""
    # Read previously fetched data from JSON files.
    with metrics_file.open("r") as f_json:
        metrics = json.load(f_json)
    with publications_file.open("r") as f_json:
        publications = json.load(f_json)["docs"]
    # Create a dictionary with required numbers
    stats = {}
    stats["Total Pub."] = metrics["basic stats"]["number of papers"]
    stats["Refereed"] = metrics["basic stats refereed"]["number of papers"]
    stats["First Author"] = sum(
        1
        for pub in publications
        if pub["author"][0].split(",")[0] == last_name
    )
    stats["Citations"] = metrics["citation stats"]["total number of citations"]
    stats["h-index"] = metrics["indicators"]["h"]
    # Write the dictionary in a TeX-table format
    with stats_file.open("w") as f_tex:
        for key, val in stats.items():
            f_tex.write(f"{key} & \\textbf{{{val}}} \\\\\n")


if __name__ == "__main__":
    main(last_name="Sergeev")
