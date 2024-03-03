# Name: Anubhav Jaiswal
# Date: 27 Feb 2024
# Description: Contains various functions for the Beeline Game, loadFlowerData() loads the data in flowerList.* files
# into a dictionary and returns it,

import os
import random


def loadFlowerData(file_name: str = '') -> dict:
    """
    Continuously prompts the user for a valid file_name if it exists, processes it to a dictionary that
    contains the flower Letter as the key and the value as a tuple of the letter, name and points for that flower.
    :param file_name: [optional] reserved for testing.
    :type file_name: str
    :return: flowerData - Dictionary containing the flower data
    :rtype: dict
    """
    flowerData: dict = {}

    while not os.path.exists(file_name):
        file_name = input('Please enter the name of the file containing your flower to points mapping: ')
        if not os.path.exists(file_name):
            print('\033[91;1m%s\033[0m file does not exist!' % file_name)
    flower_file = open(file_name, 'r')  # Opens the file for reading.
    flower_file_line = flower_file.readline()  # Reads the first Line.
    while flower_file_line:  # Keeps Reading until EOF
        flower_file_line_elements = flower_file_line.strip().split(
            ',')  # Strips the line of unwanted characters, then splits it.
        flowerData[flower_file_line_elements[0]] = tuple(
            flower_file_line_elements)  # # Creates the dictionary with tuple values.
        flower_file_line = flower_file.readline()  # Reads the next line.
    flower_file.close()
    return flowerData


