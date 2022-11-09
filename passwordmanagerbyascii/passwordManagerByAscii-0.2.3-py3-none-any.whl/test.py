from passwordManagerByAscii import generator, validate, encrypt, decoder

print("Hello!")

while True:
    print("\nPlease choose one of the following options:\n")
    print("1. Generate password")
    print("2. Encrypt password")
    print("3. Decrypt password")
    print("4. Validate password")
    print("5. Exit program")
    option = int(input("Your choice: "))

    if option < 1 or option > 5:
        print("Invalid option. Please try again.")
        continue
    elif option == 5:
        break
    elif option == 1:
        length = int(input("Choose the length of the password (between 6 to 15 characters): "))
        password = generator.generate_password(length)
        print("Here is your generated password: " + password)
        continue
    elif option == 2:
        password = input("Enter a password to encrypt: ")
        encrypted_password = encrypt.encode_password(password)
        print("Here is your password and encoded password: " + password + " / " + encrypted_password)
        continue
    elif option == 3:
        password = input("Enter an encrypted password to decrypt: ")
        decrypted_password = decoder.decode_password(password)
        print("Here is your encrypted password and decoded password: " + password + " / " + decrypted_password)
        continue
    else:
        password = input("Enter a password to check if it is valid: ")
        is_valid = validate.validate_password(password)
        if is_valid == True:
            print(password + " is a valid password!")
        else:
            print(password + " is an invalid password!")
        continue










