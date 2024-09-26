import plotly.express as px
import plotly.graph_objects as go
from yuliana.util import get_blocks, get_correlation, load_data, preprocess_blocks


def preprocessing_dataset_blocksize_analysis(datasets, methods, block_sizes):
    """
    The yuliana provides an evaluation of correlation before
    and after applying the preprocessing method, in two
    scenarios and with two block sizes.

    Each algorithm in the preprocessing phase is applied
    independently to eachblock and the correlation
    measurement is taken for the RSS signal as a whole.
    """

    plot = {
        "dataset": [],
        "stage": [],
        "correlation": [],
    }

    def add_result(dataset, stage, correlation):
        plot["dataset"].append(dataset)
        plot["stage"].append(stage)
        plot["correlation"].append(correlation)

    for dataset in datasets:
        gw, node = load_data(dataset)
        correlation_pre = get_correlation(gw, node)
        add_result(dataset, "measurement", correlation_pre)

    for dataset in datasets:
        for block_size in block_sizes:
            gw, node = load_data(dataset)
            for method in methods:
                gw = preprocess_blocks(gw, method, block_size)
                node = preprocess_blocks(node, method, block_size)
                correlation = get_correlation(gw, node)
            add_result(dataset, str(block_size), correlation)

    fig = px.bar(
        plot,
        x="dataset",
        y="correlation",
        color="stage",
        title="Correlation after processing with multiple block sizes.",
        barmode="group",
        range_y=[-1, 1],
    )
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.show()


def preprocess_block_correlation_analysis(datasets, methods, block_size):
    """
    The authors also provide an overview of the frequency of
    blocks for several bins of correlation coefficients. This
    is performed for both scenarios, but only for the block
    size which showed best general performance.
    """

    plot = {
        "dataset": [],
        "stage": [],
        "correlation": [],
    }

    def add_result(dataset, stage, correlation):
        plot["dataset"].append(dataset)
        plot["stage"].append(stage)
        plot["correlation"].append(correlation)

    def get_block_correlation(gw, node, block_size):
        blocks = zip(get_blocks(gw, block_size), get_blocks(node, block_size))
        return [get_correlation(gwb, nob) for gwb, nob in blocks]

    for dataset in datasets:
        gw, node = load_data(dataset)
        print("Analysing block-level correlation for: ", dataset)

        for correlation in get_block_correlation(gw, node, block_size):
            add_result(dataset, "measurement", correlation)

        for method in methods:
            gw = preprocess_blocks(gw, method, block_size)
            node = preprocess_blocks(node, method, block_size)

        for correlation in get_block_correlation(gw, node, block_size):
            add_result(dataset, "processed", correlation)
            print(correlation)

    fig = px.histogram(
        plot,
        x="correlation",
        color="stage",
        facet_row="dataset",
        title=f"Block level correlation ({block_size}bit block size)",
        range_x=[-1, 1],
        nbins=20,
        barmode="group",
    )
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.show()
