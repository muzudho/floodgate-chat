from client_state.none_state import NoneState


class ClientP():
    def __init__(self):
        self._state = NoneState()

    def listen_line(self, line):
        result = self._state.listen_line(line)

        if self._state == '[None]':
            if result == '<LoginOk>':
                pass
        elif self._state == '[LoggedIn]':
            pass
        else:
            pass


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.listen_line(line)
    if result == '<LoginOk>':
        print('.', end='')
    else:
        print('f', end='')
