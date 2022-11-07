from random import choice, seed
from CookJoke.laugh import getLaughString
seed(1)

PROFESSIONS = ['повар', 'милиционер', 'пожарник', "строитель", "бухгалтер"]
def getRandomProfession():
	return choice(PROFESSIONS)


class Question:
	actor1: 'Cook'
	actor2: 'Cook'
	def __init__(self, actor1: 'Cook', actor2: 'Cook'):
		self.actor1 = actor1
		self.actor2 = actor2
		print(f'{self.actor1} спрашивает {self.actor2}а:'.capitalize())

	def whatIsProfession(self, maybe: str) -> 'Reply':
		print(f'{self.actor1}, какова твоя профессия?'.capitalize(), f'Ты {maybe}?')
		return Reply(self.actor2, maybe == self.actor2.getProfession())

class Reply:
	message: str
	sender: 'Cook'
	def __init__(self, sender: 'Cook', correct: bool):
		self.sender = sender
		if not correct:
			self.message = f'Нет! Отвечает {sender}.'
		else:
			self.message = f'Да, отвечает {sender}.'

	def logCookAnswer(self) -> 'Cook':
		print(self.message)
		return self.sender

class Cook:
	def __init__(self, name: str, profession: str):
		self.name = name
		self.profession = profession

	def ask(self, povar: 'Cook') -> 'Question':
		return Question(self, povar)

	def getProfession(self) -> str:
		return self.profession

	def logMainProfession(self) -> None:
		print(f'Моя главная профессия - {self.getProfession()}')

	def __str__(self):
		return self.name
