import sys
import signal
from threading import Thread
from client import Client
from scripts.client_p import ClientP, SplitTextBlock
from scripts.log_output import log_output
from scripts.client_socket import client_socket


def test():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)
    client = Client()
    client.set_up()

    try:
        # Send `LOGIN e-gov-vote-kifuwarabe floodgate-300-10F,egov-kif`
        received = 'LOGIN:egov-kifuwarabe OK'
        client.client_p.parse_line(received)
        if client.client_p.state.name != '<LoggedInState/>':
            print('Unimplemented login')

        received = """BEGIN Game_Summary
Protocol_Version:1.2
Protocol_Mode:Server
Format:Shogi 1.0
Declaration:Jishogi 1.1
Game_ID:wdoor+floodgate-300-10F+e-gov-vote-kifuwarabe+Kristallweizen-Core2Duo-P7450+20211105220005
Name+:e-gov-vote-kifuwarabe
Name-:Kristallweizen-Core2Duo-P7450
Your_Turn:+
Rematch_On_Draw:NO
To_Move:+
Max_Moves:256
BEGIN Time
Time_Unit:1sec
Total_Time:300
Byoyomi:0
Increment:10
Least_Time_Per_Move:0
END Time
BEGIN Position
P1-KY-KE-GI-KI-OU-KI-GI-KE-KY
P2 * -HI *  *  *  *  * -KA * 
P3-FU-FU-FU-FU-FU-FU-FU-FU-FU
P4 *  *  *  *  *  *  *  *  * 
P5 *  *  *  *  *  *  *  *  * 
P6 *  *  *  *  *  *  *  *  * 
P7+FU+FU+FU+FU+FU+FU+FU+FU+FU
P8 * +KA *  *  *  *  * +HI * 
P9+KY+KE+GI+KI+OU+KI+GI+KE+KY
+
END Position
END Game_Summary
"""

        lines = SplitTextBlock(received)

        for line in lines:
            _result = client.client_p.parse_line(line)

        if client.client_p.state.name != '<GameState/>':
            print(
                f'Unimplemented begin board. client.client_p.state.name=[{client.client_p.state.name}]')

    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        client.clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


# Test
# python.exe "./scripts/client_p.py"
if __name__ == "__main__":
    """テストします"""
    sys.exit(test())
