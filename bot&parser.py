from telegram import Update, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler
from telethon import TelegramClient 
from multiprocessing import Process
from unused.cleaner import clean_text
from entities_parser import parse_entities
import db_handler as db
import json
import asyncio
from random import randint
import simularity_handler as sh
from texts import *
import classes
from emoji import replace_emoji

#from channels_handler import add_message_to_channels_list


# greeting_text_en = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help.\n"
# help_text_en = "Commands List: \n /subscribe_to [channel] — Add channel to list of channels, whose posts will be fetched (Thereafter — list of channels) \n/unsubscribe_from [channel] — delete channel from list of channels \n/my_channels — show full list of my channels."
# channel_added_text_en = "Channel added successfully."
# wrong_channel_error_text_en = "Something went wrong, check your input and try again."
# adding_channel_internal_error_text_en = "Something went wrong on our side, you may try again."
# already_subscribed_text_en = "You are already subscribed to this channel."
# successfully_unsubscribed_text_en = "You successfully unsubscribed from this channel."
# didnt_unsubscribe_text_en = "You were not subscribed to this channel. So, well, nothing really happened."
# no_subscribed_channels_text_en = "you are not subscribed to any channels.\nUse /subscribe_to command to subscribe to new channel"
# there_is_no_such_channel_text_en = "There is no such channel"

# greeting_text_ru = "Я бот, объединяющий новости из разных каналов в единую ленту.\nЧтобы получить список команд, введите /help."
# help_text_ru = "Список каналов \n /subscribe_to [канал] — добавить канал в список каналов, из которых будут браться посты \n/unsubscribe_from [канал] — удалить канал из этого списква \n/my_channels — показать этот список."
# channel_added_text_ru  = "Вы успешно подписались на канал."
# wrong_channel_error_text_ru = "Что-то пошло не так, проверьте своё сообщение и попробуйте снова."
# adding_channel_internal_error_text_ru = "Something went wrong on our side, you may try again."
# already_subscribed_text_ru = "Вы уже подписаны на этот канал."
# successfully_unsubscribed_text_ru = "Вы успешно отписались от этого канала."
# didnt_unsubscribe_text_ru = "Вы и не были подписаны на этот канал, так что, в сущности, ничего не произошло."
# no_subscribed_channels_text_ru = "Вы не подписаны ни на один канал.\nИспользуйте команду /subscribe_to, чтобы это исправить"
# there_is_no_such_channel_text_ru = "Такого канала не существует"

async def start_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /start command
    db.add_user(update.effective_chat.id)
    await context.bot.send_message(update.effective_chat.id, texts.greeting_text(db.get_user(update.effective_chat.id).lang)) 
async def help_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /help command
	await context.bot.send_message(update.effective_chat.id, texts.help_text(db.get_user(update.effective_chat.id).lang))       
async def add_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /subscribe_to command
    try:
        entity = await parser.get_entity(update.message.text.replace("/subscribe_to", ""))
        name = entity.username  
        #getting telegram's internal channel entity (used to verify thet the link is valid and unify stored data)
        channel_lastmessage = -1 #used for handling errors
        channel_lastmessage = await get_channel_lm(name)
        if channel_lastmessage != -1:
            if db.save_channel(name, channel_lastmessage - randint(1, 10), update.effective_chat.id):
                await context.bot.send_message(update.effective_chat.id, texts.channel_added_text(db.get_user(update.effective_chat.id).lang)) 
            else:
                await context.bot.send_message(update.effective_chat.id, texts.already_subscribed_text(db.get_user(update.effective_chat.id).lang)) 
        else:
            await context.bot.send_message(update.effective_chat.id, texts.wrong_channel_error_text(db.get_user(update.effective_chat.id).lang))
    except Exception as e:
        print("Error while getting channel: ", e)
        await context.bot.send_message(update.effective_chat.id, texts.wrong_channel_error_text(db.get_user(update.effective_chat.id).lang))
