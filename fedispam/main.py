import logging

from socketify import App


logger = logging.getLogger("FediSpam")
app = App()
router = app.router()


@router.get("/")
def hello_world(res, req):
    """Simple hello world response"""
    return res.end("Hello, World!")


@router.post("/echo")
def echo(res, req):
    """Echoes the request body back"""
    data = req.body
    return res.end(data)


def main():
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    app.listen(
        3000,
        lambda config: logger.info(
            "Listening on port http://localhost:%d now", config.port
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
