from pydantic import BaseModel, StrictStr
from fastapi import APIRouter, UploadFile, HTTPException

from common.logger import get_logger
from inky_dsp.pipelines import display_image_from_file, FileItem


logger = get_logger(__name__)


VALID_FILE_FORMATS = {
    "image/jpeg",
    "image/png",
}


display_image_router = APIRouter()


class DisplayImageOutput(BaseModel):
    status: StrictStr


@display_image_router.post("/inky_dsp/display_image/", tags=["display"])
async def diplay_image(file: UploadFile) -> DisplayImageOutput:
    content_type = file.content_type
    if content_type not in VALID_FILE_FORMATS:
        raise HTTPException(
            status_code=500,
            detail=(
                f"Invalid content type: {content_type}.",
                f"Valid types are: {list(VALID_FILE_FORMATS)}",
            ),
        )

    file_name = file.filename
    assert file_name is not None

    display_image_from_file(
        file_item=FileItem(
            file_name=file_name,
            content_type=content_type,
            content=file.file.read(),
        )
    )

    return DisplayImageOutput(status="ok")
