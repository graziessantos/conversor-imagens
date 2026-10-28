import logging
import os

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    # limite do upload: 5 MB por padrão, configurável por variável de ambiente
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024

    from .routes import bp

    app.register_blueprint(bp)

    @app.errorhandler(413)
    def too_large(_):
        return jsonify({"error": "arquivo grande demais"}), 413

    return app