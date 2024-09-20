import plotly.express as px

from yuliana.util import apply_quantisation, get_agreed_keys, get_blocks, load_data, make_keys, preprocess_blocks


def inspect_preprocessing(dataset, processing_methods, quantisation_method):

    preprocessing_block_size = 128
    quantisation_block_size = 128
    target_key_length = 128

    plot = {
        "stage": [],
        "value": [],
        "source": [],
        "index": [],
    }

    gw, node = load_data(dataset)

    def add_signal(samples, stage, source):
        for index, value in enumerate(samples):
            plot["stage"].append(stage)
            plot["source"].append(source)
            plot["index"].append(index)
            plot["value"].append(value)

    def add_signals(gw, node, stage):
        add_signal(gw, stage, "gw")
        add_signal(node, stage, "node")

    def show_plot():
        px.line(
            plot,
            x="index",
            y="value",
            color="source",
            facet_col="stage",
            title=f'Processing "{dataset}" dataset',
        ).show()

    add_signals(gw, node, "measurements")

    for method in processing_methods:
        gw = preprocess_blocks(gw, method, preprocessing_block_size)
        node = preprocess_blocks(node, method, preprocessing_block_size)
        add_signals(gw, node, method.__name__)

    gw_keys, node_keys = apply_quantisation(gw, node, quantisation_method, quantisation_block_size, target_key_length)
    candidates = get_agreed_keys(gw_keys, node_keys)
    [print(len(key)) for key in gw_keys]
    [print(len(key)) for key in node_keys]

    for index, key in enumerate(candidates):
        signal = [int(bit) for bit in key]
        add_signal(signal, "keys", f"key-{index}")

    show_plot()
