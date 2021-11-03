import re

# Format: `LOGIN:<username> OK`
# Example: `LOGIN:e-gov-vote-kifuwarabe OK`
__login_ok_pattern = re.compile(r'^LOGIN:[0-9A-Za-z_-]{1,32} OK$')


class ClientP():
    def __init__(self):
        pass

    def lissonMessage(self, line):
        matched = __login_ok_pattern.match(line)
        if matched:
            # ログイン成功
            return '<LoginOk>'

        return '<Unknown>'


if __name__ == "__main__":
    """テストします"""
    line = 'LOGIN:egov-kifuwarabe OK'
    matched = __login_ok_pattern.match(line)
    if matched:
        print('.', end='')
    else:
        print('f', end='')
