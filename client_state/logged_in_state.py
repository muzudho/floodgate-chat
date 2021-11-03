import re


class LoggedInState():

    def __init__(self):
        # Format: `Game_ID:<GameId>`
        # Example: `Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002`
        self._game_id_pattern = re.compile(r'^Game_ID:[0-9A-Za-z_-+]+$')

    def dialog(self, line):
        # Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002
        pass

    def lisson(self, line):
        matched = self._game_id_pattern.match(line)
        if matched:
            # ログイン成功
            return '<GameId>'

        return '<Unknown>'
