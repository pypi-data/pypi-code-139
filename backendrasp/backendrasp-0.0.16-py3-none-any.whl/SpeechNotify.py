from backendrasp import ShynaTelegramBot, ShynaIs, ShynaSpeak
from ShynaDatabase import Shdatabase
from Shynatime import ShTime
import random


# Todo: can add more feature
# cron: Add to cron Job

class SpeechNotify:
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    s_bot = ShynaTelegramBot.ShynaTelegramBot()
    s_is = ShynaIs.ShynaIs()
    s_speak = ShynaSpeak.ShynaSpeak()

    def check_service(self):
        try:
            if not self.s_is.is_termux_device_online():
                msg = "Boss!Termux device is offline| Here we go, Termux is offline | we should get rid of this Termux," \
                      " this is not working anymore"
                msg = random.choice(msg.split("|"))
                self.s_speak.shyna_speaks(msg=msg)
            if self.s_is.is_shivam_working_late_night():
                msg = "You are not me. with that perception you made me. Why this late night work?| you are working late" \
                      " | Shiv! better get up and sleep | enough for today,go to sleep"
                msg = random.choice(msg.split("|"))
                self.s_speak.shyna_speaks(msg=msg)
            if self.s_is.saw_after_long_time():
                msg = "Hello!Ello!elo!elo!lulo!| sup? | hey, long time no see"
                msg = random.choice(msg.split("|"))
                self.s_speak.shyna_speaks(msg=msg)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    SpeechNotify().check_service()
