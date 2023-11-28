import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime
import pytz

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
TOKEN = "6942272197:AAE8kJKRkz_y3CbOgGzXl_ocVlnrvG51MM0"

# Função para exibir a hora e o fuso horário atual
def handle_horario(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Obtém a hora e o fuso horário atual
    now = datetime.now()
    tz = pytz.timezone('America/Maceio')  # Ajuste para o fuso horário de Maceió
    hora_atual = now.astimezone(tz).strftime("%H:%M:%S")
    periodo_dia = get_periodo_dia(now.hour)
    localizacao = get_localizacao(tz)

    # Envia a mensagem com a hora e o fuso horário
    context.bot.send_message(chat_id, "{}, agora são {} {} do {}.".format(name, hora_atual, periodo_dia, localizacao))

# Funções de saudação e ajuda
def handle_greeting(update, context):
    chat_id = update.effective_chat.id
    name = update.effective_user.first_name

    # Enviando a mensagem de saudação personalizada com as opções de atendimento
    context.bot.send_message(chat_id, "Oi {}, se você está me acionando é porque precisa de alguma ajuda, não é mesmo?".format(name), parse_mode="html", disable_web_page_preview=True)
    context.bot.send_message(chat_id, "Aqui estão as opções de atendimento do meu bot:")
    context.bot.send_message(chat_id, "/ajuda - Tô ferrado(a)")
    context.bot.send_message(chat_id, "/contato - Quero falar com o boss")
    context.bot.send_message(chat_id, "/horario - Tô perdido na hora")

# Função de ajuda
def handle_help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Então você quer uma ajudinha, não é mesmo?")

# Função de contato
def handle_contact(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Poxa, tente lá e veja se o chefe te responde: @arinelson")

# Função para obter o período do dia
def get_periodo_dia(hour):
    if 5 <= hour < 12:
        return "da manhã"
    elif 12 <= hour < 18:
        return "da tarde"
    else:
        return "da noite"

# Função para obter a localização com base no fuso horário
def get_localizacao(tz):
    localizacao = tz.zone
    return localizacao

# Inicia o bot
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Adiciona os handlers
dispatcher.add_handler(CommandHandler("ajuda", handle_help))
dispatcher.add_handler(CommandHandler("contato", handle_contact))
dispatcher.add_handler(CommandHandler("horario", handle_horario))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_greeting))

# Inicia o polling
updater.start_polling()
updater.idle()
