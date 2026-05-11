from src.types.core import Direction


def get_direction_input() -> Direction:
    """Read keyboard input and return the selected direction."""
    try:
        import keyboard
        
        if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
            return Direction.UP
        elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
            return Direction.DOWN
        elif keyboard.is_pressed('left') or keyboard.is_pressed('a'):
            return Direction.LEFT
        elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
            return Direction.RIGHT
    except ImportError:
        pass
    
    return Direction.UP


def handle_pause() -> bool:
    """Check if pause was requested."""
    try:
        import keyboard
        return keyboard.is_pressed('p') or keyboard.is_pressed('escape')
    except ImportError:
        return False


def get_difficulty_selection() -> str:
    """Get difficulty selection from user."""
    try:
        import keyboard
        
        if keyboard.is_pressed('1'):
            return 'easy'
        elif keyboard.is_pressed('2'):
            return 'medium'
        elif keyboard.is_pressed('3'):
            return 'hard'
    except ImportError:
        pass
    
    return 'medium'
