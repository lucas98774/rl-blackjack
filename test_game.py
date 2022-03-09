import pytest

from environment import Game

# TODO: move this into the format for a test using pytest 
# --- this will also require changing the code into a formal package
def test_game():
    gm = Game(repeats=1)

    # TODO: find a better way to do this --- a nonmatched except block is not good code ...
    try:
        gm.play()
    except:
        raise AssertionError("Something went wrong when playing a game")

if __name__ == '__main__':
    test_game()