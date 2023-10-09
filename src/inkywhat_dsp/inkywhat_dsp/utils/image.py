from PIL import Image
from io import BytesIO
from torchvision.transforms.functional import resize, pad, rotate

from .text import b64_encode, b64_decode


def encode_image(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")

    encoded_image = b64_encode(buffered.getvalue()).decode()
    return encoded_image


def decode_image(encoded_image: str) -> Image.Image:
    decoded_bytes = b64_decode(encoded_image)
    decoded_image = Image.open(BytesIO(decoded_bytes))

    return decoded_image


def resize_image(image: Image.Image, size: int, max_size: int):
    w, h = image.size
    if w < h:
        image = rotate(img=image, angle=90, expand=True)

    resized_image = resize(
        img=image,
        size=size,
        max_size=max_size,
    )

    w_, h_ = resized_image.size
    w_diff = max_size - w_
    h_diff = size - h_

    if w_diff:
        resized_image = pad(
            img=resized_image,
            padding=[w_diff // 2, 0],
        )

    if h_diff:
        resized_image = pad(
            img=resized_image,
            padding=[0, h_diff // 2],
        )

    resized_image = resize(
        img=resized_image,
        size=(size, max_size),
    )

    return resized_image


def get_inky_image(input_image: Image.Image) -> Image.Image:
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    inky_image = input_image.convert("RGB").quantize(palette=pal_img)
    return inky_image
