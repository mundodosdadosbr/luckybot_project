import pytest
from flask import Flask
from app.webhook import webhook_bp
from app.utils import salvar_log
from app.config import LLAMA2_MODEL_PATH, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, WHATSAPP_NUMBER
import os

# Configuração do Flask para testes
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["TWILIO_ACCOUNT_SID"] = TWILIO_ACCOUNT_SID
    app.config["TWILIO_AUTH_TOKEN"] = TWILIO_AUTH_TOKEN
    app.config["WHATSAPP_NUMBER"] = WHATSAPP_NUMBER
    app.config["LLAMA2_MODEL_PATH"] = LLAMA2_MODEL_PATH
    app.register_blueprint(webhook_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_webhook_mensagem_texto(client):
    """
    Testa o webhook com uma mensagem de texto.
    """
    # Simula uma mensagem de texto enviada pelo WhatsApp
    data = {
        "Body": "Como posso participar da rifa?",
        "From": "whatsapp:+5511999999999",
    }

    # Faz uma requisição POST para o webhook
    response = client.post("/webhook", data=data)

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert b"Resposta gerada para o prompt" in salvar_log.calls  # Verifica se o log foi registrado

def test_webhook_comprovante_imagem(client):
    """
    Testa o webhook com um comprovante de pagamento (imagem).
    """
    # Simula uma mensagem com uma imagem enviada pelo WhatsApp
    data = {
        "MediaUrl0": "https://exemplo.com/comprovante.jpg",
        "From": "whatsapp:+5511999999999",
    }

    # Faz uma requisição POST para o webhook
    response = client.post("/webhook", data=data)

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert b"Texto extraído:" in salvar_log.calls  # Verifica se o log foi registrado

def test_webhook_comprovante_pdf(client):
    """
    Testa o webhook com um comprovante de pagamento (PDF).
    """
    # Simula uma mensagem com um PDF enviado pelo WhatsApp
    data = {
        "MediaUrl0": "https://exemplo.com/comprovante.pdf",
        "From": "whatsapp:+5511999999999",
    }

    # Faz uma requisição POST para o webhook
    response = client.post("/webhook", data=data)

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert b"Texto extraído:" in salvar_log.calls  # Verifica se o log foi registrado

def test_webhook_erro_processamento(client):
    """
    Testa o webhook com um erro no processamento do comprovante.
    """
    # Simula uma mensagem com uma URL inválida
    data = {
        "MediaUrl0": "https://exemplo.com/arquivo_invalido.txt",
        "From": "whatsapp:+5511999999999",
    }

    # Faz uma requisição POST para o webhook
    response = client.post("/webhook", data=data)

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert b"Erro ao processar o arquivo" in salvar_log.calls  # Verifica se o log foi registrado