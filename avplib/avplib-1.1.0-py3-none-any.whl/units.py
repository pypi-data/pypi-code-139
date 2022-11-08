ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]
ASCII_CHARS_GRADIENTION_K = (256 / len(ASCII_CHARS))+1
ASCII_CHARS_GRADIENTION = {}

for i in range(0, 257):
    ASCII_CHARS_GRADIENTION[i] = ASCII_CHARS[i // ASCII_CHARS_GRADIENTION_K]

del i