from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

updater = Updater("5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0", use_context=True)


def start(update: Update, context: CallbackContext):
	update.message.reply_text("Shalom, my friend")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("Guys, I lost Crtl. There is no Esc. Just gimme some Space")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("I'm sorry, '%s' is a not a valid command" % update.message.text) #Oh shit, piece of shit, 

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("I don't understand") # \nOr fuck you, leatherman


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    # Filters out unknown commands
    Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


updater.start_polling()