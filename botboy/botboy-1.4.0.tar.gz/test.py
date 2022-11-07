"""Tests the core module"""

from botboy import BotBoy

bot = BotBoy('Adder', lambda x, y: x + y)

def test_display_information():
  global bot
  bot.display_information()

def test_execute():
  global bot
  bot.execute(1, 2)
  bot.set_processing()
  bot.execute(3, 4)
  bot.set_processing()
  bot.execute(5, 6)
  bot.set_on_file()
  bot.execute(7, 8)
  bot.set_on_file()

def test_pause():
  global bot

  bot.set_wait()
  bot.execute(100, 10000)
  bot.set_wait()
  bot.execute(1, 2)
  bot.execute(3, 4)

def test_get_result():
  global bot
  bot.set_wait()
  bot.execute(1, 2)

  if bot.get_result(): print(bot.get_result())

if __name__ == '__main__':
  test_display_information()
  test_execute()
  test_pause()
  test_get_result()
