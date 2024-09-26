from app.services.nist_test_suite.ApproximateEntropy import ApproximateEntropy
from app.services.nist_test_suite.CumulativeSums import CumulativeSums
from app.services.nist_test_suite.FrequencyTest import FrequencyTest
from app.services.nist_test_suite.RunTest import RunTest
from yuliana.plots import KeyInspectionPlot, KeyRandomnessTable
from yuliana.util import (
    apply_preprocessing,
    apply_privacy_amplification,
    apply_quantisation,
    get_agreed_keys,
    get_bdr,
    load_data,
)
import plotly.express as px


def quantisation_block_bdr_analysis(
    datasets,
    processing_methods,
    quantisation_method,
    preprocessing_block_size,
    quantisation_block_size,
    target_key_length,
):

    plot = {"dataset": [], "bdr": []}

    def add_result(dataset, bdr):
        plot["dataset"].append(dataset)
        plot["bdr"].append(bdr)

    for dataset in datasets:
        gw, node = load_data(dataset)
        gw, node = apply_preprocessing(gw, node, processing_methods, preprocessing_block_size)
        gw_keys, node_keys = apply_quantisation(
            gw, node, quantisation_method, quantisation_block_size, target_key_length
        )

        print(f"evaluating block-level bdr of {dataset}")

        for gwk, nok in zip(gw_keys, node_keys):
            bdr = get_bdr(gwk, nok)
            print(bdr)
            add_result(dataset, bdr)

        print(f"{len(get_agreed_keys(gw_keys, node_keys))} blocks with 0 BDR from {dataset} ")

    fig = px.histogram(
        plot,
        x="bdr",
        nbins=10,
        color="dataset",
        title=f"Block level BDR with block sizes ({preprocessing_block_size}, {quantisation_block_size})",
        range_x=[0, 1],
        barmode="group",
    )
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig.show()


def quantisation_key_randomness_analysis(
    datasets,
    processing_methods,
    quantisation_method,
    preprocessing_block_size,
    quantisation_block_size,
    target_key_length,
):

    randomness_tests = [
        ApproximateEntropy.approximate_entropy_test,
        FrequencyTest.monobit_test,
        FrequencyTest.block_frequency,
        RunTest.run_test,
        RunTest.longest_one_block_test,
        CumulativeSums.cumulative_sums_test,
    ]

    table = KeyRandomnessTable()

    for dataset in datasets:
        gw, node = load_data(dataset)
        gw, node = apply_preprocessing(gw, node, processing_methods, preprocessing_block_size)
        gw_keys, node_keys = apply_quantisation(
            gw, node, quantisation_method, quantisation_block_size, target_key_length
        )
        candidates = get_agreed_keys(gw_keys, node_keys)
        key_plot = KeyInspectionPlot()
        key_plot.add_keys(candidates)
        key_plot.make().show()

        for key_index, key in enumerate(candidates):
            for test in randomness_tests:
                pval, passed = test(key)
                test_name = " ".join(test.__name__.split("_"))
                print(dataset, test_name, pval)
                table.add_result(key_index, dataset, test_name, pval)

    fig = table.make()
    fig.update_layout(title_text="Without privacy amplification")
    fig.show()

    table = KeyRandomnessTable()

    for dataset in datasets:
        gw, node = load_data(dataset)
        gw, node = apply_preprocessing(gw, node, processing_methods, preprocessing_block_size)
        gw_keys, node_keys = apply_quantisation(
            gw, node, quantisation_method, quantisation_block_size, target_key_length
        )
        gw_keys, node_keys = apply_privacy_amplification(gw_keys, node_keys, target_key_length)
        candidates = get_agreed_keys(gw_keys, node_keys)

        key_plot = KeyInspectionPlot()
        key_plot.add_keys(candidates)
        key_plot.make().show()

        for key_index, key in enumerate(candidates):
            for test in randomness_tests:
                pval, passed = test(key)
                test_name = " ".join(test.__name__.split("_"))
                print(dataset, test_name, pval)
                table.add_result(key_index, dataset, test_name, pval)

    fig = table.make()
    fig.update_layout(title_text="With privacy amplification")
    fig.show()
