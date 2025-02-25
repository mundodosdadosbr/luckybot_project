from flask import Flask
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar a aplicação Flask
def create_app():
    app = Flask(__name__)

    # Configurações do Flask
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "uma_chave_secreta_padrao")
    app.config["TWILIO_ACCOUNT_SID"] = os.getenv("TWILIO_ACCOUNT_SID")
    app.config["TWILIO_AUTH_TOKEN"] = os.getenv("TWILIO_AUTH_TOKEN")
    app.config["WHATSAPP_NUMBER"] = os.getenv("WHATSAPP_NUMBER")
    app.config["LLAMA2_MODEL_PATH"] = os.getenv("LLAMA2_MODEL_PATH")

    # Registrar blueprints (rotas)
    from .webhook import webhook_bp
    app.register_blueprint(webhook_bp)

    # Configurar logging (opcional)
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        # Criar diretório de logs se não existir
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/logs")
        os.makedirs(log_dir, exist_ok=True)

        # Configurar o handler de arquivo de log
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "luckybot.log"),
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