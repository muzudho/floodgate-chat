# このファイルを直接実行したときは、以下の関数を呼び出します
import sys
import signal
import socket
from threading import Thread
from datetime import datetime
from client_config import SERVER_HOST, SERVER_PORT, CLIENT_USER, CLIENT_PASS

MESSAGE_SIZE = 1024


sock = None
log_output = None


def listen_for_messages():
    global sock

    while True:
        message = sock.recv(MESSAGE_SIZE).decode()

        # ログイン成功時
        # > LOGIN:<username> OK
        # > LOGIN:e-gov-vote-kifuwarabe OK

        # ログイン失敗時
        # > LOGIN:incorrect

        # ログアウト成功時
        # < LOGOUT
        # > LOGOUT:completed

        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        s = f"[{date_now}] > {message}\n"

        # Display
        print(s)

        # Log
        log_output.write(s)
        log_output.flush()


def set_up():
    global log_output
    print("# Set up")
    log_output = open("client-chat.log", "w", encoding="utf-8")


def clean_up():
    print("# Clean up")

    # Close log file
    if not(log_output is None):
        log_output.close()


def send_to(msg):
    global sock
    global log_output

    # Send to server
    sock.send(msg.encode())

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s = f"[{date_now}] < {msg}\n"

    # Display
    print(s)

    # Log
    log_output.write(s)
    log_output.flush()


def run_client():
    global sock

    # initialize TCP socket
    sock = socket.socket()
    # connect to the server
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    sock.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")

    # Hand shake
    send_to(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    # make a thread that listens for messages to this client & print them
    thr = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    thr.daemon = True
    # start the thread
    thr.start()

    while True:
        # input message we want to send to the server
        to_send = input()

        # a way to exit the program
        if to_send.lower() == 'q':
            break

        # Send the message
        send_to(to_send)


def main():
    def sigterm_handler(_signum, _frame) -> None:
        sys.exit(1)

    # 強制終了のシグナルを受け取ったら、強制終了するようにします
    signal.signal(signal.SIGTERM, sigterm_handler)
    set_up()
    try:
        run_client()
    finally:
        # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        clean_up()
        # 強制終了のシグナルを有効に戻します
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == "__main__":
    sys.exit(main())
