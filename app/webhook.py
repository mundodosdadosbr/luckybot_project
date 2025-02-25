from flask import Blueprint, request, jsonify
import requests
import hashlib
import hmac
import os
from app.llm_handler import gerar_resposta
from app.payment_processor import processar_arquivo, validar_comprovante
from app.utils import download_file, salvar_log

webhook_bp = Blueprint('webhook', __name__)

# Configurações da API do WhatsApp
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
API_URL = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"

# Verificação do Webhook (GET)
@webhook_bp.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return challenge, 200
    return "Verificação falhou", 403

# Receber Mensagens (POST)
@webhook_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()
    salvar_log(f"Dados recebidos: {data}")

    # Processar mensagem
    if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_number = message["from"]
        message_type = message["type"]

        if message_type == "text":
            resposta = gerar_resposta(message["text"]["body"])
        elif message_type == "image" or message_type == "document":
            media_id = message["image"]["id"] if message_type == "image" else message["document"]["id"]
            media_url = get_media_url(media_id)
            file_path = download_file(media_url)
            texto_extraido = processar_arquivo(file_path)
            resposta = validar_comprovante(texto_extraido)
        else:
            resposta = "Formato não suportado."

        # Enviar resposta
        send_message(user_number, resposta)

    return jsonify({"status": "success"}), 200

def get_media_url(media_id):
    response = requests.get(
        f"https://graph.facebook.com/v19.0/{media_id}",
        headers={"Authorization": f"Bearer {WHATSAPP_API_TOKEN}"}
    )
    return response.json().get("url")

def send_message(user_number, text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": user_number,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    salvar_log(f"Resposta enviada: {response.json()}")