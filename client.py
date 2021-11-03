# このファイルを直接実行したときは、以下の関数を呼び出します
import sys
import signal
import socket
from threading import Thread
from datetime import datetime

MESSAGE_SIZE = 1024

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "wdoor.c.u-tokyo.ac.jp"
SERVER_PORT = 4081

sock = None
out_file = None


def listen_for_messages():
    global sock

    while True:
        message = sock.recv(MESSAGE_SIZE).decode()

        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        s = f"[{date_now}] > {message}\n"

        # Display
        print(s)

        # Log
        out_file.write(s)


def set_up():
    global out_file
    out_file = open("chat.log", "w", encoding="utf-8")


def clean_up():
    if not(out_file is None):
        out_file.close()


def run_client():
    global sock

    # initialize TCP socket
    sock = socket.socket()
    # connect to the server
    print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    sock.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")

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
        sock.send(to_send.encode())

        # Log
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        out_file.write(f"[{date_now}] < {to_send}\n")


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
