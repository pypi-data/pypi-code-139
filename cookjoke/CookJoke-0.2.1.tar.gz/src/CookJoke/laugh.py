from random import choice

laughSamples = ('аха', 'вха', 'арраа', 'ихи', 'фф')

def getLaughString(n: int) -> str:
	s = choice(laughSamples).capitalize()
	for _ in range(n):
		s += choice(laughSamples)
	return s


