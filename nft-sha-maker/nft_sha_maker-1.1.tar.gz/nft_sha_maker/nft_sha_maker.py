import csv
import json
import hashlib

csvfile = input("Enter the name of your CSV file: ")
jsonfile = csvfile.replace(".csv",".json")
outputfile = csvfile.replace(".csv",".output.csv")

def main():
# Read CSV File
    with open(csvfile, 'r') as file:
        reader = csv.reader(file)

        # Iterate over each row after the header in the CSV file
        header = next(reader)
        for row in reader:

            # Create a dictionary with the values
            data = dict(zip(header, row))

            # Create JSON file
            with open(jsonfile, 'a') as json_file:
                json.dump(data, json_file)
                json_file.write('\n')

# Get SHA256 Hash
    with open(jsonfile, 'rb') as f:
        data = f.read() # read the file
        for line in data:      
            sha256_hash = hashlib.sha256((line).to_bytes(8, 'big')).hexdigest()

# Append SHA256 Hash to CSV file
    with open(csvfile, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        with open(outputfile, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header + ['SHA256 Hash'])

            for row in reader:
                writer.writerow(row + [sha256_hash])


