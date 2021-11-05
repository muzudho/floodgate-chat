import re


class LoggedInState():

    def __init__(self):
        # Format: `Game_ID:<GameId>`
        # Example: `Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002`
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')
        self._game_id = ''

    @property
    def name(self):
        return "<LoggedIn/>"

    @property
    def game_id(self):
        return self._game_id

    def listen_line(self, line):

        if line == 'END Game_Summary':
            return '<EndGameSummary/>'

        matched = self._game_id_pattern.match(line)
        if matched:
            # ログイン成功
            self._game_id = matched.group(1)
            return '<GameId/>'

        return '<LoggedInState.Unknown>'
