# このファイルを直接実行したときは、以下の関数を呼び出します
import sys
import signal
from threading import Thread
from scripts.client_p import ClientP
from scripts.log_output import log_output
from scripts.client_socket import client_socket


client_p = None


def listen_for_messages():
    global client_socket
    global client_p

    while True:
        text_block = client_socket.receive_text_block()

        # 1. 空行は無限に送られてくるので無視
        if text_block == '':
            continue

        log_output.display_and_log_receive(text_block)

        # TODO 受け取った行を、改行でスプリットできるか？
        lines = text_block.split('\n')
        for line in lines:

            # 例えば 'abc\n' を '\n' でスプリットすると 'abc' と '' になって、
            # 空文字列ができる。これは無視します
            if line == '':
                continue

            log_output.display_and_log_receive(f"<LINE>{line}</LINE>")

            # 処理は client_p に委譲します
            client_p.parse_line(line)


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
    client_p.login()

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
