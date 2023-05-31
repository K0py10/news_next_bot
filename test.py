from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

getter_token = "5909054565:AAHilbEQT8IozDDmn7b4i_GkN4XE2FxHTrQ"
sender_token = "5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0"
destination = "311427839"
file_id = ""

'''
async def get_destination(update: Update, context: ContextTypes):
    destination = update.effective_chat.id
    print(destination)
    '''

async def only_func(update: Update, context: ContextTypes):
    file_id = update.message.document.file_id
    print("FILE ID: " + file_id)
    await getter.bot.send_document(chat_id=destination, document=file_id)
    await sender.bot.send_document(chat_id=destination, document=file_id)
    
if __name__ == "__main__":
    sender = ApplicationBuilder().token(sender_token).build()
    getter = ApplicationBuilder().token(getter_token).build()
    getter.add_handler(MessageHandler(filters.ALL , only_func))
    #sender.add_handler(MessageHandler(None, get_destination))

    getter.run_polling()
    #sender.run_polling()