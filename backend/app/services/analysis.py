import csv


def load_dataset(filename: str):
    gateway_samples = []
    node_samples = []

    with open(filename, "r") as file:
        is_header_row = True
        dataset = csv.reader(file)
        for gw, node in dataset:
            if is_header_row:
                is_header_row = False
                continue

            gateway_samples.append(int(gw))
            node_samples.append(int(node))

    return gateway_samples, node_samples


def std_dev(samples):
    n = len(samples)
    mean = sum(samples) / n
    sumsq = sum(v * v for v in samples)
    return (sumsq / n - mean * mean) ** 0.5


def mean_std_quantization(samples):
    mean = sum(samples) / len(samples)
    std = std_dev(samples)
    alpha = 0
    threshold_pos = mean + alpha * std
    threshold_neg = mean - alpha * std

    bits = []

    for sample in samples:
        if threshold_pos < sample:
            bits.append(1)
        if sample < threshold_neg:
            bits.append(0)
        else:
            continue

    return bits


def differential_quantization():
    raise NotImplementedError()
