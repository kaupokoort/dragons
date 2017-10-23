from helper import TerminalFontColors
from dragons_game import DragonsOfMugloarGame
from pyfiglet import figlet_format
from termcolor import cprint


def start_game():
    valid_number = False
    while not valid_number:
        try:
            number_of_battles = int(raw_input("How many rounds would you like to play? "))
            if 0 < number_of_battles < 50:
                valid_number = True
                run_game_specified_amount_of_times(number_of_battles)
            if number_of_battles < 1:
                print(TerminalFontColors.ERROR + "Please insert a positive number.")
            if number_of_battles > 50:
                print(TerminalFontColors.ERROR + "Too many battles, please enter an integer between 1 - 50.")
        except ValueError:
            print(TerminalFontColors.ERROR + "Incorrect type, please enter an integer!")


def run_game_specified_amount_of_times(number_of_battles):
    for _ in range(number_of_battles):
        DragonsOfMugloarGame().fetch_new_game_from_api()


cprint(figlet_format('Dragons of Mugloar', font='standard'), 'yellow', attrs=['bold'])
start_game()
