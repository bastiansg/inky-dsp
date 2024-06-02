from PIL import Image
from openai import OpenAI

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
        self.base_propmt = load_yaml(
            file_path="/resources/generation/prompts/base.yaml"
        )["text"]

        logger.info(f"base_propmt => {self.base_propmt}")

    def generate(self, prompt: str) -> Image.Image:
        prompt = self.base_propmt.format(object_description=prompt)
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
