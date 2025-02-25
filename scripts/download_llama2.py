from huggingface_hub import snapshot_download
from huggingface_hub import login
import os

# 1. Autenticação na Hugging Face Hub
# Substitua 'SEU_TOKEN_AQUI' pelo seu token da Hugging Face
HUGGINGFACE_TOKEN = "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"
login(token=HUGGINGFACE_TOKEN)

# 2. Defina o caminho onde o modelo será salvo
MODEL_DIR = "../data/modelos/Llama-2-13b-chat-hf"
os.makedirs(MODEL_DIR, exist_ok=True)

# 3. Nome do modelo no Hugging Face
MODEL_NAME = "meta-llama/Llama-2-13b-chat-hf"

# 4. Baixar o modelo
print(f"Baixando o modelo {MODEL_NAME}...")
snapshot_download(
    repo_id=MODEL_NAME,
    cache_dir=MODEL_DIR,
    ignore_patterns=["*.bin", "*.safetensors"],  # Ignora arquivos grandes (opcional)
    local_dir=MODEL_DIR,
    local_dir_use_symlinks=False,
    resume_download=True,
)

print(f"Modelo baixado e salvo em: {MODEL_DIR}")