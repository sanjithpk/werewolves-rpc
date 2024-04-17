import rpyc
from rpyc.utils.server import ThreadedServer
import time
from threading import Timer, Lock, Thread
import random

USER_CREDENTIALS = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3',
    'user4': 'password4',
    'user5': 'password5'
}

class MyService(rpyc.Service):
    active_users = []
    connections = {}
    lock = Lock()
    game_started = False

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

    def send_countdown(self, start_time, countdown_time):
        while time.time() - start_time < countdown_time and not self.game_started:
            remaining = countdown_time - (time.time() - start_time)
            message = f"Game starts in {int(remaining)} seconds"
            with self.lock:
                for conn in self.connections:
                    if self.connections[conn]["authenticated"]:
                        try:
                            conn.root.receive_message(message)
                        except Exception as e:
                            print(f"Error sending message: {e}")
            time.sleep(10)  # Update every 10 seconds
        self.start_game()

    def start_game(self):
        print("called")
        with self.lock:
            self.game_started = True
            if len(self.active_users) >= 2:
                werewolves = random.sample(self.active_users, 2)
            else:
                werewolves = []
            for conn in self.connections:
                print("triggered")
                if self.connections[conn]["authenticated"]:
                    try:
                        conn.root.receive_message("Game has started")
                        if self.connections[conn]["username"] in werewolves:
                            conn.root.receive_message("You are the werewolves")
                    except Exception as e:
                        print(e)

if __name__ == "__main__":
    service = MyService()
    t = Thread(target=service.send_countdown, args=(time.time(), 60))  # 60 seconds countdown
    t.start()
    server = ThreadedServer(service, port=18812, hostname='localhost')
    server.start()
