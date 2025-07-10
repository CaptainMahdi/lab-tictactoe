from tic_tac_toe_board import TicTacToeBoard
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--player", type=str, choices=["X", "O"], required=False)
parser.add_argument("--reset", action="store_true")
args = parser.parse_args()

def play_game():
    if args.reset:
        board = TicTacToeBoard()
        board.reset()
        print("Game board has been reset.")
        return

    board = TicTacToeBoard.load_from_redis()

    if not board.is_my_turn(args.player):
        print(f"Not your turn. It is currently {board.player_turn}'s turn.")
        return

    board.print_board()

    try:
        index = int(input(f"Your move, {args.player}. Choose index [0-8]: "))
        board.make_move(index)
        board.save_to_redis()
        print("Move saved.")
    except ValueError as ve:
        print(f"Invalid move: {ve}")
    except Exception as e:
        print(f"Error: {e}")

    board.print_board()

    if board.state == "is_won":
        print(f"Game over. {board.check_winner()} wins!")
    elif board.state == "is_draw":
        print("Game ended in a draw.")

if __name__ == "__main__":
    play_game()
