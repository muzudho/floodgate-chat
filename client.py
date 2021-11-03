# このファイルを直接実行したときは、以下の関数を呼び出します
import sys
import signal
import socket
from threading import Thread
from datetime import datetime
from client_config import SERVER_HOST, SERVER_PORT, CLIENT_USER, CLIENT_PASS
from scripts.client_p import ClientP

MESSAGE_SIZE = 1024


sock = None
log_output = None
client_p = None


def listen_for_messages():
    global sock
    global client_p

    while True:
        message = sock.recv(MESSAGE_SIZE).decode()

        # 1. 空行は無限に送られてくるので無視
        if message == '':
            continue

        display_and_log_receive(message)

        # Parse
        client_p.listen_line(message)


def set_up():
    global log_output
    global client_p

    print("# Set up")
    log_output = open("client-chat.log", "w", encoding="utf-8")
    client_p = ClientP()


def clean_up():
    print("# Clean up")

    # Close log file
    if not(log_output is None):
        log_output.close()


def date_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_receive(message):
    return f"[{date_now()}] > {message}\n"


def display_and_log_receive(text):
    s = format_receive(text)

    # Display
    print(s)

    # Log
    log_output.write(s)
    log_output.flush()


def display_and_log_internal(text):
    s = format_internal(text)

    # Display
    print(s)

    # Log
    log_output.write(s)
    log_output.flush()


def format_internal(message):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[{date_now}] : {message}\n"


def send_line(line):
    global sock
    global log_output

    # 1. Change Newline (Windows to CSA Protocol)
    if line.endswith('\r\n'):
        print('1. Change Newline (Windows to CSA Protocol)')
        line = line.rstrip('\r\n')
        line = f"{line}\n"
    elif line.endswith('\n'):
        print('1. Newline Ok')
    else:
        # コマンドラインから打鍵したときは、改行が付いていません
        print('1. Line without newline')
        line = f"{line}\n"

    # Send to server
    sock.send(line.encode())

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s = f"[{date_now}] < {line}"

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
    send_line(f"LOGIN {CLIENT_USER} {CLIENT_PASS}\n")

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
        send_line(to_send)


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
