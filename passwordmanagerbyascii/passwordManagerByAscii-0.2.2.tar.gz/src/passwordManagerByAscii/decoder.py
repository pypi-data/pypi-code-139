def decode_password(password):
    # check if password is instance of string
    if not isinstance(password, str):
        raise TypeError("Only string input is allowed!")

    # check if encrypted length of password is multiple of 3
    if(len(password) %3 !=0):
        raise ValueError("Cannot be Decrypted : Encryption length does not match!")
    
    # check if the password is in range for decryption
    for character in password:
        if(ord(character) < 33 or ord(character)>126):
            raise ValueError("Cannot be Decrypted : Chracter must be in range 33 to 126!")

    #decrypt password
    chunk_size=3
    chunks=[]
    counter=0
    while counter<len(password):
        if counter+chunk_size < len(password):
            chunks.append(password[counter: counter+chunk_size])
        else:
            chunks.append(password[counter :len(password)])
        counter+=chunk_size

    decimal_password=''
    for position, chunk in enumerate(chunks):
        decrypted_character= ord(chunk[0])-position-1
        if decrypted_character < 34:
            remainder = 33-decrypted_character
            decrypted_character= 126-remainder
        decimal_password+= chr(decrypted_character)
        
        for index in range(1,3):
            right= ord(chunk[index])
            left= ord(chunk[index-1])  
            if(right>left):
                diff= right-left
            else:
                diff = right-33 + 126-left
            if(diff != (position+1)*(index+1)):
                raise ValueError("Cannot be Decrypted : Encryption logic does not match!")

    chunk_size=2
    chunks=[]
    counter=0
    while counter<len(decimal_password):
        if counter+chunk_size < len(decimal_password):
            chunks.append(decimal_password[counter: counter+chunk_size])
        else:
            chunks.append(decimal_password[counter :len(decimal_password)])
        counter+=chunk_size
        
    decrypted=''
    for pairs in chunks:
        swapped = pairs[::-1]
        for character in swapped:
            decrypted+=character

    return decrypted[::-1]