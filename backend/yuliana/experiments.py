from yuliana.algorithms import (
    combined_multilevel_quantisation,
    kalman_yuliana,
    polynomial_regression_yuliana,
)
from yuliana.preprocessing_evaluation import (
    preprocess_block_correlation_analysis,
    preprocessing_dataset_blocksize_analysis,
)
from yuliana.quantisation_evaluation import quantisation_block_bdr_analysis, quantisation_key_randomness_analysis


def experiment_one():
    scenarios = ["oliviera-los-near.csv", "oliviera-los-far.csv"]
    methods = [polynomial_regression_yuliana, kalman_yuliana]
    quantisation_method = combined_multilevel_quantisation

    test_block_sizes = [64, 128]
    preprocessing_dataset_blocksize_analysis(scenarios, methods, test_block_sizes)

    preprocessing_block_size = 128
    quantisation_block_size = 128
    target_key_length = 128

    preprocess_block_correlation_analysis(scenarios, methods, preprocessing_block_size)

    quantisation_block_bdr_analysis(
        scenarios,
        methods,
        quantisation_method,
        preprocessing_block_size,
        quantisation_block_size,
        target_key_length,
    )

    quantisation_key_randomness_analysis(
        scenarios,
        methods,
        quantisation_method,
        preprocessing_block_size,
        quantisation_block_size,
        target_key_length,
    )
