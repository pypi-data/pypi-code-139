def stringToBinary(String:str):
    return ''.join(format(i, '08b') for i in bytearray(String, encoding ='utf-8'))
def binaryToString(Binary:str):
    return ''.join(chr(int(Binary[i*8:i*8+8],2)) for i in range(len(Binary)//8))
def intToBinary(Integer:int):
    return ''.join(format(i, '08b') for i in bytearray((str(Integer))[2:], encoding ='utf-8'))
print(intToBinary(69420))