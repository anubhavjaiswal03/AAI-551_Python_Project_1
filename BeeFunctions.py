# Name: Anubhav Jaiswal
# Date: 27 Feb 2024
# Description:

import os
import random


def loadFlowerData(file_name: str = '') -> dict:
    """
    Continuously prompts the user for a valid file_name if it exists, processes it to a dictionary that
    contains the flower Letter as the key and the value as a tuple of the letter, name and points for that flower.
    :return: flowerData - Dictionary containing the flower data
    :rtype: dict
    """
    flowerData: dict = {}
    # file_name: str = ''

    while not os.path.exists(file_name):
        file_name = input('Please enter the name of the file containing your flower to points mapping: ')
        if not os.path.exists(file_name):
            print('\033[91;1m%s\033[0m file does not exist!' % file_name)
    flower_file = open(file_name, 'r')
    flower_file_line = flower_file.readline()
    while flower_file_line:
        flower_file_line_elements = flower_file_line.strip().split(',')
        flowerData[flower_file_line_elements[0]] = tuple(flower_file_line_elements)
        flower_file_line = flower_file.readline()
    flower_file.close()
    return flowerData


def createHiddenField(flower_data: dict, file_name: str = '') -> list:
    """
    Creates the 2D field from the valid field input file prompted to the user, returns the 2D field if all elements of
    the field have a valid symbol, valid symbols are P for Pitcher Plant, H for Hive, " " for Space, and flower symbols
    from the flowerList file.
    :param file_name: (Optional) for testing.
    :param flower_data: Dictionary containing the information of all flowers in field returned by loadFlowerData()
    :type flower_data: dict
    :return: field2D
    :rtype: list
    """
    field2D: list = []  # Builds and stores the 2D List from the field file
    # file_name: str = ''  # Variable to hold the field_file's file_name
    valid_fields: list = ["P", "H", " ", *list(flower_data.keys())]
    # A valid list of elements built from the symbols of flower_data and P, H & " ".
    # .keys() returns a dict_keys object, so we use list to type cast it to a list object
    # and * to unwrap it to individual elements.

    while not os.path.exists(file_name):
        file_name = input('Please enter the name of the file containing your field: ')
        if not os.path.exists(file_name):
            print('\033[91;1m%s\033[0m field does not exist!' % file_name)
    field_file = open(file_name, 'r')
    field_file_line = field_file.readline()

    try:
        while field_file_line:
            field_file_line_elements = field_file_line.rstrip('\n').split(',')
            # Checks validity of each element in the file:
            for element in field_file_line_elements:
                if element not in valid_fields:
                    # Raises a type error if an element is outside to the valid list of elements
                    raise TypeError('\033[91;1m%s\033[0m in file \033[91;1m%s\033[0m is not a known flower type!' % (
                        element, file_name))
            field2D.append(field_file_line_elements)
            field_file_line = field_file.readline()
    except TypeError as err:
        print(err)
        quit(1)
    except Exception as err:
        print(err)
        quit(-1)  # Quits with an Error Code 1
    else:
        return field2D
    finally:
        field_file.close()


def createVisibleField(field: list) -> list:
    """
    Creates the fog of war or the visible list where initially only the Hive is located.
    The hidden_field is passed as argument
    :param field: The 2D List field that is provided as input, usually the hidden_field is passed to create the visible_field.
    :type field: list
    :return: fog_of_war: The visible_field named so as this is what is visible to the user,
    all features except the Hive are hidden.
    :rtype: list
    """
    fog_of_war: list = []

    for line in field:
        new_line = []
        for element in line:
            if element != 'H':
                # new_line.append('\033[40m   \033[0m')
                new_line.append(' ')
            elif element == 'H':
                new_line.append('H')
        fog_of_war.append(new_line)

    return fog_of_war


