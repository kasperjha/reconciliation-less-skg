from yuliana.plots import KeyInspectionPlot, QuantisationIntervalPlot, QuantisationIntervalPlotCorrected
from yuliana.util import (
    apply_preprocessing,
    apply_quantisation,
    get_agreed_keys,
    get_bdr,
    get_blocks,
    load_data,
    preprocess_signal,
)
import plotly.express as px
import numpy as np


def inspect_quantisation(
    dataset,
    preprocessing_methods,
    quantisation_method,
    preprocessing_block_size,
    quantisation_block_size,
    target_key_length,
    use_corrected,
):
    gw, node = load_data(dataset)
    gw, node = apply_preprocessing(gw, node, preprocessing_methods, preprocessing_block_size)
    blocks = zip(get_blocks(gw, preprocessing_block_size), get_blocks(node, preprocessing_block_size))

    interval_plot = QuantisationIntervalPlotCorrected() if use_corrected else QuantisationIntervalPlot()

    for block_index, (gw_block, node_block) in enumerate(blocks):
        interval_plot.add_signal("gw", block_index, gw_block)
        interval_plot.add_signal("node", block_index, node_block)

    fig = interval_plot.make()
    fig.update_layout({"title": f"Quantiastion intervals on blocks of {dataset}"})
    fig.show()

    key_plot = KeyInspectionPlot()

    gw_keys, node_keys = apply_quantisation(gw, node, quantisation_method, quantisation_block_size, target_key_length)
    candidates = get_agreed_keys(gw_keys, node_keys)

    key_plot.add_keys(candidates)

    fig = key_plot.make()
    fig.update_layout({"title": f"Keys with BDR=0 from {dataset}"})
    fig.show()
