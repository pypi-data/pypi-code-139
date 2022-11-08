from enum import IntEnum
import random

class CharacterType(IntEnum):
    capital = 0,
    lower = 1,
    num = 2,
    special = 3

def generate_password(length=None):
    if length == None or length<6 or length >15:
        length = random.randint(6, 15)
    values = [member.value for member in CharacterType]
    password = ""
    for i in range(length):
        if len(values) == 0:
            password += chr(random.randint(33, 126))
        else:
            type = random.choice(values)
            values.remove(type)
            if type == 0:
                password += chr(random.randint(65, 90))
            elif type == 1:
                password += chr(random.randint(97, 122))
            elif type == 2:
                password += chr(random.randint(48, 57))
            elif type == 3: 
                c = []
                c.extend(range(33, 48))
                c.extend(range(58, 65))
                c.extend(range(123, 126))
                password += chr(random.choice(c))
    return password