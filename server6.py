import rpyc
from rpyc.utils.server import ThreadedServer
import threading
import random
import time

USER_CREDENTIALS = {
    'user1': 'pass1',
    'user2': 'pass2',
    'user3': 'pass3',
    'user4': 'pass4',
    'user5': 'pass5'
}

class MyService(rpyc.Service):
    def __init__(self):
        self.active_users = {}
        self.connections = {}
        self.lock = threading.Lock()
        self.game_started = False
        self.roles = {}
        self.start_time = None
    
    def on_connect(self, conn):
        with self.lock:
            self.connections[conn] = {"username": None, "authenticated": False}

    def on_disconnect(self, conn):
        with self.lock:
            user_info = self.connections.pop(conn, None)
            if user_info and user_info["username"]:
                self.active_users.pop(user_info["username"], None)
                print(f"{user_info['username']} has disconnected")

    def exposed_login(self, username, password, conn_id):
        with self.lock:
            for conn, details in self.connections.items():
                if details.get("conn_id", None) is None:  # Assign conn_id if not already assigned
                    details["conn_id"] = conn_id
                if details["conn_id"] == conn_id:
                    if USER_CREDENTIALS.get(username) == password and username not in self.active_users:
                        details["username"] = username
                        details["authenticated"] = True
                        self.active_users[username] = conn
                        print(f"{username} is connected")
                        if not self.start_time:
                            self.start_countdown(60)  # Start countdown when first user logs in
                        return True, "You are connected to the game, waiting for other players."
                    return False, "Authentication failed or user already connected."
            return False, "Invalid connection ID."

    def start_countdown(self, duration):
        self.start_time = time.time() + duration
        threading.Timer(duration, self.check_start_game).start()

    def check_start_game(self):
        with self.lock:
            if time.time() >= self.start_time and len(self.active_users) >= 2 and not self.game_started:
                self.start_game()
            else:
                print("Not enough players to start the game or already started")

    def start_game(self):
        self.game_started = True
        self.assign_roles()
        print("Game started. Roles have been assigned and night begins.")

    def assign_roles(self):
        players = list(self.active_users.keys())
        random.shuffle(players)
        num_werewolves = max(2, len(players) // 4)
        werewolves = players[:num_werewolves]
        witch = players[num_werewolves] if len(players) > num_werewolves else None
        townspeople = players[num_werewolves + 1:]
        self.roles = {player: "Werewolf" if player in werewolves else ("Witch" if player == witch else "Townspeople") for player in players}
        for username in self.roles:
            conn = self.active_users[username]
            try:
                conn.root.exposed_receive_role(self.roles[username])
            except Exception as e:
                print(f"Failed to notify {username} of their role: {str(e)}")

if __name__ == "__main__":
    port = 18812
    server = ThreadedServer(MyService(), port=port)
    print(f"Server starting on port {port}...")
    server.start()

