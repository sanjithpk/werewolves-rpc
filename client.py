import rpyc
import uuid

class MyClientService(rpyc.Service):
    # Method exposed to receive messages from the server
    def exposed_receive_message(self, message):
        print(message)

def main():
    # Connect to the server
    conn = rpyc.connect("localhost", 18812, service=MyClientService)
    conn_id = str(uuid.uuid4())

    # Instantiate and register the service
    service = MyClientService()
    bgsrv = rpyc.BgServingThread(conn, service)
    
    # Handle user input for login
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = conn.root.login(username, password, conn_id)
    print(response)

    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        print("Client is shutting down.")
    finally:
        bgsrv.stop()  # Properly close the background thread

if __name__ == "__main__":
    main()
