from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Updater, MessageHandler, filters
from telethon import TelegramClient 
from multiprocessing import Process
from unused.cleaner import clean_text
from unused.entities_parser import parse_entities
import db_handler as db
import json
import asyncio
from random import randint
import simularity_handler as sh
import classes
import time
import sqlite3
from emoji import replace_emoji

#from channels_handler import add_message_to_channels_list


greeting_text = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help"
help_text = "Commands List: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"
channel_added_text = "Channel added successfully"
channel_adding_error_text = "Something went wrong, check your input and try again"

async def start_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /start command
    await context.bot.send_message(update.effective_chat.id, greeting_text) 
async def help_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /help command
	await context.bot.send_message(update.effective_chat.id, help_text)       
async def add_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /add_channel command
    if await add_channel(update.message.text.replace("/add_channel ", ""), update.effective_chat.id):
        await context.bot.send_message(update.effective_chat.id, channel_added_text) 
    else:
        await context.bot.send_message(update.effective_chat.id, channel_adding_error_text) 
async def retrieve_messages_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #, last_message_id
    channels_list = db.get_all_channels(cur)
    print("channels list: " + str(channels_list))
    for ch in channels_list:
        last_id = 0
        print('channel' + str(ch))
        async for msg in parser.iter_messages(ch.name, min_id = ch.last_message, reverse = True): #iterate over new channel messages
            last_id = msg.id
            try:
                if msg.raw_text != None and msg.raw_text != '': #sort out technical messages
                    cleaned_text = replace_emoji(msg.raw_text.replace("\n", " "), replace = '')
                    lem_text = sh.prepare_text(cleaned_text)

                    entity = await parser.get_entity(ch.name)
                    text_to_send = entity.title + ":\n" +  msg.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)

                    similar_posts = sh.find_similar_posts(lem_text, db.get_chats_posts(cur, [update.effective_chat.id]), cutoff)
                    if similar_posts == []:
                        post_db_id = db.save_post(cur, ch.id, ' '.join(lem_text))
                        message = await context.bot.send_message(update.effective_chat.id, text = text_to_send, entities= [MessageEntity('BOLD', 1, len(entity.title) + 1)], parse_mode='HTML', disable_web_page_preview=True)
                        db.add_post_to_chat(cur, update.effective_chat.id, message.id, text_to_send, post_db_id)
                    else:
                        message = db.get_chat_post(cur, update.effective_chat.id, similar_posts[-1])
                        text_to_send = message.text + "\nhttps://t.me/" + entity.username + "/" + msg.id
                        bot.edit_message_text(text_to_send, update.effective_chat.id, message.id, parse_mode = 'HTML', disable_web_page_preview = True)
                        db.update_chat_message(cur, message, text_to_send) 
            except Exception as e:
                print("Parsing message failed\nException: ", e, "\nText:", msg.text, "\nID", msg.id)
        if last_id != 0:    
            db.update_last_message(cur, ch.id, last_id)

async def add_channel(channel_user_input, chat_id): #
    try:
        entity = await parser.get_entity(channel_user_input)
        name = entity.username  
        #getting telegram's internal channel entity (used to verify thet the link is valid and unify stored data)
        channel_lastmessage = -1 #used for handling errors
        channel_lastmessage = await get_channel_lm(name)
        if channel_lastmessage != -1:
            db.save_channel(cur, name, channel_lastmessage - randint(1, 10), chat_id)
            return True
        else:
            return False
    except Exception as e: 
        print("error: " + str(e))
        return False
async def get_channel_lm(channel_username):
    channel_lastmessage = -1
    async for message in parser.iter_messages(channel_username, limit = 1): #getting last message from channel
        channel_lastmessage = message.id #saving its id
    return channel_lastmessage

