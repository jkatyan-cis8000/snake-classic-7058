from random import randrange

from src.types.core import Direction, GameState, Position, Snake, Food
from src.config.settings import BOARD_WIDTH, BOARD_HEIGHT


def create_new_game(difficulty: str) -> GameState:
    """Create a fresh game state with default snake position and no food."""
    center_row = BOARD_HEIGHT // 2
    center_col = BOARD_WIDTH // 2
    
    snake = Snake(
        body=[
            Position(row=center_row, col=center_col),
            Position(row=center_row, col=center_col - 1),
            Position(row=center_row, col=center_col - 2),
        ],
        direction=Direction.RIGHT,
    )
    
    return GameState(
        snake=snake,
        food=Food(position=Position(row=-1, col=-1)),
        score=0,
        game_over=False,
    )


def move_snake(game_state: GameState) -> GameState:
    """Move the snake in its current direction."""
    if game_state.game_over:
        return game_state
    
    head = game_state.snake.body[0]
    direction = game_state.snake.direction
    
    new_head = Position(
        row=head.row + _get_row_delta(direction),
        col=head.col + _get_col_delta(direction),
    )
    
    new_body = [new_head] + game_state.snake.body[:-1]
    
    return GameState(
        snake=Snake(body=new_body, direction=direction),
        food=game_state.food,
        score=game_state.score,
        game_over=game_state.game_over,
    )


def handle_food_eating(game_state: GameState) -> GameState:
    """Handle eating food, growing snake, and increasing score."""
    if game_state.game_over:
        return game_state
    
    head = game_state.snake.body[0]
    food = game_state.food
    
    if head.row == food.position.row and head.col == food.position.col:
        new_body = game_state.snake.body + [food.position]
        
        return GameState(
            snake=Snake(body=new_body, direction=game_state.snake.direction),
            food=food,
            score=game_state.score + 10,
            game_over=game_state.game_over,
        )
    
    return game_state


def check_collision(game_state: GameState) -> bool:
    """Check if snake hit itself or wall."""
    head = game_state.snake.body[0]
    
    if head.row < 0 or head.row >= BOARD_HEIGHT:
        return True
    
    if head.col < 0 or head.col >= BOARD_WIDTH:
        return True
    
    for segment in game_state.snake.body[1:]:
        if head.row == segment.row and head.col == segment.col:
            return True
    
    return False


def spawn_food(game_state: GameState) -> GameState:
    """Spawn new food at a random position not occupied by snake."""
    if game_state.game_over:
        return game_state
    
    positions = _get_all_positions()
    snake_positions = set(game_state.snake.body)
    
    available = [p for p in positions if p not in snake_positions]
    
    if not available:
        return GameState(
            snake=game_state.snake,
            food=game_state.food,
            score=game_state.score,
            game_over=True,
        )
    
    new_food_position = available[randrange(len(available))]
    
    return GameState(
        snake=game_state.snake,
        food=Food(position=new_food_position),
        score=game_state.score,
        game_over=game_state.game_over,
    )


def change_direction(game_state: GameState, new_direction: Direction) -> GameState:
    """Change snake direction, preventing 180-degree turns."""
    if game_state.game_over:
        return game_state
    
    current_direction = game_state.snake.direction
    
    if _is_opposite_direction(current_direction, new_direction):
        return game_state
    
    return GameState(
        snake=Snake(body=game_state.snake.body, direction=new_direction),
        food=game_state.food,
        score=game_state.score,
        game_over=game_state.game_over,
    )


def _get_row_delta(direction: Direction) -> int:
    if direction == Direction.UP:
        return -1
    if direction == Direction.DOWN:
        return 1
    return 0


def _get_col_delta(direction: Direction) -> int:
    if direction == Direction.LEFT:
        return -1
    if direction == Direction.RIGHT:
        return 1
    return 0


def _is_opposite_direction(current: Direction, new: Direction) -> bool:
    opposites = {
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
    }
    return opposites.get(current) == new


def _get_all_positions() -> list[Position]:
    positions = []
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            positions.append(Position(row=row, col=col))
    return positions
