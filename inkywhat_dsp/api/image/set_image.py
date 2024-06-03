from inky import InkyWHAT
from fastapi import APIRouter

from inkywhat_dsp.utils.image import decode_image
from inkywhat_dsp.meta import SetImageInput, SetImageOutput


dsp = InkyWHAT(colour="red")
set_image_router = APIRouter()


@set_image_router.post("/set_image/")
async def set_image(set_image_input: SetImageInput) -> SetImageOutput:
    inky_image = decode_image(set_image_input.inky_image)
    dsp.set_image(inky_image)
    dsp.show()

    set_image_output = SetImageOutput(orientation=set_image_input.orientation)
    return set_image_output
