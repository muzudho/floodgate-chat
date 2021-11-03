import re


class ClientP():
    def __init__(self):
        # Format: `LOGIN:<username> OK`
        # Example: `LOGIN:e-gov-vote-kifuwarabe OK`
        self._login_ok_pattern = re.compile(r'^LOGIN:[0-9A-Za-z_-]{1,32} OK$')

    def lissonMessage(self, line):
        matched = self._login_ok_pattern.match(line)
        if matched:
            # ログイン成功
            return '<LoginOk>'

        return '<Unknown>'


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'

    client_p = ClientP()
    result = client_p.lissonMessage(line)
    if result == '<LoginOk>':
        print('.', end='')
    else:
        print('f', end='')
