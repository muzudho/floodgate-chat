from scripts.client_state.none_state import NoneState
from scripts.client_state.logged_in_state import LoggedInState
from scripts.client_state.game_state import GameState
from scripts.log_output import log_output
from scripts.client_socket import client_socket
from client_config import CLIENT_USER, CLIENT_PASS


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

    @property
    def state(self):
        return self._state

    def login(self):
        client_socket.send_line(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    def parse_line(self, line):
        print(f"parse_line: line=[{line}]")

        result = self._state.parse_line(line)
        log_output.display_and_log_internal(
            f"self._state.name=[{self._state.name}] result=[{result}]")

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
                client_socket.send_line(f"AGREE {self._game_id}\n")
            elif result == '<LoggedInState.Start/>':
                # 対局成立
                self._start_game_id = self._state.start_game_id
                self._state = GameState()

        elif self._state.name == '<GameState/>':
            pass

        else:
            pass
