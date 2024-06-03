import importlib.resources as pkg_resources

from PIL import Image
from openai import OpenAI
from pathlib import PosixPath

from inkywhat_dsp import data
from inkywhat_dsp.logger import get_logger
from inkywhat_dsp.utils.image import decode_image
from inkywhat_dsp.utils.yaml_data import load_yaml


logger = get_logger(__name__)


class DalleGenerator:
    def __init__(
        self,
        quality: str = "standard",
        size: str = "1024x1024",
        style: str = "vivid",
    ):
        self.quality = quality
        self.size = size
        self.style = style

        self.openai_client = OpenAI()
        self.base_prompt_path = load_yaml(
            file_path=self._parse_base_prompt_path(
                base_prompt_path="dalle/image-generation.yaml"
            )
        )["base-prompt"]

    def _parse_base_prompt_path(self, base_prompt_path: str) -> PosixPath:
        return pkg_resources.files(data).joinpath(base_prompt_path)

    def generate(self, image_description: str) -> Image.Image:
        prompt = self.base_prompt_path.format(
            image_description=image_description
        )

        logger.info(f"prompt => {prompt}")
        response = self.openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality=self.quality,
            size=self.size,
            response_format="b64_json",
            style=self.style,
            n=1,
            timeout=30,
        )

        encoded_image = response.model_dump()["data"][0]["b64_json"]
        decoded_image = decode_image(encoded_image)

        return decoded_image
