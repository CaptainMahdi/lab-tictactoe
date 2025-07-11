from tic_tac_toe_board import TicTacToeBoard
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Move(BaseModel):
    player: str
    index: int

@app.get("/state")
async def get_state():
    board = await TicTacToeBoard.load_from_redis()
    return board.to_dict()  

@app.post("/move")
async def make_move(data: Move):
    board = await TicTacToeBoard.load_from_redis()
    result = await board.make_move(data.player, data.index)
    return result

@app.post("/reset")
async def reset():
    board = await TicTacToeBoard.load_from_redis()
    result = await board.reset()
    return result
