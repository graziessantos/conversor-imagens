import io

from app import create_app
from tests.helpers import make_png


def enviar(client, conteudo, destino):
    return client.post(
        f"/api/convert?to={destino}",
        data={"file": (io.BytesIO(conteudo), "arquivo")},
        content_type="multipart/form-data",
    )


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"


def test_formats_lista_png(client):
    assert "png" in client.get("/api/formats").json


def test_convert_sucesso(client):
    r = enviar(client, make_png(), "webp")
    assert r.status_code == 200
    assert r.mimetype == "image/webp"


def test_convert_sem_arquivo_400(client):
    assert client.post("/api/convert?to=png").status_code == 400


def test_convert_formato_invalido_400(client):
    assert enviar(client, make_png(), "xyz").status_code == 400


def test_convert_arquivo_corrompido_400(client):
    assert enviar(client, b"lixo", "png").status_code == 400


def test_convert_arquivo_grande_413():
    app = create_app()
    app.config["MAX_CONTENT_LENGTH"] = 1000
    r = enviar(app.test_client(), b"x" * 5000, "png")
    assert r.status_code == 413