def createHiddenField(flower_data: dict, file_name: str = '') -> list:
    """
    Creates the 2D field from the valid field input file prompted to the user, returns the 2D field if all elements of
    the field have a valid symbol, valid symbols are P for Pitcher Plant, H for Hive, " " for Space, and flower symbols
    from the flowerList file.
    :param file_name: [Optional] for testing.
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

    # try:
    #     while field_file_line:
    #         field_file_line_elements = field_file_line.rstrip('\n').split(',')
    #         # Checks validity of each element in the file:
    #         for element in field_file_line_elements:
    #             if element not in valid_fields:
    #                 # Raises a type error if an element is outside to the valid list of elements
    #                 raise TypeError('\033[91;1m%s\033[0m in file \033[91;1m%s\033[0m is not a known flower type!' % (
    #                     element, file_name))
    #         field2D.append(field_file_line_elements)
    #         field_file_line = field_file.readline()
    # except TypeError as err:
    #     print(err)
    #     quit(-1)
    # except Exception as err:
    #     print(err)
    #     quit(-1)  # Quits with an Error Code 1
    # else:
    #     return field2D
    # finally:
    #     field_file.close()

    while field_file_line:
        field_file_line_elements = field_file_line.rstrip('\n').split(',')
        # Checks validity of each element in the file:
        for element in field_file_line_elements:
            if element not in valid_fields:
                # Raises a type error if an element is outside to the valid list of elements,
                # we also send the file object so we can close it in the beeline function()
                raise TypeError('\033[91;1m%s\033[0m in file \033[91;1m%s\033[0m is not a known flower type!' % (
                    element, file_name), field_file)
        field2D.append(field_file_line_elements)
        field_file_line = field_file.readline()
    field_file.close()
    return field2D


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


def beelineIntro(flower_data: dict, total_scout_bees: int, total_worker_bees: int, target_pollen: int):
    """
    Prints the introduction to the Beeline Game with
    :param flower_data:
    :param total_scout_bees:
    :param total_worker_bees:
    :param target_pollen:
    :return:
    """
    print("Welcome to Beeline!")
    print("You are the queen bee tasked with ensuring your hive produces enough honey.")
    print("Honey is created from pollen in flowers, which you will need to send bees out to find and harvest!")
    print("You have two kinds of bees: scout bees and worker bees.")
    print("Scout bees fly out to a location in the field and reveal 3x3 area around the specified location")
    print("Worker bees fly out to a location, harvest flowers in a 3x3 area around the specified location,")
    print(f"and also reveal the area they have harvested. However, you only have {total_scout_bees} scout "
          f"bees and {total_worker_bees} worker")
    print(
        f"bees to obtain the {target_pollen} units of pollen you need to produce enough honey. Note, once a bee has been")
    print("sent out it cannot be used again and a flower can only be harvested once! Oh, and watch out "
          "for pitcher plants!")
    print("They'll trap your bees and prevent them from returning to the hive. Good luck!\n")
    print("The flowers contains the following units of pollen:")

    for key in list(flower_data.keys()):
        print("%s: %s, %s units of pollen" % (flower_data[key][0], flower_data[key][1], flower_data[key][2]))


def beeExplore(hidden_field: list, visible_field: list, bee_x: int, bee_y: int, bee_type: str, flower_data: dict,
               debug: bool = False) -> int:
    """
    This is the heart of the game, this function checks if the target bee coordinates is within the field or not, checks
    the 3x3 grid for
    :param hidden_field: Hidden field with all the locations
    :param visible_field: Field that is shown to the user
    :param bee_x:
    :param bee_y:
    :param bee_type:
    :param flower_data:
    :param debug:
    :return:
    """

    pollen_harvested: int = 0
    max_x = len(visible_field[0])
    max_y = len(visible_field)

    # If debug is true shows extra debug info.
    if debug:
        test_total = 0
        print(f'{(max_x, max_y) = }')

    # This checks
    if bee_x >= max_x or bee_x < 0 or bee_y >= max_y or bee_y < 0:
        print("\033[91;1mOh No! Your bee has flown outside the field and gotten lost!", end='\033[0m\n')
        return pollen_harvested

    field_symbols = set()  # Used to copy all symbols under the 3x3 grid in the hidden_field
    explore_grid_coordinates = findGridCoordinates(max_x, max_y, bee_x, bee_y)  # List of 3x3 gird coordinates to search

    for coordinates in explore_grid_coordinates:
        bee_x, bee_y = coordinates  # We unwrap the coordinates tuple into x, and y variable.

        # Extra Debug information marks the 3x3 grid with # sign --------------
        if debug:
            print(f'{(bee_x, bee_y)} = {hidden_field[bee_y][bee_x]}', end='')
            if hidden_field[bee_y][bee_x] in list(flower_data.keys()):
                test_total += int(flower_data[hidden_field[bee_y][bee_x]][2])
                print(f' : {flower_data[hidden_field[bee_y][bee_x]][2]}')
            else:
                print()
        # ---------------------------------------------------------------------
        field_symbols.add(hidden_field[bee_y][bee_x])  # Creating the List of symbols

    # If the bee explores a 3x3 grid with a pitcher plant we return 0 and the grid is not revealed
    if 'P' in field_symbols:
        print("\033[91;1mSigh.... Your bee must have fallen into a pitcher plant because it never returned!",
              end='\033[0m\n')
        return pollen_harvested

    # Extra debug info
    if debug:
        print("Possible Pollen Harvest : %d" % test_total)

    for coordinates in explore_grid_coordinates:
        bee_x, bee_y = coordinates  # We unwrap the coordinates tuple into x, and y variable.
        if bee_type == 'W':
            if hidden_field[bee_y][bee_x] in list(flower_data.keys()):
                pollen_harvested += int(flower_data[hidden_field[bee_y][bee_x]][2])
                hidden_field[bee_y][bee_x] = 'U'  # Mark The Flower as Used if bee_type is 'W'
        if not debug:
            visible_field[bee_y][bee_x] = hidden_field[bee_y][bee_x]  # Reveal the location of the flowers.
        else:
            visible_field[bee_y][bee_x] = '#'

    return pollen_harvested


def findGridCoordinates(max_x: int, max_y: int, x: int, y: int) -> list:
    """
    Function to find the coordinates of a 3x3 grid surrounding x, y:
    :param max_x: Horizontal Length of the field
    :type max_x: int
    :param max_y: Vertical Length of the field
    :type max_y: int
    :param x: Target x position of Worker/Scout Bee
    :type x: int
    :param y: Target x position of Worker/Scout Bee
    :type y: int
    :return: grid - List containing tuples of the 3x3 grid surrounding x, y (inclusively).
    :rtype: list
    """
    temp: set = set()
    grid: list
    # Assuming x, y are valid coordinates (not out of bounds of the 2D List), else this function isn't called.
    # WE GET THE FOLLOWING 3X3 GRID:
    # x-1, y-1      x, y-1      x+1, y-1
    # x-1, y        x, y        x+1, y
    # x-1, y+1      x, y+1      x+1, y+1

    # adding tuples to a set to avoid duplicates
    temp.add((x, y))
    if x + 1 < max_x:
        temp.add((x + 1, y))
        if y - 1 >= 0:
            temp.add((x, y - 1))
            temp.add((x + 1, y - 1))
        if y + 1 < max_y:
            temp.add((x, y + 1))
            temp.add((x + 1, y + 1))

    if x - 1 >= 0:
        temp.add((x - 1, y))
        if y - 1 >= 0:
            temp.add((x, y - 1))
            temp.add((x - 1, y - 1))
        if y + 1 < max_y:
            temp.add((x, y + 1))
            temp.add((x - 1, y + 1))

    # Earlier logic produced duplicates so, creating sets to avoid duplicates.
    grid = list(temp)  # Casting to list again

    return grid


if __name__ == '__main__':
    # Test Initial Data
    # This test only tests the functionality of each method, not its flow.
    harvested_pollen = 0
    total_scouts = 5
    total_workers = 5
    pollen_required = 20
    bee_type = 'S'
    field_file_name = 'field3.csv'
    flower_data_filename = 'flowerList3.txt'
    print('-' * 80)
    # --------------------------------------------------------------------------------------
    flowerdata: dict = loadFlowerData(flower_data_filename)
    print(flowerdata)
    try:
        hidden_field = createHiddenField(flowerdata, field_file_name)
    except TypeError as err:
        print(err.args[0])
        err.args[1].close()
        quit(-1)
    showField(hidden_field)
    visible_field = createVisibleField(hidden_field)
    showField(visible_field)

    beelineIntro(flowerdata, total_scouts, total_workers, pollen_required)
    max_x = len(visible_field[0])
    max_y = len(visible_field)
    # --------------------------------------------------------------------------------------
    print('-' * 80)

    for x in range(-1, max_x + 1):
        for y in range(-1, max_y + 1):
            print(f'\n{bee_type = } sent to {(x, y) = }')
            try:
                hidden_field = createHiddenField(flowerdata, field_file_name)
            except TypeError as err:
                print(err.args[0])
                err.args[1].close()
                quit(-1)
            visible_field = createVisibleField(hidden_field)
            harvested_pollen = beeExplore(hidden_field, visible_field, x, y, bee_type, flowerdata, debug=True)
            print(f"You have {total_scouts} scout bees left, {total_workers} worker bees left, "
                  f"and have harvested {harvested_pollen} units of pollen.")
            showField(visible_field)
