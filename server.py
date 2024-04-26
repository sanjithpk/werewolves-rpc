from concurrent import futures
import time
import random

import grpc
import werewolves_pb2
import werewolves_pb2_grpc
from datetime import datetime, timedelta
import threading

class WerewolvesService(werewolves_pb2_grpc.WerewolvesService):
    def __init__(self):
        self.credentials = {'user1': 'pass1', 'user2': 'pass2', 'user3': 'pass3', 'user4': 'pass4', 'user5': 'pass5'}
        self.clients = {}
        self.werewolves = set()
        self.townspeople = set()
        self.lock = threading.Lock()
        self.server_start_time = datetime.now()
        self.game_start_time = self.server_start_time + timedelta(seconds=15)
        self.werewolves_vote_time = self.game_start_time + timedelta(seconds=15)
        self.townspeople_vote_time = self.werewolves_vote_time + timedelta(seconds=15)
        self.vote = {}

    def Connect(self, request, context):
        username = request.username
        password = request.password
        if username in self.credentials and self.credentials[username] == password:
            self.clients[username] = context
            print(f"{username} connected")
            return werewolves_pb2.ConnectResponse(message="Connected successfully")
        else:
            return werewolves_pb2.ConnectResponse(message="Invalid credentials")
    
    def StartGame(self, request, context):
        time_now = datetime.now()
        wait_time = (self.game_start_time - time_now).total_seconds()
        reply = werewolves_pb2.MessageResponse()
        if wait_time < 0:
            reply.message = "Game has already started"
            return reply
        time.sleep(wait_time)
        with self.lock:
            if len(self.werewolves) == 0:
                usernames = list(self.clients.keys())
                werewolf_usernames = random.sample(usernames, 2)
                for username in usernames:
                    if username in werewolf_usernames:
                        self.werewolves.add(username)
                    else:
                        self.townspeople.add(username)
        if request.message in self.werewolves:
            reply.message = "You are the werewolves, now vote"
        else:
            reply.message = "Game has started"
        return reply
    
    def WerewolvesVote(self, request, context):
        reply = werewolves_pb2.MessageResponse()
        if request.username not in self.clients:
            reply.message = "You are already dead"
            return reply
        username = request.message
        if username in self.clients:
            self.vote[username] = self.vote.get(username, 0) + 1

        def max_vote(vote):
            return max(vote, key=vote.get)
        time_now = datetime.now()
        wait_time = (self.werewolves_vote_time - time_now).total_seconds()
        if wait_time < 0:
            reply.message = "You cannot vote anymore"
            return reply
        time.sleep(wait_time)
        print(self.vote)
        if self.vote:
            user_to_kill = max_vote(self.vote)
        else: user_to_kill = "user1"
        if user_to_kill in self.werewolves:
            self.werewolves.remove(user_to_kill)
        if user_to_kill in self.townspeople:
            self.townspeople.remove(user_to_kill)
        reply.message = f"{user_to_kill} has beeen killed"
        with self.lock:
            self.vote = {}
        return reply
    
    def TownsPeopleVote(self, request, context):
        reply = werewolves_pb2.MessageResponse()
        if request.username not in self.clients:
            reply.message = "You are already dead"
            return reply
        username = request.message
        if username in self.clients:
            self.vote[username] = self.vote.get(username, 0) + 1

        def max_vote(vote):
            return max(vote, key=vote.get)
        time_now = datetime.now()
        wait_time = (self.townspeople_vote_time - time_now).total_seconds()
        
        if wait_time < 0:
            reply.message = "You cannot vote anymore"
            return reply
        time.sleep(wait_time)
        if self.vote:
            user_to_kill = max_vote(self.vote)
        else: user_to_kill = "user1"
        if user_to_kill in self.werewolves:
            self.werewolves.remove(user_to_kill)
        if user_to_kill in self.townspeople:
            self.townspeople.remove(user_to_kill)
        reply.message = f"{user_to_kill} has beeen killed"
        self.vote = {}
        return reply
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    werewolves_pb2_grpc.add_WerewolvesServiceServicer_to_server(WerewolvesService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()