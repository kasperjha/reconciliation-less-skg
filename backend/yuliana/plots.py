from plotly.subplots import make_subplots
from pandas import DataFrame
import plotly.graph_objects as go


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

    def make_plot(self):
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

    def show(self):
        """Show the plot."""
        fig = self.get_plot()
        fig.show()

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
