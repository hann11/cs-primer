def print_board(board: list[str]):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print(f"{board[6]} | {board[7]} | {board[8]}")


def start_choose_mark():
    while True:
        p1 = input("P1: Choose X or O: ")

        if p1 not in ["X", "O"]:
            print("ERROR: Need to choose X or O")
        else:
            break

    if p1 == "X":
        p2 = "O"
    else:
        p2 = "X"

    return {"p1": p1, "p2": p2}


def move(mark_map: dict, next_move: str, board: list[str]):
    while True:
        place = int(input(f"{next_move}, choose a spot: "))
        if place not in list(range(9)):
            print("INVALID: Choose a spot on the board")
            continue

        if board[place] == "_":
            board[place] = mark_map[next_move]
            break
        else:
            print(f"Invalid move, already taken by {board[place]}")

    return board, place


def check_winning_config(places):
    winning_configs = [
        {0, 1, 2},
        {0, 3, 6},
        {1, 4, 7},
        {2, 5, 8},
        {3, 4, 5},
        {6, 7, 8},
        {0, 4, 8},
    ]

    for player in places.keys():
        for config in winning_configs:
            if len(config.intersection(places[player])) == 3:
                print(f"{player=} wins")
                return True
    if len(places["p1"]) + len(places["p2"]) == 9:
        print("draw")
        return True
    return False


if __name__ == "__main__":
    places = {"p1": set(), "p2": set()}
    board = ["_" for i in range(9)]
    mark_map = start_choose_mark()
    print(f"{mark_map}")
    next_move = "p1"
    while True:
        board, place = move(mark_map, next_move, board)
        places[next_move].update([place])
        print_board(board)
        if check_winning_config(places):
            break
        if next_move == "p1":
            next_move = "p2"
        else:
            next_move = "p1"
