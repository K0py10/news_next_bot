from telegram import Update, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from telegram.error import Forbidden
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

async def start_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /start command
    db.add_user(update.effective_chat.id)
    await context.bot.send_message(update.effective_chat.id, texts.greeting(db.get_user(update.effective_chat.id).lang)) 
async def help_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /help command
    await context.bot.send_message(update.effective_chat.id, texts.help(db.get_user(update.effective_chat.id).lang))
async def subscribe_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(texts.ask_channel(db.get_user(update.effective_chat.id).lang))
    return 1
async def cancel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END
async def add_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        entity = await parser.get_entity(update.message.text.replace("/subscribe_to", ""))
        name = entity.username  
        #getting telegram's internal channel entity (used to verify thet the link is valid and unify stored data)
        channel_lastmessage = -1 #used for handling errors
        channel_lastmessage = await get_channel_lm(name)
        if channel_lastmessage != -1:
            if db.save_channel(name, channel_lastmessage - randint(1, 10), update.effective_chat.id):
                await context.bot.send_message(update.effective_chat.id, texts.channel_added(db.get_user(update.effective_chat.id).lang)) 
                return ConversationHandler.END
            else:
                await context.bot.send_message(update.effective_chat.id, texts.already_subscribed(db.get_user(update.effective_chat.id).lang)) 
                return 1
        else:
            await context.bot.send_message(update.effective_chat.id, texts.wrong_channel_error(db.get_user(update.effective_chat.id).lang))
            return 1
    except Exception as e:
        print("Error while getting channel: ", e)
        await context.bot.send_message(update.effective_chat.id, texts.wrong_channel_error(db.get_user(update.effective_chat.id).lang))
        return 1
async def delete_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        entity = await parser.get_entity(update.message.text.replace("/unsubscribe_from", ""))
        ch_name = entity.username
        if db.unsubscribe(ch_name, update.effective_chat.id):
            await context.bot.send_message(update.effective_chat.id, texts.successfully_unsubscribed(db.get_user(update.effective_chat.id).lang))
        else:
            await context.bot.send_message(update.effective_chat.id, texts.didnt_unsubscribe(db.get_user(update.effective_chat.id).lang))
    except:
        await context.bot.send_message(update.effective_chat.id, texts.there_is_no_such_channel(db.get_user(update.effective_chat.id).lang))
async def my_channels_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('my channels')
    user_channels = db.get_user_channels(update.effective_chat.id)
    if user_channels != []:
        text_to_send = "List of channels that you are subscribed to: "
        for ch in user_channels:
            text_to_send += '\n' + ch
        await context.bot.send_message(update.effective_chat.id, text_to_send)
    else:
        await context.bot.send_message(update.effective_chat.id, texts.no_subscribed_channels(db.get_user(update.effective_chat.id).lang))
