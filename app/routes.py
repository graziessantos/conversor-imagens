import logging

from flask import Blueprint, Response, jsonify, request

from .converter import FORMATS, ConversionError, convert_image

bp = Blueprint("main", __name__)
log = logging.getLogger(__name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/api/formats")
def formats():
    return jsonify(sorted(FORMATS))


@bp.post("/api/convert")
def convert():
    target = request.args.get("to", "")
    upload = request.files.get("file")
    if upload is None:
        return jsonify({"error": "envie o arquivo no campo 'file'"}), 400
    try:
        data, mime = convert_image(upload.read(), target)
    except ConversionError as exc:
        log.warning("conversão recusada: %s", exc)
        return jsonify({"error": str(exc)}), 400
    log.info("convertido para %s (%d bytes)", target, len(data))
    return Response(data, mimetype=mime)