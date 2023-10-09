from fastapi import FastAPI

from inkywhat_dsp.meta import EncodedImage
from inkywhat_dsp.logger import get_logger
from inkywhat_dsp.utils.image import decode_image


logger = get_logger(__name__)

app = FastAPI()


@app.post("/set_image/")
async def set_image(encoded_image: EncodedImage):
    image = decode_image(EncodedImage.encoded_image)