async def settings_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('settings')
    user = db.get_user(update.effective_chat.id)
    if user.del_sim == 1:
        keyboard = [[InlineKeyboardButton(texts.settings_lang_button(user.lang), callback_data='lang')], 
                    [InlineKeyboardButton(texts.settings_del_sim_turn_off_button(user.lang), callback_data='del_sim')], 
                    [InlineKeyboardButton(texts.settings_shorten_msgs_button(user.lang), callback_data='shorten_msgs')]]
    else: 
        keyboard = [[InlineKeyboardButton(texts.settings_lang_button(user.lang), callback_data='lang')], 
                    [InlineKeyboardButton(texts.settings_del_sim_turn_on_button(user.lang), callback_data='del_sim')], 
                    [InlineKeyboardButton(texts.settings_shorten_msgs_button(user.lang), callback_data='shorten_msgs')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(texts.settings(user.lang), reply_markup=reply_markup)
async def set_lang_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('')
    lang = db.get_user(update.effective_chat.id).lang
    keyboard = [[InlineKeyboardButton('English', callback_data = 'en')],
                [InlineKeyboardButton('Русский', callback_data = 'ru')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(texts.lang_setting(lang), reply_markup=reply_markup)
async def change_lang_en_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('')
    user = db.get_user(update.effective_chat.id)
    db.change_user_lang(user.chat, 'en')
    await update.callback_query.edit_message_text(texts.settings_changed(user.lang))
async def change_lang_ru_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_user_lang(user.chat, 'ru')
    await update.callback_query.edit_message_text(texts.settings_changed(user.lang))
async def change_del_sim_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_user_del_sim(user.chat)
    await update.callback_query.edit_message_text(texts.settings_changed(user.lang))
async def set_shorten_msgs_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = db.get_user(update.effective_chat.id).lang
    keyboard = [[InlineKeyboardButton(texts.not_shorten_msgs_option(lang), callback_data = 'no_shorten')],
                [InlineKeyboardButton(texts.basic_shorten_msgs_option(lang), callback_data = 'bas_shorten')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(texts.shorten_msgs_setting(lang), reply_markup=reply_markup)
async def change_shorten_no_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_shorten_msgs(user.chat, 0)
    await update.callback_query.edit_message_text(texts.settings_changed(user.lang))
async def change_shorten_bas_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = db.get_user(update.effective_chat.id)
    db.change_shorten_msgs(user.chat, 1)
    await update.callback_query.edit_message_text(texts.settings_changed(user.lang))

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
                        
                        for sub in dest_list:
                            try:
                                lang = db.get_user(sub).lang
                                if len(msg.text) > 2000 and db.get_user(sub).shorten_msgs == 1:
                                    text_to_send = entity.title + ":\n" +  msg.text[:msg.text.find('\n', 1500)] + '...' + '\n<a href="https://t.me/' + entity.username + "/" + str(msg.id) + '/">' + texts.read_more(lang) + '</a>'#msg.text.find('\n', 600)
                                else:
                                    text_to_send = entity.title + ":\n" +  msg.text + '\n<a href="https://t.me/' + entity.username + "/" + str(msg.id) + '/">' + texts.source(lang) + '</a>'
                                # print(text_to_send)
                                sim_msgs_in_chat = set(sim_ids) & set(db.get_chat_post_ids(sub))
                                if sim_msgs_in_chat == set() or db.get_user(sub).del_sim == 0:
                                    post_db_id = db.save_post(ch.id, ' '.join(lem_text))
                                    if msg.photo or msg.video or msg.audio or msg.voice or msg.video_note or msg.sticker or msg.gif or msg.file:
                                        message = await bot.send_message(sub, text = text_to_send, parse_mode = 'HTML') 
                                    else:
                                        message = await bot.send_message(sub, text = text_to_send, parse_mode = 'HTML', disable_web_page_preview = True)
                                    db.add_post_to_chat(sub, message.id, text_to_send, post_db_id)
                                else:
                                    for sim_msg in sim_msgs_in_chat:
                                        message = db.get_chat_post(sub, sim_msg)
                                        text_to_send = message.text + '\n<a href="https://t.me/' + entity.username + "/" + str(msg.id) + '/">' + texts.source(lang) + '</a>'
                                        await bot.edit_message_text(text_to_send, sub, message.id, parse_mode = 'HTML', disable_web_page_preview = True)
                                        db.update_chat_message(message, text_to_send) 
                            except Forbidden as e:
                                db.delete_user(sub)
                            except Exception as e:
                                print("Sending message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch.name, "\nID: ", msg.id, "\nMessage: ", text_to_send)
                except Exception as e:
                    print("Parsing message failed\nException: ", e, "\nChannel: ", ch.name, "\nID: ", msg.id)
            if last_id != 0:
                db.update_last_message(ch.id, last_id)

async def run_updater():
    while True:
        try:
            # print('Calling telethon update...')
            await update()
            await asyncio.sleep(1)
        except Exception as e:
            print("TELETHON ERROR: " + str(e))

async def run_bot():
    await application.initialize()
    await application.updater.start_polling(poll_interval = 0, bootstrap_retries = 0)
    await application.start()
    update_offset = 0
    while True:
        try:
            # print("Calling bot updates...")
            # await update()
            updates = await bot.get_updates(offset = update_offset, read_timeout = 1)
            if updates != ():
                # print("got update:" + str(updates[-1]))
                update_offset = updates[-1].update_id
            await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            print("Stopping bot...")
            break
        except Exception as e:
            continue
            # print("ERROR: " + str(e))

    await application.updater.stop()
    await application.stop()
    await application.shutdown()

async def send_all():
    for user in db.get_all_users():
        try: 
            await bot.send_message(user, '<a href="http://www.example.com/">inline URL</a>', parse_mode = 'HTML')
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
    # db.restart_db()

    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    add_channel_CH = ConversationHandler(
        entry_points=[CommandHandler('subscribe', subscribe_CR)],
        states={1: [MessageHandler(filters.TEXT, add_channel)]},
        fallbacks = [CommandHandler('cancel', cancel_CR)]
    )
    application.add_handler(add_channel_CH)
    application.add_handler(CommandHandler('unsubscribe_from', delete_channel_CR)) 
    # application.add_handler(CommandHandler('retrieve_messages', update)) 
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
    loop = asyncio.get_event_loop()
    loop.create_task(run_updater())
    loop.create_task(run_bot())
    loop.run_forever()
    # asyncio.run(run_bot())
 