import telegram
import os
from ShynaDatabase import Shdatabase
from Shynatime import ShTime


# Done: Will help in sending telegram message. News, Broadcast, Shyna
class ShynaTelegramBot:
    """
    bot_send_msg_to_master
    bot_send_news_to_master
    bot_send_broadcast_msg_to_master
    bot_send_msg_to_shyna
    bot_send_msg_to_chat_id
    """
    token = os.environ.get('bot_token')
    bot = telegram.Bot(token=token)
    news_bot = telegram.Bot(token=os.environ.get('news_bot_token'))
    broadcast_bot = telegram.Bot(token=os.environ.get('broadcast_bot_token'))
    status = False
    master_telegram_chat_id = os.environ.get('master_telegram_chat_id')
    message = "Default"
    shyna_chat = os.environ.get('shyna_chat')
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()

    def bot_send_msg_to_master(self):
        """Bot name: ShynaBot"""
        self.status = self.bot.send_message(chat_id=self.master_telegram_chat_id, text=str(self.message))
        self.update_db(bot_name='ShynaBot')
        return self.status

    def bot_send_news_to_master(self):
        """Bot name: ShynaNewsBot"""
        self.status = self.news_bot.send_message(chat_id=self.master_telegram_chat_id, text=str(self.message))
        self.update_db(bot_name='ShynaNewsBot')
        return self.status

    def bot_send_broadcast_msg_to_master(self):
        """Bot name: ShynaBroadcastBot"""
        self.status = self.broadcast_bot.send_message(chat_id=self.master_telegram_chat_id, text=str(self.message))
        self.update_db(bot_name='ShynaBroadcastBot')
        return self.status

    def bot_send_msg_to_shyna(self):
        """Bot name: ShynaBot"""
        self.status = self.bot.send_message(chat_id=self.shyna_chat, text=str(self.message))
        self.update_db(bot_name='ShynaSelfBot')
        return self.status

    def bot_send_msg_to_chat_id(self, chat_id):
        """Bot name: ShynaBot"""
        self.status = self.bot.send_message(chat_id=chat_id, text=str(self.message))
        self.update_db(bot_name='ShynaBot')
        return self.status

    def update_db(self, bot_name):
        self.s_data.default_database = os.environ.get('notify_db')
        self.s_data.query = "Insert Into Bot_msg_backup (text_time, text_date, bot_name, message_text, device_id) " \
                            "VALUES ('" + str(self.s_time.now_time) + "', '" + str(self.s_time.now_date) + "', '" \
                            + str(bot_name) + "', '" + str(self.message) + "', '" + str(os.environ.get('device_id')) + \
                            "')"
        self.s_data.create_insert_update_or_delete()
        self.s_data.set_date_system(process_name=bot_name)
