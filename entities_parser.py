from telethon.tl.types import MessageEntityBankCard, MessageEntityBlockquote, MessageEntityBotCommand, MessageEntityBold, MessageEntityCashtag, MessageEntityCode, MessageEntityCustomEmoji, MessageEntityEmail, MessageEntityHashtag, MessageEntityItalic, MessageEntityMention, MessageEntityMentionName, MessageEntityPhone, MessageEntityPre, MessageEntitySpoiler, MessageEntityStrike, MessageEntityTextUrl, MessageEntityUnderline, MessageEntityUnknown, MessageEntityUrl
from telegram import MessageEntity

def parse_entities(th_entities, start_offset):
    res = []
    for ent, txt in th_entities:
        if ent == MessageEntityMention:
            res.append(MessageEntity('MENTION', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityHashtag:
            res.append(MessageEntity('HASHTAG', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityBotCommand:
            res.append(MessageEntity('BOTCOMMAND', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityUrl:
            res.append(MessageEntity('URL', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityEmail:
            res.append(MessageEntity('EMAIL', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityPhone:
            res.append(MessageEntity('PHONE_NUMBER', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityBold:
            res.append(MessageEntity('BOLD', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityItalic:
            res.append(MessageEntity('ITALIC', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityStrike:
            res.append(MessageEntity('STRIKETHROUGH', ent.offset + start_offset, ent.length))
        elif ent == MessageEntitySpoiler:
            res.append(MessageEntity('SPOILER', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityCode:
            res.append(MessageEntity('CODE', ent.offset + start_offset, ent.length))
        elif ent == MessageEntityPre:
            res.append(MessageEntity('PRE', ent.offset, ent.length + start_offset, language = ent.language))
        elif ent == MessageEntityTextUrl:
            res.append(MessageEntity('TEXT_LINK', ent.offset, ent.length + start_offset, url = ent.url))
        elif ent == MessageEntityMentionName:
            res.append(MessageEntity('TEXT_MENTION', ent.offset, ent.length + start_offset, user = ent.user_id))
        elif ent == MessageEntityCustomEmoji:
            res.append(MessageEntity('CUSTOM_EMOJI', ent.offset, ent.length + start_offset, custom_emoji_id = ent.document_id))
    return res