import time

from inky import InkyWHAT

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from inkywhat_dsp.logger import get_logger
from inkywhat_dsp.utils.image import decode_image
from inkywhat_dsp.meta import SetImageInput, SetImageOutput
from inkywhat_dsp.utils.image import resize_image, get_inky_image


dsp = InkyWHAT(colour="red")
logger = get_logger(__name__)

app = FastAPI()
app.add_middleware(CORSMiddleware)
app.get("/", include_in_schema=False)(lambda: RedirectResponse(url="/docs/"))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    process_time = int((time.time() - start_time) * 1000)
    response.headers["X-Process-Time"] = f"{process_time}ms"

    return response


@app.post("/set_image/")
async def set_image(set_image_input: SetImageInput) -> SetImageOutput:
    image = decode_image(set_image_input.image)
    orientation, resized_image = resize_image(image, size=300, max_size=400)
    inky_image = get_inky_image(input_image=resized_image)

    dsp.set_image(inky_image)
    dsp.show()

    set_image_output = SetImageOutput(orientation=orientation)
    return set_image_output