def showField(field: list, line_offset: int = 4, char_offset: int = 3, start_index: int = 0):
    """
    Show the field that is the 2D List
    :param field: The 2D List field that is provided as input, usually the visible_field is passed to show to the user.
    :type field: list
    :param line_offset: (Optional) for adjusting pretty print, strongly advised to use default values.
    :type line_offset: int
    :param char_offset: (Optional) for adjusting pretty print, strongly advised to use default values.
    :type char_offset: int
    :param start_index: How the rows and columns are numbered from 0 or 1;
    :type start_index: int
    :return: None
    """
    col = start_index
    print(' ' * line_offset, end='')
    for idx in range(len(field[0])):
        print(f"{col:^{line_offset}}", end="")
        col += 1
    print()
    row = start_index
    for line in field:
        print('%2d ' % row, end='')
        for el in line:
            print(f'|{el:^{char_offset}}', end='')
        print(end='|\n')
        row += 1
    print()


def beelineIntro(flower_data: dict, total_scout_bees: int, total_worker_bees: int):
    pollen_harvested = 0
    print("Welcome to Beeline!")
    print("You are the queen bee tasked with ensuring your hive produces enough honey.")
    print("Honey is created from pollen in flowers, which you will need to send bees out to find and harvest!")
    print("You have two kinds of bees: scout bees and worker bees.")
    print("Scout bees fly out to a location in the field and reveal 3x3 area around the specified location")
    print("# Worker bees fly out to a location, harvest flowers in a 3x3 area around the specified location,")
    print("and also reveal the area they have harvested. However, you only have 5 scout bees and 5 worker")
    print("bees to obtain the 20 units of pollen you need to produce enough honey. Note, once a bee has been")
    print("sent out it cannot be used again and a flower can only be harvested once! Oh, and watch out for pitcher plants!")
    print("They'll trap your bees and prevent them from returning to the hive. Good luck!\n")
    print("The flowers contains the following units of pollen:")
    for key in list(flower_data.keys()):
        print("%s: %s, %s units of pollen" % (flower_data[key][0], flower_data[key][1], flower_data[key][2]))

    print("You have %d scout bees left, %d worker bees left, and have harvested %d units of pollen." % (
        total_scout_bees, total_worker_bees, pollen_harvested))
    print("H is the hive, U is a used flower")


def beeExplore(hidden_field: list, visible_field: list, x: int, y: int, bee_type: str, flower_data: dict) -> int:
    pollen_harvested = 0
    max_x = len(visible_field[0])
    max_y = len(visible_field)
    print(f'{(max_x, max_y) = }')
    explore_grid_coordinates = findGridCoordinates(max_x, max_y, x, y)
    for coordinates in explore_grid_coordinates:
        print(coordinates)
        if coordinates == (x, y):
            visible_field[coordinates[1]][coordinates[0]] = 'Ж'
        else:
            visible_field[coordinates[1]][coordinates[0]] = '░'
    return pollen_harvested


def findGridCoordinates(max_x: int, max_y: int, x: int, y: int) -> list:
    grid:list = []
    # assuming x, y are valid coordinates (not out of bounds of the 2D List), else this function isn't called.
    grid.append((x, y))
    if x + 1 < max_x:
        grid.append((x + 1, y))
        if y - 1 >= 0:
            grid.append((x, y - 1))
            grid.append((x + 1, y - 1))
        if y + 1 < max_y:
            grid.append((x, y + 1))
            grid.append((x + 1, y + 1))

    if x - 1 >= 0:
        grid.append((x - 1, y))
        if y - 1 >= 0:
            grid.append((x, y - 1))
            grid.append((x - 1, y - 1))
        if y + 1 < max_y:
            grid.append((x, y + 1))
            grid.append((x - 1, y + 1))

    return grid


if __name__ == '__main__':
    flowerdata: dict = loadFlowerData("flowerList1.txt")
    print(flowerdata)
    hidden_field = createHiddenField(flowerdata, "field1.csv")
    showField(hidden_field)
    visible_field = createVisibleField(hidden_field)
    showField(visible_field)

    beelineIntro(flowerdata, 5, 5)
    max_x = len(visible_field[0])
    max_y = len(visible_field)

    for x in range(0, max_x):
        for y in range(0, max_y):
            print(f'{(x, y) = }')
            visible_field = createVisibleField(hidden_field)
            beeExplore(hidden_field, visible_field, x=x, y=y, bee_type='W', flower_data=flowerdata)
            showField(visible_field)
