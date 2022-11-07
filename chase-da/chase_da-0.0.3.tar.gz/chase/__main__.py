import logging
import argparse
from configparser import ConfigParser

from chase.logic.gameSimulation import GameSimulation


def is_positive(value):
    local_value = int(value)
    if local_value <= 0:
        raise argparse.ArgumentTypeError("the value cannot be less than 0")
    logging.debug("the value entered: " + value + " is positive")
    return local_value


def config_parser(file):
    config = ConfigParser()
    config.read(file)
    init_pos = config.get('Terrain', 'InitPosLimit')
    sheep_mov = config.get('Movement', 'SheepMoveDist')
    wolf_move = config.get('Movement', 'WolfMoveDist')
    if float(init_pos) < 0 or float(sheep_mov) < 0 or float(wolf_move) < 0:
        logging.critical("the value cannot be less than 0")
        raise ValueError("value less than 0")
    logging.debug("parsing the configuration file")
    return float(init_pos), float(sheep_mov), float(wolf_move)


def parameter_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="an auxiliary configuration file", action='store', dest='config',
                        metavar='FILE')
    parser.add_argument('-d', '--dir', action='store', help="subdirectory where files should be placed",
                        dest='directory', metavar='DIR')
    parser.add_argument('-l', '--log', action='store', help="events logged level", dest='logger_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store', help=" the number of rounds", dest='round_number',
                        type=is_positive, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store', help="the number of sheep in a flock",
                        dest='sheep_number', type=is_positive, metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true',
                        help="if simulation should be paused at the end of each round", dest='wait')
    logging.debug("parsing args")
    return parser.parse_args()


def main():
    number_of_sheep = 15
    number_of_rounds = 50
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    directory = None
    wait = False
    args = parameter_parser()

    if args.config:
        init_pos_limit, sheep_move_dist, wolf_move_dist = config_parser(args.config)
    if args.directory:
        directory = args.directory
    if args.logger_lvl:
        if args.logger_lvl == "INFO":
            log_level = logging.INFO
        elif args.logger_lvl == "DEBUG":
            log_level = logging.DEBUG
        elif args.logger_lvl == "WARNING":
            log_level = logging.WARNING
        elif args.logger_lvl == "ERROR":
            log_level = logging.ERROR
        elif args.logger_lvl == "CRITICAL":
            log_level = logging.CRITICAL
        else:
            logging.error("login level unrecognized!")
            raise ValueError("login level unrecognized!")
        logging.basicConfig(level=log_level, filename="chase.log", force=True)
    if args.round_number:
        number_of_rounds = args.round_number
    if args.sheep_number:
        number_of_sheep = args.sheep_number
    if args.wait:
        wait = args.wait
    game = GameSimulation(init_pos_limit, number_of_sheep, sheep_move_dist, wolf_move_dist, wait, directory)
    game.start_simulation(number_of_rounds)


if __name__ == '__main__':
    main()
