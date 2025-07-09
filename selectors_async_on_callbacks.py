import selectors
import socket

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    print('[INIT] Сервер слушает порт 5000')
    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
    )

    print(f'[DEBUG] Зарегистрирован server_socket: {server_socket}')
    print_current_selector_state()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'[NEW] Подключился клиент: {addr}')
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )
    print(f'[DEBUG] Зарегистрирован client_socket: {client_socket}')
    print_current_selector_state()


def send_message(client_socket):
    try:
        data = client_socket.recv(4096)
        if data:
            print(f'[DATA] Клиент прислал: {data.decode().strip()}')
            response = 'Hello world\n'.encode()
            client_socket.send(response)
            print('[SEND] Ответ отправлен клиенту')
        else:
            print('[CLOSE] Клиент закрыл соединение')
            selector.unregister(client_socket)
            client_socket.close()
    except ConnectionResetError:
        print('[ERROR] Клиент внезапно отключился')
        selector.unregister(client_socket)
        client_socket.close()
    except Exception as e:
        print(f'[ERROR] {e}')
        selector.unregister(client_socket)
        client_socket.close()


def event_loop():
    print('[LOOP] Запускаем главный событийный цикл...')
    while True:
        print('[WAIT] Ждём активности на сокетах...')
        events = selector.select(timeout=None)

        print(f'[INFO] selector.select() вернул {len(events)} событие(й)')
        for key, mask in events:
            print(f'[DEBUG] SelectorKey: {key}')
            print(f'        fileobj: {key.fileobj}')
            print(f'        fd:      {key.fd}')
            print(f'        events:  {key.events}')
            print(f'        data:    {key.data}')
            print(f'        mask:    {mask}')
            print('-------------------------------------------')

            callback = key.data
            sock = key.fileobj
            callback(sock)


def print_current_selector_state():
    print('[STATE] Текущий список зарегистрированных сокетов:')
    for key in selector.get_map().values():
        print(f'   - fd={key.fd}, obj={key.fileobj}, callback={key.data}')
    print('-------------------------------------------')


if __name__ == '__main__':
    server()
    event_loop()
