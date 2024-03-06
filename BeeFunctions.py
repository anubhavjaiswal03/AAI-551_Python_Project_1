# Name: Anubhav Jaiswal
# Date: 27 Feb 2024
# Description: Contains various functions for the Beeline Game, loadFlowerData() loads the data in flowerList.* files
# into a dictionary and returns it,

import os
import random


def loadFlowerData() -> dict:
    """
    Continuously prompts the user for a valid file_name if it exists, processes it to a dictionary that
    contains the flower Letter as the key and the value as a tuple of the letter, name and points for that flower.
    :return: flowerData - Dictionary containing the flower data
    :rtype: dict
    """

    flowerData: dict = {}  # Used to build the dictionary of the file
    file_name: str = ''  # Holds the flower data file's file name, (e.g. flowerList1.txt or flowerList2.txt, etc)
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
    flower_file.close()  # Closes the File
    return flowerData


def createHiddenField(flower_data: dict) -> list:
    """
    Creates the 2D field from the valid field input file prompted to the user, returns the 2D field if all elements of
    the field have a valid symbol, valid symbols are P for Pitcher Plant, H for Hive, " " for Space, and flower symbols
    from the flowerList file.
    :param flower_data: Dictionary containing the information of all flowers in field returned by loadFlowerData()
    :return: field2D
    :rtype: list
    """
    field2D: list = []  # Builds and stores the 2D List from the field file
    file_name: str = ''  # Variable to hold the field_file's file name.
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
    :return: fog_of_war: The visible_field named so as this is what is visible to the user,
    all features except the Hive are hidden.
    :rtype: list
    """
    fog_of_war: list = []  # This variable is used to build the visible_field field. visible to the user.

    for line in field:
        new_line = []  # Creating an empty List
        for element in line:
            if element != 'H':
                # new_line.append('\033[40m   \033[0m')
                new_line.append(' ')  # Ensure to add all symbols that are not H to be added as ' ' empty space
            elif element == 'H':
                new_line.append('H')  # Only symbol that is added is the 'H' or Hive symbol;
        fog_of_war.append(new_line)

    return fog_of_war


def showField(field: list):
    """
    Displays the field that is the 2D List Neatly Numbered with rows and columns starting at 0.
    :param field: The 2D List field that is provided as input, usually the visible_field is passed to show to the user.
    :type field: list
    :return: None
    """
    line_offset: int = 4  # for adjusting horizontal line number, strongly advised to use default values.
    char_offset: int = 3  # for adjusting character width, strongly advised to use default values.
    start_index: int = 0  # How the rows and columns are numbered from 0 or 1.

    col = start_index
    print(' ' * line_offset, end='')  # adjusts the columns numbering higher numbers move right.
    for idx in range(len(field[0])):
        print(f"{col:^{line_offset}}", end="")  # Printing Column Numbers
        col += 1
    print()  # Printing a newline
    row = start_index
    for line in field:
        print('%2d ' % row, end='')  # Printing Row Number
        for el in line:
            print(f'|{el:^{char_offset}}', end='')  # Printing the New character.
        print(end='|\n')  # Printing a newline
        row += 1
    print()  # print a newline after printing the entire field, Looks neat.


def beelineIntro(flower_data: dict, total_scout_bees: int, total_worker_bees: int, target_pollen: int):
    """
    Prints the introduction to the Beeline Game with some important parameters.
    :param flower_data: Dictionary containing the flower data as a view.
    :param total_scout_bees: The total number of Scout Bees you start the game with.
    :param total_worker_bees: The total number of Worker Bees you start the game with.
    :param target_pollen: The total amount of pollen needed to win the game.
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


