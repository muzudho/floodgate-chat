from client_state.none_state import NoneState


class ClientP():
    def __init__(self):
        self._state = NoneState()

    def lisson(self, line):
        return self._state.lisson(line)


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.lisson(line)
    if result == '<LoginOk>':
        print('.', end='')
    else:
        print('f', end='')
