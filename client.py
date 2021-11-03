# このファイルを直接実行したときは、以下の関数を呼び出します
import sys
import signal
from threading import Thread
from client_config import SERVER_HOST, SERVER_PORT, CLIENT_USER, CLIENT_PASS
from scripts.client_p import ClientP
from scripts.log_output import LogOutput, log_output
from scripts.client_socket import ClientSocket, client_socket


client_p = None


def listen_for_messages():
    global client_socket
    global client_p

    while True:
        message = client_socket.receive_message()

        # 1. 空行は無限に送られてくるので無視
        if message == '':
            continue

        log_output.display_and_log_receive(message)

        # Parse
        client_p.listen_line(message)


def set_up():
    global log_output
    global client_p

    print("# Set up")
    log_output.set_up()

    client_p = ClientP()


def clean_up():
    print("# Clean up")

    # Close log file
    if not(log_output is None):
        log_output.clean_up()


def run_client():
    global client_socket

    client_socket.set_up()
    client_socket.connect()

    # Hand shake
    client_socket.send_line(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

    # make a thread that listens for messages to this client & print them
    thr = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    thr.daemon = True
    # start the thread
    thr.start()

    while True:
        # input message we want to send to the server
        # 末尾に改行は付いていません
        to_send = input()

        # a way to exit the program
        if to_send.lower() == 'q':
            break

        # Send the message
        client_socket.send_line(to_send)


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
