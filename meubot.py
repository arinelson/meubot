import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3

# Configuração de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais
TOKEN = "6942272197:AAE8kJKRkz_y3CbOgGzXl_ocVlnrvG51MM0"
DATABASE = "database.db"

# Função para criar o banco de dados e a tabela
def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            name TEXT
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_id ON users(chat_id)')
    connection.commit()
    connection.close()

# Funções
def handle_help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Aqui estão as opções de atendimento do meu bot:")
    context.bot.send_message(chat_id, "/ajuda - Exibe esta mensagem de ajuda")
    context.bot.send_message(chat_id, "/contato - Envia uma mensagem para o administrador: @arinelson")

def handle_contact(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Olá, administrador. Estou precisando de ajuda.")

def handle_message(update, context):
    chat_id = update.effective_chat.id
    # Acessando o primeiro nome do usuário
    name = update.effective_user.first_name

    # Enviando a mensagem de saudação personalizada
    context.bot.send_message(chat_id, "Oi {}, se você está me acionando é porque precisa de alguma ajuda, não é mesmo?".format(name), parse_mode="html", disable_web_page_preview=True)

    # Enviando mensagem com as opções de comando
    context.bot.send_message(chat_id, "Aqui estão as opções de atendimento do meu bot:")
    context.bot.send_message(chat_id, "/ajuda - Exibe esta mensagem de ajuda")
    context.bot.send_message(chat_id, "/contato - Envia uma mensagem para o administrador:")

    # Verifica se a mensagem é um comando
    if update.message.text.startswith("/"):
        # Verifica qual comando foi enviado
        if update.message.text == "/ajuda":
            handle_help(update, context)
        elif update.message.text == "/contato":
            handle_contact(update, context)

# Chama a função para criar o banco de dados
create_database()

# Inicia o bot
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Adiciona os handlers
dispatcher.add_handler(CommandHandler("ajuda", handle_help))
dispatcher.add_handler(CommandHandler("contato", handle_contact))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Inicia o polling
updater.start_polling()
updater.idle()
