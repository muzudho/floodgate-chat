from scripts.log_output import LogOutput
from scripts.client_state.logged_in_state import LoggedInState
from scripts.client_state.none_state import NoneState


class ClientP():
    def __init__(self):
        self._state = NoneState()

    def listen_line(self, line):
        result = self._state.listen_line(line)

        if self._state == '[None]':
            if result == '<LoginOk>':
                self._sate = LoggedInState()
        elif self._state == '[LoggedIn]':
            if result == '<GameId>':
                # TODO AGREE 返したい
                pass
            pass
        else:
            pass

        # display_and_log_internal(result)


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.listen_line(line)
    if result == '<LoginOk>':
        print('.', end='')
    else:
        print('f', end='')
