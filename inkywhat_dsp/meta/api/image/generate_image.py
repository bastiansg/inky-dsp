from pydantic import BaseModel, StrictStr, StrictBool, Field


class GenerateImageInput(BaseModel):
    image_description: StrictStr = Field(examples=["a cute dog"])


class GenerateImageOutput(BaseModel):
    orientation: StrictBool
