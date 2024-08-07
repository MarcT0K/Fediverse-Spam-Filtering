from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
import uvicorn

from fedispam.config import PORT
from fedispam.filter import SpamFilter

filtering_model = SpamFilter()


async def filter_spam(request: Request):
    """Predicts whether a message is a spam or not.

    Request body: {"id": message_ID, "content": message_content}
    """
    data = await request.json()
    if "id" not in data or "content" not in data:
        return JSONResponse({"error": "Invalid data format"}, status_code=400)

    decision = await filtering_model.predict(data)
    return JSONResponse({"id": data["id"], "decision": decision})


async def get_outliers(_request):
    """Returns the list of outliers identified spam filtering (waiting for a manual decision)."""
    return JSONResponse(await filtering_model.get_all_outliers())


async def classify_outliers(request):
    """Receives manual decisions for previously identified outliers.

    Request body: [[outliar_ID_1, decision_1], ...]
    """
    data = await request.json()
    try:
        await filtering_model.outliar_manual_confirmation(data)
    except TypeError:
        return JSONResponse(
            {"success": False, "error": "Invalid data format"}, status_code=400
        )

    return JSONResponse({"success": True})


async def random_check_confirmation_get(_request):
    """Returns a list of randomly selected messages requiring a manual check."""
    return JSONResponse(await filtering_model.get_all_random_checks())


async def random_check_confirmation_post(request):
    """Receives manual decisions for randomly selected messages.

    Request body: [[message_ID_1, decision_1], ...]
    """
    data = await request.json()
    try:
        await filtering_model.random_check_manual_confirmation(data)
    except TypeError:
        return JSONResponse(
            {"success": False, "error": "Invalid data format"}, status_code=400
        )

    return JSONResponse({"success": True})


async def model_import(request):
    """Import model parameters"""
    data = await request.json()
    if "model" not in data:
        return JSONResponse(
            {"success": False, "error": "Model is missing"}, status_code=400
        )

    await filtering_model.import_model(data["model"])
    return JSONResponse({"success": True})


async def model_export(_request):
    """Export model parameters"""
    return JSONResponse(filtering_model.export_model())


async def training_data_import(request):
    """Update the model based on imported data

    Request body: [[message_content_1, message_type_1], ...]
    """
    data = await request.json()
    try:
        await filtering_model.add_training_data(data)
    except TypeError:
        return JSONResponse(
            {"success": False, "error": "Invalid data format"}, status_code=400
        )

    return JSONResponse({"success": True})


routes = [
    Route("/filter", filter_spam, methods=["POST"]),
    Route("/outliers", get_outliers, methods=["GET"]),
    Route("/outliers/classify", classify_outliers, methods=["POST"]),
    Route("/random_check/", random_check_confirmation_get, methods=["GET"]),
    Route("/random_check/", random_check_confirmation_post, methods=["POST"]),
    Route("/model/import", model_import, methods=["POST"]),
    Route("/model/export", model_export, methods=["GET"]),
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
