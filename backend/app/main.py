from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.services.analysis import mean_std_quantization
from .routers import collections

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(collections.router)


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
