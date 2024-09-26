import plotly.express as px

from yuliana.plots import PreprocessingInspectionPlot
from yuliana.util import load_data, preprocess_blocks


def inspect_preprocessing(dataset, processing_methods, preprocessing_block_size):
    plot = PreprocessingInspectionPlot()

    gw, node = load_data(dataset)
    plot.add_signals(gw, node, "raw")

    for method in processing_methods:
        gw = preprocess_blocks(gw, method, preprocessing_block_size)
        node = preprocess_blocks(node, method, preprocessing_block_size)
        plot.add_signals(gw, node, method.__name__)

    fig = plot.make()
    fig.update_layout(title_text=f"Pre-processing inspection of {dataset}")
    fig.show()
