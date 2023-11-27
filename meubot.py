import telegram

def handle_message(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text

    if message == "ajuda":
        context.bot.send_message(chat_id, "Aqui estão as opções de atendimento do meu bot:")
        context.bot.send_message(chat_id, "/ajuda - Exibe esta mensagem de ajuda")
        context.bot.send_message(chat_id, "/contato - Envia uma mensagem para o administrador")
    elif message == "contato":
        context.bot.send_message(chat_id, "Olá, administrador. Estou precisando de ajuda.")

bot = telegram.Bot(token="6942272197:AAHQ3XxW-ddCO8SG4-1W9dk-hkgAgt6DOVs")

bot.on_message(handle_message)

bot.start()
