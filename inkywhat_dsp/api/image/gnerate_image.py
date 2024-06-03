from inky import InkyWHAT
from fastapi import APIRouter

from inkywhat_dsp.image_generation import DalleGenerator
from inkywhat_dsp.meta import GenerateImageInput, GenerateImageOutput
from inkywhat_dsp.utils.image import (
    get_rbw_image,
    resize_image,
    get_inky_image,
)


dsp = InkyWHAT(colour="red")
dalle_generator = DalleGenerator()
generate_image_router = APIRouter()


@generate_image_router.post("/generate_image/")
async def generate_image(
    generate_image_input: GenerateImageInput,
) -> GenerateImageOutput:

    generated_image = dalle_generator.generate(
        image_description=generate_image_input.image_description
    )

    rbw_image = get_rbw_image(image=generated_image)
    orientation, resized_image = resize_image(
        rbw_image,
        size=300,
        max_size=400,
    )

    inky_image = get_inky_image(resized_image)
    dsp.set_image(inky_image)
    dsp.show()

    return GenerateImageOutput(orientation=orientation)
