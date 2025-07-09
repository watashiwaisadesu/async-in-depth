import select
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()
print('[INIT] Сервер запущен и слушает порт 5000')
print("server_socket:", server_socket)

to_monitor = []

def accept_connection(server_socket):
    print('[EVENT] Готов к принятию нового соединения...')
    client_socket, addr = server_socket.accept()
    print(f'[CONNECT] Новое соединение от {addr}')
    to_monitor.append(client_socket)
    print(f'[INFO] Клиентский сокет добавлен в to_monitor. Сейчас следим за {len(to_monitor)} сокет(ами).')

def send_message(client_socket):
    print('[EVENT] Готов к чтению данных от клиента...')
    try:
        request = client_socket.recv(4096)
        print(f'[RECEIVED] Получено сообщение: {request.decode().strip()}')
        if request:
            response = 'Hello world\n'.encode()
            client_socket.send(response)
            print('[SENT] Отправлен ответ клиенту.')
        else:
            print('[INFO] Клиент закрыл соединение.')
    except ConnectionResetError:
        print('[ERROR] Соединение было сброшено клиентом.')
    except Exception as e:
    # finally:
        client_socket.close()
        to_monitor.remove(client_socket)
        print('[CLOSE] Соединение закрыто и удалено из списка наблюдения.')

def event_loop():
    print('[LOOP] Запуск событийного цикла...')
    while True:
        print(f'[WAIT] Ожидание активности на {len(to_monitor)} сокет(ах)...')
        print("to_monitor:", to_monitor)
        ready_to_read, _, _ = select.select(to_monitor, [], [])
        print("ready_to_read:", type(ready_to_read))
        for sock in ready_to_read:
            print("sock:", type(sock),sock)
            if sock == server_socket:
                print('[SELECT] Событие на серверном сокете — новое подключение.')
                accept_connection(sock)
            else:
                print('[SELECT] Событие на клиентском сокете — сообщение от клиента.')
                send_message(sock)

if __name__ == '__main__':
    to_monitor.append(server_socket)
    print('[START] Серверный сокет добавлен в список наблюдения.')
    event_loop()
