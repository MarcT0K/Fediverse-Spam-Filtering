from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
import uvicorn

from fedispam.config import PORT
from fedispam.filter import SpamFilter

filtering_model = SpamFilter()


async def filter_spam(request: Request):
    data = await request.json()
    if "id" not in data or "content" not in data:
        return JSONResponse({"error": "Invalid data format"}, status_code=400)

    decision = await filtering_model.predict(data)
    return JSONResponse({"id": data["id"], "decision": decision})


async def get_outliars(_request):
    return JSONResponse(await filtering_model.get_all_outliars())


async def classify_outliars(request):
    return JSONResponse({"hello": "world"})  # TODO


async def random_check_confirmation_get(_request):
    return JSONResponse(await filtering_model.get_all_random_checks())


async def random_check_confirmation_post(request):
    return JSONResponse({"hello": "world"})  # TODO


async def model_import(request):
    data = await request.json()
    if "model" not in data:
        return JSONResponse(
            {"success": False, "error": "Model is missing"}, status_code=400
        )

    await filtering_model.import_model(data["model"])
    return JSONResponse({"success": True})


async def model_export(_request):
    return JSONResponse(filtering_model.export_model())


async def training_data_import(request):
    return JSONResponse({"hello": "world"})  # TODO


routes = [
    Route("/filter", filter_spam, methods=["POST"]),
    Route("/outliars", get_outliars, methods=["GET"]),
    Route("/outliars/classify", classify_outliars, methods=["POST"]),
    Route("/random_check/", random_check_confirmation_get, methods=["GET"]),
    Route("/random_check/", random_check_confirmation_post, methods=["POST"]),
    Route("/model/import", model_import, methods=["GET"]),
    Route("/training_data/import", training_data_import, methods=["POST"]),
]

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[filtering_model.start],
    on_shutdown=[filtering_model.stop],
)


def main():
    uvicorn.run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
