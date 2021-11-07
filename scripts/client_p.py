from scripts.client_state.none_state import NoneState
from scripts.client_state.logged_in_state import LoggedInState
from scripts.client_state.game_state import GameState
from scripts.log_output import log_output


def SplitTextBlock(text_block):
    """受信したテキストブロックを行の配列にして返します"""
    lines = text_block.split('\n')

    # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
    # 最後に空文字列ができます。これは無視します
    if lines[len(lines)-1] == '':
        lines = lines[:-1]

    return lines


class ClientP():
    def __init__(self):
        self._state = NoneState()
        self._game_id = ''
        self._start_game_id = ''

        def none_func():
            pass

        self._agree_func = none_func

    @property
    def state(self):
        return self._state

    @property
    def agree_func(self):
        return self._agree_func

    @agree_func.setter
    def agree_func(self, func):
        self._agree_func = func

    def parse_line(self, line):
        # print(f"parse_line: line=[{line}]")

        result = self._state.parse_line(line)
        log_output.display_and_log_internal(
            f"[DEBUG] state=[{self._state.name}] result=[{result}]")

        if self._state.name == '<NoneState/>':
            if result == '<NoneState.LoginOk/>':
                # ログインした
                self._state = LoggedInState()

        elif self._state.name == '<LoggedInState/>':
            if result == '<LoggedInState.GameId/>':
                # Game ID を取得
                self._game_id = self._state.game_id
            elif result == '<LoggedInState.EndGameSummary/>':
                # 初期局面終了
                # 常に AGREE を返します
                self._agree_func()
            elif result == '<LoggedInState.Start/>':
                # 対局成立
                self._start_game_id = self._state.start_game_id

                # 次のステートへ引継ぎ
                next_state = GameState()
                next_state.position = self._state.position
                next_state.player_names = self._state.player_names
                self._state = next_state

        elif self._state.name == '<GameState/>':
            pass

        else:
            pass
