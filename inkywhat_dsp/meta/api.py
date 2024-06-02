from pydantic import BaseModel, StrictStr, StrictInt


class SetImageInput(BaseModel):
    image: StrictStr


class SetImageOutput(BaseModel):
    orientation: StrictInt
