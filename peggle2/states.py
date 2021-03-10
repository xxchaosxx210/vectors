from enum import Enum

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    LEVEL_EDITING = 2

class MenuState(Enum):
    MAIN = 0
    LEVEL_SELECT = 1
    EDIT_SELECT = 2
    POWER_SELECT = 3
    SETTINGS = 4
    CREDITS = 5

class PlayerState(Enum):
    SPAWNING_PEGS = 0
    AIMING = 1
    BALL_DROPPING = 2
    ADJUSTING_SCORE = 3
    GAME_OVER = 4

gamestate = GameState.PLAYING
menustate = MenuState.MAIN
playstate = PlayerState.SPAWNING_PEGS