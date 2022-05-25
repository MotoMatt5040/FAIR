import logging

import socket
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(message)s')
file_handler = logging.FileHandler('logs\\Candle.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

# TODO Find correct Port and Address for TCP/IP

PORT = 8678
ADDR = "10.1.10.58"


def socket_ini():
    logger.info('Creating server socket...')
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind((ADDR, PORT))
        server_socket.listen(10)

        connection, addr = server_socket.accept()
        print("[INFO]\t", addr, "connected")
    except Exception as err:
        print(err)

    return connection, server_socket


def thread_candle(stop_event, data):
    logger.info(f'''Creating candle threads with the following parameters:
    Stop Event: {stop_event}
    Data: {data}''')
    msg = ""

    connection, server_socket = socket_ini()
    logger.info(f'''Connection: {connection}
    Server Socket: {server_socket}''')

    while not stop_event.is_set():
        msg = connection.recv(1024).decode()

        if "END" in msg:
            break

        try:
            temp = json.loads(msg)
            data['0'], data['1'] = temp['0'], temp['1']
        except:
            print("[INFO]\tError trying to convert to float, ignored")
            break

    logger.info(f'''Stop Event occurred. Stop Event: {stop_event}''')
    connection.close()
    server_socket.close()