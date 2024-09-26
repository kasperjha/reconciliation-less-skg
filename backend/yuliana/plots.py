from typing import override
from plotly.subplots import make_subplots
from pandas import DataFrame
import plotly.graph_objects as go
from plotly import express as px
import numpy as np


class KeyRandomnessTable:
    """Presents a table subplot with randomness test results for each dataset."""

    def __init__(self, num_decimals=6):
        self.tables = {}
        self.num_decimals = num_decimals

    def add_result(self, key_index, dataset, test, alpha):
        """Add the results of a randomness test."""
        if dataset not in self.tables.keys():
            self.tables[dataset] = {"test": []}
        if key_index not in self.tables[dataset].keys():
            self.tables[dataset][key_index] = []
        if test not in self.tables[dataset]["test"]:
            self.tables[dataset]["test"].append(test)
        self.tables[dataset][key_index].append(round(alpha, self.num_decimals))

    def make(self):
        """Get a copy of the final plot instance."""
        specs = [[{"type": "table"}], [{"type": "table"}]]
        fig = make_subplots(rows=len(self.tables.keys()), cols=1, specs=specs)
        row = 1
        for dataset, table in self.tables.items():
            df = DataFrame(table)
            cells = [df[col] for col in df.columns]
            table_fig = go.Table({"header": dict(values=df.columns), "cells": dict(values=cells)})
            fig.add_trace(table_fig, row=row, col=1)
            row += 1
        fig.update_layout(title_text=f"Randomness results for datasets: {list(self.tables.keys())}")
        return fig


class KeyInspectionPlot:
    """A plot to inspect the bits of one or more secret keys."""

    def __init__(self):
        self.plot = {"key_index": [], "bit_index": [], "bit_value": []}

    def add_key(self, key_index, key):
        for bit_index, bit_value in enumerate(key):
            self.plot["key_index"].append(key_index)
            self.plot["bit_index"].append(bit_index)
            self.plot["bit_value"].append(bit_value)

    def add_keys(self, keys):
        """Add multiple keys at once. Key index is taken as index of key in iterable."""
        for key_index, key in enumerate(keys):
            self.add_key(key_index, key)

    def make(self):
        return px.line(self.plot, x="bit_index", y="bit_value", facet_row="key_index", line_shape="hv")


class PreprocessingInspectionPlot:
    """Plot to inspect what the different steps of preprocessing does."""

    def __init__(self):
        self.plot = {
            "stage": [],
            "value": [],
            "source": [],
            "index": [],
        }

    def add_signal(self, samples, stage, source):
        for index, value in enumerate(samples):
            self.plot["stage"].append(stage)
            self.plot["source"].append(source)
            self.plot["index"].append(index)
            self.plot["value"].append(value)

    def add_signals(self, gw, node, stage):
        self.add_signal(gw, stage, "gw")
        self.add_signal(node, stage, "node")

    def make(self):
        return px.line(self.plot, x="index", y="value", color="source", facet_col="stage")


class QuantisationIntervalPlot:
    """A plot to inspect the quantiation intervals for CMQ together with gateway and node signals."""

    def __init__(self, dataset=None):
        self.plot = {
            "sample_index": [],
            "sample_value": [],
            "block_index": [],
            "source": [],
        }
        self.lines = {}

    def add_signal(self, source, block_index, signal):
        if source not in self.lines.keys():
            self.lines[source] = {}

        self.lines[source][block_index] = (np.var(signal), np.mean(signal))

        for sample_index, sample_value in enumerate(signal):
            self.plot["source"].append(source)
            self.plot["block_index"].append(block_index)
            self.plot["sample_index"].append(sample_index)
            self.plot["sample_value"].append(sample_value)

    def get_intervals(self, mean, variance):
        return zip([mean, mean - variance], ["blue", "red"])

    def make(self):
        fig = px.line(self.plot, x="sample_index", y="sample_value", facet_row="source", facet_col="block_index")
        sources = list(self.lines.keys())
        for source, source_lines in self.lines.items():
            for block_index, (variance, mean) in source_lines.items():
                source_index = sources.index(source)
                intervals = self.get_intervals(mean, variance)
                for y_value, color in intervals:
                    fig.add_hline(
                        y=y_value,
                        line_dash="dash",
                        line_color=color,
                        line_width=0.5,
                        row=source_index,
                        col=block_index + 1,
                    )
        return fig


class QuantisationIntervalPlotCorrected(QuantisationIntervalPlot):
    """Same as parent class, but with corrected quantisation intervals."""

    @override
    def get_intervals(self, mean, variance):
        return zip([mean, mean - variance, mean + variance], ["blue", "red", "green"])
