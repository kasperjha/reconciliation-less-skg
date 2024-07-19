from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class Collection(BaseModel):
    id: int
    name: str


# TODO: use a database
collections = [
    {"id": 1, "name": "Collection A"},
    {"id": 2, "name": "Collection B"},
]


@app.get("/collections/")
def get_collections() -> list[Collection]:
    return collections


class CollectionCreate(BaseModel):
    name: str


@app.post("/collections/")
def create_collection(collection: CollectionCreate) -> Collection:
    newCollection: Collection = {
        "id": len(collections) + 1,
        "name": collection.name,
    }
    collections.append(newCollection)
    return newCollection


class ProtoAnalysisResponse(BaseModel):
    result: str


@app.get("/proto/analysis")
def proto_analysis() -> str:
    datasets = [
        "oliviera-car.csv",
        "oliviera-los-far.csv",
        "oliviera-los-near.csv",
        "oliviera-nlos.csv",
        "oliviera-walking.csv",
    ]

    result = ""
    for dataset in datasets:
        result += "\n"
        result += "".join(map(lambda x: str(x), mean_std_quantization(gw[0:100])))
        result += "".join(map(lambda x: str(x), mean_std_quantization(node[0:100])))
        result += "\n"

    return {result: result}
