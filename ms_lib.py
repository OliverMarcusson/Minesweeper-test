import random
from time import sleep
from os import system
import colorama

class Board:
    def __init__(self, mines: int) -> None:
        self.board = []
        self.player_board = []
        self.mine_coords = []
        self.mines = mines
        
        for i in range(8):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0])
            self.player_board.append(["#", "#", "#", "#", "#", "#", "#", "#"])
        
        for i in range(mines):
            while True:
                coord = random.randint(0, 63) 
                row, index = Coord.get_row_index(coord)
                if not self.board[row][index] == 1:
                    # print(f"Placed mine at row {row}, coord {coord}")
                    self.board[row][index] = 1
                    self.mine_coords.append(coord)
                    break
                else:
                    pass
                    # print(f"Could not place mine at row {row}, coord {coord}")

        for coord in range(64):
            row, index = Coord.get_row_index(coord)
            nearby_mines = Coord.nearby_mines(self.mine_coords, coord)

            if nearby_mines == "MINE":
                self.board[row][index] = colorama.Fore.RED + "X" + colorama.Fore.RESET
            else:
                self.board[row][index] = str(nearby_mines)
    
    def display(self):
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
    COORDS = {
    "A": 8,
    "B": 7,
    "C": 6,
    "D": 5,
    "E": 4,
    "F": 3,
    "G": 2,
    "H": 1,
    }
    
    def reveal(board: Board, coord: int):
        row, index = Coord.get_row_index(coord)
        board.player_board[row][index] = board.board[row][index]
        return board

    def convert_input(board: Board, player_input: str): 
        coord = int(player_input[1]) * 8 - Coord.COORDS[player_input[0]]
        if coord in board.mine_coords:
            print(f"{player_input} is a mine. Game over!")
            exit()
        
        return coord

    def nearby_mines(mine_coords: list, coord: int):
        if coord < 0 or coord > 63:
            return "OUT_OF_BOUNDS"
        
        if coord in mine_coords:
            return "MINE"
        
        if coord % 8 == 0:
            adjacent_coords = [coord - 8, coord + 8]
            diagonal_coords = [coord - 8 + 1, coord + 8 + 1]
        elif coord % 8 == 7:
            adjacent_coords = [coord - 8, coord + 8]
            diagonal_coords = [coord - 8 - 1, coord + 8 - 1]
        else:
            adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
            diagonal_coords = [coord - 8 - 1, coord - 8 + 1, coord + 8 - 1, coord + 8 + 1]
        
        nearby_mines = 0
        
        for ac in adjacent_coords:
            if ac in mine_coords:
                nearby_mines += 1

        for dc in diagonal_coords:
            if dc in mine_coords:
                nearby_mines += 1

        return nearby_mines

    def find_adjacent_zeroes(board: Board, coord: int, found_coords: list=[]):
        to_search = []
        old_found = found_coords.copy()
        row, index = Coord.get_row_index(coord)
        match index:
            case 0:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 + 1, coord + 8 + 1]
            case 7:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 - 1, coord + 8 - 1]
            case other:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 - 1, coord - 8 + 1, coord + 8 - 1, coord + 8 + 1]
        
        for ac in adjacent_coords:
            row, index = Coord.get_row_index(ac)
            if board.board[row][index] == "0":
                if not ac in found_coords:
                    to_search.append(ac)
                    found_coords.append(ac)
        
        if len(to_search) == 0:
            return found_coords
        else:
            print(f"To search: {to_search}")
            for tc in to_search:
                found_coords = Coord.find_adjacent_zeroes(board, tc, found_coords)
                sleep(0.1)
    
    def check(board: Board, coord: int, reveal_coords: list=[], recursing: bool=False, to_recurse: list=[]):
        print(reveal_coords)
        row, index = Coord.get_row_index(coord)
        print(f"Checking{' recursing' if recursing else ''} {coord} at row {row}, index {index}.")
        if coord in board.mine_coords:
            return "MINE"

        match index:
            case 0:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 + 1, coord + 8 + 1]
            case 7:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 - 1, coord + 8 - 1]
            case other:
                adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
                diagonal_coords = [coord - 8 - 1, coord - 8 + 1, coord + 8 - 1, coord + 8 + 1]
        
        if not recursing:
            reveal_coords.append(coord)
            adjacent_zeroes: list = Coord.find_adjacent_zeroes(coord)
            for adjacent in adjacent_zeroes:
                reveal_coords.append(adjacent)
            
        if board.board[row][index] == "0":
            print(f"Coord {coord} at row {row}, index {index} is zero.")
            if recursing:
                reveal_coords.append(coord)
            
        else:
            print(f"Coord {coord} at row {row}, index {index} is not zero, it's {board.board[row][index]}.")
        
        recursing_zeroed_coord = board.board[row][index] == "0" and recursing
        
        if recursing_zeroed_coord or not recursing:
            for acoord in adjacent_coords:
                if not acoord in reveal_coords:
                    to_recurse.append(acoord)
                
                Coord.check(board, acoord, reveal_coords, recursing=True)
                sleep(0.1)
        
            for rcoord in reveal_coords:
                board = Coord.reveal(board, rcoord)
        
        return board
    
    def get_row_index(coord: int): return coord // 8, coord % 8
    
def main():
    system("python minesweeper.py")
    
if __name__ == "__main__":
    main()