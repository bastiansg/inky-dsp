import inky

from inky.auto import auto

from PIL import Image
from common.logger import get_logger
from tempfile import NamedTemporaryFile

from inky_dsp.utils.image import resize_image


logger = get_logger(__name__)


display = auto()
width, height = display.resolution  # type: ignore


def display_image(file_item: dict) -> None:
    with NamedTemporaryFile(
        prefix=file_item["file_name"],
        suffix=file_item["content_type"].split("/")[-1],
    ) as tmp_file:
        tmp_file.write(file_item["content"])
        tmp_file.seek(0)

        image = Image.open(tmp_file.name)
        is_portrait, resized_image = resize_image(
            image=image,
            size=height,
            max_size=width,
        )

        logger.info(f"is_portrait => {is_portrait}")

        display.set_image(resized_image)
        display.set_border(inky.BLACK)
        display.show()
