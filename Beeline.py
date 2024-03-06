# Name: Anubhav Jaiswal
# Date: 27 Feb 2024
# Description: Contains the main function, also imports the BeeFunctions as bf and uses the functions defined to
# construct the game.


import BeeFunctions as bf
import random


def main():
    # Loading the flower Data
    flower_data = bf.loadFlowerData()  # Holds the flower dictionary data that contains
    # the flower name, letter and points

    # Creating the hidden field
    try:
        hidden_field = bf.createHiddenField(flower_data)  # Creates the hidden field loaded from the field file.
    except TypeError as err:
        print(err.args[0])  # Prints the error
        err.args[1].close()  # Closes the file. If the Exception occurs.
        quit(-1)  # quits with -1 error code or 255

    # Creating the Visible Field from a copy of the hidden field
    visible_field = bf.createVisibleField(hidden_field)

    # Storing the dimensions of field
    max_x = len(visible_field[0])  # Horizontal Length of the field
    max_y = len(visible_field)  # Vertical Length of the field

    # Creating Some important game variables
    total_scout_bees: int = 5  # Number of scout bees
    total_worker_bees: int = 5  # Number of worker bees
    total_pollen_harvested: int = 0  # Current harvested pollen
    TARGET_POLLEN: int = 20  # The number of pollens needed to win
    bee_type: str = ''  # Variable that holds the type of bee requested by the user.

    # Cool and funny warning messages when the bee type entered are not W or S.
    bee_type_msg = ["\033[93;1mThat's too fancy to be a bee, why dont you try W or S?\033[0m",
                    "\033[93;1mI don't think that's even a bee.\033[0m",
                    "\033[93;1mWe only have Workers or Scouts, try again with a W or S.\033[0m",
                    "\033[93;1mToo Bee or not to Bee? That was not a Bee.\033[0m",
                    "\033[93;1mNope, try again.\033[0m"]

    #
    bf.beelineIntro(flower_data, total_scout_bees, total_worker_bees, TARGET_POLLEN)

    while total_worker_bees != 0 and total_pollen_harvested <= TARGET_POLLEN:
        print("You have %d scout bees left, %d worker bees left, and have harvested %d units of pollen." % (
            total_scout_bees, total_worker_bees, total_pollen_harvested))
        print("H is the hive, U is a used flower")
        bf.showField(visible_field)

        # Prompts the user to select a bee type to send out
        bee_type = input("What type of bee would you like to send out (S for scout or W for worker): ")
        if bee_type.isalpha():
            bee_type = bee_type.upper()
        if bee_type not in ['W', 'S']:
            print(random.choice(bee_type_msg))

        if bee_type == 'S':
            if total_scout_bees > 0:
                x = int(input(f'\033[93;1m0 <= x <= {max_x - 1}\033[0m:'))
                y = int(input(f'\033[93;1m0 <= y <= {max_y - 1}\033[0m:'))
                total_scout_bees -= 1
                print("Sending out the Scout Bee")
                total_pollen_harvested += bf.beeExplore(hidden_field, visible_field, x, y, bee_type, flower_data)
            else:
                print("\033[93;1mNo more Scout Bees Left.\033[0m")

        if bee_type == 'W':
            if total_worker_bees > 0:
                x = int(input(f'\033[93;1m0 <= x <= {max_x - 1}\033[0m:'))
                y = int(input(f'\033[93;1m0 <= y <= {max_y - 1}\033[0m:'))
                total_worker_bees -= 1
                print("Sending out the Worker Bee")
                total_pollen_harvested += bf.beeExplore(hidden_field, visible_field, x, y, bee_type, flower_data)
            else:
                print('\033[93;1mNo more Worker Bees Left. \033[0m')

    if total_pollen_harvested >= 20:
        print(
            "\033[92;1mYay!! You're the Best Queen Bee! You Won!! You Collected %d pollen!!\033[0m" % total_pollen_harvested)
    else:
        print("\033[91;1mOh No!! You have been deposed\n You lost the Game!!\033[0m")

    # print("You had %d scout bees left, %d worker bees left, and had harvested %d units of pollen." % (
    #     total_scout_bees, total_worker_bees, total_pollen_harvested))
    # print("H is the hive, U is a used flower")
    # bf.showField(hidden_field)


if __name__ == '__main__':
    main()
