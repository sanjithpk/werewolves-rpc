from concurrent import futures
import time

import grpc
import werewolves_pb2
import werewolves_pb2_grpc
from datetime import datetime, timedelta
import threading

class WerewolvesService(werewolves_pb2_grpc.WerewolvesService):
    def __init__(self):
        self.credentials = {'user1': 'pass1', 'user2': 'pass2', 'user3': 'pass3', 'user4': 'pass4', 'user5': 'pass5'}
        self.clients = {}
        self.server_start_time = datetime.now()
        self.game_start_time = self.server_start_time + timedelta(seconds=30)

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
        print(wait_time)
        reply = werewolves_pb2.MessageResponse()
        time.sleep(wait_time)
        reply.message = "working"
        return reply
     
    def InteractiveMessage(self, request_iterator, context):
        count = 0
        for request in request_iterator:
            count += 1
            print("InteractingHello Request Made:")
            print(request)

            hello_reply = werewolves_pb2.MessageResponse()
            hello_reply.message = request.message 
            if count <= 3:
                yield hello_reply
            else:
                return hello_reply

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    werewolves_pb2_grpc.add_WerewolvesServiceServicer_to_server(WerewolvesService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()