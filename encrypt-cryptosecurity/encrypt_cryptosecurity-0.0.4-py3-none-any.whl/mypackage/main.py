def des():
    des1 = """
        from Crypto.Cipher import DES
        from secrets import token_bytes

        key = token_bytes(8)

        def encrypt(msg):
            cipher = DES.new(key, DES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
            return nonce, ciphertext, tag

        def decrypt(nonce, ciphertext, tag):
            cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            try:
                cipher.verify(tag)
                return plaintext.decode('ascii')
            except:
                return False
        nonce, ciphertext, tag = encrypt(input('Enter a message: '))
        plaintext = decrypt(nonce, ciphertext, tag)

        print(f'Cipher text: {ciphertext}')

        if not plaintext:
            print('Message is corrupted!')
        else:
        print((f'Plain text: {plaintext}'))
    """
    return des1


def aes():
    aes1 = """
    from Crypto.Cipher import AES
    from secrets import token_bytes

    key = token_bytes(16)

    def encrypt(msg):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
        return nonce, ciphertext, tag

    def decrypt(nonce, ciphertext, tag):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            return plaintext.decode('ascii')
        except:
            return False

    nonce, ciphertext, tag = encrypt(input('Enter a message: '))
    plaintext = decrypt(nonce, ciphertext, tag)
    print(f'Cipher text: {ciphertext}')
    if not plaintext:
        print('Message is corrupted')
    else:
        print(f'Plain text: {plaintext}')
    """
    return aes1


def playfair():
    playfair1 = """
        def toLowerCase(text):
        return text.lower()
    def removeSpaces(text):
        newText = ""
        for i in text:
            if i == " ":
                continue
            else:
                newText = newText + i
        return newText
    def Diagraph(text):
        Diagraph = []
        group = 0
        for i in range(2, len(text), 2):
            Diagraph.append(text[group:i])

            group = i
        Diagraph.append(text[group:])
        return Diagraph
    def FillerLetter(text):
        k = len(text)
        if k % 2 == 0:
            for i in range(0, k, 2):
                if text[i] == text[i+1]:
                    new_word = text[0:i+1] + str('x') + text[i+1:]
                    new_word = FillerLetter(new_word)
                    break
                else:
                    new_word = text
        else:
            for i in range(0, k-1, 2):
                if text[i] == text[i+1]:
                    new_word = text[0:i+1] + str('x') + text[i+1:]
                    new_word = FillerLetter(new_word)
                    break
                else:
                    new_word = text
        return new_word
    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    def generateKeyTable(word, list1):
        key_letters = []
        for i in word:
            if i not in key_letters:
                key_letters.append(i)

        compElements = []
        for i in key_letters:
            if i not in compElements:
                compElements.append(i)
        for i in list1:
            if i not in compElements:
                compElements.append(i)
        matrix = []
        while compElements != []:
            matrix.append(compElements[:5])
            compElements = compElements[5:]

        return matrix
    def search(mat, element):
        for i in range(5):
            for j in range(5):
                if(mat[i][j] == element):
                    return i, j
    def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1c == 4:
            char1 = matr[e1r][0]
        else:
            char1 = matr[e1r][e1c+1]

        char2 = ''
        if e2c == 4:
            char2 = matr[e2r][0]
        else:
            char2 = matr[e2r][e2c+1]

        return char1, char2
    def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        if e1r == 4:
            char1 = matr[0][e1c]
        else:
            char1 = matr[e1r+1][e1c]
        char2 = ''
        if e2r == 4:
            char2 = matr[0][e2c]
        else:
            char2 = matr[e2r+1][e2c]
        return char1, char2
    def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
        char1 = ''
        char1 = matr[e1r][e2c]
        char2 = ''
        char2 = matr[e2r][e1c]
        return char1, char2
    def encryptByPlayfairCipher(Matrix, plainList):
        CipherText = []
        for i in range(0, len(plainList)):
            c1 = 0
            c2 = 0
            ele1_x, ele1_y = search(Matrix, plainList[i][0])
            ele2_x, ele2_y = search(Matrix, plainList[i][1])
            if ele1_x == ele2_x:
                c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            elif ele1_y == ele2_y:
                c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            else:
                c1, c2 = encrypt_RectangleRule(
                    Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
            cipher = c1 + c2
            CipherText.append(cipher)
        return CipherText
    text_Plain = 'instruments'
    text_Plain = removeSpaces(toLowerCase(text_Plain))
    PlainTextList = Diagraph(FillerLetter(text_Plain))
    if len(PlainTextList[-1]) != 2:
        PlainTextList[-1] = PlainTextList[-1]+'z'
    key = "Monarchy"
    print("Key text:", key)
    key = toLowerCase(key)
    Matrix = generateKeyTable(key, list1)
    print("Plain Text:", text_Plain)
    CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)
    CipherText = ""
    for i in CipherList:
        CipherText += i
    print("CipherText:", CipherText)
    """
    return playfair1


def rsa():
    rsa1 = """
    import math
    def gcd(a, h):
        temp = 0
        while(1):
            temp = a % h
            if (temp == 0):
                return h
            a = h
            h = temp
    p = 3
    q = 7
    n = p*q
    e = 2
    phi = (p-1)*(q-1)
    while (e < phi):
        if(gcd(e, phi) == 1):
            break
        else:
            e = e+1
    k = 2
    d = (1 + (k*phi))/e
    msg = 12.0

    print("Message data = ", msg)
    c = pow(msg, e)
    c = math.fmod(c, n)
    print("Encrypted data = ", c)
    m = pow(c, d)
    m = math.fmod(m, n)
    print("Original Message Sent = ", m)
    """
    return rsa1


def caesar():
    caesar1 = """
    def encrypt(text,s):
    result = ""
    for char in text:
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result
    def decrypt(text,s):
        result = ""
        for char in text:
            if (char.isupper()):
                result += chr((ord(char) - s-65) % 26 + 65)
            else:
                result += chr((ord(char) - s - 97) % 26 + 97)
        return result
    text = "abcdefghijklmno"
    s = 1
    cipher = encrypt(text,s)
    print("encryption: ", cipher)
    print("decryption: ", decrypt(cipher, s))
    """
    return caesar1

def vig():
    vig1 = """
    def generateKey(string, key):
	key = list(key)
	if len(string) == len(key):
		return(key)
	else:
		for i in range(len(string) -
					len(key)):
			key.append(key[i % len(key)])
	return("" . join(key))
    def cipherText(string, key):
        cipher_text = []
        for i in range(len(string)):
            x = (ord(string[i]) +
                ord(key[i])) % 26
            x += ord('A')
            cipher_text.append(chr(x))
        return("" . join(cipher_text))
    def originalText(cipher_text, key):
        orig_text = []
        for i in range(len(cipher_text)):
            x = (ord(cipher_text[i]) -
                ord(key[i]) + 26) % 26
            x += ord('A')
            orig_text.append(chr(x))
        return("" . join(orig_text))
    if __name__ == "__main__":
        string = "GEEKSFORGEEKS"
        keyword = "AYUSH"
        key = generateKey(string, keyword)
        cipher_text = cipherText(string,key)
        print("Ciphertext :", cipher_text)
        print("Original/Decrypted Text :",
            originalText(cipher_text, key))
    """
    return vig1