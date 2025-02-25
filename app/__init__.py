from flask import Flask
from dotenv import load_dotenv
import os
from app.config import WHATSAPP_API_TOKEN, WHATSAPP_PHONE_ID, LLAMA2_MODEL_PATH, LOG_DIR

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar a aplicação Flask
def create_app():
    app = Flask(__name__)

    # Configurações do Flask
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "uma_chave_secreta_padrao")
    app.config["WHATSAPP_API_TOKEN"] = WHATSAPP_API_TOKEN
    app.config["WHATSAPP_PHONE_ID"] = WHATSAPP_PHONE_ID
    app.config["LLAMA2_MODEL_PATH"] = LLAMA2_MODEL_PATH

    # Registrar blueprints (rotas)
    from .webhook import webhook_bp
    app.register_blueprint(webhook_bp)

    # Configurar logging (opcional)
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        # Criar diretório de logs se não existir
        os.makedirs(LOG_DIR, exist_ok=True)

        # Configurar o handler de arquivo de log
        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, "luckybot.log"),
            maxBytes=1024 * 1024,  # 1 MB
            backupCount=10,
        )
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Inicializando LuckyBot...")

    return app

# Inicializar a aplicação
app = create_app()