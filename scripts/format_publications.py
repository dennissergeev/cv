#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Format publication entries."""

import json
import re

from paths import (
    journal_abbr_file,
    publications_file,
    pubs_formatted,
    pubs_formatted_short,
)


def replace_subscripts_and_superscripts(text):
    """Replace SUB / SUPER in NASA ADS titles."""
    # Regex pattern to match <SUB>...</SUB> and <SUPER>...</SUPER>
    pattern = re.compile(r"<(SUB|SUPER)>(.*?)</\1>", re.IGNORECASE)

    # Replacement function that wraps the content
    # in \textsubscript{} or \textsuperscript{}
    def replacement(match):
        tag = match.group(1).lower()
        content = match.group(2)
        if tag == "sub":
            return f"\\textsubscript{{{content}}}"
        elif tag == "super":
            return f"\\textsuperscript{{{content}}}"

    # Perform the substitution
    return pattern.sub(replacement, text)


def format_publication(pub: dict, idx: int = None, my_name: str = None) -> str:
    """Load publications from a JSON file and format them in TeX."""
    # Load journal abbreviations
    with journal_abbr_file.open("r") as f_json:
        JOURNAL_ABBR = json.load(f_json)
    refereed = pub["doctype"] == "article"

    entry = ""
    # Format the author list
    authors = []
    my_pos = -1
    for n_auth, author in enumerate(pub["author"]):
        last, first = author.split(", ")
        first_fmt = " ".join([f"{i[0]}." for i in first.split(" ")])
        if my_name in author:
            my_pos = n_auth
            name = rf"\textbf{{{last}, {first_fmt}}}"
        else:
            name = f"{last}, {first_fmt}"
        authors.append(name)

    authors_fmt = ""
    if n_auth > 3:
        authors_fmt += ", ".join(authors[:4])
        authors_fmt += ", et al."
        if my_pos > 3:
            authors_fmt += f" (incl. {authors[my_pos]})"
    elif n_auth > 0:
        authors_fmt += ", ".join(authors[:-1])
        authors_fmt += rf", \& {authors[-1]}"
    else:
        authors_fmt += {authors[0]}

    entry += authors_fmt

    # Format the year
    entry += f", {pub['year']}"

    # Format the title
    title = pub["title"][0]
    title = replace_subscripts_and_superscripts(title)
    entry += f", {title}"

    # Format the journal
    if journal := pub.get("pub"):
        if "arxiv" in journal.lower():
            entry += f", {pub['page'][0]}"
        else:
            entry += f", {JOURNAL_ABBR.get(journal, journal)}"

    # Add URL
    if doi := pub.get("doi"):
        link = rf"https://doi.org/{doi[0]}"
    elif url := pub.get("url"):
        link = url
    elif page := pub.get("page"):
        if "arxiv" in page[0].lower():
            arxiv_id = page[0].lstrip("arXiv:")
            link = rf"https://arxiv.org/abs/{arxiv_id}"
    else:
        link = rf"https://ui.adsabs.harvard.edu/abs/{pub['bibcode']}"
    entry += rf"~\href{{{link}}}{{\link}}"

    # Format the number of citations
    cit_count = pub.get("citation_count", 0)
    if cit_count == 0:
        cites = r"\textbullet"
    else:
        cites = cit_count

    if idx is None:
        idx = r"\textbullet"

    if refereed:
        line = rf"\small{{\highlightdark{{{idx}}}}} & {entry} & \small{{\highlightdark{{\textbf{{{cites}}}}}}} \\"
    else:
        line = rf"\small{{\tbc{{{idx}}}}} & \tbc{{{entry}}} & \small{{\tbc{{\textbf{{{cites}}}}}}} \\"

    return line


if __name__ == "__main__":
    last_name = "Sergeev"
    # Load the publications from the JSON file
    with publications_file.open("r") as f_json:
        pubs = json.load(f_json)["docs"]
    pubs = sorted(pubs, key=lambda x: x["pubdate"], reverse=True)

    # All publications
    with pubs_formatted.open("w") as f_tex:
        n_pub = len(pubs)
        for idx, pub in enumerate(pubs):
            f_tex.write(format_publication(pub, n_pub - idx, my_name=last_name) + "\n")

    # Publications for the short CV
    select_bibcodes = [
        "2025arXiv250419883S",
        "2024MNRAS.529.1776Z",
        "2024ApJ...970....7S",
        "2023JGRD..12839343M",
        "2023GMD....16.5601S",
        "2023GMD....16..621M",
        "2022PSJ.....3..213F",
        "2022PSJ.....3..211T",
        "2022PSJ.....3..212S",
        "2022PSJ.....3..214S",
        "2020ApJ...894...84S",
    ]
    with pubs_formatted_short.open("w") as f_tex:
        for idx, pub in enumerate([p for p in pubs if p["bibcode"] in select_bibcodes]):
            f_tex.write(format_publication(pub, my_name=last_name) + "\n")
