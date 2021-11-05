import re


class NoneState():
    def __init__(self):
        # Format: `LOGIN:<username> OK`
        # Example: `LOGIN:e-gov-vote-kifuwarabe OK`
        self._login_ok_pattern = re.compile(r'^LOGIN:[0-9A-Za-z_-]{1,32} OK$')

    @property
    def name(self):
        return "[None]"

    def listen_line(self, line):
        matched = self._login_ok_pattern.match(line)
        if matched:
            # ログイン成功
            return '<NoneState.LoginOk/>'

        return '<NoneState.Unknown>'
