from socketIO_client_nexus import SocketIO

from play import Play

p = Play('models/model460')

socketIO = SocketIO('http://localhost:3003')

def on_move(move):
    print(move)
    i = move['i']
    j = move['j']
    k = move['n']
    ri,rj,rk,s = p.make_move(i,j,k)

    socketIO.emit('move',{'i':int(ri),'j':int(rj),'n':int(rk)})

socketIO.on('move', on_move)
socketIO.wait()
