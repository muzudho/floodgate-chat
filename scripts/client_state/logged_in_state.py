import re


class LoggedInState():

    def __init__(self):
        # Format: `Game_ID:<GameId>`
        # Example: `Game_ID:wdoor+floodgate-300-10F+Yss1000k+e-gov-vote-kifuwarabe+20211103193002`
        self._game_id_pattern = re.compile(r'^Game_ID:([0-9A-Za-z_+-]+)$')
        self._game_id = ''

        # 先手、後手プレイヤー名判定
        # Format: Name<SenteOrGote>:<PlayerName>
        # Example: Name+:John
        # Example: Name-:e-gov-vote-kifuwarabe
        self._player_name_pattern = re.compile(
            r'^Name([+-]):([0-9A-Za-z_-]+)$')
        # プレイヤー名 [未使用, 先手プレイヤー名, 後手プレイヤー名]
        self._player_names = ['', '', '']

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

    @property
    def start_game_id(self):
        return self._start_game_id

    def parse_line(self, line):

        # 初期局面終了
        if line == 'END Game_Summary':
            return '<LoggedInState.EndGameSummary/>'

        # 先手、後手プレイヤー名
        matched = self._player_name_pattern.match(line)
        if matched:
            turn = matched.group(1)
            if turn == '+':
                self._player_names[1] = matched.group(2)
            elif turn == '-':
                self._player_names[2] = matched.group(2)
            else:
                # Error
                raise ValueError(f'ここにはこないはず')

            return '<LoggedInState.Turn/>'

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
