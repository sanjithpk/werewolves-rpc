import rpyc
from rpyc.utils.server import ThreadedServer
import random
import threading

USER_CREDENTIALS = {
    'user1': 'pass1',
    'user2': 'pass2',
    'user3': 'pass3',
    'user4': 'pass4',
    'user5': 'pass5'
}

class WerewolfGameService(rpyc.Service):
    def __init__(self):
        self.active_users = []
        self.connections = {}
        self.game_started = False
        self.player_roles = {}
        self.lock = threading.Lock()

    def on_connect(self, conn):
        with self.lock:
            self.connections[conn] = {
                "username": None,
                "authenticated": False
            }
        print(f"New connection: {conn}")

    def on_disconnect(self, conn):
        with self.lock:
            user_data = self.connections.pop(conn, None)
            if user_data and user_data["username"]:
                self.active_users.remove(user_data["username"])
                print(f"{user_data['username']} has disconnected")

    def exposed_login(self, username, password):
        if USER_CREDENTIALS.get(username) == password:
            with self.lock:
                if username not in self.active_users:
                    for conn, user_data in self.connections.items():
                        if user_data["username"] is None:
                            user_data["username"] = username
                            user_data["authenticated"] = True
                            self.active_users.append(username)
                            print(f"{username} has logged in")
                            return True, "Logged in successfully"
                else:
                    return False, "User already logged in"
        return False, "Invalid username or password"

    def exposed_start_game(self):
        with self.lock:
            if self.game_started:
                return False, "Game has already started."
            if len(self.active_users) < 2:
                return False, f"Not enough players to start the game. Need at least 2 players, but only {len(self.active_users)} are connected."

            self.game_started = True
            werewolves = random.sample(self.active_users, 2)
            self.player_roles = {user: ("Werewolf" if user in werewolves else "Townsfolk") for user in self.active_users}
            print(f"Game started with players: {self.active_users}")
            return True, "Game started successfully!"

    def exposed_get_role(self, username):
        return self.player_roles.get(username, "No role assigned yet.")

if __name__ == "__main__":
    t = ThreadedServer(WerewolfGameService, port=18812, protocol_config={"allow_public_attrs": True})
    t.start()
