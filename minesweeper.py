import random
from time import sleep
from os import system

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

def display_board(board, player_board):
    i = 1
    for row in board:
        print(f"{i} {row}")
        i += 1
    print("   A  B  C  D  E  F  G  H")
    print()
    
    i = 1
    for row in player_board:
        print(f"{i} {row}")
        i += 1
    print("    A    B    C    D    E    F    G    H")

def setup_board(mines: int):
    mine_coords = []
    board = []
    player_board = []
    for i in range(8):
        board.append([0, 0, 0, 0, 0, 0, 0, 0])
        player_board.append(["X", "X", "X", "X", "X", "X", "X", "X"])

    for i in range(mines):
        while True:
            coord = random.randint(0, 63) 
            row = coord // 8
            index = coord % 8
            if not board[row][index] == 1:
                # print(f"Placed mine at row {row}, coord {coord}")
                board[row][index] = 1
                mine_coords.append(coord)
                break
            else:
                pass
                # print(f"Could not place mine at row {row}, coord {coord}")

    return board, player_board, mine_coords

def reveal_coord(player_board: list, coord):
    row = coord // 8
    index = coord % 8
    player_board[row][index] = "O"
    return player_board

def hande_input(mine_coords: list, player_input: str): 
    coord = int(player_input[1]) * 8 - COORDS[player_input[0]]
    if coord in mine_coords:
        print(f"{player_input} is a mine. Game over!")
        exit()
    
    return coord

def check_nearby_mines(mine_coords: list, coord: int):
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

def check_coord(mine_coords: list, player_board: list, coord: int, reveal_coords: list=[], recursing: bool=False):
    if coord in mine_coords:
        return "MINE"

    adjacent_coords = [coord - 8, coord - 1, coord + 1, coord + 8]
    diagonal_coords = [coord - 8 - 1, coord - 8 + 1, coord + 8 - 1, coord + 8 + 1]
    
    if not recursing:
        reveal_coords.append(coord)
    
    nearby_mines = check_nearby_mines(mine_coords, coord)
    print(f"{coord} has {nearby_mines} nearby mines.")

    if nearby_mines == 0:
        if recursing:
            reveal_coords.append(coord)
        
        map(reveal_coords.append, diagonal_coords)
        map(reveal_coords.append, adjacent_coords)
    
    if nearby_mines == 0 and recursing or not recursing:
        for acoord in adjacent_coords:
            print(f"Recursing {acoord}.")
            if not acoord in reveal_coords:
                check_coord(mine_coords, player_board, acoord, reveal_coords, recursing=True)
            sleep(0.1)
    
        print(reveal_coords)
        for rcoord in reveal_coords:
            reveal_coord(player_board, rcoord)
    
    return player_board

board, player_board, mine_coords = setup_board(10)
print(mine_coords)

while True:
    # system("cls")
    for coord in range(64):
        row = coord // 8
        index = coord % 8
        nearby_mines = check_nearby_mines(mine_coords, coord)

        if nearby_mines == "MINE":
            board[row][index] = "X"
        else:
            board[row][index] = str(nearby_mines)

    display_board(board, player_board)
    print()

    while True:
        player_choice = input(":")
        if not len(player_choice) == 2:
            print("Invalid input!")
        else:
            break
    
    player_board = check_coord(mine_coords, player_board, hande_input(mine_coords, player_choice))
    
    
