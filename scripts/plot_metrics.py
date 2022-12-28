#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plot NASA ADS metrics."""
import json
import sys
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from paths import metrics_file, images


COLORS = ["#022020", "#003c3c", "#007d69", "#00c896", "#00dca5"]


def plot_total_pubs(metrics, ax=None):
    """Plot total publications from ADS metrics JSON data."""
    # Convert data from dict-like to pandas series
    pub_series = pd.Series(
        metrics["histograms"]["publications"]["all publications"]
    ).cumsum()
    pub_series.index = pub_series.index.astype(int)
    # Make a plot
    if ax is None:
        ax = plt.axes()
    ax.plot(pub_series.index, pub_series, marker="s", color=COLORS[1], ms=4)
    ax.set_ylabel("Publications")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))


def plot_total_cits(metrics, ax=None):
    """Plot total citations from ADS metrics JSON data."""
    # Convert data from dict-like to pandas series
    cit_series = sum(
        pd.Series(metrics["histograms"]["citations"][key])
        for key in [
            "refereed to refereed",
            "refereed to nonrefereed",
            "nonrefereed to refereed",
            "nonrefereed to nonrefereed",
        ]
    ).cumsum()
    cit_series.index = cit_series.index.astype(int)
    # Make a plot
    if ax is None:
        ax = plt.axes()
    ax.plot(cit_series.index, cit_series, marker="*", color=COLORS[3], ms=6)
    ax.set_ylabel("Citations")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))


def plot_indices(metrics, ax=None):
    """Plot indices from ADS metrics JSON data."""
    # Convert data from dict-like to pandas series
    h_series = pd.Series(metrics["time series"]["h"])
    i10_series = pd.Series(metrics["time series"]["i10"])
    h_series.index = h_series.index.astype(int)
    i10_series.index = i10_series.index.astype(int)
    # Make a plot
    if ax is None:
        ax = plt.axes()
    ax.plot(
        h_series.index, h_series, marker="X", color=COLORS[2], label="h", ms=5
    )
    ax.plot(
        i10_series.index,
        i10_series,
        marker="D",
        color=COLORS[4],
        label="i10",
        linestyle="--",
        dash_capstyle="round",
        ms=3,
    )
    ax.legend(loc="upper left")
    ax.set_ylabel("Index")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))


def make_plots(year_start=None, style="default"):
    """Make the plots."""
    # Load pre-fetched data
    with metrics_file.open("r") as f_json:
        metrics = json.load(f_json)
    # Make a figure and plot metrics in each of the subplots
    with plt.style.context(style):
        fig, axs = plt.subplots(
            ncols=3, figsize=(8, 2), sharex=True, gridspec_kw=dict(wspace=0.5)
        )
        plot_total_pubs(metrics=metrics, ax=axs[0])
        plot_total_cits(metrics=metrics, ax=axs[1])
        plot_indices(metrics=metrics, ax=axs[2])

        for ax in axs:
            if year_start is not None:
                ax.set_xlim(
                    year_start,
                    datetime.now().year + datetime.now().month // 12,
                )
                ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=4))
            plt.setp(ax.get_xticklabels(), rotation=30)
        fig.align_ylabels()
        fig.align_xlabels()
        fig.savefig(images / "sergeev_ads_metrics.pdf", bbox_inches="tight")


if __name__ == "__main__":
    matplotlib.use("agg")
    if len(sys.argv) > 1 and sys.argv[1] == "--year_start":
        year_start = int(sys.argv[2])
    else:
        year_start = None
    make_plots(year_start=year_start, style="ggplot")
