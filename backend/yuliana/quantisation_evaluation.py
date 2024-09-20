from app.services.nist_test_suite.ApproximateEntropy import ApproximateEntropy
from app.services.nist_test_suite.CumulativeSums import CumulativeSums
from app.services.nist_test_suite.FrequencyTest import FrequencyTest
from app.services.nist_test_suite.RunTest import RunTest
from yuliana.util import (
    apply_preprocessing,
    apply_quantisation,
    get_agreed_keys,
    get_bdr,
    load_data,
    make_keys,
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
        facet_col="dataset",
        title=f"Block level BDR with block sizes ({preprocessing_block_size}, {quantisation_block_size})",
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

    plot = {
        "dataset": [],
        "test": [],
        "p-value": [],
    }

    randomness_tests = [
        ApproximateEntropy.approximate_entropy_test,
        CumulativeSums.cumulative_sums_test,
        FrequencyTest.block_frequency,
        FrequencyTest.monobit_test,
        RunTest.longest_one_block_test,
        RunTest.run_test,
    ]

    def add_result(dataset, test, pval):
        plot["dataset"].append(dataset)
        plot["test"].append(test)
        plot["p-value"].append(pval)

    for dataset in datasets:
        gw, node = load_data(dataset)
        gw, node = apply_preprocessing(gw, node, processing_methods, preprocessing_block_size)
        gw_keys, node_keys = apply_quantisation(
            gw, node, quantisation_method, quantisation_block_size, target_key_length
        )
        candidates = get_agreed_keys(gw_keys, node_keys)

        print(f"{len(candidates)} candiate keys from {dataset}")

        for index, key in enumerate(candidates):

            num_passed = 0
            for test in randomness_tests:
                pval, passed = test(key)
                num_passed += 1 if passed else 0
                add_result(dataset, test.__name__, pval)
                # print(f"{round(pval, 4)} - {test.__name__}")

            print(f"key {index} passed {num_passed}/{len(randomness_tests)} tests")

    px.histogram(plot, x="p-value", color="test", facet_col="dataset", nbins=10).show()

    # plot2 = {
    #     "dataset": [],
    #     "key_index": [],
    #     "index": [],
    #     "value": [],
    # }

    # for idx, bit in enumerate(key):
    #     plot2["dataset"].append(dataset)
    #     plot2["index"].append(idx)
    #     plot2["key_index"].append(index)
    #     plot2["value"].append(int(bit))

    # px.line(plot2, x="index", color="key_index", facet_col="dataset", y="value").show()
