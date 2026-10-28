import io

from PIL import Image, UnidentifiedImageError

# formato pedido -> (nome interno do Pillow, tipo MIME da resposta)
FORMATS = {
    "png": ("PNG", "image/png"),
    "jpg": ("JPEG", "image/jpeg"),
    "jpeg": ("JPEG", "image/jpeg"),
    "webp": ("WEBP", "image/webp"),
    "gif": ("GIF", "image/gif"),
    "bmp": ("BMP", "image/bmp"),
}


class ConversionError(Exception):
    """Erro de entrada do usuário (formato ou arquivo inválido)."""


def convert_image(data: bytes, target: str) -> tuple[bytes, str]:
    target = target.lower()
    if target not in FORMATS:
        raise ConversionError(f"formato não suportado: {target}")
    pil_format, mime = FORMATS[target]

    try:
        img = Image.open(io.BytesIO(data))
        img.load()  # força a leitura completa: pega arquivos corrompidos
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ConversionError("arquivo não é uma imagem válida") from exc

    # JPEG não tem transparência: converte antes de salvar
    #if pil_format == "JPEG" and img.mode in ("RGBA", "LA", "P"):
     #   img = img.convert("RGB")

    out = io.BytesIO()
    img.save(out, format=pil_format)
    return out.getvalue(), mime

