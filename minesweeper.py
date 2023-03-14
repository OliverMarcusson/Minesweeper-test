from ms_lib import *

def main():
    colorama.just_fix_windows_console()
    board = Board(10)

    while True:
        # system("cls")
        board.display()
        print()

        while True:
            player_choice = input(f"{colorama.Fore.CYAN}:{colorama.Fore.RESET}")
            if not len(player_choice) == 2:
                print("Invalid input!")
            else:
                break
        
        board = Coord.check(board, Coord.convert_input(board, player_choice))
    
if __name__ == "__main__":
    try: main() 
    except KeyboardInterrupt: print("Exiting..."); exit() 
