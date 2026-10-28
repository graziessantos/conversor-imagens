import io

from PIL import Image


def make_png(mode="RGB", size=(10, 10)) -> bytes:
    """Gera uma imagem PNG pequena em memória."""
    buf = io.BytesIO()
    Image.new(mode, size, "red").save(buf, format="PNG")
    return buf.getvalue()