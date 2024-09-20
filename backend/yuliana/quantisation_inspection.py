from yuliana.util import apply_preprocessing, get_blocks, load_data
import plotly.express as px
import numpy as np


def inspect_quantisation(
    dataset,
    preprocessing_methods,
    quantisation_method,
    preprocessing_block_size,
    quantisation_block_size,
    target_key_length,
):
    gw, node = load_data(dataset)
    gw, node = apply_preprocessing(gw, node, preprocessing_methods, preprocessing_block_size)
    blocks = zip(get_blocks(gw, preprocessing_block_size), get_blocks(node, preprocessing_block_size))

    plot = {
        "index": [],
        "block_index": [],
        "value": [],
        "source": [],
    }

    gw_lines = []
    node_lines = []

    def add_signal(block_index, signal, source):
        for index, value in enumerate(signal):
            plot["index"].append(index)
            plot["block_index"].append(block_index)
            plot["value"].append(value)
            plot["source"].append(source)

    for block_index, (gw_block, node_block) in enumerate(blocks):
        add_signal(block_index, gw_block, "gw")
        gw_lines.append((np.var(gw_block), np.mean(gw_block)))
        add_signal(block_index, node_block, "node")
        node_lines.append((np.var(node_block), np.mean(node_block)))

    fig = px.line(plot, x="index", y="value", facet_row="source", facet_col="block_index")

    def add_line(var, mean, source, block_index):
        row = 0 if source == "gw" else 1
        fig.add_hline(y=mean - var, line_dash="dash", line_color="blue", line_width=0.5, row=row, col=block_index + 1)
        fig.add_hline(y=mean, line_dash="dash", line_color="red", line_width=0.5, row=row, col=block_index + 1)
        fig.add_hline(y=mean + var, line_dash="dash", line_color="green", line_width=0.5, row=row, col=block_index + 1)

    for block_index, (var, mean) in enumerate(gw_lines):
        add_line(var, mean, "gw", block_index)
    for block_index, (var, mean) in enumerate(node_lines):
        add_line(var, mean, "node", block_index)

    fig.show()
