from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class Position:
    row: int
    col: int


@dataclass
class Snake:
    body: list[Position]
    direction: Direction


@dataclass
class Food:
    position: Position


@dataclass
class GameState:
    snake: Snake
    food: Food
    score: int
    game_over: bool
