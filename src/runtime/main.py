import time
from typing import Callable

from ..types.core import Direction, GameState
from ..config.settings import SPEED_DELAY
from ..service.game import (
    check_collision,
    change_direction,
    create_new_game,
    handle_food_eating,
    move_snake,
    spawn_food,
)
from ..providers.input import get_direction_input, handle_pause


def run_game(
    difficulty: str,
    clear_screen,
    render_board,
    render_score,
    render_game_over,
) -> None:
    """Main entry point that orchestrates the game."""
    if difficulty not in SPEED_DELAY:
        difficulty = "MEDIUM"
    
    game_state = create_new_game(difficulty)
    game_state = spawn_food(game_state)
    
    delay = SPEED_DELAY[difficulty]
    
    try:
        while not game_state.game_over:
            clear_screen()
            render_board(game_state)
            render_score(game_state.score)
            
            if handle_pause():
                input("Paused. Press Enter to continue...")
            
            new_direction = get_direction_input()
            if new_direction != game_state.snake.direction:
                game_state = change_direction(game_state, new_direction)
            
            game_state = move_snake(game_state)
            game_state = handle_food_eating(game_state)
            
            if check_collision(game_state):
                game_state = GameState(
                    snake=game_state.snake,
                    food=game_state.food,
                    score=game_state.score,
                    game_over=True,
                )
                continue
            
            if game_state.snake.body[0] == game_state.food.position:
                game_state = spawn_food(game_state)
            
            time.sleep(delay / 1000.0)
    except KeyboardInterrupt:
        pass
    
    clear_screen()
    render_game_over(game_state.score)


# Entry point that wires runtime with UI layer is in main.py at repo root
