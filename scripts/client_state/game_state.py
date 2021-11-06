import re
from scripts.position import Position


class GameState():
    """`START:` してからの状態"""

    def __init__(self):
        self._position = Position()

    @property
    def name(self):
        return "<GameState/>"

    @property
    def position(self):
        return self._position

    def parse_line(self, line):
        result = self._position.parse_line(line)

        if result == '<Position.Unknown/>':
            pass

        return result


# Test
# python.exe "./scripts/client_state/game_state.py"
if __name__ == "__main__":
    line = 'LOGIN:egov-kifuwarabe OK'

    none_state = GameState()
    result = none_state.parse_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