async def update():
    channels_list = db.get_all_channels(cur)
    for ch in channels_list:
        if get_channel_lm(ch.name) != ch.last_message: #if there are new messages
            dest_list = db.get_channel_subs(cur, ch.id)
            last_id = 0
            async for msg in parser.iter_messages(ch.name, min_id = ch.last_message, reverse=True):
                try:
                    last_id = msg.id
                    if msg.text != None and msg.text != '': #sort out technical & mediagroup messages
                        cleaned_text = replace_emoji(msg.raw_text.replace("\n", " "), replace = '')
                        lem_text = sh.prepare_text(cleaned_text)
                        sim_posts = sh.find_similar_posts(lem_text, db.get_chats_posts(cur, dest_list), cutoff)
                        sim_ids = [sim_post.id for sim_post in sim_posts]
                        entity = await parser.get_entity(ch.name)
                        text_to_send = entity.title + ":\n" +  msg.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                        for sub in dest_list:
                            try:
                                sim_msgs_in_chat = set(sim_ids) & set(db.get_chat_post_ids(cur, sub))
                                if sim_msgs_in_chat == set():
                                    post_db_id = db.save_post(cur, ch.id, lem_text)
                                    message = await bot.send_message(sub, text = text_to_send, parse_mode='HTML')
                                    db.add_post_to_chat(update.effective_chat.id, message.id, text_to_send, post_db_id)
                                else:
                                    message = db.get_chat_post(cur, sub, max(sim_msgs_in_chat))
                                    text_to_send = message.text + "\nhttps://t.me/" + entity.username + "/" + msg.id
                                    bot.edit_message_text(text_to_send, sub, message.id, parse_mode = 'HTML', disable_web_page_preview = True)
                                    db.update_chat_message(cur, message, text_to_send) 
                            except Exception as e:
                                print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch[1], "\nID: ", msg.id)
                except Exception as e:
                    print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch[1], "\nID: ", msg.id)
            if last_id != 0:
                db.update_last_message(cur, ch.id, last_id)
    time.sleep(1)

async def run_bot():
    second_loop = asyncio.new_event_loop()
    loop.run_until_complete(application.run_polling())

async def run_updater():
    while True:
        try:
            print('Calling telethon update...')
            await update()
            await asyncio.sleep(1)
        except Exception as e:
            print("TELETHON ERROR: " + str(e))

async def run_bot():
    await application.initialize()
    await application.updater.start_polling(poll_interval = 1, timeout = 1)
    await application.start()

    while True:
        try:
            print("Calling bot updates...")
            global update_offset
            updates = await bot.get_updates(read_timeout = 1)
            print('UPDATE OFFSET: ' + str(update_offset))
            if updates != ():
                update_offset = updates[0].update_id + 1
            await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            print("Stopping bot...")
            break
        except Exception as e:
            print("PTB ERROR: " + str(e))

    # await application.updater.stop()
    await application.stop()
    await application.shutdown()

if __name__ == "__main__":
    with open("credentials.json" , 'r') as cr:
        data = json.load(cr)
        api_id = data["api_id"]
        api_hash = data["api_hash"]
        bot_token = data["bot_token"]
    parser = TelegramClient('anon', api_id, api_hash).start()
    parser.parse_mode = 'html'
    ApplicationBuilder.concurrent_updates = True
    application = ApplicationBuilder().token(bot_token).build()
    bot = application.bot
    con = sqlite3.connect('db.sql')
    cur = con.cursor()
    cutoff = 0.4
    update_offset = 0
    db.restart_db(cur)

    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    application.add_handler(CommandHandler('add_channel', add_channel_CR))   
    application.add_handler(CommandHandler('retrieve_messages', retrieve_messages_CR)) 

    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.create_task(run_updater())
    loop.run_forever()
    
    # bot_process = Process(target = application.run_polling())
    # bot_process.start()
    # bot_process.join()

    # parser_process = Process(target = run_updater, args=(parser,))
    # parser_process.start()
    # parser_process.join()

    

    # await application.initialize()
    # await application.updater.start_polling()
    # await application.start()
    # while True:
    #     try:
    #         await bot.get_updates()
    #         await update()
    #         time.sleep(1)
    #     except (KeyboardInterrupt, SystemExit) as e:
    #         break
    #     except Exception as e:
    #         print("ERROR:"+ str(e))

    # application.updater.stop()
    # await application.stop()
    # await application.shutdown()