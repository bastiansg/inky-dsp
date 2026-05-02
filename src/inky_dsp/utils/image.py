from PIL import Image
from torchvision.transforms.functional import (
    resize,
    pad,
    rotate,
    # InterpolationMode,
)


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
    is_portrait = False
    if w < h:
        is_portrait = True
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

        return is_portrait, resized_image

    # NOTE in case of vertical padding
    if h_pad_size:
        t_pad, b_pad = get_pad_sizes(h_pad_size)
        resized_image = pad(
            img=resized_image,
            padding=[0, t_pad, 0, b_pad],
            fill=pad_fill,
        )

    return is_portrait, resized_image
