'use strict';

var express = require('express');
var socket = require('socket.io');

var app = express();

app.use(express.static(__dirname + '/dist'));

var port = process.env.PORT || 3003;
var ready = new Promise(function willListen(resolve, reject) {
    var server = app.listen(port, function didListen(err) {
        if (err) {
            reject(err);
            return;
        }
        console.log('app.listen on http://localhost:%d', port);
        resolve(server);
    });
});

ready.then(server => {
    var io = socket(server);
    io.on('connection',socket => {
        console.log(`Connection established to ${socket.id}`)
        socket.on('move',data => {
            console.log(`Move by ${socket.id} : ${JSON.stringify(data)}`)
            io.sockets.emit('move',data)
        })
    })
})

exports.ready = ready;
exports.app = app;
