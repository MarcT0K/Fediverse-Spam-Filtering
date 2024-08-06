from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

from fedispam.config import PORT


async def filter_spam(request):
    return JSONResponse({"hello": "world"})


async def get_outliars(request):
    return JSONResponse({"hello": "world"})


async def classify_outliars(request):
    return JSONResponse({"hello": "world"})


async def filter_confirmation_get(request):
    return JSONResponse({"hello": "world"})


async def filter_confirmation_post(request):
    return JSONResponse({"hello": "world"})


async def model_import(request):
    return JSONResponse({"hello": "world"})


async def model_export(request):
    return JSONResponse({"hello": "world"})


async def training_data_import(request):
    return JSONResponse({"hello": "world"})


def start(): ...


def stop(): ...


routes = [
    Route("/filter", filter_spam, methods=["POST"]),
    Route("/outliars", get_outliars, methods=["GET"]),
    Route("/outliars/classify", classify_outliars, methods=["POST"]),
    Route("/filter/confirmations", filter_confirmation_get, methods=["GET"]),
    Route("/filter/confirmations", filter_confirmation_post, methods=["POST"]),
    Route("/model/import", model_import, methods=["GET"]),
    Route("/training_data/import", training_data_import, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes, on_startup=[start], on_shutdown=[stop])


def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
