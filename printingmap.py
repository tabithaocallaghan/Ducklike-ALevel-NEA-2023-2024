import csv

with open('level0_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(" ".join(row))
