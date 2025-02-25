from flask import Blueprint, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app.llm_handler import gerar_resposta
from app.payment_processor import processar_arquivo, validar_comprovante
from app.utils import download_file, salvar_log
import os

# Criação do Blueprint para o webhook
webhook_bp = Blueprint('webhook', __name__)

# Rota para receber mensagens do WhatsApp
@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    # Inicializa a resposta do Twilio
    response = MessagingResponse()

    # Obtém a mensagem recebida
    incoming_msg = request.form.get("Body", "").strip().lower()
    media_url = request.form.get("MediaUrl0")  # URL da mídia (imagem ou PDF)

    # Log da mensagem recebida
    salvar_log(f"Mensagem recebida: {incoming_msg}")

    # Verifica se a mensagem contém uma mídia (comprovante)
    if media_url:
        try:
            # Baixa o arquivo
            file_extension = media_url.split(".")[-1]
            file_path = os.path.join("data", "comprovantes", f"comprovante.{file_extension}")
            download_file(media_url, file_path)

            # Processa o comprovante
            texto_extraido = processar_arquivo(file_path)
            if texto_extraido:
                resposta = validar_comprovante(texto_extraido)
            else:
                resposta = "Não foi possível ler o comprovante. Envie uma imagem ou PDF mais nítido."
        except Exception as e:
            salvar_log(f"Erro ao processar comprovante: {e}")
            resposta = "Ocorreu um erro ao processar o comprovante. Tente novamente."
    else:
        # Gera uma resposta usando o modelo LLaMA 2
        try:
            resposta = gerar_resposta(incoming_msg)
        except Exception as e:
            salvar_log(f"Erro ao gerar resposta: {e}")
            resposta = "Desculpe, ocorreu um erro ao processar sua mensagem."

    # Adiciona a resposta ao Twilio
    response.message(resposta)

    # Log da resposta enviada
    salvar_log(f"Resposta enviada: {resposta}")

    # Retorna a resposta no formato XML (exigido pelo Twilio)
    return str(response)