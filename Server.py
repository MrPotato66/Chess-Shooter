import socket
import pickle
from _thread import *
from Game import *


server = "10.188.218.156"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

game = Game()


def threaded_client(conn, p):
    global currentId

    print('Sending player\'s id: '+str(p))
    conn.send(str.encode(str(p)))

    while True:
        if game.p0Went:
            print('Player 0 went')
        if game.p1Went:
            print('Player 1 went')
        try:
            data = pickle.loads(conn.recv(4096))

            if not data:
                print('Disconnected')
                break
            else:
                if data.reset:
                    game.resetWent()
                if data.nature != 'unknown':
                    print(str(p)+' just sent a move')
                    game.play(p, data)
                conn.sendall(pickle.dumps(game))
        except:
            break
    print('Connection Lost')
    conn.close()

    currentId = 0
    game.reset()


currentId = 0

while True:
    connection, addr = s.accept()
    print('Connected to', addr)

    start_new_thread(threaded_client, (connection, currentId))
    currentId += 1