async def delete_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        entity = await parser.get_entity(update.message.text.replace("/unsubscribe_from", ""))
        ch_name = entity.username
        if db.unsubscribe(ch_name, update.effective_chat.id):
            await context.bot.send_message(update.effective_chat.id, texts.successfully_unsubscribed_text(db.get_user(update.effective_chat.id).lang))
        else:
            await context.bot.send_message(update.effective_chat.id, texts.didnt_unsubscribe_text(db.get_user(update.effective_chat.id).lang))
    except:
        await context.bot.send_message(update.effective_chat.id, texts.there_is_no_such_channel_text(db.get_user(update.effective_chat.id).lang))
async def my_channels_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_channels = db.get_user_channels(update.effective_chat.id)
    if user_channels != []:
        text_to_send = "List of channels that you are subscribed to: "
        for ch in user_channels:
            text_to_send += '\n' + ch
        await context.bot.send_message(update.effective_chat.id, text_to_send)
    else:
        await context.bot.send_message(update.effective_chat.id, texts.no_subscribed_channels_text(db.get_user(update.effective_chat.id).lang))
async def settings_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = db.get_user(update.effective_chat.id).lang
    keyboard = [[InlineKeyboardButton(texts.settings_lang_button_text(lang), callback_data='lang')], 
                [InlineKeyboardButton(texts.settings_del_sim_button_text(lang), callback_data='del_sim')], 
                [InlineKeyboardButton(texts.settings_shorten_msgs_button_text(lang), callback_data='shorten_msgs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texts.settings_text(lang), reply_markup=reply_markup)
async def set_lang_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = db.get_user(update.effective_chat.id).lang
    keyboard = [[InlineKeyboardButton('English', callback_data = 'en')],
                [InlineKeyboardButton('Русский', callback_data = 'ru')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(texts.lang_setting_text(lang), reply_markup=reply_markup)
async def change_lang_en_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_user_lang(user.chat, 'en')
    await update.callback_query.edit_message_text(texts.settings_changed_text(user.lang))
async def change_lang_ru_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_user_lang(user.chat, 'ru')
    await update.callback_query.edit_message_text(texts.settings_changed_text(user.lang))
async def change_del_sim_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_user_del_sim(user.chat)
    await update.callback_query.edit_message_text(texts.settings_changed_text(user.lang))
async def set_shorten_msgs_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = db.get_user(update.effective_chat.id).lang
    keyboard = [[InlineKeyboardButton(texts.not_shorten_msgs_option_text(lang), callback_data = 'no_shorten')],
                [InlineKeyboardButton(texts.basic_shorten_msgs_option_text(lang), callback_data = 'bas_shorten')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(texts.shorten_msgs_setting_text(lang), reply_markup=reply_markup)
async def change_shorten_no_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_shorten_msgs(user.chat, 0)
    await update.callback_query.edit_message_text(texts.settings_changed_text(user.lang))
async def change_shorten_bas_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_shorten_msgs(user.chat, 1)
    await update.callback_query.edit_message_text(texts.settings_changed_text(user.lang))

async def get_channel_lm(channel_username):
    channel_lastmessage = -1
    async for message in parser.iter_messages(channel_username, limit = 1): #getting last message from channel
        channel_lastmessage = message.id #saving its id
    return channel_lastmessage

async def update(): #update : Update, context : ContextTypes.DEFAULT_TYPE
    channels_list = db.get_all_channels()
    for ch in channels_list:
        if await get_channel_lm(ch.name) != ch.last_message: #if there are new messages
            dest_list = db.get_channel_subs(ch.id)
            last_id = 0
            async for msg in parser.iter_messages(ch.name, min_id = ch.last_message, reverse=True):
                try:
                    last_id = msg.id
                    if msg.text != None and msg.text != '': #sort out technical & mediagroup messages
                        # print(msg.text)
                        cleaned_text = replace_emoji(msg.raw_text.replace("\n", " "), replace = '')
                        lem_text = sh.prepare_text(cleaned_text)
                        sim_posts = sh.find_similar_posts(lem_text, db.get_chats_posts(dest_list), cutoff)
                        sim_ids = [sim_post.id for sim_post in sim_posts]
                        entity = await parser.get_entity(ch.name)
                        text_to_send = entity.title + ":\n" +  msg.raw_text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                        for sub in dest_list:
                            try:
                                sim_msgs_in_chat = set(sim_ids) & set(db.get_chat_post_ids(sub))
                                if sim_msgs_in_chat == set():
                                    post_db_id = db.save_post(ch.id, ' '.join(lem_text))
                                    message = await bot.send_message(sub, text = text_to_send, disable_web_page_preview = True) # entities = text_entities,
                                    db.add_post_to_chat(sub, message.id, text_to_send, post_db_id)
                                else:
                                    for sim_msg in sim_msgs_in_chat:
                                        message = db.get_chat_post(sub, sim_msg)
                                        text_to_send = message.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                                        await bot.edit_message_text(text_to_send, sub, message.id, parse_mode = 'HTML', disable_web_page_preview = True)
                                        db.update_chat_message(message, text_to_send) 
                            except Exception as e:
                                print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch.name, "\nID: ", msg.id)
                except Exception as e:
                    print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch[1], "\nID: ", msg.id)
            if last_id != 0:
                db.update_last_message(ch.id, last_id)

async def run_updater():
    while True:
        # try:
            # print('Calling telethon update...')
            # await update()
            await asyncio.sleep(1)
        # except Exception as e:
        #     print("TELETHON ERROR: " + str(e))
async def run_bot():
    await application.initialize()
    await application.updater.start_polling(poll_interval = 0)
    await application.start()

    while True:
        try:
            # print("Calling bot updates...")
            await update()
            global update_offset
            updates = await bot.get_updates(read_timeout = 1)
            # print('UPDATE OFFSET: ' + str(update_offset))
            if updates != ():
                update_offset = updates[0].update_id + 1
            await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            print("Stopping bot...")
            break
        except Exception as e:
            # continue
            print("ERROR: " + str(e))

    await application.updater.stop()
    await application.stop()
    await application.shutdown()

async def send_all():
    for user in db.get_all_users():
        try: 
            await bot.send_message(user, "Пристегнуть ремни, база данных сбрасывается")
        except:
            continue

if __name__ == "__main__":
    with open("credentials.json" , 'r') as cr:
        data = json.load(cr)
        api_id = data["api_id"]
        api_hash = data["api_hash"]
        bot_token = data["bot_token"]
    parser = TelegramClient('anon', api_id, api_hash).start()
    parser.parse_mode = 'html'
    ApplicationBuilder().connection_pool_size(100)
    ApplicationBuilder().pool_timeout(0.1)
    application = ApplicationBuilder().token(bot_token).build()
    bot = application.bot
    updater = application.updater
    cutoff = 0.4
    update_offset = 0
    db.restart_db()

    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    application.add_handler(CommandHandler('subscribe_to', add_channel_CR))  
    application.add_handler(CommandHandler('unsubscribe_from', delete_channel_CR)) 
    application.add_handler(CommandHandler('retrieve_messages', update)) 
    application.add_handler(CommandHandler('my_channels', my_channels_CR))
    application.add_handler(CommandHandler('settings', settings_CR))
    application.add_handler(CallbackQueryHandler(set_lang_CR, 'lang'))
    application.add_handler(CallbackQueryHandler(change_lang_en_CR, 'en'))
    application.add_handler(CallbackQueryHandler(change_lang_ru_CR, 'ru'))
    application.add_handler(CallbackQueryHandler(change_del_sim_CR, 'del_sim'))
    application.add_handler(CallbackQueryHandler(set_shorten_msgs_CR, 'shorten_msgs'))
    application.add_handler(CallbackQueryHandler(change_shorten_no_CR, 'no_shorten'))
    application.add_handler(CallbackQueryHandler(change_shorten_bas_CR, 'bas_shorten'))

    # asyncio.run(send_all())

    # loop = asyncio.get_event_loop()
    # loop.create_task(run_updater())
    # loop.create_task(run_bot())
    # loop.run_forever()
    asyncio.run(run_bot())
 