import random
from time import sleep
from os import system
import colorama
import copy

class Board:
    TYPES = {
    "MINE": colorama.Fore.RED + "X" + colorama.Fore.RESET,
    "ZERO": colorama.Fore.WHITE + "0" + colorama.Fore.RESET,
    "ONE": colorama.Fore.CYAN + "1" + colorama.Fore.RESET,
    "TWO": colorama.Fore.GREEN + "2" + colorama.Fore.RESET,
    "THREE": colorama.Fore.MAGENTA + "3" + colorama.Fore.RESET,
    "FOUR": colorama.Fore.YELLOW + "4" + colorama.Fore.RESET,
    "FIVE": colorama.Fore.BLUE + "5" + colorama.Fore.RESET,
    "SIX": colorama.Fore.LIGHTBLUE_EX + "6" + colorama.Fore.RESET,
    "SEVEN": colorama.Fore.LIGHTYELLOW_EX + "7" + colorama.Fore.RESET,
    "EIGHT": colorama.Fore.LIGHTGREEN_EX + "8" + colorama.Fore.RESET,
    "MARKED": colorama.Fore.YELLOW + "M" + colorama.Fore.RESET,
    "POUND": "#"
    }
    
    def __init__(self, row_length: int, mines: int) -> None:
        self.board = []
        self.player_board = []
        self.mine_coords = []
        self.mines = mines
        self.row_length = 10
        self.Coord = Coord(self)
        self.total_coords = self.row_length ** 2
        
        for i in range(self.row_length):
            self.board.append([0 for _ in range(self.row_length)])
            self.player_board.append([Board.TYPES["POUND"] for _ in range(self.row_length)])
        
        for i in range(mines):
            while True:
                coord = random.randint(0, self.total_coords - 1) 
                row, index = self.Coord.get_row_index(coord)
                if not self.board[row][index] == 1:
                    # print(f"Placed mine at row {row}, coord {coord}")
                    self.board[row][index] = 1
                    self.mine_coords.append(coord)
                    break

        for coord in range(self.total_coords):
            row, index = self.Coord.get_row_index(coord)
            print(f"row: {row}, index: {index}, coord: {coord}")
            nearby_mines = self.Coord.nearby_mines(self.mine_coords, coord)

            match nearby_mines:
                case "MINE":
                    self.board[row][index] = Board.TYPES["MINE"]
                case 0:
                    self.board[row][index] = Board.TYPES["ZERO"]
                case 1:
                    self.board[row][index] = Board.TYPES["ONE"]
                case 2:
                    self.board[row][index] = Board.TYPES["TWO"]
                case 3:
                    self.board[row][index] = Board.TYPES["THREE"]
                case 4:
                    self.board[row][index] = Board.TYPES["FOUR"]
                case 5:
                    self.board[row][index] = Board.TYPES["FIVE"]
                case 6:
                    self.board[row][index] = Board.TYPES["SIX"]
                case 7:
                    self.board[row][index] = Board.TYPES["SEVEN"]
                case 8:
                    self.board[row][index] = Board.TYPES["EIGHT"]
                case _:
                    print(nearby_mines)
                    raise BaseException("Error: Invalid nearby_mines value!")
    
    def check_win(self):
        win_board = copy.deepcopy(self.player_board)
        
        for row in win_board:
            for index in range(len(row)):
                if row[index] == Board.TYPES["MARKED"]: row[index] = Board.TYPES["MINE"]
        
        if win_board == self.board: 
            self.player_board = self.board
            for row in self.player_board:
                for index in range(len(row)):
                    if row[index] == Board.TYPES["MINE"]: row[index] = Board.TYPES["MARKED"]
            system("cls")
            print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M {colorama.Fore.GREEN}:D{colorama.Fore.RESET}.")
            self.display()
            
            print(f"Congratulations! You won!")
            exit()

    def mark(self, coord: int):
        row, index = self.Coord.get_row_index(coord)
        if self.player_board[row][index] == Board.TYPES["POUND"]:
            self.player_board[row][index] = Board.TYPES["MARKED"]
        elif self.player_board[row][index] == Board.TYPES["MARKED"]:
            self.player_board[row][index] = Board.TYPES["POUND"]
        
        self.check_win()

    def reveal(self, coord: int, skip_check: bool = False):
        if coord in self.mine_coords and not skip_check:
            for coord in self.mine_coords:
                self.reveal(coord, True)
            system("cls")
            print(f"{colorama.Fore.YELLOW}Minesweeper{colorama.Fore.RESET}, by {colorama.Fore.CYAN}Oliver M {colorama.Fore.RED}:({colorama.Fore.RESET}.")
            self.display()
            print(f"That square contains a {colorama.Fore.RED}mine{colorama.Fore.RESET}. Game over!")
            exit()
        
        row, index = self.Coord.get_row_index(coord)
        self.player_board[row][index] = self.board[row][index]
        
        if not skip_check:
            self.check_win()
        
    
    def display(self, debug: bool = False):
        if debug:
            i = 1
            for row in self.board:
                print(f"{i} | ", flush=False, end="")
                for index in row:
                    print(f"{index} ", flush=False, end="")
                print("|", flush=True)
                i += 1
            print("    A B C D E F G H")
            print()
        
        i = 1
        for row in self.player_board:
            print(f"{i} | ", flush=False, end="")
            for index in row:
                print(f"{index} ", flush=False, end="")
            print("|", flush=True)
            i += 1
        print("    A B C D E F G H")
        print()

