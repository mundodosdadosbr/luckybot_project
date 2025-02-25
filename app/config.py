import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da WhatsApp Business API
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")  # Token de acesso da API
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")    # ID do número de telefone do WhatsApp
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")  # Token de verificação do webhook

# Configurações do modelo LLaMA 2
LLAMA2_MODEL_PATH = os.getenv("LLAMA2_MODEL_PATH")    # Caminho para o modelo LLaMA 2

# Configurações do servidor
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")     # Host do servidor Flask
SERVER_PORT = os.getenv("SERVER_PORT", "5000")        # Porta do servidor Flask

# Configurações de logging
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Cria o diretório de logs se não existir
LOG_FILE = os.path.join(LOG_DIR, "luckybot.log")