from os import system
import colorama
from ms_lib import *


print(Board.TYPES)

def handle_input(Coord: Coord, player_input):
    good_letter = player_input[0].upper() in Coord.COORDS.keys()
    good_number = int(player_input[1]) in range(1, 9)
    match len(player_input):
        case 2:
            if good_letter and good_number:
                return player_input
            else:
                return -1
        case 3:
            is_mark = player_input[2].isalpha() and player_input[2].upper() == "M"
            if good_letter and good_number and is_mark:
                return player_input
            else:
                return -1
        case other:
            return -1

def main():
    while True:
        system("cls")
        print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M{colorama.Fore.RESET}.")
        
        while True:
            try:
                row_length = int(input("How many tiles per row would you like? (Standard: 10) "))
                if row_length < 3 or row_length > 25:
                    print("Invalid input!")
                    continue
                break
            except ValueError:
                print("Invalid input!")
                continue
        
        while True:
            try:
                mines = int(input("How many mines would you like? (Standard: 10) "))
                if mines < 1 or mines > row_length ** 2:
                    print("Invalid input!")
                    continue
                break
            except ValueError:
                print("Invalid input!")
                continue
        
        board = Board(row_length, mines)
        Coord = board.Coord

        while True:
            system("cls")
            print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M {colorama.Fore.GREEN}:){colorama.Fore.RESET}.")
            board.display()
            print()

            while True:
                while True:
                    player_choice = handle_input(Coord, input(f"{colorama.Fore.CYAN}:{colorama.Fore.RESET}"))
                    if not player_choice == -1:
                        break
                    else:
                        print("Invalid input!")
                
                match len(player_choice):
                    case 2:
                        coord = Coord.convert_input(board, player_choice)
                        found_coords = Coord.check(board, [coord])
                        for coord in found_coords:
                            end = board.reveal(coord)
                            if end == "GAME OVER":
                                break
                        break
                    case 3:
                        board.mark(Coord.convert_input(board, player_choice[0:2]))
                        break
                
                if end == "GAME OVER":
                    break
            if end == "GAME OVER":
                break
        play_again = input("Play again? (y/n) ")
        if play_again.lower() == "n":
            break
        
    
if __name__ == "__main__":
    try: colorama.just_fix_windows_console(); main() 
    except KeyboardInterrupt: print("Exiting...") 
