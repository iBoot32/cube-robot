import socket
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import time

PORT = 12345
QUARTER_TURN = 51

k1 = MotorKit()
k2 = MotorKit(address = 0x61)
k3 = MotorKit(address = 0x62)

prev = "Z"

def main():
    # set up socket to receive data from the client sending moves
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # infintely accept connections/move data
            while True:
                data = conn.recv(1024).decode()
                start_time = time.time()
                for mov in data.split(" "):
                    move(mov)
                    print(mov, end =" ", flush=True)
                lapsed = time.time() - start_time
                mins = lapsed // 60
                sec = lapsed % 60
                print("Time Lapsed = {0}:{1}".format(int(mins),round(sec,2)))

                if not data:
                    break

def onSameDriver(m1, m2):
    if m1 == m2:
        return True
    elif (m1 == "R" or m2 == "R") and (m1 == "L" or m2 == "L"):
        return True
    elif (m1 == "F" or m2 == "F") and (m1 == "B" or m2 == "B"):
        return True
    return False

def move(mov):
    global prev
    if (onSameDriver(prev[0], mov[0])):
        time.sleep(0.8)
    else:
        time.sleep(0.3)

    if mov == "R":
        for step in range(QUARTER_TURN):
            k1.stepper2.onestep(direction=2, style=stepper.DOUBLE)
        k1.stepper2.release()
    elif mov == "R'":
        for step in range(QUARTER_TURN):
            k1.stepper2.onestep(direction=1, style=stepper.DOUBLE)
        k1.stepper2.release()
    elif mov == "R2":
        for step in range(2*QUARTER_TURN):
            k1.stepper2.onestep(direction=2, style=stepper.DOUBLE)
        k1.stepper2.release()

    elif mov == "L":
        for step in range(QUARTER_TURN):
            k1.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k1.stepper1.release()
    elif mov == "L'":
        for step in range(QUARTER_TURN):
            k1.stepper1.onestep(direction=1, style=stepper.DOUBLE)
        k1.stepper1.release()
    elif mov == "L2":
        for step in range(2*QUARTER_TURN):
            k1.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k1.stepper1.release()

    elif mov == "U":
        for mov in ["R", "L", "F2", "B2", "R'", "L'", "D", "R", "L", "F2", "B2", "R'", "L'"]:
            move(mov)
    elif mov == "U'":
        for mov in ["R", "L", "F2", "B2", "R'", "L'", "D'", "R", "L", "F2", "B2", "R'", "L'"]:
            move(mov)
    elif mov == "U2":
        for mov in ["R", "L", "F2", "B2", "R'", "L'", "D2", "R", "L", "F2", "B2", "R'", "L'"]:
            move(mov)

    elif mov == "D":
        for step in range(QUARTER_TURN):
            k3.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k3.stepper1.release()
    elif mov == "D'":
        for step in range(QUARTER_TURN):
            k3.stepper1.onestep(direction=1, style=stepper.DOUBLE)
        k3.stepper1.release()
    elif mov == "D2":
        for step in range(2*QUARTER_TURN):
            k3.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k3.stepper1.release()

    elif mov == "F":
        for step in range(QUARTER_TURN):
            k2.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k2.stepper1.release()
    elif mov == "F'":
        for step in range(QUARTER_TURN):
            k2.stepper1.onestep(direction=1, style=stepper.DOUBLE)
        k2.stepper1.release()
    elif mov == "F2":
        for step in range(2*QUARTER_TURN):
            k2.stepper1.onestep(direction=2, style=stepper.DOUBLE)
        k2.stepper1.release()

    elif mov == "B":
        for step in range(QUARTER_TURN):
            k2.stepper2.onestep(direction=2, style=stepper.DOUBLE)
        k2.stepper2.release()
    elif mov == "B'":
        for step in range(QUARTER_TURN):
            k2.stepper2.onestep(direction=1, style=stepper.DOUBLE)
        k2.stepper2.release()
    elif mov == "B2":
        for step in range(2*QUARTER_TURN):
            k2.stepper2.onestep(direction=2, style=stepper.DOUBLE)
        k2.stepper2.release()

    prev = mov

if __name__ == "__main__":
    main()
