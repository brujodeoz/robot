from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import requests
import re
import logging
from ModuloProvisorio import ModuloProvisorio
import json
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(update, context):
    print("comando recibido")
    url = get_image_url()
    print("mostrar",url)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No me pagan para eso")

def document_handler(update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download('./voice.xlsx')
    controlSiga = ModuloProvisorio('./voice.xlsx')
    controlSiga.calculo_info()
    context.bot.send_message(chat_id=update.effective_chat.id, text=str(controlSiga))

def main():
    with open('configuracion.json', 'r') as file:
        self.config = json.load(file)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(str(config['TOMBOLA']['TOKEN']), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(MessageHandler(Filters.document, document_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()