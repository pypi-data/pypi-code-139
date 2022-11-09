import string

def toEnglish(s):

    sentence = process_input(s,"e")

    english = ""
    for word in sentence:
        trans = word.split("-")
        noay =  trans[1]
        english += noay[:len(noay) - 2]+ str(trans[0]) + " "
    return english.lower()



def toPL(s, intermediate_output_flag = True):

    sentence = process_input(s,"p")

    # Our rules for pig latin:
    #Take away the first letter of a word, then add a new word that uses the first letter of the word with "ay" added to it e.g., hello becomes ello-hay
    #For words that start with a vowel, you add "ay" to the end of the word e.g., enter becomes enter-ay
    #For words that start with a consonant, all letters are removed until a vowel is reached and then all removed consonants are used to create a second word, with "ay" added to the end of it e.g., happy becomes appy-hay    
    pl = ""
    pl_word = ""
    hy = ""
    vowels = "aeiouyAEIOUY"

    if intermediate_output_flag:  #Flag to hyphenate pig latin words, makes it easier to check the english --> pl and back translation functions
        hy = "-"

    for w in sentence:
        if len(w) > 0:
            if w[0] in vowels:  #check if the first letter is a vowel
                pl_word = w + hy + "ay"  #if we're looking for intermediate output, this will add a hyphen here
                pl += pl_word + " "
            else:  #starts with a consonant   

                consonants = ""
                while len(w) > 0:
                    if not(w[0] in vowels):
                        consonants = consonants + w[0]
                        w = w[1:]
                    else:
                        break
                
                pl_word = w + hy + consonants + "ay"
                pl += pl_word + " "
    return pl



#Function to parse the input string to a usable list, depending on the 
#type of translation needed. Also prints useful output for debugging / running
#Takes in the user's input string and a flag corresponding to the type of translation

#when we call this, we can make sure that it returns a list with something in it by checking the len()
def process_input(s, translation_flag):
    
    s = s.strip()

    for punc in string.punctuation:
        if punc != "-":
            s = s.replace(punc, '') #remove all punctation except the hyphens, helps w edge cases

    if len(s) < 1 or s == '':
        print("There's nothing to translate from your message: ", s)
        return [] #helps us avoid the case where someone just submitted all punctuation
    
    #a flag for deciding if we're translating english --> latin or vice versa
    if translation_flag.lower() == "e": #I've decided that "e" means "translate to english"
        if "-" not in list(s):
            print("Every Pig Latin word needs a hyphen, so we can translate it effectively")
            return []
        else:
            s = s.strip()
            return s.split(" ")
    elif translation_flag.lower() == "p": # "p" means "translate to pig latin"
        s = s.strip()
        return s.split(" ")
    
    else:
        print("Invalid translation flag entered: ", translation_flag)
        return []

def speech_bubble(message):
    result = "\n"
    words = message.split(" ")
    
    lines = []

    words_per_line = 7
    line = ""
    max_lines = 0
    for i in range(len(words)):
        # append the current line to lines if max number of words in line is reached
        if (i % words_per_line == 0 and i != 0):
            lines.append(line)
            line = ""

        # if new line, start without a space
        if i % words_per_line != 0:
            line += " " + words[i]
        else:
            line += words[i]

        # if (i == len(words) - 1 and i % words_per_line != 0):
        if (i == len(words) - 1):
            lines.append(line)

    for i in range(len(lines)):
        if len(lines[i]) > max_lines:
            max_lines = len(lines[i])

    result += " " + "-" * max_lines + "\n"
    for i in range(len(lines)):
        result += "(" + lines[i] + " " * (max_lines - len(lines[i])) + ")" + "\n"
    result += " " + "-" * max_lines

    return result

def arrow_to_bubble():
    result = "       \\\n"
    result += "        \\"

    return result

def print_pig():
    result = "         <`--'\>______" + "\n"
    result += "         /. .  `'     \\" + "\n"
    result += "        (`')  ,        @" + "\n"
    result += "         `-._,        /" + "\n"
    result += "            )-)_/--( >" + "\n"
    result += "           ''''  ''''" + "\n"
    return result


def print_everything(message):
    result = speech_bubble(message) + "\n"
    result += arrow_to_bubble() + "\n"
    result += print_pig()

    return result
