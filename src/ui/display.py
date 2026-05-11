import os

from ..types.core import GameState


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render_board(game_state: GameState) -> None:
    snake = game_state.snake
    food = game_state.food
    width = 20
    height = 20

    board = [[" " for _ in range(width)] for _ in range(height)]

    for segment in snake.body:
        if 0 <= segment.row < height and 0 <= segment.col < width:
            board[segment.row][segment.col] = "O"

    if 0 <= food.position.row < height and 0 <= food.position.col < width:
        board[food.position.row][food.position.col] = "*"

    print("+" + "-" * width + "+")
    for row in board:
        print("|" + "".join(row) + "|")
    print("+" + "-" * width + "+")


def render_score(score: int) -> None:
    print(f"Score: {score}")


def render_game_over(score: int) -> None:
    clear_screen()
    print("GAME OVER")
    print(f"Final Score: {score}")
    print("Thanks for playing!")
