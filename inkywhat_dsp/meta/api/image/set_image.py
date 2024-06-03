from pydantic import BaseModel, StrictStr, StrictBool


class SetImageInput(BaseModel):
    inky_image: StrictStr
    orientation: StrictBool


class SetImageOutput(BaseModel):
    orientation: StrictBool
