from typing import Union, Literal, List
from fastapi import FastAPI
import csv


app = FastAPI()


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


for dataset in [
    "oliviera-car.csv",
    "oliviera-los-far.csv",
    "oliviera-los-near.csv",
    "oliviera-nlos.csv",
    "oliviera-walking.csv",
]:
    print(dataset)
    gw, node = load_dataset(dataset)
    print()
    print("".join(map(lambda x: str(x), mean_std_quantization(gw[0:100]))))
    print("".join(map(lambda x: str(x), mean_std_quantization(node[0:100]))))
    print()
