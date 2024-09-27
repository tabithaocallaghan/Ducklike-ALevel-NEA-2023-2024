import random
import csv

ROWS = 150
COLS = 16

def getBlock():
    if random.randint(1,100) < 10:
        return '1'
    else:
        return '-1'
    
def generateRow():
    return ['1'] + [getBlock() for _ in range (ROWS  - 2)] + ['1']

walls = ['1'] * ROWS
level = [walls] + [generateRow() for _ in range (COLS - 2)] +[walls]

for ROWS in level:
    print('-1'.join(ROWS))

with open(f'levelnew_data.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for ROW in level:
                writer.writerow(ROW)
    
