from pydantic import BaseModel, StrictStr


class EncodedImage(BaseModel):
    encoded_image: StrictStr
