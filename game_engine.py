from tic_tac_toe_board import TicTacToeBoard

board = TicTacToeBoard()

which_one = input("X or O? ")

while board.state == "is_playing":
    if board.is_my_turn(which_one):
        try:
            index = int(input("Index? "))
            board.make_move(index)
            board.print_board()
        except ValueError:
            print("Invalid index")
        except IndexError:
            print("Index out of bounds")
        except Exception as e:
            print(e)

if board.state == "is_won":
    print(f"Player {board.check_winner()} won!")
else:
    print("Draw!")

