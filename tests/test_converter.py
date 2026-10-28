import io

import pytest
from PIL import Image

from app.converter import ConversionError, convert_image
from tests.helpers import make_png


def test_png_para_webp():
    data, mime = convert_image(make_png(), "webp")
    assert mime == "image/webp"
    assert Image.open(io.BytesIO(data)).format == "WEBP"


def test_png_com_transparencia_para_jpg():
    data, mime = convert_image(make_png("RGBA"), "jpg")
    assert mime == "image/jpeg"
    assert Image.open(io.BytesIO(data)).format == "JPEG"


def test_formato_em_maiusculas_e_aceito():
    _, mime = convert_image(make_png(), "PNG")
    assert mime == "image/png"


def test_formato_nao_suportado():
    with pytest.raises(ConversionError):
        convert_image(make_png(), "xyz")


def test_arquivo_corrompido():
    with pytest.raises(ConversionError):
        convert_image(b"isso nao e uma imagem", "png")