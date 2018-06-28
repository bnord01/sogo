from socketIO_client_nexus import SocketIO

from play import Play

p = Play('models/model380')

socketIO = SocketIO('http://playsogo.herokuapp.com')


def on_move(move):
    i = move['i']
    j = move['j']
    k = move['n']
    ri, rj, rk, s = p.make_move(i, j, k)
    response = {'i': int(ri), 'j': int(rj), 'n': int(rk)}
    print(f"Received move: {move} ({s}) response: {response}")
    socketIO.emit('move', response)
    if not s == 'open':
        p.reset()
        print(f"Game reset!")


socketIO.on('move', on_move)
print("Client connected!")
socketIO.wait()
