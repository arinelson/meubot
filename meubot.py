import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import pytz
from cachetools import TTLCache

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
TOKEN = "6942272197:AAE8kJKRkz_y3CbOgGzXl_ocVlnrvG51MM0"

# Criação do cache com uma capacidade de 1 item e tempo de vida de 60 segundos
cache = TTLCache(maxsize=1, ttl=30)

# Função para enviar mensagens
def enviar_mensagem(chat_id, mensagem, context):
    try:
        context.bot.send_message(chat_id, mensagem)
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")

# Função para exibir a hora e o fuso horário atual
def handle_horario(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Limpar cache antes de obter a resposta
    cache.clear()

    # Verifica se a resposta está em cache
    if "horario" in cache:
        response = cache["horario"]
    else:
        try:
            # Obtém a hora e o fuso horário atual
            now = datetime.now()
            user_location = update.effective_user.location
            tz = pytz.timezone(user_location.timezone) if user_location else pytz.timezone('America/Maceio')
            hora_atual = now.astimezone(tz).strftime("%H:%M:%S")
            periodo_dia = get_periodo_dia(now.hour)

            # Obtém a localização do usuário
            pais = user_location.country_code if user_location else "Brasil"
            estado = user_location.state if user_location else "Alagoas"
            municipio = user_location.city if user_location else "Maceió"

            # Monta a resposta
            response = f"{name}, agora são {hora_atual} {periodo_dia} do {pais}, {estado}, {municipio}."

            # Armazena a resposta no cache
            cache["horario"] = response
        except Exception as e:
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
        "/horario - Tô perdido na hora",
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
dispatcher.add_handler(CommandHandler("horario", handle_horario))
dispatcher.add_handler(CommandHandler("ajuda", handle_ajuda))
dispatcher.add_handler(CommandHandler("contato", handle_contato))
# Restante dos handlers...

# Inicia o polling
updater.start_polling()
updater.idle()
