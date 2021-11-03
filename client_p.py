import re

# Format: `LOGIN:<username> OK`
# Example: `LOGIN:e-gov-vote-kifuwarabe OK`
__login_ok_pattern = re.compile(r'^\s*"(\w+)": "(\w+)",$')


class ClientP():
    def __init__(self):
        pass

    def lissonMessage(msg):

        pass
