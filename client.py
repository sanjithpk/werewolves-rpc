import werewolves_pb2
import werewolves_pb2_grpc
import time
import grpc
import argparse

def connect(server_address, username, password):
    # Establish a connection to the server
    channel = grpc.insecure_channel(server_address)
    stub = werewolves_pb2_grpc.WerewolvesServiceStub(channel)
    
    # Send a connection request
    connect_response = stub.Connect(werewolves_pb2.ConnectRequest(username=username, password=password))
    print(f"Server response: {connect_response.message}")
    return stub

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        hello_request = werewolves_pb2.MessageRequest(message = name)
        yield hello_request
        time.sleep(1)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesServiceStub(channel)
        responses = stub.InteractiveMessage(get_client_stream_requests())

        for response in responses:
            print("InteractiveMessage Response Received: ")
            print(response)

        # responses = stub.InteractiveMessage(get_client_stream_requests())

        # for response in responses:
        #     print("InteractiveMessage Response Received: ")
        #     print(response)

def main(username, password):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = werewolves_pb2_grpc.WerewolvesServiceStub(channel)
        req = werewolves_pb2.ConnectRequest(username=username, password=password)
        stub.Connect(req)

        req = werewolves_pb2.MessageRequest(message="Start")
        res = stub.StartGame(req)
        print(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Connect to Werewolves server")
    parser.add_argument('username', type=str, help="Username for connection")
    parser.add_argument('password', type=str, help="Password for connection")
    args = parser.parse_args()

    main(args.username, args.password)
