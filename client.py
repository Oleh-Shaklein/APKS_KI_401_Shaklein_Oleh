import serial

def display_menu():
    """
    @brief Displays the game menu options to the player.
    """
    print("Rock-Paper-Scissors Game Menu:")
    print("1. New Game")
    print("2. Save Game")
    print("3. Load Game")
    print("4. Play Move")
    print("5. Exit")

def run_client():
    """
    @brief Runs the client program for the Rock-Paper-Scissors game.
    Establishes a serial connection and interacts with the user to play the game.
    """
    ser = serial.Serial('COM12', 9600, timeout=1)
    print("Rock-Paper-Scissors client is running on COM12...")

    try:
        while True:
            display_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                ser.write("new\n".encode())
                print("New game command sent.")
            elif choice == "2":
                ser.write("save\n".encode())
                print("Save game command sent.")
            elif choice == "3":
                ser.write("load\n".encode())
                print("Load game command sent.")
            elif choice == "4":
                player_choice = input("Enter your choice (rock, paper, or scissors): ").strip().lower()
                ser.write(f"play {player_choice}\n".encode())
                print(f"Sent move: {player_choice}")
            elif choice == "5":
                print("Exiting game.")
                break

            # Read the response from the server
            response = ser.readline().decode().strip()
            print(f"Server response: {response}")

    except KeyboardInterrupt:
        print("Client shutting down.")
    finally:
        ser.close()
