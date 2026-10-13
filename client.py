import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


def receive_messages(client):
    """Nhận tin nhắn từ server."""
    try:
        while True:
            data = client.recv(4096)

            if not data:
                break

            print("\n" + data.decode("utf-8"))

    except OSError:
        pass

    finally:
        print("\nĐã mất kết nối với server.")


def start_client():
    HOST = input("Nhập IP server : ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    name = input("Nhập tên của bạn: ").strip()
    
    if not name:
            name = "Anonymous"
    try:
        client.connect((HOST, PORT))

        client.sendall(name.encode("utf-8"))

        print("Đã kết nối đến server.")
        print("Nhập /exit để thoát phòng chat.\n")

        thread = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )

        thread.start()

        while True:
            message = input()

            if message.lower() == "/exit":
                break

            client.sendall(message.encode("utf-8"))

    except ConnectionRefusedError:
        print("Không thể kết nối. Hãy kiểm tra server.")

    except OSError as error:
        print(f"Lỗi kết nối: {error}")

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
