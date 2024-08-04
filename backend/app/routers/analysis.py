from fastapi import APIRouter

from app.services.analysis import mean_std_quantization


router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/prototype")
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
