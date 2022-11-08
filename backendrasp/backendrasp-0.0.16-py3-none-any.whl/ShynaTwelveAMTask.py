from backendrasp import UpdateWeather


# cron: add to cron job
# Done: May need to add other 12 AM task
class RunAtTwelve:
    update_weather = UpdateWeather.UpdateWeather()

    def at_twelve(self):
        try:
            self.update_weather.update_weather_sentence()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    RunAtTwelve().at_twelve()
