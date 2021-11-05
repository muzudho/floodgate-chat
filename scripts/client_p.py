from scripts.client_state.logged_in_state import LoggedInState
from scripts.client_state.none_state import NoneState
from scripts.log_output import log_output
from scripts.client_socket import client_socket
from client_config import CLIENT_USER, CLIENT_PASS


class ClientP():
    def __init__(self):
        self._state = NoneState()
        self._game_id = ''

    def login(self):
        client_socket.send_line(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    def parse_line(self, line):
        print(f"parse_line: line=[{line}]")

        result = self._state.parse_line(line)
        log_output.display_and_log_internal(
            f"self._state.name=[{self._state.name}] result=[{result}]")

        if self._state.name == '<NoneState/>':
            if result == '<NoneState.LoginOk/>':
                self._state = LoggedInState()
        elif self._state.name == '<LoggedInState/>':
            if result == '<GameId/>':
                # Game ID を取得
                self._game_id = self._state.game_id
            elif result == '<EndGameSummary/>':
                # 常に AGREE を返します
                client_socket.send_line(f"AGREE {self._game_id}\n")
        else:
            pass


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.parse_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
