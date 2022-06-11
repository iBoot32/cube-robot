import socket

s = socket.socket()
port = 12345

def main():
    s.connect(('10.0.0.88', port))

    while True:
        moves = input("enter moves, or 'q' to quit: ")

        if moves[0] == "q":
            s.close()
            break

        s.send(moves.encode())

if __name__ == "__main__":
    main()