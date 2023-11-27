import telegram
import sqlite3

# Variáveis globais
TOKEN = "6942272197:AAHQ3XxW-ddCO8SG4-19dk-hkgAgt6DOVs"
DATABASE = "database.db"

# Funções
def handle_help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Aqui estão as opções de atendimento do meu bot:")
    context.bot.send_message(chat_id, "/ajuda - Exibe esta mensagem de ajuda")
    context.bot.send_message(chat_id, "/contato - Envia uma mensagem para o administrador")

def handle_contact(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Olá, administrador. Estou precisando de ajuda.")

def handle_message(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text

    # Verifica se a mensagem é um comando
    if message.startswith("/"):
        # Verifica qual comando foi enviado
        if message == "/ajuda":
            handle_help(update, context)
        elif message == "/contato":
            handle_contact(update, context)
    else:
        # Verifica se o usuário já está cadastrado no banco de dados
        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM users WHERE chat_id = ?", (chat_id,))
        name = cursor.fetchone()
        connection.close()

        # Se o usuário não estiver cadastrado, cadastra-o no banco de dados
        if name is None:
            name = update.message.from_user.first_name
            connection = sqlite3.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (chat_id, name) VALUES (?, ?)", (chat_id, name))
            connection.commit()
            connection.close()

        # Envia uma mensagem de resposta ao usuário
        context.bot.send_message(chat_id, "Olá, " + name + "!")

# Inicia o bot
bot = telegram.Bot(token=TOKEN)
bot.on_message(handle_message)
bot.start()
