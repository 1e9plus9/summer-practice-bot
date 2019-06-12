from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from imgurpython import ImgurClient

import os, logging, random, string

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']
client = ImgurClient(client_id, client_secret)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi, send your picture to upload it to imgur!")

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def upload(update, context):
    photoId = update.message.photo[-1].file_id
    filePath = os.path.dirname(os.path.abspath(__file__)) + "//" + context.bot.get_file(photoId).download()

    image = client.upload_from_path(filePath, anon=True)

    try:
        os.remove(filePath)
    except OSError:
        pass

    context.bot.send_message(chat_id=update.message.chat_id, text="Here's your link!")
    context.bot.send_message(chat_id=update.message.chat_id, text="{0}".format(image['link']))

def main():

    TOKEN = os.environ['TELEGRAM_TOKEN']

    updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=1)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    photo_handler = MessageHandler(Filters.photo, upload)
    dispatcher.add_handler(photo_handler)

    updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get('PORT', '8443')), url_path=TOKEN)
    updater.bot.set_webhook("https://gentle-eyrie-90977.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
