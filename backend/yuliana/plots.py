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
