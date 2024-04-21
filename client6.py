import rpyc

def main():
    # Try to establish a connection to the server; adjust "localhost" and "18812" if your server is on a different host or port
    try:
        conn = rpyc.connect("localhost", 18812)
    except ConnectionRefusedError:
        print("Failed to connect to the server. Please ensure the server is running and check the connection details.")
        return
    
    service = conn.root

    # Login process
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        success, message = service.exposed_login(username, password)
        print(message)
        if success:
            break
        else:
            choice = input("Would you like to try again? (yes/no): ")
            if choice.lower() != 'yes':
                return

    # Check to start the game
    while True:
        print("Press enter to start the game or type 'exit' to quit:")
        start_input = input().strip().lower()
        if start_input == 'exit':
            print("Exiting game...")
            return
        
        success, message = service.exposed_start_game()
        print(message)
        if success:
            role = service.exposed_get_role(username)
            print(f"You are a {role}.")
            break
        else:
            print("Failed to start the game.")
            choice = input("Try to start the game again? (yes/no): ")
            if choice.lower() != 'yes':
                print("Exiting game...")
                return

    # Game session active
    try:
        print("You are now in the game session. Press Ctrl+C to exit.")
        while True:
            # This loop keeps the client running; in a real application, this is where you could poll for game updates or listen for server push messages.
            pass
    except KeyboardInterrupt:
        print("Client is shutting down.")

if __name__ == "__main__":
    main()
