import rpyc
import uuid

class MyClientService(rpyc.Service):
    # Method exposed to receive messages from the server
    def exposed_receive_role(self, role):
        print(f"You have been assigned the role: {role}")

    def exposed_receive_message(self, message):
        print(message)

def main():
    # Connect to the server
    conn = rpyc.connect("localhost", 18812, config={"allow_public_attrs": True})
    service = MyClientService(exposed=True)
    bgsrv = rpyc.BgServingThread(conn, service)
    
    # Generate a unique connection ID for this session
    conn_id = str(uuid.uuid4())

    # Get username and password input from the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # Attempt to login
    authenticated, response = conn.root.login(username, password, conn_id)
    print(response)
    
    if not authenticated:
        print("Failed to authenticate or connect. Please check your credentials or try again later.")
        bgsrv.stop()
        return
    
    try:
        # Keep the main thread alive while the client interacts with the server
        print("Waiting for game to start...")
        while True:
            pass
    except KeyboardInterrupt:
        print("Client is shutting down.")
    finally:
        bgsrv.stop()  # Properly close the background thread

if __name__ == "__main__":
    main()
