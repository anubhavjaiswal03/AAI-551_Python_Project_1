# Name: Anubhav Jaiswal
# Date: 27 Feb 2024
# Description: Contains various functions for the Beeline Game, loadFlowerData() loads the data in flowerList.* files
# into a dictionary and returns it. We build a list by adding the letters to the list according to their
# frequencies keeping a count of how many letters we have added then we add one more for the letter H and
# fill the list up with blanks, then we shuffle this 1D list. We know how many black spaces to add since
# the total number of spaces = horizontal_length * vertical_length - total_number_of_letters.
# Then we splice the list row wise and save it to a file while also showing it to the user.

import os.path
from BeeFunctions import loadFlowerData  # Using the load FLowerData function to load the correct FLower Data.
import random


def fieldGenerator():
    file_name = input("Enter a suitable field filename (e.g. field4.csv): ")
    while os.path.exists(file_name):
        if os.path.exists(file_name):
            print(f'{file_name} file exists please specify another name. ', end='')
        file_name = input('Enter a suitable field filename (e.g. field4.csv): ')

    flower_data = loadFlowerData()  # Flower Data to reference when creating a new field.

    max_x = int(input('Enter the Horizontal length of the field (e.g. 10): '))
    max_y = int(input('Enter the Vertical length of the field (e.g. 10): '))

    symbol_frequency = {}  # Dictionary to store the frequency entered by the user.
    total_count = 0  # Keeps count of the total number of symbols
    temp = []

    for key in list(flower_data.keys()):
        count = int(input("Enter the count for %s (%s pts): " % (key, flower_data[key][2])))
        total_count += count
        symbol_frequency[key] = count
    count = int(input("Enter the count for P: "))
    symbol_frequency['P'] = count
    symbol_frequency['H'] = 1
    total_count += count + 1

    for i in range(0, max_x * max_y - total_count):
        temp.append(' ')

    for key in list(symbol_frequency.keys()):
        for i in range(0, symbol_frequency[key]):
            temp.append(key)

    # Randomly shuffles the whole 1D list Gives the desired randomly places effect.
    random.shuffle(temp)

    with open(file_name, 'x') as field_file:
        for i in range(max_y):
            # print(*temp[i*max_x:i*max_x+max_x], sep=',', end='\n')
            line = ','.join(
                temp[i * max_x:i * max_x + max_x])  # String and list comprehension to give the line to print.
            print(line)  # Shows the use what the file looks like.
            field_file.write(line + '\n')


if __name__ == '__main__':
    fieldGenerator()
