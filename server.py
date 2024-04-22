import rpyc
from rpyc.utils.server import ThreadedServer
import time
from threading import Timer, Lock, Thread
import random

USER_CREDENTIALS = {
    'user1': 'pass',
    'user2': 'pass',
    'user3': 'pass',
    'user4': 'pass',
    'user5': 'pass'
}

class MyService(rpyc.Service):
    active_users = []
    connections = {}
    lock = Lock()
    game_started = False
    werewolves = []

    def on_connect(self, conn):
        # Initialize connection with placeholder data
        self.connections[conn] = {"username": None, "authenticated": False, "conn_id": None}

    def on_disconnect(self, conn):
        # Remove user from active list on disconnect
        with self.lock:
            if conn in self.connections:
                username = self.connections[conn]["username"]
                if username and username in self.active_users:
                    self.active_users.remove(username)
                    print(f"{username} has disconnected")
                del self.connections[conn]

    def exposed_login(self, username, password, conn_id):
        for conn, details in self.connections.items():
            if not details['conn_id']:  # Assign conn_id if not already assigned
                details['conn_id'] = conn_id
            if details["conn_id"] == conn_id:
                if USER_CREDENTIALS.get(username) == password and username not in self.active_users:
                    with self.lock:
                        details["username"] = username
                        details["authenticated"] = True
                        self.active_users.append(username)
                        print(f"{username} is connected")
                        return "You are connected to the game, waiting for other players."
                return "Authentication failed or user already connected."
        return "Invalid connection ID."

    def start_game(self):
        print("called")
        with self.lock:
            self.game_started = True
            if len(self.active_users) >= 2:
                self.werewolves = random.sample(self.active_users, 2)
            for conn in self.connections:
                print("triggered")
                if self.connections[conn]["authenticated"]:
                    try:
                        conn.root.receive_message("Game has started")
                        if self.connections[conn]["username"] in self.werewolves:
                            conn.root.receive_message("You are the werewolves")
                    except Exception as e:
                        print(e)

if __name__ == "__main__":
    service = MyService()
    t = Timer(60, service.start_game)
    t.start()
    server = ThreadedServer(service, port=18812, hostname='localhost')
    server.start()
