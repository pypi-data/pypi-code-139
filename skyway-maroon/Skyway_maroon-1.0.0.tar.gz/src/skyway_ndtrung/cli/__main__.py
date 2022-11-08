import skyway.cli as cli
import sys


def list_commands():
    print("\nList of commands:\n\n" + "\n".join([" " + c for c in cli.commands]) + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='skyway', description='Skyway Mater Command Caller.')
    parser.add_argument('command', type=str, nargs='?', help='skyway command name')
    parser.add_argument('-l', '--list', default=False, action='store_true', help="list all commands")
    args = parser.parse_args()
    
    if args.list or args.command is None:
        list_commands()

        

if __name__ == '__main__':
    
    
    
    if len(sys.argv)>1 and sys.argv[1][0]!='-':
        command = sys.argv[1]
        
        if command not in cli.commands:
            print("Error: unknown command [%s].\n" % (command))
            sys.argv = sys.argv[0:1] + ['--list'] 
            main()
        else:
            sys.argv = sys.argv[0:1] + sys.argv[2:]
            cli.commands[command].main()
    else:
        main()
        
    