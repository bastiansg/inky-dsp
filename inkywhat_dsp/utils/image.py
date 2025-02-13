import numpy as np

from PIL import Image
from io import BytesIO
from base64 import b64encode, b64decode

from torchvision.transforms.functional import (
    resize,
    pad,
    rotate,
    # InterpolationMode,
)


def encode_image(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")

    encoded_image = b64encode(buffered.getvalue()).decode()
    return encoded_image


def decode_image(encoded_image: str) -> Image.Image:
    decoded_bytes = b64decode(encoded_image)
    decoded_image = Image.open(BytesIO(decoded_bytes))

    return decoded_image


def get_pad_sizes(pad_size: int) -> tuple[int, int]:
    if pad_size == 0:
        return (0, 0)

    if (pad_size % 2) == 0:
        size = pad_size // 2
        pad_sizes = (size, size)
        return pad_sizes

    size = pad_size // 2
    pad_sizes = (size, size + 1)
    return pad_sizes


def resize_image(
    image: Image.Image,
    size: int,
    max_size: int,
    pad_fill: int = 0,
) -> tuple[bool, Image.Image]:
    w, h = image.size
    orientation = False
    if w < h:
        orientation = True
        image = rotate(img=image, angle=90, expand=True)

    resized_image = resize(
        img=image,
        size=size,
        # interpolation=InterpolationMode.NEAREST,
        # interpolation=InterpolationMode.BILINEAR,
        # interpolation=InterpolationMode.NEAREST_EXACT,
        max_size=max_size,
    )

    rw, rh = resized_image.size
    w_pad_size = max_size - rw
    h_pad_size = size - rh

    # NOTE in case of horizontal padding
    if w_pad_size:
        l_pad, r_pad = get_pad_sizes(w_pad_size)
        resized_image = pad(
            img=resized_image,
            padding=[l_pad, 0, r_pad, 0],
            fill=pad_fill,
        )

        return orientation, resized_image

    # NOTE in case of vertical padding
    if h_pad_size:
        t_pad, b_pad = get_pad_sizes(h_pad_size)
        resized_image = pad(
            img=resized_image,
            padding=[0, t_pad, 0, b_pad],
            fill=pad_fill,
        )

    return orientation, resized_image


def get_inky_image(input_image: Image.Image) -> Image.Image:
    pal_img = Image.new("P", (1, 1))
    # pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)

    return input_image.convert("RGB").quantize(palette=pal_img)


def get_rbw_image(
    image: Image.Image,
    r_thresh: int = 120,
    b_thresh: int = 120,
) -> Image.Image:
    image = image.convert("RGB")
    image_data = np.array(image)

    red, green, blue = (
        image_data[:, :, 0],
        image_data[:, :, 1],
        image_data[:, :, 2],
    )

    mask_r = (red >= r_thresh) & (green < r_thresh) & (blue < r_thresh)
    mask_g = (red < r_thresh) & (green >= r_thresh) & (blue < r_thresh)
    mask_b = (red < r_thresh) & (green < r_thresh) & (blue >= r_thresh)

    mask_black = (red < b_thresh) & (green < b_thresh) & (blue < b_thresh)
    mask_red = (mask_r | mask_g | mask_b) & (~mask_black)

    rbw_image_data = np.full(image_data.shape, [255, 255, 255], dtype=np.uint8)
    rbw_image_data[mask_red] = [255, 0, 0]
    rbw_image_data[mask_black] = [0, 0, 0]

    rbw_image = Image.fromarray(rbw_image_data)
    return rbw_image
