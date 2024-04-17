import rpyc

class MyClientService(rpyc.Service):
    def exposed_receive_message_from_server(self, message):
        print("Message from server:", message)

def main():
    # Establish the connection to the server and use MyClientService to handle incoming calls
    conn = rpyc.connect("localhost", 18812, service=MyClientService())
    print("Connected to server.")
    
    # Start a background thread to handle incoming requests from the server
    bgsrv = rpyc.BgServingThread(conn)

    try:
        while True:
            pass  # Keep the client running to receive messages
    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        # bgsrv.stop()  # Properly close the background thread
        conn.close()

if __name__ == "__main__":
    main()