class Coord:
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    def __init__(self, board: Board) -> None:
        self.COORDS = {} 
        self.row_length = board.row_length
        counter = board.row_length
        for i in range(0, counter):
            self.COORDS[self.CHARS[i]] = counter
            counter -= 1

    def convert_input(self, board: Board, player_input: str): 
        coord = int(player_input[1]) * self.row_length - self.COORDS[player_input[0].upper()]
        return coord

    def nearby_mines(self, mine_coords: list, coord: int):
        if coord < 0 or coord > (self.row_length ** 2) - 1:
            return "OUT_OF_BOUNDS"
        
        if coord in mine_coords:
            return "MINE"
        
        adjacent_coords, diagonal_coords = self.get_adjacent_coords(coord)
        nearby_mines = 0
        
        for ac in adjacent_coords:
            if ac in mine_coords:
                nearby_mines += 1

        for dc in diagonal_coords:
            if dc in mine_coords:
                nearby_mines += 1

        return nearby_mines

    def get_adjacent_coords(self, coord: int):
        row, index = self.get_row_index(coord)
        match index:
            case 0:
                adjacent_coords = [coord - self.row_length, coord + 1, coord + self.row_length]
                diagonal_coords = [coord - self.row_length + 1, coord + self.row_length + 1]
            case 7:
                adjacent_coords = [coord - self.row_length, coord - 1, coord + self.row_length]
                diagonal_coords = [coord - self.row_length - 1, coord + self.row_length - 1]
            case other:
                adjacent_coords = [coord - self.row_length, coord - 1, coord + 1, coord + self.row_length]
                diagonal_coords = [coord - self.row_length - 1, coord - self.row_length + 1, coord + self.row_length - 1, coord + self.row_length + 1]
        
        return adjacent_coords, diagonal_coords
        
    def check(self, board: Board, found_coords: list):
        row, index = self.get_row_index(found_coords[0])
        
        first_coord_zero: bool = board.board[row][index] == Board.TYPES["ZERO"]
        if not first_coord_zero: return found_coords 

        old_found_coords = found_coords.copy()
        for coord in found_coords:
            adjacent_coords, diagonal_coords = self.get_adjacent_coords(coord)

            for ac in adjacent_coords:
                if ac < 0 or ac > self.row_length - 1: adjacent_coords.remove(ac); continue
                row, index = self.get_row_index(ac)
                if board.board[row][index] == Board.TYPES["ZERO"] and not ac in found_coords:
                    found_coords.append(ac)
        
        search_again = not old_found_coords == found_coords
        if search_again:
            Coord.check(board, found_coords)

        iterator = found_coords.copy()
        found_coords: set = set(found_coords)
        for coord in iterator:
            adjacent_coords, diagonal_coords = self.get_adjacent_coords(coord)
            
            for ac in adjacent_coords:
                if ac < 0 or ac > self.row_length - 1: adjacent_coords.remove(ac); continue
                found_coords.add(ac)
            
            for dc in diagonal_coords:
                if dc < 0 or dc > self.row_length - 1: diagonal_coords.remove(dc); continue
                found_coords.add(dc)
        
        return list(found_coords)
                
    def get_row_index(self, coord: int): return coord // self.row_length, coord % self.row_length
    
def main():
    print(Coord.COORDS)
    # print("You have ran the Minesweeper library module. Please run the main python file instead.")
    
if __name__ == "__main__":
    main()