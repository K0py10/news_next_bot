class texts:
    def greeting_text(lang):
        greeting_text_en = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help."
        greeting_text_ru = "Я бот, объединяющий новости из разных каналов в единую ленту.\nЧтобы получить список команд, введите /help."
        if lang == "null":
            return greeting_text_en
        elif lang == 'ru':
            return greeting_text_ru
        elif lang == 'en':
            return greeting_text_en
    def help_text(lang):
        help_text_en = "Commands List: \n /subscribe_to [channel] — Add channel to list of channels, whose posts will be fetched (Thereafter — list of channels) \n/unsubscribe_from [channel] — delete channel from list of channels \n/my_channels — show full list of my channels."
        help_text_ru = "Список каналов \n /subscribe_to [канал] — добавить канал в список каналов, из которых будут браться посты \n/unsubscribe_from [канал] — удалить канал из этого списква \n/my_channels — показать этот список."
        if lang == "null":
            return help_text_en
        elif lang == 'ru':
            return help_text_ru
        elif lang == 'en':
            return help_text_en
    def channel_added_text(lang):
        channel_added_text_en = channel_added_text_en = "Channel added successfully."
        channel_added_text_ru  = "Вы успешно подписались на канал."
        if lang == "null":
            return channel_added_text_en
        elif lang == 'ru':
            return channel_added_text_ru
        elif lang == 'en':
            return channel_added_text_en
    def wrong_channel_error_text(lang):
        text_en = "Something went wrong, check your input and try again."
        text_ru = "Что-то пошло не так, проверьте своё сообщение и попробуйте снова."
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def already_subscribed_text(lang):
        text_en = "You are already subscribed to this channel."
        text_ru = "Вы уже подписаны на этот канал."
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def successfully_unsibscribed_text(lang):
        text_en = "You successfully unsubscribed from this channel."
        text_ru = "Вы успешно отписались от этого канала."
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en  
    def didnt_unsubscribe_text(lang):
        text_en = "You were not subscribed to this channel. So, well, nothing really happened."
        text_ru = "Вы и не были подписаны на этот канал, так что, в сущности, ничего не произошло."
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def no_subscribed_channels_text(lang):
        text_en = "You are not subscribed to any channels.\nUse /subscribe_to command to subscribe to new channel"
        text_ru = "Вы не подписаны ни на один канал.\nИспользуйте команду /subscribe_to, чтобы это исправить"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def there_is_no_such_channel_text(lang):
        text_en = "There is no such channel"
        text_ru = "Такого канала не существует"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def settings_text(lang):
        text_en = "What do you want to change?"
        text_ru = "Что вы хотите настроить?"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def settings_lang_button_text(lang):
        text_en = "language"
        text_ru = "язык"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def lang_setting_text(lang):
        text_en = "Choose your language"
        text_ru = "Выберите язык"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def settings_del_sim_button_text(lang):
        text_en = "removal of similar posts"
        text_ru = "удаление похожих постов"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def settings_shorten_msgs_button_text(lang):
        text_en = "posts shortening"
        text_ru = "сокращение постов"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def shorten_msgs_setting_text(lang):
        text_en = "Choose your option"
        text_ru = "Выберите свой вариант"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def not_shorten_msgs_option_text(lang):
        text_en = "Do not shorten at all"
        text_ru = "Не сокращать вовсе"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def basic_shorten_msgs_option_text(lang):
        text_en = "Show only the beginning"
        text_ru = "Показывать только начало поста"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en
    def settings_changed_text(lang):
        text_en = "Done"
        text_ru = "Сделано"
        if lang == "null":
            return text_en
        elif lang == 'ru':
            return text_ru
        elif lang == 'en':
            return text_en