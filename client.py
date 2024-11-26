import serial

def display_menu():
    """
    Displays the menu for the Rock-Paper-Scissors game.

    Provides options for starting a new game, saving, loading, making a move, or exiting.
    """
    print("Rock-Paper-Scissors Game Menu:")
    print("1. New Game")
    print("2. Save Game")
    print("3. Load Game")
    print("4. Play Move")
    print("5. Exit")


def run_client():
    """
    Runs the Rock-Paper-Scissors client application.

    Establishes a serial connection with the server and provides a menu-driven interface
    for interacting with the server.

    The client connects to the server on COM12 with a baud rate of 9600. Users can choose
    actions from the menu, and corresponding commands are sent to the server. The client
    listens for server responses and displays them.

    Exceptions:
        KeyboardInterrupt: Handles interruption by the user (Ctrl+C) gracefully.
        serial.SerialException: Handles errors related to the serial port.
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


if __name__ == "__main__":
    run_client()
