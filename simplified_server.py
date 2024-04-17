import rpyc
from rpyc.utils.server import ThreadedServer

class MyService(rpyc.Service):
    def on_connect(self, conn):
        print("Client connected.")
        # Send a message to the client after connecting
        conn.root.receive_message_from_server("Hello, client! Welcome to the server.")

    def on_disconnect(self, conn):
        print("Client disconnected.")

if __name__ == "__main__":
    server = ThreadedServer(MyService, port=18812, hostname='localhost')
    server.start()
