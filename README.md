# LuckyBot - Agente LLM para Rifas no WhatsApp

O **LuckyBot** é um agente de inteligência artificial que auxilia na gestão de grupos de rifas no WhatsApp. Ele utiliza o modelo de linguagem **LLaMA 2** para responder a perguntas, processar comprovantes de pagamento e automatizar tarefas relacionadas a rifas. Este projeto foi desenvolvido para rodar em um servidor Ubuntu e pode ser integrado à **API do WhatsApp Business** (WhatsApp Cloud API).

---

## Funcionalidades

- **Respostas Automáticas**: Responde a perguntas frequentes sobre as rifas.
- **Processamento de Comprovantes**: Extrai informações de comprovantes de pagamento (imagens ou PDFs) usando OCR.
- **Validação de Comprovantes**: Valida informações como valor, data e nome do pagador.
- **Integração com WhatsApp**: Recebe e envia mensagens via **WhatsApp Business API**.

---

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python 3.8 ou superior**
- **Tesseract OCR** (para processamento de comprovantes)
- **Conta no Meta for Developers** (para acessar a WhatsApp Business API)
- **Acesso ao modelo LLaMA 2** (solicite acesso em [Hugging Face](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf))

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/luckybot-project.git
   cd luckybot-project
   ```
   
   
2. **Crie um ambiente virtual e ative-o:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    
3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Configure as variáveis de ambiente:** 
     - Crie um arquivo **.env** na raiz do projeto e adicione as seguintes variáveis:
     ```text
     # WhatsApp Business API
    WHATSAPP_API_TOKEN=seu_token_aqui
    WHATSAPP_PHONE_ID=seu_phone_id
    WHATSAPP_VERIFY_TOKEN=seu_token_de_verificacao
    
    # Modelo LLaMA 2
    LLAMA2_MODEL_PATH=./data/modelos/Model_Llama
    ```
5. **Baixe o modelo LLaMA 2:**
     - Execute o script para baixar o modelo:
      ```bash
      python scripts/download_llama2.py
      ```

---

## Como Usar

1. **Inicie o servidor:**
    ```bash
      bash scripts/start_server.sh
      ```

2. **Configure o webhook da WhatsApp Business API:**
    - Use o **ngrok** para expor o servidor local:
    ```bash
      ngrok http 5000
      ```
    - No painel do Meta for Developers, configure o webhook para apontar para a URL do ngrok (ex: https://seu-subdomínio.ngrok.io/webhook).  
    - Defina o **WHATSAPP_VERIFY_TOKEN** no painel e no arquivo **.env**.

3. **Envie mensagens para o número do WhatsApp configurado e veja o LuckyBot em ação!**
    

---

## Estrutura do Projeto

```text  
/luckybot_project/
├── app/                           # Código principal da aplicação
│   ├── __init__.py                # Inicialização do módulo
│   ├── webhook.py                 # Lógica do webhook do WhatsApp
│   ├── llm_handler.py             # Integração com o LLaMA 2
│   ├── payment_processor.py       # Processamento de comprovantes
│   ├── utils.py                   # Funções utilitárias
│   └── config.py                  # Configurações globais
├── data/                          # Dados do projeto
│   ├── comprovantes/              # Comprovantes de pagamento
│   ├── modelos/                   # Modelos LLaMA 2
│   └── logs/                      # Logs da aplicação
├── scripts/                       # Scripts auxiliares
│   ├── install_dependencies.sh    # Instala dependências
│   ├── start_server.sh            # Inicia o servidor
│   └── download_llama2.py         # Baixa o modelo LLaMA 2
├── tests/                         # Testes automatizados
│   ├── test_webhook.py            # Testes para o webhook
│   ├── test_llm.py                # Testes para o LLM
│   └── test_payments.py           # Testes para processamento de comprovantes
├── requirements.txt               # Lista de dependências
├── README.md                      # Documentação do projeto
└── .env                           # Variáveis de ambiente
```
    

---

## Testes

Para executar os testes automatizados, use o comando:
```bash
pytest tests/ -v
```

### Configuração da WhatsApp Business API

1. **Registrar um Negócio no Meta**

     - Acesse o [Facebook Business Manager](https://business.facebook.com/) e crie uma conta de negócio.
    
     - Siga as etapas para registrar seu número de telefone no WhatsApp Business API.

2. **Configurar a WhatsApp Cloud API**

     - Acesse o [Meta for Developers](https://developers.facebook.com/) e crie um aplicativo do tipo **WhatsApp**.
     
     - Gere um **token de acesso permanente** para autenticar suas requisições.

3. **Configurar Webhooks**

    - Defina os webhooks (endpoints) para receber notificações de mensagens.
    
    - O WhatsApp enviará eventos para seu servidor via POST.

---

### Contribuição

**Contribuições são bem-vindas! Siga os passos abaixo:**

1. Faça um fork do projeto.

2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).

3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`).

4. Faça push para a branch (`git push origin feature/nova-feature`).

5. Abra um pull request.


---

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato
Se tiver dúvidas ou sugestões, entre em contato:

Email: [lucky_bot@mundodosdadosbr.com.br](mailto:lucky_bot@mundodosdadosbr.com.br)