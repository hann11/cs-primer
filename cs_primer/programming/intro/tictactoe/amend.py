# moves: list[int] contains the co-ord (0-8) of where the user has chosen to move. starting index and every two after are 'X' turn

MARKS = ["X", "O"]

WINNING_SETS = [
    {0, 1, 2},
    {0, 3, 6},
    {1, 4, 7},
    {2, 5, 8},
    {3, 4, 5},
    {6, 7, 8},
    {0, 4, 8},
]


def print_board(moves: list[int]):
    board = ["_" for _ in range(9)]
    for i, move in enumerate(moves):
        board[move] = MARKS[i % 2]
    print("|".join(board[:3]))
    print("|".join(board[3:6]))
    print("|".join(board[6:9]))


def check_win(moves: list[int]):
    for winning_set in WINNING_SETS:
        if len(winning_set - set(moves[::2])) == 0:
            print("Player 0 wins")
            return True
        elif len(winning_set - set(moves[1::2])) == 0:
            print("Player 1 wins")
            return True
        elif len(moves) == 9:
            print("Draw")
            return True

    return False


def move(moves: list[int]) -> list[int]:
    while True:
        coord_requested = int(input("Where to move? "))
        if coord_requested not in list(range(9)):
            print("Illegal move, not on the board. Retry")
            continue
        if coord_requested in moves:
            print("That spot is taken")
        else:
            moves.append(coord_requested)
            break

    return moves


if __name__ == "__main__":
    moves = []
    while True:
        player_to_move = len(moves) % 2
        print(
            f"Player {player_to_move}'s turn (symbol {MARKS[player_to_move]})"
        )
        move(moves)
        print_board(moves)

        if check_win(moves):
            break
