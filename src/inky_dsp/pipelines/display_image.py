import inky

from inky.auto import auto
from rich.console import Console
from pydantic import BaseModel, StrictStr, StrictBytes

from PIL import Image
from tempfile import NamedTemporaryFile

from inky_dsp.utils.image import resize_image


console = Console()


display = auto()
width, height = display.resolution


class FileItem(BaseModel):
    file_name: StrictStr
    content_type: StrictStr
    content: StrictBytes


def display_image(file_path: str) -> None:
    image = Image.open(file_path)
    is_portrait, resized_image = resize_image(
        image=image,
        size=height,
        max_size=width,
    )

    console.log(f"is_portrait => {is_portrait}")
    display.set_image(resized_image)
    display.set_border(inky.BLACK)
    display.show()


def display_image_from_file(file_item: FileItem) -> None:
    with NamedTemporaryFile(
        prefix=file_item.file_name,
        suffix=file_item.content_type.split("/")[-1],
    ) as tmp_file:
        tmp_file.write(file_item.content)
        tmp_file.seek(0)

        display_image(file_path=tmp_file.name)
