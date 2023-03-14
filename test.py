from ms_lib import *

def main():
    print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M{colorama.Fore.RESET}.")
    mines = int(input("How many mines would you like? "))
    board = Board(mines)

    while True:
        # system("cls")
        print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M {colorama.Fore.GREEN}:){colorama.Fore.RESET}.")
        board.display()
        print()

        while True:
            player_choice = input(f"{colorama.Fore.CYAN}:{colorama.Fore.RESET}")
            
            match len(player_choice):
                case 2:
                    coord = Coord.convert_input(board, player_choice)
                    found_coords = Coord.check(board, [coord])
                    for coord in found_coords:
                        board.reveal(coord)
                    break
                case 3:
                    board.mark(Coord.convert_input(board, player_choice[0:2]))
                    break
                case _:
                    print("Invalid input!")
        
        
    
if __name__ == "__main__":
    try: colorama.just_fix_windows_console(); main() 
    except KeyboardInterrupt: print("Exiting...") 
