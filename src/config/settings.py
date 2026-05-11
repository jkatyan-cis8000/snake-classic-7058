from typing import Dict

BOARD_WIDTH: int = 20
BOARD_HEIGHT: int = 20
POINTS_PER_FOOD: int = 10
DEFAULT_DIFFICULTY: str = "MEDIUM"

SPEED_DELAY: Dict[str, int] = {
    "EASY": 150,
    "MEDIUM": 100,
    "HARD": 50,
}
