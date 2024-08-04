from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile
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


class Dataset(BaseModel):
    filename: str


class Collection(BaseModel):
    id: int
    name: str
    datasets: list[Dataset]


# TODO: use a database
collections: list[Collection] = []
collections.append(
    {"id": 1, "name": "Collection A", "datasets": [{"filename": "oliviera-car.csv"}]}
)  # type: ignore
collections.append({"id": 2, "name": "Collection B", "datasets": []})  # type: ignore


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
        "datasets": [],
    }  # type: ignore

    collections.append(newCollection)
    return newCollection


class ProtoAnalysisResponse(BaseModel):
    result: str


@app.post("/collections/{collection_id}/datasets")
def upload_datasets(collection_id: int, files: list[UploadFile]):
    collection = next(filter(lambda c: c["id"] == collection_id, collections), None)

    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found.")

    datasets = Path("datasets")
    for file in files:
        if file.filename is None:
            raise HTTPException(status_code=400, detail="File without filename.")

        if datasets.joinpath(file.filename).exists():
            raise HTTPException(
                status_code=409,
                detail=f"Dataset with name '{file.filename}' already exists.",
            )

        # TODO: validate the format of the dataset

    for dataset in files:
        filename = dataset.filename
        assert filename is not None
        with open(datasets.joinpath(filename), "wb") as file:
            content = dataset.file.read()
            file.write(content)

    datasets = [{"filename": file.filename} for file in files]
    collection["datasets"].extend(datasets)

    return {"message": "Files processed sucessfully."}


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
