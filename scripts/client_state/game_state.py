import re


class GameState():
    """TODO `START:` してからの状態"""

    def __init__(self):
        # Format: `LOGIN:<username> OK`
        # Example: `LOGIN:e-gov-vote-kifuwarabe OK`
        self._login_ok_pattern = re.compile(r'^LOGIN:[0-9A-Za-z_-]{1,32} OK$')

    @property
    def name(self):
        return "<GameState/>"

    def parse_line(self, line):
        matched = self._login_ok_pattern.match(line)
        if matched:
            # ログイン成功
            return '<GameState.LoginOk/>'

        return '<GameState.Unknown>'


# Test
# python.exe "./scripts/client_state/none_state.py"
if __name__ == "__main__":
    line = 'LOGIN:egov-kifuwarabe OK'

    none_state = GameState()
    result = none_state.parse_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
