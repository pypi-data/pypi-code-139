import csv
import json
import logging
import os

csv_file_name = 'alive.csv'
json_file_name = 'pos.json'


def check_path(directory):
    if directory:
        logging.debug("Entering a path")
        os.makedirs(directory, exist_ok=True)
        os.chdir(directory)


def save_csv(round_number, sheep_amount, directory):
    try:
        logging.debug("attempting to write values to the file (" + str(round_number) + ", " + str(sheep_amount) + ")")
        column_titles = ['round', 'alive']
        mode = lambda x: 'w' if (x == 1) else 'a'
        with open(csv_file_name, mode=mode(round_number), newline='') as file:
            file_writer = csv.DictWriter(file, fieldnames=column_titles)
            if round_number == 1:
                logging.info("Create a new csv file")
                check_path(directory)
                file_writer.writeheader()
            file_writer.writerow({'round': round_number, 'alive': sheep_amount})
    except IOError as e:
        logging.error("error while trying to save csv file: " + e)


def save_json(round_number, sheep_list, wolf):
    try:
        logging.debug("trying to write data to json")
        simplified_Sheep = list()
        for sheep in sheep_list:
            if sheep.isAlive:
                simplified_Sheep.append(
                    "ID: " + str(sheep.id) + ", " + str(round(sheep.coX, 3)) + ", " + str(round(sheep.coY, 3)))
            else:
                simplified_Sheep.append("ID: " + str(sheep.id) + ", NONE")
        json_message = {
            "round_number": round_number,
            "Sheep": simplified_Sheep,
            "wolf": str(wolf.coX) + ", " + str(wolf.coY)
        }

        if round_number == 1:
            logging.info("Create a new json file")
            f = open(json_file_name, "w")
        else:
            f = open(json_file_name, "a")
        f.write(json.dumps(json_message, indent=4))
        f.close()
    except IOError as e:
        logging.error("error while trying to save json file: " + e)
