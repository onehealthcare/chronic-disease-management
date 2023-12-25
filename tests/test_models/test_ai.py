import os

import pytest
import requests
from libs.azure_vision.dto import Metadata, ReadResult, Result
from models.ai import img_data_ocr, img_ocr
from models.init_db import azure_vision


mocked_result: Result = Result(
    readResult=ReadResult(
        content="test",
        stringIndexType="",
        pages=[],
        styles=[],
        modelVersion=""
    ),
    modelVersion="",
    metadata=Metadata(
        width=0,
        height=0
    ),
)


@pytest.fixture
def azure_vision_mock():
    def _azure_vision_mock():
        return mocked_result
    setattr(azure_vision, 'analyze_read_from_img_url', _azure_vision_mock)
    setattr(azure_vision, 'analyze_read_by_img_data', _azure_vision_mock)


def test_img_ocr(azure_vision_mock):
    img_url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
    img_path = "test.png"

    with pytest.raises(ValueError):
        img_ocr("")

    with pytest.raises(ValueError):
        img_ocr(mocked_result)

    with pytest.raises(ValueError):
        img_ocr("https://baidu.com")

    with pytest.raises(FileExistsError):
        img_ocr(img_path)

    r = requests.get(img_url)
    with open(img_path, 'wb') as f:
        f.write(r.content)

    assert img_ocr(img_url) == mocked_result.readResult.content
    assert img_ocr(img_path) == mocked_result.readResult.content

    with pytest.raises(ValueError):
        img_data_ocr("")

    with pytest.raises(ValueError):
        img_data_ocr(img_path)

    with open(img_path, 'rb') as f:
        assert img_data_ocr(f.read()) == mocked_result.readResult.content

    os.remove(img_path)
