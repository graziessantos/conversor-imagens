# 🖼️ Conversor de Imagens

API REST simples, escrita em **Flask** e **Pillow**, que converte imagens entre formatos (PNG, JPEG, WebP, GIF e BMP). O projeto também serve como exemplo de um pipeline completo de CI/CD: lint, testes, auditoria de dependências, scan de vulnerabilidades da imagem Docker e publicação no GitHub Container Registry (GHCR).

## ✨ Funcionalidades

- Conversão de imagens via upload (`multipart/form-data`)
- Formatos suportados: `png`, `jpg`, `jpeg`, `webp`, `gif`, `bmp`
- Tratamento automático de transparência ao converter para JPEG
- Validação de arquivos inválidos/corrompidos e limite de tamanho de upload
- Endpoint de *health check* com versão e ambiente
- Container Docker rodando com usuário não-root e `HEALTHCHECK`
- Pipeline de CI no GitHub Actions

## 🧱 Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11 |
| Framework web | Flask 3.1 |
| Processamento de imagem | Pillow |
| Servidor de produção | Gunicorn |
| Testes | pytest |
| Lint | Ruff |
| Segurança | pip-audit, Trivy |
| Container | Docker / Docker Compose |
| CI/CD | GitHub Actions + GHCR |

## 📁 Estrutura do projeto

```
conversor-imagens/
├── app/
│   ├── __init__.py        # create_app(): configuração, logging e limite de upload
│   ├── converter.py       # lógica de conversão com Pillow
│   └── routes.py          # endpoints da API
├── tests/
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_api.py        # testes dos endpoints
│   └── test_converter.py  # testes da lógica de conversão
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml     # ambientes de staging e produção
├── requirements.txt
├── requirements-dev.txt
└── run.py                 # ponto de entrada
```

## 🚀 Como executar

### Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/graziessantos/conversor-imagens.git
cd conversor-imagens

# 2. Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie a aplicação
python run.py
```

A API ficará disponível em `http://localhost:8080`.

### Com Docker

```bash
docker build -t conversor-imagens .
docker run -p 8080:8080 conversor-imagens
```

### Com Docker Compose (staging + produção)

O `docker-compose.yml` sobe dois ambientes a partir de imagens publicadas no GHCR. As tags são obrigatórias:

```bash
STAGING_TAG=1.1.0 PROD_TAG=1.0.0 docker compose up -d
```

| Ambiente | Porta | Log level |
|---|---|---|
| staging | `8081` | `INFO` |
| production | `8082` | `WARNING` |

## 📡 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Status da aplicação, versão e ambiente |
| `GET` | `/api/version` | Versão e ambiente atuais |
| `GET` | `/api/formats` | Lista de formatos de saída suportados |
| `POST` | `/api/convert?to=<formato>` | Converte a imagem enviada no campo `file` |

### Exemplos

**Converter uma imagem para WebP:**

```bash
curl -X POST "http://localhost:8080/api/convert?to=webp" \
  -F "file=@foto.png" \
  --output foto.webp
```

**Listar formatos suportados:**

```bash
curl http://localhost:8080/api/formats
# ["bmp","gif","jpeg","jpg","png","webp"]
```

**Health check:**

```bash
curl http://localhost:8080/health
# {"environment":"development","status":"ok","version":"local"}
```

### Respostas de erro

| Status | Situação | Corpo |
|---|---|---|
| `400` | Campo `file` ausente | `{"error": "envie o arquivo no campo 'file'"}` |
| `400` | Formato de destino não suportado | `{"error": "formato não suportado: xyz"}` |
| `400` | Arquivo corrompido ou que não é imagem | `{"error": "arquivo não é uma imagem válida"}` |
| `413` | Arquivo maior que o limite permitido | `{"error": "arquivo grande demais"}` |

## ⚙️ Configuração

A aplicação é configurada por variáveis de ambiente:

| Variável | Padrão | Descrição |
|---|---|---|
| `PORT` | `8080` | Porta em que o servidor escuta |
| `MAX_UPLOAD_MB` | `5` | Tamanho máximo do upload, em MB |
| `LOG_LEVEL` | `INFO` | Nível de log (`DEBUG`, `INFO`, `WARNING`, ...) |
| `APP_VERSION` | `local` | Versão exibida nos endpoints |
| `APP_ENVIRONMENT` | `development` | Nome do ambiente exibido nos endpoints |

## 🧪 Testes e qualidade

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Rodar os testes
pytest -v

# Rodar o lint
ruff check .

# Auditar dependências
pip-audit -r requirements.txt
```

## 🔄 Pipeline de CI/CD

O workflow em `.github/workflows/ci.yml` roda em *push* para `main`, em tags `v*` e em *pull requests*:

1. **Lint**: `ruff check .`
2. **Testes**: `pytest`, com o relatório JUnit salvo como artefato
3. **Segurança**: `pip-audit` nas dependências
4. **Docker**:
   - build da imagem
   - scan de vulnerabilidades críticas com **Trivy**
   - *smoke test* do container em `/health`
   - publicação no **GHCR** (somente fora de pull requests)

### Tags das imagens

| Tag | Quando é gerada |
|---|---|
| `latest` | Push na branch `main` |
| `sha-<commit>` | Todo push |
| `X.Y.Z` | Ao criar uma tag Git `vX.Y.Z` |

## 🔒 Boas práticas de segurança adotadas

- Container executa com **usuário não-root**
- Imagem base `python:3.11-slim`
- Dependências com versões fixas e auditadas
- Limite de tamanho de upload e proteção contra *decompression bombs*
- Scan de vulnerabilidades da imagem no pipeline

## 📄 Licença

Defina aqui a licença do projeto (por exemplo, MIT).
