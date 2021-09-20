from socketIO_client_nexus import SocketIO

from play import Play

p = Play('models/model0')

socketIO = SocketIO('http://playsogo.herokuapp.com')


def on_move(move):
    print(move)
    i = move['i']
    j = move['j']
    ri, rj, rk, s = p.make_move(i, j)
    response = {'i': int(ri), 'j': int(rj), 'n': int(rk)}
    print(f"Received move: {move} ({s}) response: {response}")
    socketIO.emit('move', response)
    if not s == 'open':
        p.reset()
        socketIO.emit('reset')
        print(f"Game reset!")

def on_reset(v):
    p.reset()
    print(f"Game reset!")

socketIO.on('move', on_move)
socketIO.on('reset', on_reset)
print("Client connected!")
socketIO.wait()
