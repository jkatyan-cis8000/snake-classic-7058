#!/usr/bin/env python3
"""Entry point for the Snake game."""

from src.runtime.main import run_game
from src.ui.display import clear_screen, render_board, render_game_over, render_score


def main() -> None:
    """Entry point that wires runtime with UI layer."""
    run_game("MEDIUM", clear_screen, render_board, render_score, render_game_over)


if __name__ == "__main__":
    main()
