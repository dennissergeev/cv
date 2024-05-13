#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Format publication entries."""
import json

from paths import (
    journal_abbr_file,
    publications_file,
    pubs_formatted,
    pubs_formatted_short,
)


def format_publication(pub, my_name):
    """Load publications from a JSON file and format them in TeX."""
    # Load journal abbreviations
    with journal_abbr_file.open("r") as f_json:
        JOURNAL_ABBR = json.load(f_json)

    entry = ""
    # Format the number of citations
    cit_count = pub["citation_count"]
    if cit_count == 0:
        cites = r"\textbullet"
    else:
        cites = cit_count

    refereed = pub["doctype"] == "article"
    if refereed:
        entry += rf"\item[\small{{\highlightdark{{\textbf{{{cites}}}}}}}] "
    else:
        entry += rf"\item[\small{{\tbc{{\textbf{{{cites}}}}}}}] "
        entry += r"\tbc{"

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

    # Format the title and URL
    title = pub["title"][0]
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

    entry += rf", \href{{{link}}}{{{title}}}"

    # Format the journal
    if journal := pub.get("pub"):
        if "arxiv" in journal.lower():
            entry += f", {pub['page'][0]}"
        else:
            entry += f", {JOURNAL_ABBR.get(journal, journal)}"

    if not refereed:
        entry += "}"  # to close \tbc{

    return entry


if __name__ == "__main__":
    last_name = "Sergeev"
    select_bibcodes = [
        "2024MNRAS.529.1776Z",
        "2024MNRAS.529.3971M",
        "2024arXiv240219277S",
        "2023JGRD..12839343M",
        "2023GMD....16.5601S",
        "2023GMD....16..621M",
        "2022MNRAS.517.2383B",
        "2022PSJ.....3..213F",
        "2022PSJ.....3..211T",
        "2022PSJ.....3..212S",
        "2022PSJ.....3..214S",
        "2022ApJ...930..152C",
        "2020A&A...639A..99E",
        "2020ApJ...894...84S",
        "2020ApJ...892L..33J",
    ]

    with publications_file.open("r") as f_json:
        pubs = json.load(f_json)["docs"]
    pubs = sorted(pubs, key=lambda x: x["pubdate"], reverse=True)

    with pubs_formatted.open("w") as f_tex:
        for pub in pubs:
            f_tex.write(format_publication(pub, my_name=last_name) + "\n")
    with pubs_formatted_short.open("w") as f_tex:
        for pub in pubs:
            if pub["bibcode"] in select_bibcodes:
                f_tex.write(format_publication(pub, my_name=last_name) + "\n")
