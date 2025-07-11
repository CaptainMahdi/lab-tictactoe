import asyncio
from tic_tac_toe_board import TicTacToeBoard, r, PUBSUB_CHANNEL
import argparse
import json
from dataclasses import asdict

async def handle_board_state(i_am_playing: str):
    board = await TicTacToeBoard.load_from_redis()
    
    print(board.print_board())

    if board.state != "is_playing":
        print("Game over!")
        winner = board.check_winner()
        if winner:
            print(f"Player {winner} wins!")
        else:
            print("It's a draw.")
        return

    if board.is_my_turn(i_am_playing):
        try:
            index = int(input(f"Your turn, {i_am_playing}. Pick a square [0-8]: "))
            await board.make_move(i_am_playing, index)
            await r.publish(PUBSUB_CHANNEL, f"{i_am_playing} made a move.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Waiting for {board.player_turn} to move...")


async def listen_for_updates(i_am_playing: str):
    pubsub = r.pubsub()
    await pubsub.subscribe(PUBSUB_CHANNEL)

    print(f"Listening for board updates on channel '{PUBSUB_CHANNEL}'...")

    # Call once immediately
    await handle_board_state(i_am_playing)

    async for message in pubsub.listen():
        if message["type"] == "message":
            print(f"\n📢 Update received: {message['data']}")
            await handle_board_state(i_am_playing)




async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player", choices=["X", "O"], required=True)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    if args.reset:
        board = TicTacToeBoard()
        result = await board.reset()
        print(result["message"])
        return

    await listen_for_updates(args.player)

async def test():
    board = TicTacToeBoard()
    product = await board.make_move("X", 0)
    print(board.print_board())
    print(product["message"])

if __name__ == "__main__":
    asyncio.run(main())
