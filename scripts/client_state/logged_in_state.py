import re


class LoggedInState():

    def __init__(self):
        # Format: `Game_ID:<GameId>`
        # Example: `Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002`
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')
        self._game_id = ''

        # Format: `START:<GameID>`
        # Example: `START:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005`
        self._start_pattern = re.compile(r'^START:([0-9A-Za-z_+-]+)$')
        self._start_game_id = ''

    @property
    def name(self):
        return "<LoggedInState/>"

    @property
    def game_id(self):
        return self._game_id

    def parse_line(self, line):

        # 初期局面終了
        if line == 'END Game_Summary':
            return '<LoggedInState.EndGameSummary/>'

        # Game_ID
        matched = self._game_id_pattern.match(line)
        if matched:
            # ログイン成功
            self._game_id = matched.group(1)
            return '<LoggedInState.GameId/>'

        # START
        matched = self._start_pattern.match(line)
        if matched:
            # 対局合意成立
            self._start_game_id = matched.group(1)
            return '<LoggedInState.Start/>'

        return '<LoggedInState.Unknown>'
