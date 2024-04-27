import werewolves_pb2
import werewolves_pb2_grpc
import grpc
import argparse
import time
import sys

def main(username, password):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesServiceStub(channel)
        req = werewolves_pb2.ConnectRequest(username=username, password=password)
        res = stub.Connect(req)
        print(res)

        req = werewolves_pb2.MessageRequest(username=username, message=username)
        res = stub.StartGame(req)
        if res.message == "Game has already started":
            print(res)
            return
        
        def round(n, res, role):
            print(f"Round {n}")
            if res.message.startswith("Game has started,") or role == 1:
                role = 1
                vote = input("Game has started, you are the werewolf, select a player to kill: ")
                req = werewolves_pb2.MessageRequest(username=username, message=vote)
                res = stub.WerewolvesVote(req)
                print(res)
            elif res.message == "Game has started" or role == 2:
                req = werewolves_pb2.MessageRequest(username=username, message=username) 
                res = stub.WerewolvesVote(req)
                print(res)
            else:
                print(res)

            user_killed = res.message.split()[0]

            if res.werewolves == 0:
                print("Townspeople win!")
                return
            
            if res.townspeople == 0:
                print("Werewolves win!")
                return 

            if user_killed == username:
                print("You are dead")
                sys.exit()
            vote = input("Vote for a werewolf to kill: ")
            req = werewolves_pb2.MessageRequest(username=username, message=vote) 
            res = stub.TownsPeopleVote(req)
            print(res)
            
            user_killed = res.message.split()[0]

            if res.werewolves == 0:
                print("Townspeople win!")
                return
            
            if res.townspeople == 0:
                print("Werewolves win!")
                return 

            if user_killed == username or res.message == "You are already dead":
                print("You are dead")
                sys.exit()
            round(n + 1, res, role)
            
        round(1, res, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connect to Werewolves server")
    parser.add_argument('username', type=str, help="Username for connection")
    parser.add_argument('password', type=str, help="Password for connection")
    args = parser.parse_args()

    main(args.username, args.password)
