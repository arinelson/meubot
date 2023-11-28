import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz
from cachetools import TTLCache

# Constantes
COMMAND_HORARIO = "horario"
CACHE_KEY_HORARIO = "horario"

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
TOKEN = "6942272197:AAE8kJKRkz_y3CbOgGzXl_ocVlnrvG51MM0"

# Criação do cache com uma capacidade de 1 item e tempo de vida de 5 segundos
cache = TTLCache(maxsize=1, ttl=5)

# Função para enviar mensagens
def enviar_mensagem(chat_id, mensagem, context):
    try:
        context.bot.send_message(chat_id, mensagem)
    except Exception as e:
        # Tratamento de erro ao enviar mensagem
        logger.error(f"Erro ao enviar mensagem: {e}")

# Função para exibir a hora e o fuso horário atual
def handle_horario(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Limpar cache antes de obter a resposta
    cache.clear()

    try:
        # Obtém a hora e o fuso horário atual
        now = datetime.now()
        user_location = update.effective_user.location

        # Tratamento de localização nula
        if user_location is None:
            raise ValueError("Localização do usuário não disponível.")

        tz = pytz.timezone(user_location.timezone)
        hora_atual = now.astimezone(tz).strftime("%H:%M:%S")
        periodo_dia = get_periodo_dia(now.hour)

        # Obtém a localização do usuário
        pais = user_location.country_code
        estado = user_location.state
        municipio = user_location.city

        # Monta a resposta
        response = f"{name}, agora são {hora_atual} {periodo_dia} do {pais}, {estado}, {municipio}."

        # Armazena a resposta no cache
        cache[CACHE_KEY_HORARIO] = response
    except Exception as e:
        # Tratamento de erro ao processar o horário
        logger.error(f"Erro ao processar o horário: {e}")
        response = "Desculpe, ocorreu um erro ao obter o horário."

    # Envia a mensagem com a hora e o fuso horário
    enviar_mensagem(chat_id, response, context)

# Funções de saudação e ajuda
def handle_greeting(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Mensagem de saudação
    saudacao = f"Oi {name}, se você está me acionando é porque precisa de algo, não é mesmo?"

    # Mensagens de opções
    opcoes = [
        "/ajuda - Tô ferrado(a)",
        "/contato - Quero falar com o boss",
        f"/{COMMAND_HORARIO} - Tô perdido na hora",
    ]

    # Envia as mensagens
    enviar_mensagem(chat_id, saudacao, context)
    for opcao in opcoes:
        enviar_mensagem(chat_id, opcao, context)

# Função de ajuda
def handle_ajuda(update, context):
    chat_id = update.effective_chat.id
    enviar_mensagem(chat_id, "Precisa de uma ajudinha? Estou aqui para ajudar!")

# Função de contato
def handle_contato(update, context):
    chat_id = update.effective_chat.id
    enviar_mensagem(chat_id, "Quer falar com o chefe? Tente lá: @arinelson", context)

# Função para obter o período do dia
def get_periodo_dia(hour):
    if 5 <= hour < 12:
        return "da manhã"
    elif 12 <= hour < 18:
        return "da tarde"
    else:
        return "da noite"

# Inicia o bot
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Adiciona os handlers
dispatcher.add_handler(CommandHandler(COMMAND_HORARIO, handle_horario))
dispatcher.add_handler(CommandHandler("ajuda", handle_ajuda))
dispatcher.add_handler(CommandHandler("contato", handle_contato))
# Restante dos handlers...

# Inicia o polling
updater.start_polling()
updater.idle()
