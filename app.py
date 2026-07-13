import sys, asyncio
from pathlib import Path
import uvicorn
from fastapi import FastAPI
import gradio as gr

sys.path.insert(0, str(Path(__file__).parent))

from ui import create_app  # noqa: E402, F811

app, css, nav_js = create_app()

fastapi_app = FastAPI()

# Mount the Gradio blocks application onto FastAPI root
mounted = gr.mount_gradio_app(
    app=fastapi_app,
    blocks=app,
    path="",
    css=css,
    head=nav_js,
    theme="soft"
)


from ui.routing import get_route_by_path


class SPAWrapper:
    """Wraps the ASGI app to rewrite frontend SPA routes to "/" for deep-link support."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["method"] == "GET":
            path = scope["path"]
            if get_route_by_path(path) is not None:
                scope["path"] = "/"
                if "raw_path" in scope:
                    scope["raw_path"] = b"/"

        await self.app(scope, receive, send)


if __name__ == "__main__":
    spa_app = SPAWrapper(fastapi_app)
    uvicorn.run(spa_app, host="0.0.0.0", port=8501)