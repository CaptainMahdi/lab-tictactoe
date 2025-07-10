from dataclasses import dataclass, field

@dataclass
class TicTacToeBoard:
    state: str = field(default="is_playing")
    player_turn: str = field(default="X")
    positions: list[str] = field(default_factory= lambda: [" " for _ in range(9)])
    
    def is_my_turn(self, i_am: str):
        return self.player_turn == i_am
    def make_move(self, index:int):
        if self.state != "is_playing":
            raise ValueError("Game is not playing")
        if not (0 <= index <= 8):
            raise ValueError("Position is out of bounds")
        if self.positions[index] != " ":
            raise ValueError("Position is already taken")
        self.positions[index] = self.player_turn
        if self.check_winner() is not None:
            self.state = "is_won"
        elif self.check_draw():
            self.state = "is_draw"
        else:
            self.switch_turn()

    def switch_turn(self):
        if self.player_turn == "X":
            self.player_turn = "O"
        elif self.player_turn == "O":
            self.player_turn = "X"
    def check_winner(self):
        if self.positions[0] == self.positions[1] == self.positions[2] != " ":
            return self.positions[0]
        if self.positions[3] == self.positions[4] == self.positions[5] != " ":
            return self.positions[3]
        if self.positions[6] == self.positions[7] == self.positions[8] != " ":
            return self.positions[6]
        if self.positions[0] == self.positions[3] == self.positions[6] != " ":
            return self.positions[0]
        if self.positions[1] == self.positions[4] == self.positions[7] != " ":
            return self.positions[1]
        if self.positions[2] == self.positions[5] == self.positions[8] != " ":
            return self.positions[2]
        if self.positions[0] == self.positions[4] == self.positions[8] != " ":
            return self.positions[0]
        if self.positions[2] == self.positions[4] == self.positions[6] != " ":
            return self.positions[2]
        return None
    def check_draw(self):
        if " " not in self.positions:
            return True
        return False
    def print_board(self):
        p = self.positions
        print("\n".join([
            f"{p[0]} | {p[1]} | {p[2]}",
            "---------",
            f"{p[3]} | {p[4]} | {p[5]}",
            "---------",
            f"{p[6]} | {p[7]} | {p[8]}"
        ]))

    def play_game():
        which_one = input("X or O? ").strip().upper()
        if which_one not in ["X", "O"]:
            raise ValueError("Invalid input")
        board = TicTacToeBoard()
        board.player_turn = which_one

        while board.state == "is_playing":
            try:
                board.print_board()
                index = int(input(f"{board.player_turn}'s turn. Index? "))
                board.make_move(index)
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