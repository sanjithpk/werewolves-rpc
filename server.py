from concurrent import futures

import grpc
import time
import threading
import random
import os

import werewolves_pb2 as chat
import werewolves_pb2_grpc as rpc

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        # Add more users as needed
        self.credentials = {'user1': 'pass1', 'user2': 'pass2', 'user3': 'pass3', 'user4': 'pass4', 'user5': 'pass5', 'user6': 'pass6'}
        self.wait_time = 10
        self.max_werewolves = 2
        self.chats = []
        self.werewolves_chats = []
        self.clients = {}
        self.werewolves = set()
        self.townspeople = set()
        self.game_started = False
        self.phase = 0
        self.round = 1
        self.votes = {}
        threading.Timer(self.wait_time, self.start_game).start()

    def Connect(self, request, context):
        if self.game_started: return chat.Message(message="Game has already started!")
        username = request.username
        password = request.password
        if username in self.credentials and self.credentials[username] == password:
            self.clients[username] = context
            print(f"{username} connected")
            return chat.Message(message="Connected successfully")
        else:
            return chat.Message(message="Invalid credentials")
        
    def broadcast(self, message):
        self.chats.append(chat.Message(message=message, name="Moderator"))

    def werewolves_broadcast(self, message):
        self.werewolves_chats.append(chat.Message(message=message, name="Moderator"))

    def start_game(self):
        if len(self.clients) < self.max_werewolves * 2:
            self.broadcast("Not enough players")
            self.wait(1, self.close_server)
        else:
            usernames = list(self.clients.keys())
            werewolf_usernames = random.sample(usernames, self.max_werewolves)
            for username in usernames:
                if username in werewolf_usernames:
                    self.werewolves.add(username)
                else:
                    self.townspeople.add(username)
            self.game_started = True
            self.werewolves_discussion()

    def werewolves_discussion(self):
        if self.round > 1:
            user_to_kill = self.user_to_kill()
            self.kill_user(user_to_kill)
            self.votes = {}
            self.broadcast(f"{user_to_kill} has been killed, discuss on which user to kill")
            self.is_game_over()
        self.broadcast(f"Round {self.round} has started")
        self.werewolves_broadcast(f"Night has fallen, {", ".join(self.werewolves)} are the werewolves now discuss")
        self.phase = 1
        self.wait(self.wait_time, self.werewolves_vote)
    
    def werewolves_vote(self):
        self.werewolves_broadcast("Werewolves discussion Time up, now time to vote!")
        self.phase = 2
        self.wait(self.wait_time, self.townspeople_discussion)

    def townspeople_discussion(self):
        user_to_kill = self.user_to_kill()
        self.kill_user(user_to_kill)
        self.votes = {}
        self.broadcast(f"{user_to_kill} has been killed, discuss on which user to kill")
        self.is_game_over()
        self.phase = 3
        self.wait(self.wait_time, self.townspeople_vote)

    def townspeople_vote(self):
        self.broadcast("Discussion time up, time to vote!")
        self.phase = 4
        self.wait(self.wait_time, self.werewolves_discussion)
        self.round += 1

    def is_game_over(self):
        if len(self.werewolves) == 0:
            self.broadcast("Townspeople Win")
        if len(self.townspeople) == 0:
            self.broadcast("Werewolves Win")

    def check_game_over(self, message):
        results = ["Townspeople Win", "Werewolves Win", "Not enough players"]
        if message in results:
            return True
        return False
    
    def user_to_kill(self):
        if len(self.votes) == 0: return "Nobody"
        return max(self.votes, key=self.votes.get)
    
    def kill_user(self, user):
        if user in self.clients:
            del self.clients[user]
        if user in self.werewolves:
            self.werewolves.remove(user)
        if user in self.townspeople:
            self.townspeople.remove(user)

    def close_server(self):
        os._exit(1)

    def wait(self, t, f):
        threading.Timer(t, f).start() 

    def ChatStream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        pastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while context.is_active():
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                if self.check_game_over(n.message):
                    yield n
                    self.wait(2, self.close_server)
                lastindex += 1
                yield n
            while len(self.werewolves_chats) > pastindex and request_iterator.name in self.werewolves:
                n = self.werewolves_chats[pastindex]
                pastindex += 1
                yield n
        else:
            user = request_iterator.name
            self.kill_user(user)
            print(f"{user} disconnected")

    def HandleMessage(self, request: chat.Message, context):
        """
        This method is called when a clients sends a Message to the server.

        :param request:
        :param context:
        :return:
        """
        if request.name not in self.clients:
           return chat.Empty()
        if self.phase == 1:
            print(f"[{request.name}] {request.message}")
            if request.name in self.werewolves:
                self.werewolves_chats.append(request)
        if self.phase == 2:
            if request.message in self.clients:
                self.votes[request.message] = self.votes.get(request.message, 0) + 1
        if self.phase == 3:
            print(f"[{request.name}] {request.message}")
            self.chats.append(request)
        if self.phase == 4:
            if request.message in self.clients:
                self.votes[request.message] = self.votes.get(request.message, 0) + 1
        return chat.Empty()  # something needs to be returned required by protobuf language, we just return empty msg


if __name__ == '__main__':
    port = 11912  # a random port for the server to run on
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)