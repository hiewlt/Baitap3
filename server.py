import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}
lock = threading.Lock()


def broadcast(message, sender=None):
    """Gửi tin nhắn đến tất cả client đang kết nối."""
    with lock:
        recipients = [
            (client, name)
            for client, name in clients.items()
            if client != sender
        ]

    for client, name in recipients:
        try:
            client.sendall(message.encode("utf-8"))
        except OSError:
            remove_client(client)


def remove_client(client):
    """Xóa client khi ngắt kết nối."""
    with lock:
        name = clients.pop(client, None)

    try:
        client.close()
    except OSError:
        pass

    if name:
        print(f"{name} đã ngắt kết nối.")
        broadcast(f"[SERVER] {name} đã rời phòng chat.")


def handle_client(client, address):
    """Xử lý từng client bằng một thread riêng."""
    try:
        name = client.recv(1024).decode("utf-8").strip()

        if not name:
            return

        with lock:
            clients[client] = name

        print(f"{name} kết nối từ {address}")
        broadcast(f"[SERVER] {name} đã tham gia phòng chat.")

        while True:
            data = client.recv(4096)

            if not data:
                break

            message = data.decode("utf-8")
            print(f"{name}: {message}")

            broadcast(f"{name}: {message}", sender=client)

    except (ConnectionResetError, OSError):
        pass

    finally:
        remove_client(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server đang chạy tại cổng {PORT}...")
    print("Đang chờ client kết nối...")

    try:
        while True:
            client, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nĐang tắt server...")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()

