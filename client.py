import werewolves_pb2
import werewolves_pb2_grpc
import grpc
import argparse
import time

def main(username, password):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesServiceStub(channel)
        req = werewolves_pb2.ConnectRequest(username=username, password=password)
        res = stub.Connect(req)
        print(res)

        req = werewolves_pb2.MessageRequest(username=username, message=username)
        res = stub.StartGame(req)
        print(res)

        if res.message == "Game has started":
            time.sleep(15)
        else:
            vote = input("Game has started, you are the werewolf, select a player to kill: ")
            req = werewolves_pb2.MessageRequest(username=username, message=vote)
            res = stub.WerewolvesVote(req)
            print(res)

        vote = input("Vote for a werewolf to kill: ")
        req = werewolves_pb2.MessageRequest(username=username, message=vote) 
        res = stub.TownsPeopleVote(req)
        print(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connect to Werewolves server")
    parser.add_argument('username', type=str, help="Username for connection")
    parser.add_argument('password', type=str, help="Password for connection")
    args = parser.parse_args()

    main(args.username, args.password)
