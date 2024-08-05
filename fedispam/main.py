from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn


async def homepage(request):
    return JSONResponse({"hello": "world"})


routes = [
    Route("/", homepage),
]


app = Starlette(debug=True, routes=routes)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
