from ShynaDatabase import Shdatabase
from Shynatime import ShTime


# cron: Add to Cron Job
# Done: will help in Raspberry pi status
class RaspStatus:
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()

    def update_status(self):
        try:
            self.s_data.set_date_system(process_name='rasp_online_check')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    RaspStatus().update_status()
