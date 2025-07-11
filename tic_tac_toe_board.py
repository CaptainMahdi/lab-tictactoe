from dataclasses import dataclass, field
import redis.asyncio as aioredis
from dotenv import load_dotenv
import os
load_dotenv("creds.env")

r = aioredis.Redis(
    host=os.getenv("HOST"),
    port=int(os.getenv("PORT")),
    password=os.getenv("PASS"),
    db=int(os.getenv("DATA")),
    decode_responses=True
)
 
PUBSUB_CHANNEL = "tictactoe:updates"



@dataclass
class TicTacToeBoard:
    state: str = field(default="is_playing")
    player_turn: str = field(default="X")
    positions: list[str] = field(default_factory= lambda: [" " for _ in range(9)])
    
    def is_my_turn(self, i_am: str) -> bool:
        if self.state == "is_playing" and self.player_turn == i_am:
            return True
        return False 
    async def make_move(self, index: int) -> None:
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
            await self.switch_turn()

        await self.save_to_redis()

    async def switch_turn(self) -> None:
        self.player_turn = "O" if self.player_turn == "X" else "X"
        await self.save_to_redis()
    def check_winner(self) -> str | None:
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
    def check_draw(self) -> bool:
        if " " not in self.positions:
            return True
        return False
    def print_board(self) -> None:
        p = self.positions
        print("\n".join([
            f"{p[0]} | {p[1]} | {p[2]}",
            "---------",
            f"{p[3]} | {p[4]} | {p[5]}",
            "---------",
            f"{p[6]} | {p[7]} | {p[8]}"
        ]))


    def serialize(self) -> dict[str, str | list[str]]:
        return {
            "state": self.state,
            "player_turn": self.player_turn,
            "positions": self.positions
        }
    async def save_to_redis(self) -> None:
        data = self.serialize()
        await r.json().set("board", ".", data)
    @classmethod
    async def load_from_redis(cls) -> "TicTacToeBoard":
        data = await r.json().get("board")
        return cls(**data)

    async def reset(self) -> None:
        self.state = "is_playing"
        self.player_turn = "X"
        self.positions = [" " for _ in range(9)]
        await self.save_to_redis()
        print("Board reset")
    def ttt_game_state_changed():
        pubsub = r.pubsub()
        pubsub.subscribe(TicTacToeBoard.PUBSUB_CHANNEL)
    def handle_board_state(i_am_playing):
        load_from_redis()
