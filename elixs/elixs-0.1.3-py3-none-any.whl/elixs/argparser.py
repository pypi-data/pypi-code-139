from .colors import color

class SimpleArgParser:
    #option1 = {"Debug mode": [["+d", "enable_debug", "debug_on", 1], ["-d", "disable_debug", "debug_off", 1]]}
    #option2 = {"Django mode": [["+s", "enable_django", "django_on", 1], ["-s", "disable_django", "django_off", 1]]}
    #option3 = {"Helping mode": [["h", "help", "hilb", "halp"]]}
    #Array must contain 4 items. Fill up with a character that doesn't make sense such as 1 if your args are text
    #option1.values()[0] is enable, option1.values()[1] is disable

    def __init__(self, option1, option2 = {"":[["","","",""],["","","",""],False]}, option3 = {"":[["","","",""],["","","",""],False]}):
        global name1, name2, name3, enopt1, disopt1, enopt2, disopt2, enopt3, disopt3, def1, def2, def3
        values1 = list(option1.values())[0]
        values2 = list(option2.values())[0]
        values3 = list(option3.values())[0]

        name1 = list(option1.keys())[0]
        enopt1 = values1[0]
        disopt1 = values1[1]
        def1 = values1[2]

        if option2 != None:
            name2 = list(option2.keys())[0]
            enopt2 = values2[0]
            disopt2 = values2[1]
            def2 = values2[2]
        else:
            name2 = None
            enopt2 = None
            disopt2 = None
            def2 = False

        if option3 != None:
            name3 = list(option3.keys())[0]
            enopt3 = values3[0]
            disopt3 = values3[1]
            def3 = values3[2]
        else:
            name3 = None
            enopt3 = None
            disopt3 = None
            def3 = False


    def setargs(self, args):
        one = def1
        two = def2
        three = def3

        for arg in args:
                if arg == enopt1[0] or arg == enopt1[1] or arg == enopt1[2] or arg == enopt1[3]: 
                    color(f'{name1} enabled.', "info")
                    one = True
                elif arg == disopt1[0] or arg == disopt1[1] or arg == disopt1[2] or arg == disopt1[3]: 
                    color(f'{name1} disabled.', "info")
                    one = False
                elif arg == enopt2[0] or arg == enopt2[1] or arg == enopt2[2] or arg == enopt2[3]: 
                    color(f'{name2} enabled.', "info")
                    two = True
                elif arg == disopt2[0] or arg == disopt2[1] or arg == disopt2[2] or arg == disopt2[3]: 
                    color(f'{name2} disabled.', "info")
                    two = False
                elif arg == enopt3[0] or arg == enopt3[1] or arg == enopt3[2] or arg == enopt3[3]: 
                    color(f'{name3} enabled.', "info")
                    three = True
                elif arg == disopt3[0] or arg == disopt3[1] or arg == disopt3[2] or arg == disopt3[3]: 
                    color(f'{name3} disabled.', "info")
                    three = False
                elif arg == "default":
                    color("Default mode", "info")
                    one = def1
                    two = def2
                    three = def3
                else:
                    color("Invalid argument", "error")
                    raise ValueError("Invalid argument: " + arg) 
        return (one, two, three)
        
    def parse(self, argv, expected_args = 3):
        match len(argv):
            case 1 : one, two, three = self.setargs(["default"])
            case 2: one, two, three = self.setargs([argv[1]])
            case 3: one, two, three = self.setargs([argv[1], argv[2]])
            case 4: one, two, three = self.setargs([argv[1], argv[2], argv[3]])
            case _: color("Too many arguments", "error"); raise ValueError("Too many arguments: got " + str(len(argv) - 1) + " fromm max 3")

        match expected_args:
            case 1: return one
            case 2: return (one, two)
            case 3: return (one, two, three)
            case _: color("Invalid number of expected arguments", "error"); raise ValueError("Invalid number of expected arguments: got " + str(len(argv)) + " fromm max 3")