def beeExplore(hidden_field: list, visible_field: list, bee_x: int, bee_y: int, bee_type: str,
               flower_data: dict) -> int:
    """
    This is the heart of the game, this function checks if the target bee coordinates is within the field or not, checks
    the 3x3 grid for
    :param hidden_field: Hidden field with all the locations
    :param visible_field: Field that is shown to the user
    :param bee_x: The target x location in the field entered by the user for a certain bee.
    :param bee_y: The target y location in the field entered by the user for a certain bee.
    :param bee_type: The type of bee to send out.
    :param flower_data: The flower data dictionary that contains essential information.
    :return: pollen_harvested: The amount of pollen harvested by the Worker type bee.
    """

    pollen_harvested: int = 0   # The variable to store the number of pollen harvested by a bee.
    max_x = len(visible_field[0])   # The
    max_y = len(visible_field)

    # This checks if the bee coordinates are valid.
    if bee_x >= max_x or bee_x < 0 or bee_y >= max_y or bee_y < 0:
        print("\033[91;1mOh No! Your bee has flown outside the field and gotten lost!", end='\033[0m\n')
        return pollen_harvested

    field_symbols = set()  # Used to copy all symbols under the 3x3 grid in the hidden_field
    explore_grid_coordinates = findGridCoordinates(max_x, max_y, bee_x, bee_y)  # List of 3x3 gird coordinates to search

    for coordinates in explore_grid_coordinates:
        bee_x, bee_y = coordinates  # We unwrap the coordinates tuple into x, and y variable.
        field_symbols.add(hidden_field[bee_y][bee_x])  # Creating the List of symbols

    # If the bee explores a 3x3 grid with a pitcher plant we return 0 and the grid is not revealed
    if 'P' in field_symbols:
        print("\033[91;1mSigh.... Your bee must have fallen into a pitcher plant because it never returned!",
              end='\033[0m\n')
        return pollen_harvested  # Currently it is Zero 0.

    for coordinates in explore_grid_coordinates:
        bee_x, bee_y = coordinates  # We unwrap the coordinates tuple into x, and y variable.
        if bee_type == 'W':
            if hidden_field[bee_y][bee_x] in list(flower_data.keys()):
                pollen_harvested += int(flower_data[hidden_field[bee_y][bee_x]][2])
                hidden_field[bee_y][bee_x] = 'U'  # Mark The Flower as Used if bee_type is 'W'

    return pollen_harvested


def findGridCoordinates(max_x: int, max_y: int, x: int, y: int) -> list:
    """
    Function to find the coordinates of a 3x3 grid surrounding x, y.
    :param max_x: Horizontal Length of the field
    :param max_y: Vertical Length of the field
    :param x: Target x position of Worker/Scout Bee
    :param y: Target x position of Worker/Scout Bee
    :return: grid - List containing tuples of the 3x3 grid surrounding x, y (inclusively).
    """
    temp: set = set()   # A set is used to build the grid it ensures that there are no duplicate co-ordinates.
    grid: list          # The

    # Assuming x, y are valid coordinates (not out of bounds of the 2D List), else this function isn't called.
    # WE GET THE FOLLOWING 3X3 GRID:
    # x-1, y-1      x, y-1      x+1, y-1
    # x-1, y        x, y        x+1, y
    # x-1, y+1      x, y+1      x+1, y+1

    # adding tuples to a set to avoid duplicates
    temp.add((x, y))    # (x, y) are valid co-ordinates we check them in the calling function, so we directly add them here.
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

    grid = list(temp)  # Casting to list again

    return grid


if __name__ == '__main__':
    pass
    # Test Initial Data
    # This test only tests the functionality of each method, not its flow.
    # The Code below was used for extensively testing the above functions.
    # This is the release branch hence the code is commented out.

    # harvested_pollen = 0
    # total_scouts = 5
    # total_workers = 5
    # pollen_required = 20
    # bee_type = 'S'
    # field_file_name = 'field3.csv'
    # flower_data_filename = 'flowerList3.txt'
    # print('-' * 80)
    # # --------------------------------------------------------------------------------------
    # flowerdata: dict = loadFlowerData(flower_data_filename)
    # print(flowerdata)
    # try:
    #     hidden_field = createHiddenField(flowerdata, field_file_name)
    # except TypeError as err:
    #     print(err.args[0])
    #     err.args[1].close()
    #     quit(-1)
    # showField(hidden_field)
    # visible_field = createVisibleField(hidden_field)
    # showField(visible_field)
    #
    # beelineIntro(flowerdata, total_scouts, total_workers, pollen_required)
    # max_x = len(visible_field[0])
    # max_y = len(visible_field)
    # # --------------------------------------------------------------------------------------
    # print('-' * 80)
    #
    # for x in range(-1, max_x + 1):
    #     for y in range(-1, max_y + 1):
    #         print(f'\n{bee_type = } sent to {(x, y) = }')
    #         try:
    #             hidden_field = createHiddenField(flowerdata, field_file_name)
    #         except TypeError as err:
    #             print(err.args[0])
    #             err.args[1].close()
    #             quit(-1)
    #         visible_field = createVisibleField(hidden_field)
    #         harvested_pollen = beeExplore(hidden_field, visible_field, x, y, bee_type, flowerdata, debug=True)
    #         print(f"You have {total_scouts} scout bees left, {total_workers} worker bees left, "
    #               f"and have harvested {harvested_pollen} units of pollen.")
    #         showField(visible_field)
