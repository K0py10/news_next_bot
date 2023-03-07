from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
#from channels_handler import add_channel

updater = Updater("5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0", use_context=True)
addChannel_mode = False

def start(update: Update, context: CallbackContext):
	update.message.reply_text("Shalom, my friend")

def add_channel(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a link to the channel with or without t.me/ part")
    addChannel_mode = True

def help(update: Update, context: CallbackContext):
	update.message.reply_text("Guys, I lost Crtl. There is no Esc. Just gimme some Space")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("I'm sorry, '%s' is a not a valid command" % update.message.text) 

def unknown_text(update: Update, context: CallbackContext):
    if addChannel_mode:
        if add_channel(update.message.text): 
             update.message.reply_text("Channel added")
        else:
             update.message.reply_text("Somethong went wrong, try again")
        addChannel_mode = False
    update.message.reply_text("I don't understand") 

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add_channel', add_channel))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()