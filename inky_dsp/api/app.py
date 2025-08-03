from fastapi import FastAPI

from .routers.display_image import display_image_router


app = FastAPI()
app.include_router(display_image_router)
