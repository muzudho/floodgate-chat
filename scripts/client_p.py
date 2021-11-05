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

    def listen_line(self, line):
        result = self._state.listen_line(line)

        if self._state == '[None]':
            if result == '<NoneState.LoginOk/>':
                self._state = LoggedInState()
        elif self._state == '[LoggedIn]':
            if result == '<GameId/>':
                # Game ID を取得
                self._game_id = self._sate.game_id
            elif result == '<EndGameSummary/>':
                # 常に AGREE を返します
                client_socket.send_line(f"AGREE {self._game_id}\n")
        else:
            pass

        log_output.display_and_log_internal(result)


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.listen_line(line)
    if result == '<NoneState.LoginOk/>':
        print('.', end='')
    else:
        print('f', end='')
